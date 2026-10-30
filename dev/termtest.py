#!/usr/bin/env python3
"""ANDIS terminal walk-through: plug, errors, LOAD, routing, countdown, reveal, GM controls, layouts.
usage: termtest.py URL OUTDIR"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
P = F = 0
def check(name, cond):
    global P, F
    print(("PASS " if cond else "FAIL ") + name); P += bool(cond); F += (not cond)

def plug_in(pg):
    pb = pg.locator("#tmPlug").bounding_box(); po = pg.locator("#tmPort").bounding_box()
    pg.mouse.move(pb["x"] + pb["width"] / 2, pb["y"] + pb["height"] / 2); pg.mouse.down()
    tx, ty = po["x"] + po["width"] / 2, po["y"] + po["height"] / 2 - 4
    for i in range(1, 13):
        pg.mouse.move(pb["x"] + (tx - pb["x"]) * i / 12, pb["y"] + (ty - pb["y"]) * i / 12)
    pg.mouse.up()

def screen(pg):
    return pg.evaluate("() => window.__omniTerm.lines.map(l => l[1]).join('\\n')")

def solve(pg):
    info = pg.evaluate("""() => { const T = window.__omniTerm, g = T.route.g, c = document.getElementById('tmCv'), r = c.getBoundingClientRect();
      const sx = r.width / c.width, sy = r.height / c.height;
      return T.route.sol.map(path => path.map(i => [r.left + (g.x0 + (i % g.cols) * g.cw + g.cw / 2) * sx, r.top + (g.y0 + (i / g.cols | 0) * g.ch + g.ch / 2) * sy])); }""")
    for path in info:
        pg.mouse.move(*path[0]); pg.mouse.down()
        for pt in path[1:]:
            pg.mouse.move(*pt, steps=3)
        pg.mouse.up()

with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h, tag) in [(1088, 680, "land"), (680, 1088, "port"), (1920, 1080, "big")]:
        ctx = b.new_context(viewport={"width": w, "height": h}, has_touch=True)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.clock.install()
        pg.goto(URL + ("&" if "?" in URL else "?") + "omnitest")
        pg.clock.run_for(1500); pg.click("#boot"); pg.clock.run_for(500)
        check(f"{tag}: ANDIS button visible", pg.locator("#bTerm").is_visible())
        pg.click("#bTerm"); pg.clock.run_for(300)
        check(f"{tag}: terminal opens", pg.locator("#tm").is_visible())
        pg.screenshot(path=str(OUT / f"{tag}-1-unplugged.png"))
        pg.keyboard.press("A"); pg.clock.run_for(100)
        check(f"{tag}: typing before plug says NO INPUT DEVICE", pg.locator("#tmHint").inner_text() == "NO INPUT DEVICE")
        plug_in(pg); pg.clock.run_for(1500)
        check(f"{tag}: cable connects", pg.evaluate("() => window.__omniTerm.connected"))
        check(f"{tag}: banner printed", "3583 BYTES FREE" in screen(pg))
        if tag == "land":
            for k in "HELLO":
                pg.locator(f".tm-key[data-k='{k}']").tap()
            pg.locator(".tm-key[data-k='RETURN']").tap(); pg.clock.run_for(200)
            check("land: on-screen keys type, junk gives ?SYNTAX  ERROR", "?SYNTAX  ERROR" in screen(pg) and "HELLO" in screen(pg))
            pg.keyboard.type('LOAD "PROXIMA",8,1'); pg.keyboard.press("Enter"); pg.clock.run_for(1500)
            check("land: wrong name gives ?FILE NOT FOUND  ERROR", "?FILE NOT FOUND  ERROR" in screen(pg))
            pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.clock.run_for(300)
            check("land: RUN with nothing loaded is harmless", pg.evaluate("() => window.__omniTerm.mode") == "prompt")
        pg.keyboard.type('LOAD "REMNANT",8,1'); pg.keyboard.press("Enter"); pg.clock.run_for(1200)
        check(f"{tag}: loading stripes on", "load" in pg.locator("#tmGlass").get_attribute("class"))
        pg.screenshot(path=str(OUT / f"{tag}-2-loading.png"))
        pg.clock.run_for(3000)
        check(f"{tag}: LOAD finds REMNANT", "SEARCHING FOR REMNANT" in screen(pg) and screen(pg).rstrip().endswith("READY."))
        pg.screenshot(path=str(OUT / f"{tag}-3-ready.png"))
        pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.clock.run_for(300)
        check(f"{tag}: RUN starts routing", pg.evaluate("() => window.__omniTerm.mode") == "route")
        pg.screenshot(path=str(OUT / f"{tag}-4-route.png"))
        solve(pg); pg.clock.run_for(1500)
        check(f"{tag}: solved routing starts the countdown", pg.evaluate("() => window.__omniTerm.mode") == "count")
        pg.clock.run_for(4000)
        pg.screenshot(path=str(OUT / f"{tag}-5-count.png"))
        if tag == "land":
            pg.click("#tmClose"); pg.clock.run_for(200)
            pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(300)
            st = pg.locator("#gmSigStatus").inner_text()
            check("land: GM panel shows the countdown", "decrypting" in st and "01:5" in st)
            pg.click("#gmSigPause"); pg.clock.run_for(5000)
            check("land: Pause holds the clock", "on hold" in pg.locator("#gmSigStatus").inner_text())
            pg.click("#gmSigPause"); pg.click("#gmSigAdd"); pg.clock.run_for(300)
            check("land: Add 10 min", "02:0" in pg.locator("#gmSigStatus").inner_text())
            pg.screenshot(path=str(OUT / "land-6-gm.png"))
            pg.click("#gmClose"); pg.clock.run_for(200)
            pg.clock.fast_forward(2 * 3600 * 1000 + 15 * 60 * 1000); pg.clock.run_for(500)
            check("land: ANDIS button pulses when decoded", "done" in pg.locator("#bTerm").get_attribute("class"))
            pg.click("#bTerm"); pg.clock.run_for(300)
            check("land: reopening mid-hack resumes, cable stays in", pg.evaluate("() => window.__omniTerm.connected"))
            pg.clock.run_for(800)
        else:
            pg.clock.fast_forward(2 * 3600 * 1000 + 15 * 60 * 1000); pg.clock.run_for(500)
        pg.clock.run_for(1500)
        check(f"{tag}: countdown ends in the reveal", pg.evaluate("() => window.__omniTerm.mode") == "reveal")
        pg.screenshot(path=str(OUT / f"{tag}-7-scrub.png"))
        pg.clock.run_for(6000)
        check(f"{tag}: reveal finishes and is remembered", pg.evaluate("() => window.__omniTerm.reveal.done")
              and pg.evaluate("() => JSON.parse(Object.entries(localStorage).find(([k]) => k.includes('remnant-buoy'))[1]).seen"))
        pg.screenshot(path=str(OUT / f"{tag}-8-decoded.png"))
        sw = pg.evaluate("() => document.documentElement.scrollWidth <= innerWidth")
        check(f"{tag}: no horizontal scroll", sw)
        if tag == "land":
            pg.reload(); pg.clock.run_for(1500); pg.click("#boot"); pg.click("#bTerm"); pg.clock.run_for(300)
            check("land: after reload the cable starts unplugged", not pg.evaluate("() => window.__omniTerm.connected"))
            plug_in(pg); pg.clock.run_for(1500)
            pg.keyboard.type('LOAD "REMNANT",8,1'); pg.keyboard.press("Enter"); pg.clock.run_for(5000)
            pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.clock.run_for(300)
            check("land: a decoded signal opens straight to the message", pg.evaluate("() => window.__omniTerm.mode") == "reveal"
                  and pg.evaluate("() => window.__omniTerm.reveal.done"))
            pg.keyboard.press("Escape"); pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(200)
            pg.click("#gmSigReset"); pg.clock.run_for(200)
            check("land: Reset signal clears it", "not started" in pg.locator("#gmSigStatus").inner_text())
        check(f"{tag}: no page errors", not errs)
        if errs: print("   ", errs[:3])
        ctx.close()
    b.close()
print(f"\n{P} passed, {F} failed")
