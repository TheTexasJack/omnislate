#!/usr/bin/env python3
"""omnictl: set up and manage the OMNISLATE server on unstableNHP.

Run every command with sudo from inside an unzipped omnislate folder:

    sudo python3 server/omnictl.py install              first-time setup (you become the admin GM)
    sudo python3 server/omnictl.py add-gm jarrett iron-tide
                                                        new GM user plus their campaign folder and share
    sudo python3 server/omnictl.py passwd jarrett       change a GM's password (web page and shared drive)
    sudo python3 server/omnictl.py update               install a newer omnislate zip's engine files
    sudo python3 server/omnictl.py update --library     same, and replace library/worlds.md too
    sudo python3 server/omnictl.py autobuild on|off     turn automatic builds on or off
    sudo python3 server/omnictl.py limit 20             per-campaign space limit in GB (shown on the web page)
    sudo python3 server/omnictl.py fix-perms            reapply folder permissions
    sudo python3 server/omnictl.py status               who has what, sizes, and service health

The workshop lives in /srv/omnislate.  GM settings live in /etc/omnislate/gms.json.
"""
import getpass
import grp
import json
import os
import pwd
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True  # running as root must not leave root-owned cache files in the unzipped folder
from web import hash_password, NAME_RE  # noqa: E402

ROOT = Path(os.environ.get("OMNI_ROOT", "/srv/omnislate"))
ETC = Path(os.environ.get("OMNI_ETC", "/etc/omnislate"))
CONFIG = ETC / "gms.json"
STATE = Path(os.environ.get("OMNI_STATE", "/var/lib/omnislate"))
BACKUPS = Path(os.environ.get("OMNI_BACKUPS", "/srv/omnislate-backups"))
SAMBA_INC = Path(os.environ.get("OMNI_SAMBA_INC", "/etc/samba/omnislate.conf"))
SMB_CONF = Path(os.environ.get("OMNI_SMB_CONF", "/etc/samba/smb.conf"))
UNIT = Path(os.environ.get("OMNI_UNIT", "/etc/systemd/system/omnislate-web.service"))
GROUP = "omnigm"
SVC_USER = "omnibuild"
SOURCE = Path(__file__).resolve().parent.parent
ENGINE = ["app", "build.py", "build.sh", "server", "docs", "README.md", "START-HERE.txt", "ENHANCEMENTS.md", "campaigns/_starter"]
EXEC = {"build.sh", "build.py", "server/omnictl.py", "server/web.py"}

UNIT_TEXT = f"""# Managed by omnictl.py
[Unit]
Description=OMNISLATE build server
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
User={SVC_USER}
Group={SVC_USER}
ExecStart=/usr/bin/python3 {ROOT}/server/web.py
Environment=PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
Restart=on-failure
RestartSec=3
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths={ROOT}/dist {STATE}

[Install]
WantedBy=multi-user.target
"""


def say(msg):
    print(msg, flush=True)


def die(msg):
    print(f"\nSTOPPED: {msg}", flush=True)
    sys.exit(2)


def run(cmd, check=True, **kw):
    return subprocess.run(cmd, check=check, **kw)


def need_root():
    if os.geteuid() != 0:
        die("Run this with sudo, for example: sudo python3 server/omnictl.py " + " ".join(sys.argv[1:]))


def user_exists(name):
    try:
        pwd.getpwnam(name)
        return True
    except KeyError:
        return False


def load():
    if not CONFIG.exists():
        die("No /etc/omnislate/gms.json yet.  Run the install command first.")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save(cfg):
    ETC.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    os.replace(tmp, CONFIG)
    gid = grp.getgrnam(SVC_USER).gr_gid if user_exists(SVC_USER) else 0
    os.chown(ETC, 0, gid)
    os.chmod(ETC, 0o750)
    os.chown(CONFIG, 0, gid)
    os.chmod(CONFIG, 0o640)


def ask_password(who):
    for _ in range(3):
        a = getpass.getpass(f"New password for {who}: ")
        if len(a) < 8:
            say("  Use at least 8 characters.")
            continue
        if a != getpass.getpass("Type it again: "):
            say("  Those did not match.")
            continue
        return a
    die("No password set.")


def admin_name(cfg):
    for name, gm in cfg["gms"].items():
        if gm.get("admin"):
            return name
    die("No admin GM in gms.json.")


