#!/usr/bin/env python3
"""Deterministic screenshot walk of an OMNISLATE session file.

usage: shoot.py URL OUTDIR WxH [WxH ...] [--states a,b,c]
Clock and Math.random are frozen so two builds can be pixel-diffed.
"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

SEED = """
document.addEventListener("DOMContentLoaded", () => { const st = document.createElement("style");
  st.textContent = "canvas.noise,#seqNoise,.globe-wrap canvas,#clock,[data-ts],video{visibility:hidden !important}";
  document.head.append(st); });
(() => { let s = 1234567; Math.random = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; }; })();
"""

def walk(page, out, tag, log):
    def shot(name, full=False):
        page.screenshot(path=str(out / f"{tag}-{name}.png"), full_page=full, animations="disabled")
    page.clock.run_for(7000)
    shot("01-boot")
    page.click("#boot")
    page.clock.run_for(1500)
    shot("02-scan", True)
    page.click("#tabBriefs")
    page.clock.run_for(800)
    shot("03-briefs", True)
    page.click("#tabScan")
    page.clock.run_for(800)
    page.keyboard.press("Control+Shift+G")
    page.clock.run_for(800)
    shot("04-gm")
    log.append({"tag": tag, "gmText": page.inner_text("#gm")})
    if page.is_disabled("#gmFire") or not page.is_visible("#gmFire"):
        log.append({"tag": tag, "note": "no fire button"})
        return
    page.click("#gmFire")
    page.clock.run_for(600)
    shot("05-seq1")
    page.clock.run_for(1900)
    shot("06-seq2")
    page.clock.run_for(3500)
    shot("07-seq3")
    page.clock.run_for(2500)
    shot("08-fired-briefs", True)
    page.click("#tabScan")
    page.clock.run_for(800)
    shot("09-fired-scan", True)
    page.reload()
    page.clock.run_for(7000)
    shot("10-reloaded", True)


def main():
    args = sys.argv[1:]
    url, outdir = args[0], Path(args[1])
    sizes = [a for a in args[2:] if "x" in a and not a.startswith("--")]
    outdir.mkdir(parents=True, exist_ok=True)
    log = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        for s in sizes:
            w, h = map(int, s.split("x"))
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type in ("error",) and "404" not in m.text else None)
            page.add_init_script(SEED)
            page.clock.install(time=1793000000000)
            page.goto(url)
            walk(page, outdir, s, log)
            log.append({"tag": s, "errors": errs})
            ctx.close()
        b.close()
    (outdir / "log.json").write_text(json.dumps(log, indent=1))
    for e in log:
        if e.get("errors"):
            print("ERRORS", e["tag"], e["errors"])
    print("done", outdir)

if __name__ == "__main__":
    main()
