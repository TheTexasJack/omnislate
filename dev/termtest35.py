#!/usr/bin/env python3
"""ANDIS attachments: quick hack with no routing, folders, printer, text and image views."""
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
    pt = pg.evaluate("""(label) => { const T = window.__omniTerm, R = T.reveal, c = document.getElementById('tmCv');
      const ri = R.rows.findIndex(r => r.act && r.cs.map(x => x.c).join('').includes(label)); if (ri < 0) return null;
      R.scroll = Math.max(0, Math.min(ri - 1, R.rows.length - 1)); const r = c.getBoundingClientRect();
      return [r.left + r.width / 2, r.top + (3 + (ri - R.scroll) * 10 + 5) * r.height / c.height]; }""", label)
    if not pt: return False
    pg.mouse.click(*pt); return True
mode = lambda pg: pg.evaluate("() => window.__omniTerm.mode")
kind = lambda pg: pg.evaluate("() => window.__omniTerm.reveal && window.__omniTerm.reveal.kind")
with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h, tag) in [(1088, 680, "land"), (680, 1088, "port")]:
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.clock.install()
        pg.goto(BASE + "errans-inter-astra/regulators/regulators-session-1.html?omnitest")
        pg.clock.run_for(1500); pg.click("#boot"); pg.click("#bTerm"); pg.clock.run_for(300)
        check(f"{tag}: printer is on the stage", pg.locator("#tmPrinter").is_visible())
        plug_in(pg); pg.clock.run_for(1500)
        pg.keyboard.type('LOAD "NORTHWATCH",8,1'); pg.keyboard.press("Enter"); pg.clock.run_for(4500)
        pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.clock.run_for(300)
        check(f"{tag}: Routes 0 goes straight to the countdown", mode(pg) == "count")
        pg.clock.run_for(16000); pg.clock.run_for(6000)
        check(f"{tag}: 15 seconds later the files are open", mode(pg) == "reveal")
        pg.screenshot(path=str(OUT / f"{tag}-nw-1-files.png"))
        check(f"{tag}: tap [M] INCIDENTS", tap(pg, "INCIDENTS")); pg.clock.run_for(200)
        check(f"{tag}: folder shows the disk directory", kind(pg) == "M")
        pg.screenshot(path=str(OUT / f"{tag}-nw-2-dir.png"))
        tap(pg, "NW-4404"); pg.clock.run_for(1200)
        check(f"{tag}: a [D] file runs the printer", mode(pg) == "print" and "out" in pg.locator("#tmPaper").get_attribute("class"))
        pg.screenshot(path=str(OUT / f"{tag}-nw-3-printing.png"))
        pg.clock.run_for(2500)
        check(f"{tag}: print completes", pg.evaluate("() => window.__omniTerm.print.done"))
        pg.screenshot(path=str(OUT / f"{tag}-nw-4-printed.png"))
        pg.mouse.click(*[v for v in (pg.locator("#tmCv").bounding_box()["x"] + 40, pg.locator("#tmCv").bounding_box()["y"] + 40)])
        pg.clock.run_for(200)
        check(f"{tag}: tap returns to the folder", mode(pg) == "reveal" and kind(pg) == "M")
        tap(pg, "PRINT ALL"); pg.clock.run_for(300)
        check(f"{tag}: PRINT ALL queues five", pg.evaluate("() => window.__omniTerm.print.items.length") == 5)
        pg.mouse.click(pg.locator("#tmCv").bounding_box()["x"] + 40, pg.locator("#tmCv").bounding_box()["y"] + 40); pg.clock.run_for(200)
        check(f"{tag}: tap skips the print", pg.evaluate("() => window.__omniTerm.print.done"))
        pg.keyboard.press("Enter"); pg.clock.run_for(200); pg.keyboard.press("Enter"); pg.clock.run_for(200)
        check(f"{tag}: RETURN backs out to the message", kind(pg) == "msg")
        pg.keyboard.press("Enter"); pg.clock.run_for(200)
        check(f"{tag}: RETURN again goes to the prompt", mode(pg) == "prompt")
        check(f"{tag}: no page errors (regulators)", not errs)
        # starter: text and image
        pg.goto(BASE + "_starter/chapter-1/session-1.html?omnitest"); errs.clear()
        pg.clock.run_for(1500); pg.click("#boot"); pg.click("#bTerm"); pg.clock.run_for(300)
        pg.evaluate("() => { const k = Object.keys(localStorage).find(k => k.includes('example-beacon')); }")
        plug_in(pg); pg.clock.run_for(1500)
        pg.keyboard.type('LOAD "BEACON",8,1'); pg.keyboard.press("Enter"); pg.clock.run_for(4500)
        pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(200); pg.click("#gmSigSkip"); pg.click("#gmClose"); pg.clock.run_for(200)
        pg.keyboard.type("RUN"); pg.keyboard.press("Enter"); pg.clock.run_for(6000)
        check(f"{tag}: starter decoded", kind(pg) == "msg")
        pg.screenshot(path=str(OUT / f"{tag}-st-1-msg.png"))
        tap(pg, "HOLLIS LOG"); pg.clock.run_for(200)
        check(f"{tag}: [T] opens the text", kind(pg) == "T")
        pg.screenshot(path=str(OUT / f"{tag}-st-2-text.png"))
        tap(pg, "[BACK]"); pg.clock.run_for(200)
        check(f"{tag}: [BACK] tag returns", kind(pg) == "msg")
        tap(pg, "KESTREL"); pg.clock.run_for(500)
        check(f"{tag}: [I] opens the image", kind(pg) == "I")
        pg.screenshot(path=str(OUT / f"{tag}-st-3-image.png"))
        check(f"{tag}: no page errors (starter)", not errs)
        if errs: print(errs[:3])
        ctx.close()
    b.close()
print(f"\n{P} passed, {F} failed")
