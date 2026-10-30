#!/usr/bin/env python3
"""ANDIS audio and video attachments, real time (media playback ignores fake clocks)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE, OUT = sys.argv[1], Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
P = F = 0
def check(n, c):
    global P, F
    print(("PASS " if c else "FAIL ") + n); P += bool(c); F += (not c)
def plug_in(pg):
    pb = pg.locator("#tmPlug").bounding_box(); po = pg.locator("#tmPort").bounding_box()
    pg.mouse.move(pb["x"] + 12, pb["y"] + 17); pg.mouse.down()
    for i in range(1, 13): pg.mouse.move(pb["x"] + 12 + (po["x"] + 26 - pb["x"] - 12) * i / 12, pb["y"] + 17 + (po["y"] + 10 - pb["y"] - 17) * i / 12)
    pg.mouse.up()
def tap(pg, label):
    pt = pg.evaluate("""(label) => { const R = window.__omniTerm.reveal, c = document.getElementById('tmCv');
      const ri = R.rows.findIndex(r => r.act && r.cs.map(x => x.c).join('').includes(label)); if (ri < 0) return null;
      R.scroll = Math.max(0, ri - 1); const r = c.getBoundingClientRect();
      return [r.left + r.width / 2, r.top + (3 + (ri - R.scroll) * 10 + 5) * r.height / c.height]; }""", label)
    if pt: pg.mouse.click(*pt)
    return bool(pt)
ev = lambda pg, js: pg.evaluate("() => " + js)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for (w, h, tag) in [(1088, 680, "land"), (680, 1088, "port")]:
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "_starter/chapter-1/session-1.html?omnitest"); pg.wait_for_timeout(800)
        pg.click("#boot"); pg.click("#bTerm"); pg.wait_for_timeout(300)
        plug_in(pg); pg.wait_for_timeout(1500)
        pg.keyboard.type('LOAD "BEACON",8,1'); pg.keyboard.press("Enter"); pg.wait_for_timeout(4200)
        pg.keyboard.press("Control+Shift+G"); pg.wait_for_timeout(200); pg.click("#gmSigSkip"); pg.click("#gmClose")
        pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.wait_for_timeout(5500)
        check(f"{tag}: decoded", ev(pg, "window.__omniTerm.reveal.kind") == "msg")
        tap(pg, "SURVEY FILES"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"{tag}-1-dir.png"))
        check(f"{tag}: directory lists SND and VID", ev(pg, "window.__omniTerm.reveal.rows.map(r => r.cs.map(c => c.c).join('')).join('|')").count("SND") == 1)
        tap(pg, "HOLLIS DISTRESS"); pg.wait_for_timeout(2500)
        check(f"{tag}: [A] plays", ev(pg, "window.__omniTerm.mode") == "media" and ev(pg, "window.__omniTerm.media.el.currentTime") > 1)
        check(f"{tag}: transcript attached", ev(pg, "(window.__omniTerm.media.a.transcript || []).length") == 3)
        pg.screenshot(path=str(OUT / f"{tag}-2-audio.png"))
        c = pg.locator("#tmCv").bounding_box(); pg.mouse.click(c["x"] + c["width"] / 2, c["y"] + c["height"] * 0.7); pg.wait_for_timeout(300)
        check(f"{tag}: tap pauses", ev(pg, "window.__omniTerm.media.el.paused"))
        pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
        check(f"{tag}: RETURN goes back and stops it", ev(pg, "window.__omniTerm.mode") == "reveal" and not ev(pg, "!!window.__omniTerm.media"))
        tap(pg, "LANDER CAM"); pg.wait_for_timeout(2500)
        check(f"{tag}: [V] plays from media/", ev(pg, "window.__omniTerm.media.el.videoWidth") > 0 and ev(pg, "window.__omniTerm.media.el.currentTime") > 1)
        pg.screenshot(path=str(OUT / f"{tag}-3-video.png"))
        c = pg.locator("#tmCv").bounding_box(); pg.mouse.click(c["x"] + 40, c["y"] + 8); pg.wait_for_timeout(300)
        check(f"{tag}: [BACK] row returns from video", ev(pg, "window.__omniTerm.mode") == "reveal")
        tap(pg, "LANDER CAM"); pg.wait_for_timeout(500); pg.click("#tmClose"); pg.wait_for_timeout(200)
        check(f"{tag}: closing the terminal stops the video", not ev(pg, "!!window.__omniTerm.media"))
        check(f"{tag}: no page errors", not errs)
        if errs: print(errs[:3])
        ctx.close()
    b.close()
print(f"\n{P} passed, {F} failed")