def owners(cfg, campaign):
    return [n for n, gm in cfg["gms"].items() if not gm.get("admin") and campaign in gm.get("campaigns", [])]


def set_smb_password(user, pw):
    run(["smbpasswd", "-a", "-s", user], input=f"{pw}\n{pw}\n", text=True, stdout=subprocess.DEVNULL)
    run(["smbpasswd", "-e", user], stdout=subprocess.DEVNULL)


def chown_tree(path, user, group):
    run(["chown", "-R", f"{user}:{group}", str(path)])


def fix_perms(cfg):
    admin = admin_name(cfg)
    say("Applying folder permissions...")
    for p in [ROOT] + [p for p in ROOT.iterdir() if p.name not in ("campaigns", "dist")]:
        if p == ROOT:
            os.chown(ROOT, pwd.getpwnam(admin).pw_uid, grp.getgrnam(GROUP).gr_gid)
            os.chmod(ROOT, 0o755)
            continue
        chown_tree(p, admin, GROUP)
        run(["chmod", "-R", "u=rwX,go=rX", str(p)])
    for rel in EXEC:
        f = ROOT / rel
        if f.exists():
            os.chmod(f, 0o755)
    camps = ROOT / "campaigns"
    camps.mkdir(exist_ok=True)
    os.chown(camps, pwd.getpwnam(admin).pw_uid, grp.getgrnam(GROUP).gr_gid)
    os.chmod(camps, 0o755)
    for c in sorted(p for p in camps.iterdir() if p.is_dir()):
        if c.name.startswith("_"):
            chown_tree(c, admin, GROUP)
            run(["chmod", "-R", "u=rwX,go=rX", str(c)])
            continue
        own = owners(cfg, c.name)
        owner = own[0] if own else admin
        chown_tree(c, owner, pwd.getpwnam(owner).pw_gid)
        run(["chmod", "-R", "u=rwX,g=rwX,o=", str(c)])
        run(["setfacl", "-R", "-b", str(c)])
        entries = [f"u:{SVC_USER}:rX", f"u:{admin}:rwX"] + [f"u:{o}:rwX" for o in own]
        run(["setfacl", "-R", "-m", ",".join(entries + ["m::rwX"]), str(c)])
        # Default ACLs (inherited by new files and folders) can only sit on folders.
        defaults = [f"u:{SVC_USER}:rx", f"u:{admin}:rwx"] + [f"u:{o}:rwx" for o in own] + ["u::rwx", "g::rwx", "o::-", "m::rwx"]
        run(["find", str(c), "-type", "d", "-exec", "setfacl", "-d", "-m", ",".join(defaults), "{}", "+"])
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    chown_tree(dist, SVC_USER, SVC_USER)
    run(["chmod", "-R", "u=rwX,go=", str(dist)])
    run(["setfacl", "-R", "-m", f"u:{admin}:rX", str(dist)])
    run(["find", str(dist), "-type", "d", "-exec", "setfacl", "-d", "-m", f"u:{admin}:rx", "{}", "+"])
    STATE.mkdir(parents=True, exist_ok=True)
    chown_tree(STATE, SVC_USER, SVC_USER)
    os.chmod(STATE, 0o700)


def write_samba(cfg):
    admin = admin_name(cfg)
    parts = ["# Managed by omnictl.py.  Edits here are overwritten.",
             "# Access is limited to the Tailscale network by the firewall (ufw allows only tailscale0).", "",
             "[omnislate]", "   comment = OMNISLATE reference (read-only)", f"   path = {ROOT}", "   read only = yes",
             f"   valid users = @{GROUP}", "   hide unreadable = yes", "   browseable = yes", "",
             "[omnislate-admin]", "   comment = OMNISLATE workshop (admin)", f"   path = {ROOT}", "   read only = no",
             f"   valid users = {admin}", "   inherit acls = yes", "   create mask = 0664", "   directory mask = 0775", ""]
    for c in sorted(p.name for p in (ROOT / "campaigns").iterdir() if p.is_dir() and not p.name.startswith("_")):
        who = owners(cfg, c) + [admin]
        parts += [f"[{c}]", f"   comment = OMNISLATE campaign {c}", f"   path = {ROOT}/campaigns/{c}", "   read only = no",
                  f"   valid users = {' '.join(dict.fromkeys(who))}", "   inherit acls = yes", "   create mask = 0660",
                  "   directory mask = 0770", "   veto files = /.*/", "   delete veto files = yes", ""]
    SAMBA_INC.write_text("\n".join(parts), encoding="utf-8")
    text = SMB_CONF.read_text(encoding="utf-8") if SMB_CONF.exists() else ""
    line = f"include = {SAMBA_INC}"
    if line not in text:
        with open(SMB_CONF, "a", encoding="utf-8") as fh:
            fh.write(f"\n# OMNISLATE shares\n{line}\n")
    check = run(["testparm", "-s"], check=False, capture_output=True, text=True)
    if check.returncode != 0:
        say(check.stderr)
        die("Samba rejected the share settings.  Nothing was restarted.")
    run(["systemctl", "restart", "smbd"], check=False)


