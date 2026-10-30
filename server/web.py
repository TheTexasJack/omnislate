#!/usr/bin/env python3
"""OMNISLATE build server for unstableNHP.

A small web page for GMs on the Tailscale network:
  - log in with your GM name and password
  - press Build for your campaign and read the report
  - open finished session files (videos and sounds stream from the same folder)
  - optional auto-build a few seconds after a campaign file changes

Standard library only.  Runs as the locked-down 'omnibuild' user under systemd
(see omnictl.py).  Every GM sees only the campaigns listed for them in
/etc/omnislate/gms.json.  Admins see every campaign.
"""
import base64
import hashlib
import hmac
import html
import ipaddress
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(os.environ.get("OMNI_ROOT", "/srv/omnislate")).resolve()
CONFIG = Path(os.environ.get("OMNI_CONFIG", "/etc/omnislate/gms.json"))
STATE = Path(os.environ.get("OMNI_STATE", "/var/lib/omnislate"))
PORT = int(os.environ.get("OMNI_PORT", "80"))
ALLOW_LOCAL = os.environ.get("OMNI_ALLOW_LOCAL", "") == "1"
TAILNET = [ipaddress.ip_network("100.64.0.0/10"), ipaddress.ip_network("fd7a:115c:a1e0::/48")]
LOCAL = [ipaddress.ip_network("127.0.0.0/8"), ipaddress.ip_network("::1/128")]
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
LOCKS = {}
LOCKS_GUARD = threading.Lock()
FAILS = {}

mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("audio/mpeg", ".mp3")


# ------------------------------------------------------------------ config and auth

def load_config():
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"gms": {}, "autobuild": True, "limit_gb": 20}


def hash_password(password, salt=None, rounds=240000):
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), rounds).hex()
    return {"salt": salt, "rounds": rounds, "hash": digest}


def check_password(record, password):
    if not record or "hash" not in record:
        return False
    test = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(record["salt"]), record["rounds"]).hex()
    return hmac.compare_digest(test, record["hash"])


def campaigns_on_disk():
    base = ROOT / "campaigns"
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir() and (p / "campaign.md").exists() and NAME_RE.match(p.name))


def allowed_campaigns(cfg, user):
    gm = cfg["gms"].get(user, {})
    disk = campaigns_on_disk()
    if gm.get("admin"):
        return disk
    return [c for c in gm.get("campaigns", []) if c in disk]


# ------------------------------------------------------------------ building

def campaign_lock(name):
    with LOCKS_GUARD:
        return LOCKS.setdefault(name, threading.Lock())


def report_path(name):
    return STATE / "reports" / f"{name}.json"


