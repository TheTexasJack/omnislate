#!/usr/bin/env python3
"""Functional checks for the 3.0 features: multi-trigger GM panel, reveal, attack, persistence, Start: alert, big screens."""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765/new/"
OUT = Path("/home/claude/shots/func"); OUT.mkdir(parents=True, exist_ok=True)
results = []

def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (("  " + detail) if detail and not cond else ""))

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
    def page_for(url, w=1088, h=680):
        ctx = b.new_context(viewport={"width": w, "height": h})
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.clock.install(time=1793000000000)
        pg.goto(url); pg.clock.run_for(6000)
        return ctx, pg, errs

    # ---------- starter: two triggers ----------
    ctx, pg, errs = page_for(BASE + "_starter/chapter-1/session-1.html")
    pg.screenshot(path=str(OUT / "starter-boot.png"))
    check("starter boot motto", pg.inner_text("#bootMotto").strip().lower() == "eyes open, steel ready")
    check("starter generated crest present", pg.locator("#bootCrest svg.crest").count() == 1)
    pg.click("#boot"); pg.clock.run_for(1200)
    pg.screenshot(path=str(OUT / "starter-scan.png"), full_page=True)
    check("starter briefs count 1", pg.inner_text("#briefCount").strip() == "1")
    check("starter net name", pg.inner_text("#netName") == "Field Survey Network")
    pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(500)
    pg.screenshot(path=str(OUT / "starter-gm.png"))
    trig = pg.locator("#gmTrigs button")
    check("gm shows 2 trigger buttons", trig.count() == 2, str(trig.count()))
    check("gm stamp", "OMNISLATE 3." in pg.inner_text("#gmStamp"))
    check("gm sound builtin chime", "Built-in chime" in pg.inner_text("#gmKlaxonInfo"), pg.inner_text("#gmKlaxonInfo"))
    # fire reveal
    pg.click("#gmFire"); pg.clock.run_for(400)
    check("reveal: gm closed", pg.locator("#gm").is_hidden())
    check("reveal: banner shown", pg.locator("#toast").is_visible() and "Encrypted packet" in pg.inner_text("#toast"))
    check("reveal: tab flash", "flash" in (pg.get_attribute("#tabBriefs", "class") or ""))
    check("reveal: skin still normal", pg.get_attribute("html", "data-alert") == "off")
    pg.screenshot(path=str(OUT / "starter-reveal-banner.png"))
    pg.click("#tabBriefs"); pg.clock.run_for(500)
    check("reveal: 2 briefs visible", pg.inner_text("#briefCount").strip() == "2")
    check("reveal: revealed card styling", pg.locator(".brief.revealed").count() == 1)
    pg.screenshot(path=str(OUT / "starter-reveal-briefs.png"), full_page=True)
    pg.clock.run_for(6000)
    check("reveal: banner auto hides", pg.locator("#toast").is_hidden())
    # arm attack with countdown
    pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(300)
    check("gm marks fired trigger", "(fired)" in pg.inner_text("#gmTrigs"))
    pg.locator("#gmTrigs button").nth(1).click(); pg.clock.run_for(200)
    check("gm selected attack shows alarm", "Built-in alarm" in pg.inner_text("#gmKlaxonInfo") or "klaxon" in pg.inner_text("#gmKlaxonInfo"), pg.inner_text("#gmKlaxonInfo"))
    pg.locator("#gmTimes button").first.click(); pg.clock.run_for(1000)
    check("armed: badge hollow", "armed" in (pg.get_attribute(".net-mark", "class") or ""))
    pg.clock.run_for(10000)
    check("attack: sequence running", not pg.locator("#seq").is_hidden())
    pg.screenshot(path=str(OUT / "starter-attack-seq.png"))
    pg.clock.run_for(8000)
    check("attack: alert skin on", pg.get_attribute("html", "data-alert") == "on")
    check("attack: military style", pg.get_attribute("html", "data-style") == "military")
    check("attack: net name", pg.inner_text("#netName").lower() == "sensor suite: emergency mode")
    check("attack: 3 briefs", pg.inner_text("#briefCount").strip() == "3")
    check("attack: emergency card", pg.locator(".brief.emergency").count() == 1)
    pg.screenshot(path=str(OUT / "starter-attack-briefs.png"), full_page=True)
    pg.click("#tabScan"); pg.clock.run_for(500)
    check("attack: feeds lost", "feed lost" in pg.inner_text("#dossier").lower())
    pg.screenshot(path=str(OUT / "starter-attack-scan.png"), full_page=True)
    # reload persistence
    pg.reload(); pg.clock.run_for(6000)
    check("reload: boot hidden", pg.locator("#boot").is_hidden())
    check("reload: alert persists", pg.get_attribute("html", "data-alert") == "on")
    check("reload: 3 briefs", pg.inner_text("#briefCount").strip() == "3")
    # reset
    pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(300)
    pg.click("#gmReset"); pg.clock.run_for(500)
    check("reset: normal skin", pg.get_attribute("html", "data-alert") == "off" and pg.get_attribute("html", "data-style") == "institutional")
    check("reset: 1 brief", pg.inner_text("#briefCount").strip() == "1")
    # preview skin
    pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(300)
    pg.click("#gmSkin"); pg.clock.run_for(200)
    check("preview: alert look", pg.get_attribute("html", "data-alert") == "on" and "Alert" in pg.inner_text("#gmSkin"))
    pg.click("#gmSkin"); pg.click("#gmClose")
    # arm on briefs
    pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(300)
    pg.locator("#gmTrigs button").nth(0).click()
    pg.click("#gmOnBriefs"); pg.clock.run_for(1000)
    pg.click("#tabBriefs"); pg.clock.run_for(500)
    check("arm-on-briefs fires reveal", pg.inner_text("#briefCount").strip() == "2")
    check("starter: no page errors", not errs, "; ".join(errs))
    ctx.close()

    # ---------- errans: single trigger keeps old panel layout ----------
    ctx, pg, errs = page_for(BASE + "errans-inter-astra/halas/tlc-session-2.html")
    pg.click("#boot"); pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(400)
    check("errans: trigger chooser hidden", pg.locator("#gmTrigs").is_hidden())
    check("errans: embedded klaxon", "Embedded klaxon.mp3" in pg.inner_text("#gmKlaxonInfo"), pg.inner_text("#gmKlaxonInfo"))
    check("errans: no page errors", not errs, "; ".join(errs))
    ctx.close()

    # ---------- errans: no triggers ----------
    ctx, pg, errs = page_for(BASE + "errans-inter-astra/halas/tlc-session-1.html")
    pg.click("#boot"); pg.keyboard.press("Control+Shift+G"); pg.clock.run_for(400)
    check("no triggers: arm block hidden", pg.locator("#gmTrigBlock").is_hidden())
    check("no triggers: status line", "No triggers" in pg.inner_text("#gmStatus"))
    pg.screenshot(path=str(OUT / "errans-s1-gm.png"))
    check("no triggers: no page errors", not errs, "; ".join(errs))
    ctx.close()

    # ---------- Start: alert ----------
    ctx, pg, errs = page_for(BASE + "errans-inter-astra/halas/test-alert-start.html")
    pg.screenshot(path=str(OUT / "alert-start-boot.png"))
    check("alert start: boot lines", "HALAS ACADEMY NETWORK" in pg.inner_text("#bootLines").upper())
    check("alert start: crest hidden", pg.locator("#bootCrest").is_hidden())
    check("alert start: data-alert on", pg.get_attribute("html", "data-alert") == "on")
    pg.click("#boot"); pg.clock.run_for(800)
    check("alert start: feeds lost", "feed lost" in pg.inner_text("#dossier").lower())
    pg.screenshot(path=str(OUT / "alert-start-scan.png"), full_page=True)
    check("alert start: no page errors", not errs, "; ".join(errs))
    ctx.close()

    # ---------- big screens ----------
    for w, h in ((1920, 1080), (2560, 1440)):
        for name in ("errans-inter-astra/halas/tlc-session-2.html", "_starter/chapter-1/session-1.html"):
            ctx, pg, errs = page_for(BASE + name, w, h)
            pg.screenshot(path=str(OUT / f"{w}-{name.split('/')[0]}-boot.png"))
            pg.click("#boot"); pg.clock.run_for(1000)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            check(f"{w}x{h} {name}: no horizontal scroll", sw <= w, f"scrollWidth {sw}")
            pg.screenshot(path=str(OUT / f"{w}-{name.split('/')[0]}-scan.png"))
            pg.click("#tabBriefs"); pg.clock.run_for(400)
            pg.screenshot(path=str(OUT / f"{w}-{name.split('/')[0]}-briefs.png"))
            check(f"{w}x{h} {name}: no page errors", not errs, "; ".join(errs))
            ctx.close()
    b.close()

fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
