OMNISLATE developer test tools (for Claudia or Mara threads, never needed at the table)

Serve the workshop with a dist link, then run the checks:
  mkdir -p ~/serve && ln -s "$PWD/dist" ~/serve/new && (cd ~/serve && python3 -m http.server 8765 &)

  shoot.py URL OUTDIR 1088x680 680x1088   frozen-clock screenshots of a session, for pixel parity
  diff.py OLDDIR NEWDIR                     pixel diff of two shoot.py runs (only the GM stamp should differ)
  functional.py                             boot, triggers, alert start, big screens (expects /new/ paths)
  termtest.py URL OUTDIR                    ANDIS: cable, errors, LOAD, routing, countdown, GM controls, reveal
  termtest35.py BASE OUTDIR                 ANDIS attachments, folders, printer
  termtest36.py BASE OUTDIR                 ANDIS audio and video (real time)
  font57.py                                 prints the 5x7 ANDIS pixel font table; --png FILE draws a test sheet

Pages need ?omnitest in the URL for the ANDIS tests (it exposes the terminal state to the test).
term-source.js is the ANDIS block of app/display.html with the font table left as /*__FONT5__*/.
Playwright with Chromium is required.  Take parity baselines from the previous release before changing the engine.