def run_build(name, how):
    """Build one campaign.  Arguments go straight to the process list, so nothing a user types reaches a shell."""
    lock = campaign_lock(name)
    if not lock.acquire(blocking=False):
        return {"campaign": name, "ok": False, "busy": True, "text": "A build for this campaign is already running.  Try again in a moment.",
                "when": time.strftime("%Y-%m-%d %H:%M:%S"), "how": how}
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        try:
            p = subprocess.run([sys.executable, str(ROOT / "build.py"), name], cwd=str(ROOT), env=env,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
            text, ok = (p.stdout + p.stderr).strip(), p.returncode == 0
        except subprocess.TimeoutExpired:
            text, ok = "The build took longer than 10 minutes and was stopped.", False
        rep = {"campaign": name, "ok": ok, "text": text, "when": time.strftime("%Y-%m-%d %H:%M:%S"), "how": how}
        report_path(name).parent.mkdir(parents=True, exist_ok=True)
        report_path(name).write_text(json.dumps(rep), encoding="utf-8")
        return rep
    finally:
        lock.release()


def last_report(name):
    try:
        return json.loads(report_path(name).read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return None


def tree_stamp(paths):
    newest = 0.0
    for base in paths:
        if base.is_file():
            newest = max(newest, base.stat().st_mtime)
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for f in filenames:
                if f.startswith(".") or f.startswith("~$"):
                    continue
                try:
                    newest = max(newest, os.stat(os.path.join(dirpath, f)).st_mtime)
                except OSError:
                    pass
    return newest


def autobuild_loop():
    """Rebuild a campaign about 5 seconds after its files stop changing."""
    seen = {}
    while True:
        time.sleep(4)
        try:
            cfg = load_config()
            if not cfg.get("autobuild", True):
                continue
            shared = [ROOT / "library", ROOT / "app", ROOT / "build.py"]
            for name in campaigns_on_disk():
                if name.startswith("_"):
                    continue
                stamp = tree_stamp([ROOT / "campaigns" / name] + shared)
                prev = seen.get(name)
                if prev is None:
                    # First look since the service started.  Anything saved after the last
                    # build (say, while the box was rebooting) still gets built.
                    try:
                        built = report_path(name).stat().st_mtime
                    except OSError:
                        built = 0
                    seen[name] = prev = min(stamp, built)
                if stamp > prev and time.time() - stamp > 5:
                    seen[name] = stamp
                    if run_build(name, "auto").get("busy"):
                        seen[name] = prev  # a button build was running; look again next pass
        except Exception as e:  # keep the loop alive no matter what
            print("autobuild error:", e, file=sys.stderr)


def dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.stat(os.path.join(dirpath, f)).st_size
            except OSError:
                pass
    return total


# ------------------------------------------------------------------ pages

CSS = """
:root{--bg:#06101d;--panel:#0c1c31;--line:#2c4a6e;--hi:#7fa3cc;--text:#eef3f9;--dim:#95a9bf;--accent:#c9a24a;--ok:#5fd39a;--warn:#e7a93a;--bad:#ef5350}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 "Roboto","Noto Sans","DejaVu Sans",sans-serif}
header{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-bottom:1px solid var(--line)}
header b{letter-spacing:.14em;color:var(--accent)}main{max-width:1100px;margin:0 auto;padding:18px;display:grid;gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
h2{margin:0 0 4px;font-size:22px;letter-spacing:.06em}h4{margin:10px 0 2px;font-size:15px;color:var(--accent);letter-spacing:.08em;text-transform:uppercase}h3{margin:14px 0 6px;font-size:14px;color:var(--hi);letter-spacing:.08em;text-transform:uppercase}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button{min-height:44px;padding:0 18px;border:1px solid var(--accent);background:rgba(201,162,74,.16);color:var(--accent);border-radius:8px;font:inherit;cursor:pointer}
a{color:var(--hi)}ul{margin:4px 0;padding-left:20px}.dim{color:var(--dim);font-size:14px}
pre{white-space:pre-wrap;background:#03080f;border:1px solid var(--line);border-radius:8px;padding:12px;font:13px/1.45 "DejaVu Sans Mono",monospace;overflow:auto;max-height:60vh}
.ok{color:var(--ok)}.warn{color:var(--warn)}.bad{color:var(--bad)}
.meter{height:8px;border:1px solid var(--line);border-radius:4px;overflow:hidden;max-width:320px}.meter i{display:block;height:100%;background:var(--ok)}
.meter.over i{background:var(--bad)}
"""


def page(title, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body><header><b>OMNISLATE</b><span class="dim">unstableNHP build server</span></header>
<main>{body}</main></body></html>"""


def render_report(rep, name):
    if not rep:
        return '<p class="dim">No build yet.  Press Build.</p>'
    lines = []
    for raw in rep["text"].splitlines():
        esc = html.escape(raw)
        m = re.search(r"dist/" + re.escape(name) + r"/((?:[A-Za-z0-9_-]+/)?[A-Za-z0-9._-]+\.html)", raw)
        if m:
            esc = esc.replace(html.escape(f"dist/{name}/{m.group(1)}"),
                              f'<a href="/c/{urllib.parse.quote(name)}/{urllib.parse.quote(m.group(1))}" target="_blank">dist/{html.escape(name)}/{html.escape(m.group(1))}</a>')
        cls = "bad" if ("FAILED" in raw or "BUILD FAILED" in raw) else ("warn" if raw.strip().startswith("Warn") else ("ok" if raw.strip().startswith("OK") else ""))
        lines.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
    status = '<span class="ok">Built</span>' if rep.get("ok") else '<span class="bad">Needs attention</span>'
    how = "automatic" if rep.get("how") == "auto" else "button"
    return f'<p>{status} <span class="dim">{html.escape(rep["when"])} ({how})</span></p><pre>{"<br>".join(lines)}</pre>'


def chapter_names(name):
    base = ROOT / "campaigns" / name
    return [p.name for p in sorted(base.iterdir())
            if p.is_dir() and NAME_RE.match(p.name) and (p / "campaign.md").exists()]


def session_links(name):
    """Session files grouped by chapter.  A new chapter folder shows up here on its own."""
    dist = ROOT / "dist" / name
    groups = []
    root_files = sorted(p.name for p in dist.glob("*.html")) if dist.is_dir() else []
    if root_files:
        groups.append(("", root_files))
    for ch in chapter_names(name):
        d = dist / ch
        groups.append((ch, sorted(p.name for p in d.glob("*.html")) if d.is_dir() else []))
    out = []
    for ch, files in groups:
        prefix = f"{ch}/" if ch else ""
        items = "".join(f'<li><a href="/c/{urllib.parse.quote(name)}/{urllib.parse.quote(prefix + f)}" target="_blank">{html.escape(f)}</a></li>' for f in files)
        body = f"<ul>{items}</ul>" if items else '<p class="dim">Not built yet.  It builds a few seconds after its files change, or press Build.</p>'
        out.append((f'<h4>{html.escape(ch)}</h4>' if ch else "") + body)
    return "".join(out)


def campaign_card(cfg, name):
    links = session_links(name)
    limit = float(cfg.get("limit_gb", 20)) * 1024 ** 3
    size = dir_size(ROOT / "campaigns" / name)
    pct = min(100, size / limit * 100) if limit else 0
    over = " over" if size > limit else ""
    usage = (f'<div class="meter{over}"><i style="width:{pct:.1f}%"></i></div>'
             f'<span class="dim">{size / 1024 ** 3:.2f} GB of {cfg.get("limit_gb", 20)} GB</span>')
    if size > limit:
        usage += '<p class="bad">This campaign is over its space limit.  Remove old videos from media/ before adding more.</p>'
    return f"""<section class="card"><h2>{html.escape(name)}</h2>
<form method="post" action="/build" class="row"><input type="hidden" name="campaign" value="{html.escape(name)}">
<button type="submit">Build {html.escape(name)}</button><span class="dim">Builds every chapter.  Takes a few seconds.</span></form>
<h3>Session files</h3>{links or '<p class="dim">None yet.  Copy _template inside this campaign to start a chapter.</p>'}
<h3>Space</h3>{usage}
<h3>Last build</h3>{render_report(last_report(name), name)}</section>"""


# ------------------------------------------------------------------ HTTP

class Handler(BaseHTTPRequestHandler):
    server_version = "OMNISLATE"
    sys_version = ""

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.client_address[0], fmt % args))

    # Defense in depth: the firewall already limits this to Tailscale.
    def client_ok(self):
        try:
            ip = ipaddress.ip_address(self.client_address[0].split("%")[0])
        except ValueError:
            return False
        if getattr(ip, "ipv4_mapped", None):
            ip = ip.ipv4_mapped
        nets = TAILNET + (LOCAL if ALLOW_LOCAL else [])
        return any(ip in n for n in nets)

    def user(self):
        cfg = load_config()
        h = self.headers.get("Authorization", "")
        if h.startswith("Basic "):
            try:
                name, _, pw = base64.b64decode(h[6:]).decode("utf-8").partition(":")
            except Exception:
                return None, cfg
            ip = self.client_address[0]
            if FAILS.get(ip, (0, 0))[0] >= 5 and time.time() - FAILS[ip][1] < 60:
                return None, cfg
            if name in cfg["gms"] and check_password(cfg["gms"][name].get("password"), pw):
                FAILS.pop(ip, None)
                return name, cfg
            n, _ = FAILS.get(ip, (0, 0))
            FAILS[ip] = (n + 1, time.time())
            time.sleep(1)
        return None, cfg

    def deny(self, code, text):
        body = page("OMNISLATE", f'<section class="card"><p>{html.escape(text)}</p></section>').encode()
        self.send_response(code)
        if code == 401:
            self.send_header("WWW-Authenticate", 'Basic realm="OMNISLATE", charset="UTF-8"')
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_page(self, text, code=200):
        body = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def gate(self):
        if not self.client_ok():
            self.deny(403, "This server only answers on the Tailscale network.")
            return None, None
        user, cfg = self.user()
        if not user:
            self.deny(401, "Log in with your GM name and password.")
            return None, None
        return user, cfg

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        user, cfg = self.gate()
        if not user:
            return
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            camps = allowed_campaigns(cfg, user)
            cards = "".join(campaign_card(cfg, c) for c in camps) or '<section class="card"><p>No campaigns are assigned to you yet.  Ask Nathan.</p></section>'
            auto = "on" if cfg.get("autobuild", True) else "off"
            intro = (f'<section class="card"><p>Logged in as <b>{html.escape(user)}</b>.  Edit your files on the shared drive, then press Build.  '
                     f'Auto-build is <b>{auto}</b>: saved changes also rebuild on their own after a few seconds.</p></section>')
            return self.send_page(page("OMNISLATE builds", intro + cards))
        m = re.match(r"^/c/([^/]+)/(.+)$", path)
        if m:
            return self.serve_file(cfg, user, urllib.parse.unquote(m.group(1)), urllib.parse.unquote(m.group(2)))
        self.deny(404, "Nothing here.")

    def do_POST(self):
        user, cfg = self.gate()
        if not user:
            return
        if urllib.parse.urlparse(self.path).path != "/build":
            return self.deny(404, "Nothing here.")
        origin = self.headers.get("Origin") or self.headers.get("Referer") or ""
        host = self.headers.get("Host", "")
        if origin and urllib.parse.urlparse(origin).netloc != host:
            return self.deny(403, "That request came from another site.")
        length = min(int(self.headers.get("Content-Length") or 0), 4096)
        form = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        name = (form.get("campaign") or [""])[0]
        if name not in allowed_campaigns(cfg, user):
            return self.deny(403, "That campaign is not one of yours.")
        rep = run_build(name, "button")
        body = (f'<section class="card"><p><a href="/">Back to your campaigns</a></p></section>'
                f'<section class="card"><h2>{html.escape(name)}</h2>{render_report(rep, name)}</section>')
        self.send_page(page("Build report", body))

    def serve_file(self, cfg, user, name, rel):
        if name not in allowed_campaigns(cfg, user):
            return self.deny(403, "That campaign is not one of yours.")
        base = (ROOT / "dist" / name).resolve()
        target = (base / rel).resolve()
        if base not in target.parents or any(part.startswith(".") for part in target.relative_to(base).parts):
            return self.deny(404, "Nothing here.")
        if not target.is_file():
            return self.deny(404, "Nothing here.")
        size = target.stat().st_size
        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if ctype.startswith("text/"):
            ctype += "; charset=utf-8"
        start, end, code = 0, size - 1, 200
        rng = self.headers.get("Range", "")
        mr = re.match(r"^bytes=(\d*)-(\d*)$", rng.strip())
        if mr and size:
            a, b = mr.groups()
            if a == "" and b:
                start = max(0, size - int(b))
            else:
                start = int(a or 0)
                end = min(size - 1, int(b)) if b else size - 1
            if start > end or start >= size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            code = 206
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Cache-Control", "no-cache")
        if code == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(target, "rb") as fh:
            fh.seek(start)
            left = end - start + 1
            while left > 0:
                chunk = fh.read(min(65536, left))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(chunk)


def main():
    (STATE / "reports").mkdir(parents=True, exist_ok=True)
    threading.Thread(target=autobuild_loop, daemon=True).start()
    try:
        srv = ThreadingHTTPServer(("::", PORT), Handler)
    except OSError:
        srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    srv.daemon_threads = True
    print(f"OMNISLATE build server on port {PORT}, workshop {ROOT}", file=sys.stderr)
    srv.serve_forever()


if __name__ == "__main__":
    main()