def restart_web():
    run(["systemctl", "daemon-reload"])
    run(["systemctl", "enable", "--now", "omnislate-web"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run(["systemctl", "restart", "omnislate-web"])


def copy_item(src, dst):
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


# ------------------------------------------------------------------ commands

def cmd_install(args):
    need_root()
    admin = os.environ.get("SUDO_USER") or ""
    if not admin or admin == "root":
        die("Run install with sudo from your own account (not as root) so you become the admin GM.")
    if ROOT.exists() and any(ROOT.iterdir()) and SOURCE.resolve() != ROOT.resolve():
        die(f"{ROOT} already has files.  Use 'update' to install a newer version.")
    say("Installing packages (samba, acl, Pillow, ffmpeg)...")
    run(["apt-get", "install", "-y", "samba", "acl", "python3-pil", "ffmpeg"], stdout=subprocess.DEVNULL)
    run(["groupadd", "-f", GROUP])
    if not user_exists(SVC_USER):
        run(["useradd", "--system", "--home-dir", str(STATE), "--shell", "/usr/sbin/nologin", "--user-group", SVC_USER])
    run(["usermod", "-aG", GROUP, admin])
    if SOURCE.resolve() != ROOT.resolve():
        say(f"Copying the workshop to {ROOT}...")
        ROOT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SOURCE, ROOT, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    cfg = {"autobuild": True, "limit_gb": 20, "gms": {}}
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    say(f"\nYou ({admin}) are the admin GM.  This password is for the build web page and the shared drives.")
    pw = ask_password(admin)
    cfg["gms"][admin] = {"admin": True, "campaigns": [], "password": hash_password(pw)}
    save(cfg)
    fix_perms(cfg)
    write_samba(cfg)
    set_smb_password(admin, pw)
    UNIT.write_text(UNIT_TEXT, encoding="utf-8")
    restart_web()
    say("\nDone.")
    say("  Build page:   http://unstablenhp/          (from any device on your Tailscale network)")
    say("  Shares:       \\\\unstablenhp\\omnislate-admin   and one share per campaign")
    say("  Next:         sudo python3 server/omnictl.py add-gm jarrett <his-campaign-name>")


def cmd_add_gm(args):
    need_root()
    if len(args) != 2:
        die("Usage: add-gm <username> <campaign-folder-name>")
    user, camp = args
    if not NAME_RE.match(user) or user.startswith("-") or not user.islower():
        die("Usernames are lowercase letters, numbers, dashes, or underscores.")
    if not NAME_RE.match(camp) or camp.startswith("_") or not camp.islower():
        die("Campaign folder names are lowercase letters, numbers, and dashes, such as iron-tide.")
    cfg = load()
    if not user_exists(user):
        say(f"Creating user {user} (shared drive and web page only, no desktop login)...")
        run(["useradd", "--no-create-home", "--shell", "/usr/sbin/nologin", "--user-group", user])
    run(["usermod", "-aG", GROUP, user])
    folder = ROOT / "campaigns" / camp
    if not folder.exists():
        say(f"Creating campaign {camp} from the starter...")
        shutil.copytree(ROOT / "campaigns" / "_starter", folder)
        md = folder / "campaign.md"
        md.write_text(md.read_text(encoding="utf-8").replace("Name: New Campaign", "Name: " + camp.replace("-", " ").title()), encoding="utf-8")
    gm = cfg["gms"].setdefault(user, {"campaigns": []})
    if camp not in gm["campaigns"]:
        gm["campaigns"].append(camp)
    if "password" not in gm:
        pw = ask_password(user)
        gm["password"] = hash_password(pw)
        set_smb_password(user, pw)
    save(cfg)
    fix_perms(cfg)
    write_samba(cfg)
    restart_web()
    say(f"\nDone.  {user} can now:")
    say(f"  map the drive   \\\\unstablenhp\\{camp}   (user {user}, the password you just set)")
    say(f"  build at        http://unstablenhp/")


def cmd_passwd(args):
    need_root()
    if len(args) != 1:
        die("Usage: passwd <username>")
    cfg = load()
    if args[0] not in cfg["gms"]:
        die(f"{args[0]} is not a GM.  Known: {', '.join(cfg['gms'])}")
    pw = ask_password(args[0])
    cfg["gms"][args[0]]["password"] = hash_password(pw)
    save(cfg)
    set_smb_password(args[0], pw)
    say("Password changed for the web page and the shared drives.")


def cmd_update(args):
    need_root()
    cfg = load()
    if SOURCE.resolve() == ROOT.resolve():
        die("Run update from the NEW unzipped omnislate folder (for example ~/Downloads/omnislate), not from /srv/omnislate.")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / stamp
    items = ENGINE + (["library"] if "--library" in args else [])
    say(f"Backing up the current engine to {backup}...")
    for rel in items:
        src = ROOT / rel
        if src.exists():
            copy_item(src, backup / rel)
    say("Installing the new engine files...")
    for rel in items:
        if (SOURCE / rel).exists():
            copy_item(SOURCE / rel, ROOT / rel)
    fix_perms(cfg)
    write_samba(cfg)
    restart_web()
    ver = next((l.split('"')[1] for l in (ROOT / "build.py").read_text(encoding="utf-8").splitlines() if l.startswith("ENGINE =")), "?")
    say(f"Done.  Engine {ver} installed.  Campaigns and dist were left alone.  Auto-build will refresh session files shortly.")


def cmd_autobuild(args):
    need_root()
    if not args or args[0] not in ("on", "off"):
        die("Usage: autobuild on|off")
    cfg = load()
    cfg["autobuild"] = args[0] == "on"
    save(cfg)
    say(f"Auto-build is {args[0]}.")


def cmd_limit(args):
    need_root()
    try:
        gb = float(args[0])
    except (IndexError, ValueError):
        die("Usage: limit <gigabytes>")
    cfg = load()
    cfg["limit_gb"] = gb
    save(cfg)
    say(f"Space limit is {gb:g} GB per campaign.")


def cmd_fix_perms(args):
    need_root()
    cfg = load()
    fix_perms(cfg)
    write_samba(cfg)
    say("Permissions and shares reapplied.")


def cmd_status(args):
    cfg = load()
    say(f"Workshop: {ROOT}   auto-build: {'on' if cfg.get('autobuild', True) else 'off'}   limit: {cfg.get('limit_gb', 20)} GB per campaign")
    for name, gm in cfg["gms"].items():
        say(f"  GM {name:<12} {'admin (all campaigns)' if gm.get('admin') else ', '.join(gm.get('campaigns', [])) or 'no campaigns'}")
    for c in sorted(p for p in (ROOT / "campaigns").iterdir() if p.is_dir()):
        size = sum(f.stat().st_size for f in c.rglob("*") if f.is_file())
        say(f"  campaign {c.name:<24} {size / 1024 ** 2:8.1f} MB")
    r = run(["systemctl", "is-active", "omnislate-web"], check=False, capture_output=True, text=True)
    s = run(["systemctl", "is-active", "smbd"], check=False, capture_output=True, text=True)
    say(f"  web service: {r.stdout.strip()}   samba: {s.stdout.strip()}")


COMMANDS = {"install": cmd_install, "add-gm": cmd_add_gm, "passwd": cmd_passwd, "update": cmd_update,
            "autobuild": cmd_autobuild, "limit": cmd_limit, "fix-perms": cmd_fix_perms, "status": cmd_status}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    try:
        COMMANDS[sys.argv[1]](sys.argv[2:])
    except subprocess.CalledProcessError as e:
        die(f"A system command failed: {' '.join(map(str, e.cmd))}")
