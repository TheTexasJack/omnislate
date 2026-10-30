# OMNISLATE: Project Handoff

**OMNISLATE**
*Portable Multimodal Survey, Intelligence, and Mission Display*

*Revised 2026-10-27: Build 3.6 finishes the ANDIS with [A] voice logs (live waveform, typed transcript) and [V] video with a live 90s FMV effect.  Build 3.5 adds ANDIS attachments: tappable [T] text, [I] image, [D] print, and [M] folder tags under a decoded signal, a dot-matrix printer prop, and Routes: 0 for quick hacks, with the Northwatch jailbreak as the first use.  Also the OMNISLATE principle, the Andi System lore, and the long-term web interface direction.  Build 3.4 adds the ANDIS terminal: a retro workstation where the lance plugs in a keyboard, LOADs a coded signal by name, plays a carrier-routing minigame, waits out a real-clock countdown, and reads the decoded packet.  First signal: the Proxima Prime drift packet in Remnant.  Build 3.3 adds chapters: Errans Inter Astra is now an umbrella campaign with The Last Class (`halas`), Remnant, and The Regulators inside it, under Nathan's PROMETHEUS crest, and a new chapter folder shows up on its own for every GM.  Also a no-script notice and auto-build fixes.  Build 3.2 adds the unstableNHP server (Cheese Block, Mint 22.3, Tailscale only): a shared workshop, per-GM build web page, Samba drives, and auto-build, chosen with Jarrett as the Windows answer.  Build 3.1 adds the Deep Scan tab, procedural wireframe planets, the world atlas, the NEW WORLD TEMPLATE, Larkspur, and in-fiction handling of bad world data.  Build 3.0 (same day):  The engine is campaign-agnostic, campaigns live in their own folders, the single 06:47 event became named triggers, and a starter campaign plus a desktop launcher let a second GM (Jarrett) run his own table.  Roadmap updated with statuses.  The workshop folder is now `omnislate/`.*

We're continuing work on **OMNISLATE**, the in-fiction mech display that started with my Lancer campaign *Errans Inter Astra*.  This file brings you up to speed on what exists, how it works, the decisions already made, and what comes next.  Read it fully before suggesting changes.  Rebuilding something that already works is the fastest way to waste a session.

This handoff and the latest uploaded workshop files are canonical.  Two assistants work on this project: Claudia (Claude) and Mara (ChatGPT).  Every decision should stay compatible with the architecture and naming conventions documented here.

You will be handed this file, `omnislate_<version>.zip` (the workshop, such as `omnislate_3.6.zip`), and sometimes a session HTML from the tablet.  `ENHANCEMENTS.md` inside the zip holds the detailed backlog.

---

## 1. What OMNISLATE Is

A display for the game table: an Android tablet that gets passed around as a mech's cockpit screen, and possibly the monitors built into the shop's new gaming table.  It shows planetary scans, a live globe, drone camera feeds, mission briefs, and GM-fired events such as an attack or a decrypted intel drop.

The core idea: HTML owns every frame, label, number, and caption.  Image and video generators supply artwork only.  That keeps the interface identical from world to world even when the art style wanders.

As of Build 3.0 the engine knows nothing about any one campaign.  Each campaign supplies its own name, crest, motto, skins, worlds, briefs, and triggers.  In *Errans Inter Astra* the display belongs to the mech: during the Prelude it ran as the **Halas Academy Training Network**, and when the attack fired it dropped into the raw **GMS Sensor Suite** in emergency mode.

**Naming:** OMNISLATE is the system and product name.  The workshop folder is `omnislate/` (renamed from `gravis-display/` in Build 3.0).  My campaign as a whole is *Errans Inter Astra*, and everything of mine lives under `campaigns/errans-inter-astra/`.  Since Build 3.3 it is an umbrella with three chapters: *The Last Class* (`halas/`, the Prelude, ended), *Remnant* (`remnant/`, set outside Magnus), and *The Regulators* (`regulators/`).  Remnant and The Regulators run in my every-other-Saturday Lancer game.  The umbrella crest is the PROMETHEUS sigil, my Discord symbol.  Players will not recognize it, and they do not meet Pyretica again until Season 2.

**Users:** me, and Jarrett (owner of The Stoned Gnome), who asked for a copy for his own Lancer games.  Jarrett knows some HTML, but GMs should never have to code.  Everything a GM touches is a fill-in-the-blank text file.

---

## The OMNISLATE Principle

OMNISLATE is optional garnish on a premium, paid, in-person table.  The game runs fine without it.  Every feature adds feel, stays quick, and never gates anything, and it should deliver something Roll20 or any online table cannot: physical, tactile, and shared in the room.

- **Props first.**  The GM hands out every handout regardless, even with no tablet at all.  The tablet is theater around the paper.
- **Interaction is quick.  Payoff can be slow.**  A long timer is a reveal state.  It runs in the background, costs no table time, and lands when the story needs it.  The GM panel can always skip, pause, or add time.
- **Nothing on the tablet is the only place players can get information they need.**  No timer or minigame holds back something the GM is ready to give.  If a feature needs explaining at the table, it is too much.
- **Premium means polish over quantity.**  A few things that feel great beat many half-built ones.
- **Scale guardrails to the table.**  This is two GMs at a gaming table, so check the size of any safety or process step with Nathan before adding it.
- **Long-term direction:** everything moves to a web interface eventually.  The unstableNHP lockdown is a stopgap built under time pressure and is not to be expanded before then.

## Lore Notes (campaign material)

- **ANDIS** is the **Andi System**, an NHP that handles Blinknet communications.  The ANDIS UN.#30 workstation is its terminal.
- **Drift packets:** in canon the omninet is instantaneous.  At Nathan's table, Blinknet traffic can be bundled, relayed through buoys, or knocked loose by paracausal events and surface years late.  The Proxima Prime packet, received by different players 15, 5, and 2 years ago and a few days ago, is the first example.  Mark this as campaign material, never "correct" it back to canon.

## 2. Current State: Build 3.6 (2026-10-27)

### What changed in Build 3.6: ANDIS audio and video (ANDIS is feature complete)

- **`[A]` audio:** `.mp3`, `.wav`, `.ogg`, or `.m4a` from `signals/` or `sounds/`, baked into the page (Warn over 5 MB).  The CRT shows the name, caption, a live pixel waveform from the actual audio (yellow up to the playhead), `mm:ss / mm:ss`, and PLAYING / PAUSED / ENDED.  A `.txt` with the same name types out as the transcript in step with playback.
- **`[V]` video:** `.mp4` or `.webm` from the chapter's `media/` folder (copied beside the page like drone feeds).  Drawn on the CRT about 10 times a second at the screen's own resolution, with a 4x4 ordered dither to 64 colors and darkened interlace lines, plus a blinking REC and a time code in the pixel font.  A `file://` clip the browser will not let the page read back still gets the low resolution and interlace lines.
- **Decided with Nathan:** ANDIS video is always period-degraded.  Full-quality video goes through the Surface drone 01 feed (Expand) or is played by the GM separately.  Voice logs and video always play: the GM Sound switch covers effects only.  OMNISLATE is a prop, not a video game.
- **Controls:** tap to play or pause, tap the top two rows or press RETURN to go back, SPACE toggles.  Closing the terminal, unplugging, or Reset signal stops playback.  Directories list audio as SND and video as VID.
- **Starter:** the BEACON sample's SURVEY FILES folder has a voice log with a transcript and a short lander camera clip.
- **Tests:** a real-time audio and video suite passes in landscape and portrait, alongside the 3.4 and 3.5 suites.  Sessions without signals still match pixel for pixel apart from the GM stamp.

## Build 3.5 (2026-10-27)

### What changed in Build 3.5: ANDIS attachments

- **Attachments:** a signal's optional `### Attachments` list shows as tappable tags under the decoded message.  `- NAME: print` is `[D]`, `- NAME: file.png | caption` is `[I]` (from images/ or signals/), `- NAME: notes.txt` is `[T]` (from signals/), and `- NAME:` with items indented two spaces under it is an `[M]` folder.  Folders go one level deep.  Audio and video extensions are reserved and left out with a Warn line.
- **Folders** open as a C64 disk directory (`0 "INCIDENTS       " AN 2A`, block counts, `BLOCKS FREE.`), with a PRINT ALL line when two or more files print.
- **The printer:** an ANDIS LP-4 dot-matrix printer beside the monitor (below the keyboard in portrait).  A `[D]` tap prints a generic blurry tractor-feed page in about 3 seconds (1.6 seconds each for PRINT ALL) with synthesized print-head and line-feed sound, then `PRINT COMPLETE.  COLLECT OUTPUT.`  A tap skips it.  The page on screen is always the same generic sheet: the real document is the paper the GM hands over.
- **Navigation:** `[BACK]` tags and RETURN step back through folders and files to the message, then to the prompt.  Tags have two-row tap targets.
- **`Routes: 0`** skips the routing game and starts the countdown directly.
- **Content:** `regulators/signals/northwatch.md` (LOAD "NORTHWATCH", 15 seconds, no routing) with an INCIDENTS folder (NW-4404, NW-4405, NW-4412, NW-4418, NW-4421), COVER SHEET MEMO, RIPIT MEMO, and BP-A0288 LEGACY, all print.  The starter's BEACON sample gained one text file, one image, and a print folder.
- **Fixes:** `omnictl` no longer leaves root-owned Python cache files in the unzipped release folder.
- **Parity:** sessions without signals match 3.4 pixel for pixel apart from the GM stamp.  Attachment, printer, and navigation tests pass in landscape and portrait, and the 3.4 terminal suite still passes.

### Building on Beast

Beast keeps its own full copy of the workshop, unlocked, for Nathan's own testing and ideas.  Unzip, `sudo apt install python3-pil` and `./build.sh --install-launcher` once, then the **Build OMNISLATE** icon or `./build.sh errans`.  Pages land in `dist/<campaign>/<chapter>/`.  The server is a separate copy.

## Build 3.4 (2026-10-26)

### What changed in Build 3.4: the ANDIS terminal

- **What it is:** a separate machine, outside Scan and Briefs, opened from an ANDIS button in the top bar.  The button only exists in sessions with a `Signals:` line.  Look locked with Nathan from a mockup: cream CRT with an ANDIS UN.#30 badge, C64-blue screen with scanlines, creamy gray breadbox keyboard with black keys, four do-nothing F keys, and a SER port.  No Commodore names or logos anywhere.
- **Flow:** drag the loose cable to the SER port (it snaps in; the CRT warms up from a dot and degausses), then `LOAD "NAME",8,1` on the on-screen keyboard.  Android's own keyboard never opens.  A real keyboard works on laptops, mouse and touch alike.  Wrong name: `?FILE NOT FOUND  ERROR`.  Empty name: `?MISSING FILE NAME  ERROR`.  Anything else: `?SYNTAX  ERROR`.  Loading shows striped C64 loader bars and drive-head knocks for a few seconds only.  `RUN` starts signal routing (link matching carrier pairs on a grid without crossing; a crossing costs the Penalty; puzzles come from random walks, so a solution always exists).  Then a real-clock countdown with the corruption % rolling to zero, then the decoded packet scrubs in and scrolls.  The decoded text appears only at the end.  Every new hack starts with the cable unplugged.  A decoded signal opens straight to its message on later LOADs.
- **Font:** Claudia's own 5x7 pixel font, drawn on a canvas at half resolution, so it is identical on every device and needs no font file.  Characters it lacks (the glitch marks in Nathan's clue) render as sensor noise.
- **Files:** `signals/*.md` in the umbrella or a chapter, layered like briefs.  `## id`, then `Program`, `Time`, optional `Title`, `Corruption`, `Routes` (2 to 5), `Penalty`, `Image`, then `### Encoded` and `### Decoded` blocks kept line for line, with optional `[red]`, `[amber]`, `[green]` line colors.  Program names must be typeable on the ANDIS keyboard (letters, numbers, spaces, 16 at most) and unique per session.
- **Session line:** `Signals: id`, `id@decoded`, or `id@running 00:45:00`.  State persists in localStorage under the umbrella campaign, so it carries across chapters and sessions that open from the same place.  The session line is the guaranteed path.
- **GM panel:** ANDIS SIGNALS block with Skip to decoded, Pause/Resume, Add 10 min, Reset signal.  Reset session leaves signals alone on purpose.
- **Decided with Nathan:** whoever holds the tablet plays, with no system checks (the story hands them the code word).  Page-source snooping is not a concern.  A timer may run past game night.  No bleed-through, ghost typing, or paracausal effects yet (OMNI-063).
- **Content:** `remnant/signals/remnant-buoy.md` (LOAD "REMNANT", 02:00:00, 81.8% corruption), listed in `remnant-session-1`.  `_starter/signals/example.md` (LOAD "BEACON", ten minutes) is in the starter session.
- **Parity:** sessions without signals match 3.3 pixel for pixel; only the GM stamp's version changed.  A terminal walk-through test (plug, errors, LOAD, routing, countdown, GM controls, reveal, reload) passes at 1088 × 680, 680 × 1088, and 1920 × 1080.
- **Server:** `docs/SERVER_SETUP.md` section 9 covers copying the Remnant signal onto unstableNHP, since `update` never touches campaigns.

## Build 3.3 (2026-10-26)

### What changed in Build 3.3: chapters

- **Umbrella and chapters:** a campaign folder can hold chapter folders, each with its own `campaign.md`.  Any chapter folder with a `campaign.md` and a plain name (letters, numbers, dashes, underscores, no leading `_`) builds as its own target into `dist/<campaign>/<chapter>/`.  A new folder appears on its own: on the build page, in the build report, and in auto-build.  No config to edit, for Nathan or Jarrett.
- **Inheritance:** settings merge from the campaign's `campaign.md` down to the chapter's, setting by setting (skins merge per setting, triggers merge by id, boot lines and crest are replaced whole).  Files (worlds, briefs, images, sounds, media, crest) are looked up chapter first, then campaign, then `library/`.
- **`_template/`** inside each umbrella is the copy-me chapter.  Folders starting with `_` never build.  A folder that will not build because of its name (Windows names a copy `_template - Copy`) is named in the build report.
- **Back compatible:** a campaign with its own top-level `sessions/` still builds straight into `dist/<campaign>/`.  When a campaign switches to chapters, the next full build clears the old flat files from `dist/<campaign>/`.
- **CLI:** `./build.sh errans` builds every chapter, `./build.sh errans-inter-astra/remnant` builds one, and a session path inside a chapter builds one session.
- **Errans Inter Astra:** umbrella `campaign.md` (PROMETHEUS crest `prometheus.svg`, military skins on the GMS Sensor Suite, shared `worlds.md` with Halas, `halas-map.png`, `klaxon.mp3`).  `halas/` keeps the Halas Academy crest, motto, institutional skin, `halas-attack` trigger, briefs, sessions, and videos.  `remnant/` has `remnant-session-1` (Magnus at orbital, atlas at long range).  `regulators/` has a placeholder `regulators-session-1` (Larkspur at orbital, atlas at long range) to swap for the real first world.
- **`_starter`** is now an umbrella with `chapter-1/` and `_template/`, so `add-gm` gives Jarrett the same layout.
- **Build page:** each campaign card lists session files under each chapter's name, including chapters not built yet.  Report links work for chapter files.
- **Auto-build fixes:** edits saved while the service was down (or just before it started) now build on its first pass, and a save that lands during a Build-button run is picked up on the next pass.
- **No-script notice:** with JavaScript blocked (Nathan's script blocker did this), the boot screen reads "Sensor suite offline" and says to allow scripts, in place of a dead "Tap to connect."
- **Server migration:** `docs/SERVER_SETUP.md` section 8 swaps the flat 3.2 Errans folder on unstableNHP for the chapter layout and keeps the videos.
- **Parity:** `halas/tlc-session-2.html` matches 3.2 pixel for pixel on every player-facing screen.  Only the GM panel build stamp differs.

## Build 3.2 (2026-10-26)

### What changed in Build 3.2: the unstableNHP server

- **Box:** the Cheese Block (Beelink Mini S12, N95, 16 GB, 500 GB), hostname `unstableNHP`, Linux Mint 22.3 Cinnamon, no disk encryption, never sleeps, powers on after an outage.  Firewall (ufw) accepts only Tailscale traffic.  SSH from Beast works over Tailscale.
- **Tailscale:** free Personal plan (6 users).  Nathan's account owns the network.  Jarrett joins by invite.  Tablet and laptop join as Nathan's devices.  Player access, if it ever happens, goes through a Cloudflare Tunnel with Cloudflare Access instead (OMNI-085).  Never port-forward.
- **Workshop:** `/srv/omnislate`, the single source of truth.  Engine, library, and starter are read-only for GMs.  Each campaign belongs to its GM, with admin and the build service added by ACL.
- **Build page:** `http://unstablenhp/` (`server/web.py`, systemd service `omnislate-web`, user `omnibuild`).  Per-GM login, Build button for that GM's campaigns only, live report with links, session files served with video range support, auto-build about five seconds after a save, space meter.
- **Shared drives (Samba):** `\\unstablenhp\<campaign>` per campaign, `omnislate` read-only reference, `omnislate-admin` for Nathan.
- **Management:** `server/omnictl.py` handles install, add-gm, passwd, update (backs up the engine first, never touches campaigns or dist), autobuild, limit, fix-perms, and status.
- **Testing:** the build page and every omnictl step were tested in a sandbox.  Samba and ACL commands were simulated there, so unstableNHP is their first real run.  omnictl runs `testparm` before restarting Samba.

## Build 3.1 (2026-10-26)

### What changed in Build 3.1

- **Deep Scan tab:** a data screen per world.  Rotating wireframe reconstruction, orbit diagram with the habitable zone, Cradle comparison bars, readouts with estimates (escape velocity, density index, habitability index), and hazard flags.  The build computes every derived number from the fields allowed at the world's scan depth, so nothing held back can leak.
- **Wireframe planets:** procedural and seeded by slug, so a world always draws the same way and any new world works with no art.  Scan Class sets the base form (terrestrial, ocean, ice, desert, furnace, barren, tainted, grave, jovian, shattered).  Atmosphere sets the halo, temperature tints the lines, and moons, rings, settlement signatures, hotspots, fractures, and craters come from the data.  A world with no map shows the wireframe in the Scan tab globe panel.  A session whose first world has no map opens on Deep Scan.
- **Atlas:** `Atlas: long range` in a session file adds every other known world at that depth.  The Deep Scan catalog (with a filter box) becomes the world picker, and the Scan tab shows a single "World catalog" button once a session has more than six worlds.
- **NEW WORLD TEMPLATE:** a commented block at the top of every `worlds.md` with every field and its rules.  New optional fields: `Scan Class`, `Moons`, `Rings`.
- **Bad data is diegetic:** only structural problems stop the build (missing or duplicate Slug).  Everything else shows at the table as INTERFERENCE, BAD SCAN: RESAMPLE, NO RETURN, or TOO DISTANT, and the build report lists it under `Warn`.  `[interference]`, `[too distant]`, `[bad scan]`, and `[no return]` typed as a value hide it on purpose.  Locked fields now read TOO DISTANT (formerly "Scan required").
- **GM notes in world files:** any `###` section the parser does not know (such as Campaign Locations) is skipped and never reaches a session file.  HTML comments are skipped too.
- **Larkspur** joined the pool as world 31, without its campaign notes.
- **Parity:** `tlc-session-2.html` still matches the table file pixel for pixel everywhere except the tab row, which now has a third tab.

## Build 3.0 (2026-10-26)

### What changed from Build 2.2

- **Recovery:** the `gravis-display.zip` from the Mint box held a `display.html` older than Build 2.2 (no video feeds, no drone 01 panel).  The real 2.2 template was pulled back out of the `tlc-session-2.html` that ran at the table, and the old `build.py` plus that template rebuilt the table file byte for byte.  Build 3.0 starts from that recovered template.  Retire the old `gravis-display/` folder on Mint and use `omnislate/` from now on.
- **Guardrail:** Build 3.0's `tlc-session-2.html` matches the table file pixel for pixel on every player-facing screen (boot, scan, briefs, every stage of the attack, fired state, reload), at 1088 × 680 and 680 × 1088, with and without videos beside it.  Only the GM panel differs, on purpose.
- **Campaign folders** with `campaign.md`.
- **Triggers** with `attack` and `reveal` styles and per-trigger sounds (OMNI-010, OMNI-011).
- **`Start: alert`** for post-attack sessions (the start state from OMNI-012).
- **Build stamp** in the GM panel and plain-English build errors.
- **`build.sh` launcher**, the **`_starter` campaign**, and **`START-HERE.txt`**.
- **Media copied into `dist/<campaign>/`** on every build.
- **Generated crest** when a campaign has none.

### Architecture

- **One self-contained HTML file per session.**  Layout, code, text, images, and trigger sounds are baked in.
- **Workshop:** a Linux Mint machine holds the source files.  `build.py` turns them into session files.  My PC and the shop laptop run the same workshop.
- **Display:** the tablet only opens the finished file.  No Python, no install.  It runs from local files, or from the unstableNHP build page over Tailscale.
- **Media beside the file:** videos and stills sit in the same folder as the session HTML on the tablet and get picked up at runtime.

### How a Session File Gets Made

- `app/display.html` is the engine: all the code and styling, no content.  It has two slots, `/*__DATA__*/null` and `<!--__CREST__-->`.  Opened by itself it shows "No session data in this file."
- `build.py` reads the campaign's `campaign.md`, its worlds (campaign `worlds.md` first, then `library/worlds.md`), its briefs, and one session file.  It pulls each listed world at its scan depth, fixes map poles, converts images to WebP, embeds trigger sounds from `sounds/`, fills both slots, and writes `dist/<campaign>/<chapter>/<output>.html` (or `dist/<campaign>/<output>.html` for a campaign without chapters).  Anything beyond a world's scan depth never enters the file.  Then it copies `media/` from the campaign and the chapter into that same folder.
- Either assistant can run the build in its sandbox, or I can run it on Mint.  The workshop zip rides along with each thread because assistant sandboxes are wiped between sessions.
- **What to open:** the session file in `dist/<campaign>/<chapter>/`, such as `dist/errans-inter-astra/halas/tlc-session-2.html`.  `app/display.html` is the empty engine template and only shows a pointer to `dist/`.
- Never hand-edit a file in `dist/`.  Change the source and rebuild.  A hand edit disappears on the next build.

### Running a Build

- Desktop icon **Build OMNISLATE** (installed once with `./build.sh --install-launcher`), or `./build.sh` in a terminal: a menu of campaigns, then a report.
- `./build.sh errans` builds one campaign and all its chapters (a unique start of the name is enough).  `./build.sh errans-inter-astra/remnant` builds one chapter.  `python3 build.py <session file>` builds one session.  `python3 build.py --all` builds every campaign.  Folders starting with `_` are skipped by the menu and `--all`.
- Errors name the file and line and suggest the nearest match for typos.  Exit code 0 means everything built.

### Assumptions

- **Security is a light concern.**  Files are shared only with Jarrett and used at our own tables.  The page still runs under a strict Content Security Policy, renders all text through `textContent`, and the build refuses crest SVGs that contain scripts.
- **No web hosting yet.**  This runs locally on the tablet, a laptop, or the table monitors.  A web version for players' phones is a possible goal a year or two out.
- **Private and proprietary.**  OMNISLATE is for private use by Nathan and Jarrett at The Stoned Gnome.  There is no public release, and assistants should not plan around one.  If that ever changes, Nathan will say so, and security, licensing, and hosting get a full discussion then.  Standing rule regardless: never bundle Lancer game data.  Read GM exports (COMP/CON) only.

### Workshop Folder

```text
omnislate/
├── START-HERE.txt          first stop for a new GM: what to read, build, and open
├── app/display.html        engine (no campaign content)
├── build.py                builder
├── build.sh                launcher (menu, --install-launcher)
├── library/
│   ├── worlds.md           shared pool, worlds 01 to 31
│   └── images/
├── campaigns/
│   ├── _starter/           sample umbrella to copy: chapter-1/, _template/, setup README
│   └── errans-inter-astra/
│       ├── campaign.md     umbrella: name, PROMETHEUS crest, military skins
│       ├── prometheus.svg  umbrella crest
│       ├── worlds.md       Halas (00)
│       ├── images/         halas-map.png
│       ├── sounds/         klaxon.mp3 (embedded by the build)
│       ├── briefs/  media/ shared by every chapter (empty for now)
│       ├── notes/          Operation Halas Castigation recap (player safe, posted to Discord)
│       ├── halas/          The Last Class
│       │   ├── campaign.md Halas Academy crest, motto, institutional skin, alert boot lines, halas-attack
│       │   ├── crest.svg
│       │   ├── briefs/last-class.md
│       │   ├── sessions/   tlc-session-1, tlc-session-2, test-fallbacks, test-alert-start
│       │   └── media/      halas-surface.mp4, halas-thermal.mp4, halas-surface01.mp4 (kept out of the zip)
│       ├── remnant/        Remnant: sessions/remnant-session-1.md
│       ├── regulators/     The Regulators: sessions/regulators-session-1.md
│       └── _template/      copy-me chapter
├── dist/<campaign>/<chapter>/  finished files plus media
├── server/                 web.py (build page), omnictl.py (install, users, updates)
├── docs/OMNISLATE_Handoff_Prompt.md, SERVER_SETUP.md, GM_SERVER_GUIDE.md
├── README.md
└── ENHANCEMENTS.md
```

### campaign.md

The umbrella `errans-inter-astra/campaign.md`:

```text
Name: Errans Inter Astra
Crest: prometheus.svg

## Normal Skin
Style: military
Network: GMS Sensor Suite

## Alert Skin
Style: military
Network: GMS Sensor Suite: emergency mode
```

The chapter `halas/campaign.md` overrides what *The Last Class* needs:

```text
Name: The Last Class
Motto: Unity Through Strength
Crest: crest.svg

## Normal Skin
Style: institutional
Network: Halas Academy Training Network

## Alert Skin
Style: military
Network: GMS Sensor Suite: emergency mode

### Boot Lines
- GMS sensor suite: emergency mode
- [red] Halas Academy network: no response
- [amber] Local sensor feed active

## Trigger: halas-attack
Label: 06:47 Attack
Style: attack
Reveals: tlc-emergency-0647
Sound: klaxon.mp3
Lost Text: Signal lost

### Lines
- GMS sensor suite: emergency mode
- [red] Halas Academy network: no response
- [red] Perimeter defense grid: no response
- [amber] Switching to local sensor feed
- [amber] Priority message received
```

- Top settings: `Name`, `Motto`, `Crest` (SVG, PNG, JPG, or WebP in the folder of the `campaign.md` that names it; leave out for a generated crest), `Crest Text`.  A chapter's `campaign.md` takes the same settings, and anything it leaves out comes from the umbrella.
- Skins: `Style` is `institutional` (the old academy look) or `military` (the old GMS look).  `Network` is the top-bar name.  Optional hex colors: `Background`, `Bar`, `Panel`, `Panel Highlight`, `Line`, `Line Highlight`, `Text`, `Dim Text`, `Accent`, `Alert Color`, `Boot Glow`.  The alert skin layers the red alert palette over its style unless colors override it.
- Triggers: `Label`, `Style` (`attack` or `reveal`; `hack` and `transmission` are reserved), `Reveals`, `Sound` (file in `sounds/`, or `none`; attack defaults to `klaxon.mp3`), `Lost Text`, `Banner`, and `### Lines`.  Line colors: `[red]`, `[amber]`, `[green]`.
- Lines starting with a single `#` are notes.

### Session File

```text
Session: The Last Class, Session 2
Output: tlc-session-2
Worlds: halas@planetside
Briefs: tlc-class-3, tlc-class-4, tlc-class-5
Triggers: halas-attack
Arm: 90
```

- `Worlds` takes `slug@depth`.  Depths: `long range`, `orbital`, `planetside`.  Fields beyond the chosen depth never enter the file.
- `Briefs` show from the start.  `Triggers` lists trigger ids from `campaign.md`.  Each trigger's `Reveals` briefs stay hidden until it fires.  `Arm` is the default countdown in seconds.
- Optional: `Network` overrides the Normal skin's name for one session.  `Start: alert` opens in emergency mode.  `Atlas: <depth>` adds every other known world at that depth.
- Retired: `Skin:` (prints a note) and `Held:` (fails with instructions).

### Brief Format

`## brief-id`, then `- **Title:**`, `- **Type:**`, `- **Location:**`, `- **Issued By:**`, `- **World:**` fields, then `###` sections containing paragraphs or `- ` list items.  Current *Errans Inter Astra* library: `tlc-class-3`, `tlc-class-4`, `tlc-class-5`, `tlc-emergency-0647`, `tlc-combat-1`, `tlc-combat-2`.  All text is player-facing and pulled from *The Last Class*.

### Media Beside the HTML (No Rebuild Needed)

| Feed | Where it shows | File names |
|---|---|---|
| Surface drone 02 | Main feed, Visible mode | `{slug}-surface.mp4` / `.webm` |
| Thermal | Main feed, Thermal mode | `{slug}-thermal.mp4` / `.webm` |
| Surface drone 01 | Second feed panel, no caption, free-form | `{slug}-surface01.mp4` / `.webm` |
| Trigger sound | When a trigger fires | the `Sound:` file name |

Order per feed: video, then a still with the same name (`.webp`, `.png`, `.jpg`), then an image embedded by the build, then static.  Sound order: embedded from `sounds/` by the build, then the same file name beside the session file, then a built-in alarm (attack) or chime (reveal).

Media lives in a chapter's `media/` folder (or the umbrella's, to share it) and is copied into `dist/<campaign>/<chapter>/` on each build.  Copy that whole folder to the tablet, one folder per chapter, because file names follow world slugs and could collide across chapters.  The workshop zip ships without the videos on purpose.  Assistants test with placeholders.

### Display Features

- **Boot screen** with the campaign crest and motto.  With JavaScript blocked it shows "Sensor suite offline" and asks for scripts to be allowed.  The tap unlocks fullscreen, keep-awake, and audio.  In a `Start: alert` session the boot is a terminal screen with the alert network name and boot lines.
- **Scan, Briefs, and Deep Scan tabs.**
- **WebGL2 globe** from an equirectangular map: day/night lighting, atmosphere rim, ocean glint, slow spin, drag to rotate, full-screen expand.  Globes are cached per world.  The build fixes polar starbursts.
- **Overview dossier:** header, globe, Planetary Data, drone 01 feed, quick strip, drone 02 feed, detail panels, Life.  Portrait and landscape layouts.
- **Drone feeds** with live overlay, timestamp, jitter, and static when empty.  The main feed caption follows the mode.
- **Detail panels** tap open full screen.  Locked slots show for fields held back by scan depth.
- **Skins:** Normal and Alert per campaign, each built on the `institutional` or `military` style.
- **Reveal banner** and a distinct accent styling for briefs unlocked by a reveal trigger.  Briefs unlocked by an attack keep the red emergency styling.
- **Motion switch** is the authority.  It ignores the tablet's reduce-motion setting and pauses video.

### Media Channels

- **Surface drone 02 and Thermal** are tied to the world's Surface Survey and Thermal Survey.  Visible should feel calm and normal.  Thermal can feel wrong: choppy, hard cuts, shifting hot and cold spots.
- **Surface drone 01** (`surface01`) is a deliberate free-form local media channel.  On populated worlds it may show local broadcasts, agriculture, entertainment, wildlife, traffic, public feeds, or other ambient material.  It carries no caption and ties to no world field.
- **Hidden visual intrusions:** the PROMETHEUS sigil exists (red flame, open book, slit-pupil eye) and may appear small and buried inside thermal anomalies, such as the Halas Science Wing hot spot.  Loops repeat, so intrusions belong near the end of long loops (45 to 60 seconds) to stay rare.

### Established Visual Language: Halas

- Academy: modern institutional campus on a plateau above the Verath River, parade ground with flag, mech hangars, Science Wing behind and to the right of the main hall.
- Rural locals: improvised ag-tech, one-off farm machinery, old and new construction side by side.
- One goatfolk farm family lives on Halas.  They are bioengineered humans, the rejects of a failed lab project, left alone and now native Halas farmers.  Only this family is goatfolk.  Everyone else on Halas is baseline or ordinarily modified human.

### GM Panel (Hidden)

Open by holding the top-left network badge about one second, or Ctrl+Shift+G on a laptop.

- Build stamp: engine version, campaign, session, build time
- Sound readout for the selected trigger (which sound loaded and why) and Feeds readout (what each feed found)
- Trigger picker when a session has two or more triggers
- Arm the selected trigger on a countdown (10 sec to 5 min) or to fire when the player opens Briefs
- Fire now, Disarm, Reset session
- Sound on or off, Test sound, Preview skin (Normal or Alert)
- The badge dot turns hollow while armed
- Sessions without triggers hide the arm and fire controls

### Triggers in Play

**Attack** (the 06:47 event): sound plays, the crest tears apart, full static with the lost text, terminal lines, then the Alert skin.  All feeds die, the trigger's briefs appear, the Briefs tab flashes, and the view switches to Briefs.

**Reveal:** the trigger's briefs appear with accent styling, the Briefs tab flashes, the optional banner shows for five seconds, and a chime or the named sound plays.  The skin stays as it was.

Fired triggers survive a page reload until Reset session.

### Security and Code Rules

- Content Security Policy in the page.  No external scripts, fonts, trackers, or network calls.
- All text renders through `textContent`.  The crest is the only markup a campaign supplies, and the build rejects SVGs containing scripts, event handlers, or embedded frames.
- Plain HTML, CSS, and vanilla JavaScript.  Python 3 with Pillow on the Mint side only.

---

## 3. Hardware and Table Setup

- **Tablet:** Android, Firefox (runs in desktop mode, reports a Linux user agent).  CSS viewport about 1088 × 680 landscape, 680 × 1088 portrait, pixel ratio about 1.76.  The tablet is the protected baseline for every build.  It may keep being passed around the table even after the monitors arrive.
- **Opening files:** File Manager+ hands the HTML to Firefox through an on-device local server.  Files beside the HTML are reachable.
- **Performance:** WebGL globe 55 to 60 fps.  Load under a second for a 6 MB file.
- **The tablet has reduce-motion enabled** at the system level, which is why the Motion switch overrides it.
- **Audio:** YouTube Music and trigger sounds both play from the tablet through a robot Bluetooth speaker.  Battery backup on hand.
- **unstableNHP (the Cheese Block):** the always-on OMNISLATE server at Nathan's house.  Home connection measured 789 Mbps down, 56.5 Mbps up, 26 ms latency.  The 56.5 Mbps upload limits how fast files leave the box (about 7 MB per second), which is comfortable for GMs and one tablet.  Media for the table should still ride on the tablet locally.
- **Mint Asus laptop:** on loan to The Stoned Gnome for the new gaming table, and still mine to use.  It runs the same workshop and the Build OMNISLATE launcher, so Jarrett builds there.  Still a fallback display: Firefox, same file.
- **Shop gaming table:** being built with two monitors in it.  Probably 1920 × 1080 or larger, viewed from above at an angle.  Build 3.0 was checked at 1920 × 1080 and 2560 × 1440: nothing breaks, but text reads small (OMNI-080).
- **Maps:** Roll20 will likely handle battle maps.  The tablet may show maps too.  Nothing planned yet (OMNI-083).

---

## 4. Locked Decisions

- COMP/CON owns mechanics.  OMNISLATE owns fiction.  No HP, heat, stat blocks, or dice.  (A Scan return snapshot under 2.2 is the agreed exception path.)
- Spoilers are gated at build time.  Future content never ships in a session file.
- Images and video are artwork only.  No text, labels, or UI baked in.
- The engine stays campaign-agnostic.  Campaign names, crests, skins, and event text live in `campaign.md`, never in `app/display.html`.
- GMs never code.  Everything a GM touches is a fill-in-the-blank text file, and build errors speak plain English.
- The tablet layout (1088 × 680 and 680 × 1088) is the protected baseline.  Bigger screens may never cost the tablet anything.
- One folder per campaign in the workshop, chapters inside it, and one folder per chapter on the tablet.  A new folder is the only step to a new campaign or chapter.
- Styles: `institutional` is polished and rounded.  `military` is modern military avionics.  Later manufacturers get their own styles.
- Missing art is diegetic ("SIGNAL PENDING," "CLOSE APPROACH REQUIRED").  So is bad or missing data ("INTERFERENCE," "TOO DISTANT"), and the GM always gets the plain-English warning in the build report.
- World entries hold sensor data only.  Campaign secrets live in campaign notes, and unknown `###` sections never ship.
- Events fire when the table is ready.  No clocks drive story beats.
- Canon firewall: published Lancer worlds follow the books, and gap-filling is marked as campaign material.
- "Halas" is the spelling for planet and academy.  "MONIST-1" is the correct spelling.
- The Relationship Clocks sheet is GM-only and excluded from continuity.
- Veles's secret stays off every player-facing screen.
- Never bundle Lancer game data.  Read GM exports only.
- unstableNHP is reachable only over Tailscale.  No port forwarding, no homemade public login.  Player-facing hosting needs a backend that releases held content only when the GM fires (OMNI-085).

---

## 5. Tools in the Pipeline

| Tool | Role |
|---|---|
| Claudia (Claude) | Primary architecture, code, build pipeline, briefs, testing, handoff documentation |
| Mara (ChatGPT) | Planning, visual design, image generation and editing, worldbuilding, media concepts, troubleshooting, secondary architecture review |
| GIMP | Image cleanup and compositing (thermal variants, sigil placement) |
| Peek | Screen capture |
| Kdenlive | Video assembly, editing, loops from stills, audio removal |
| Audacity | Klaxon and event audio design |
| Kling | Occasional image-to-video experiments |
| Gemini | Emergency-use-only media generation |
| Python 3, Pillow, ffmpeg | Workshop build and media conversion on Mint |
| Tailscale | Private network for unstableNHP, GMs, the tablet, and the laptop |
| Samba | Shared campaign drives on unstableNHP |
| File Manager+, Firefox | Tablet runtime path |
| COMP/CON | Pilots, NPC rosters, and combat tracking.  Deliberately outside OMNISLATE, with exports as a future read-only input |
| Roll20 | Likely battle-map surface at the shop table |

---

## 6. Roadmap

Tiers run in order.  Nothing in a later tier justifies a broad refactor of an earlier one.  Items carry tier-based IDs (2.1, 3.4, and so on).  `ENHANCEMENTS.md` holds the detail under OMNI IDs, mapped to these.

### Tier 1: Protect the Table Build

Changes stay surgical, and every build is dry-run on the tablet before a session.  The screenshot comparison used for 3.0 (frozen clock, seeded randomness, static and globe canvases hidden) is the standard check for any engine change: player-facing screens must match the previous build unless the change is meant to alter them.

### Done in Build 3.6

ANDIS audio and video (OMNI-047, OMNI-048).  OMNI-049 complete.

### Done in Build 3.5

ANDIS attachments, the printer, `Routes: 0`, the OMNISLATE principle (OMNI-049 in part).  See the Shipped table in `ENHANCEMENTS.md`.

### Done in Build 3.4

The ANDIS terminal and signals (OMNI-046), covering part of OMNI-016 and OMNI-045.  See the Shipped table in `ENHANCEMENTS.md`.

### Done in Build 3.3

Chapters inside umbrella campaigns, Errans restructured under the PROMETHEUS crest, `_template` chapters, chapter-aware build page, no-script notice, auto-build fixes, server migration steps.  See the Shipped table in `ENHANCEMENTS.md`.

### Done in Build 3.2

The unstableNHP server: build page, Samba drives, auto-build, omnictl (OMNI-084).

### Done in Build 3.1

Deep Scan tab, wireframe planets, atlas, NEW WORLD TEMPLATE, diegetic bad data, GM-note sections skipped, Larkspur added.  See the Shipped table in `ENHANCEMENTS.md`.

### Done in Build 3.0

Campaign folders and theme file, triggers and per-trigger sounds (OMNI-010, OMNI-011), `Start: alert` (roadmap 2.3 start state), build stamp and friendly errors, launcher, starter campaign, and START-HERE.txt, media sync, generated crest, README retitle (5.5, OMNI-096), ENHANCEMENTS.md recovered and merged (5.6, OMNI-097).  See the Shipped table in `ENHANCEMENTS.md`.

### Tier 2: Next Sessions

- **2.1 Multiple GM events.**  Partial.  Per-trigger arm, fire, and sound shipped.  Remaining: arming more than one trigger at a time.
- **2.2 Hostile Contact Scans.**  Open.  GM-triggered screen before a fight, public information only, hologram or targeting-return art treatment.  Absorbs 2.6 as a Scan return: when a pilot takes the Scan quick tech, the card unlocks a timestamped stat snapshot.  COMP/CON exports as the data source.
- **2.3 Combat 1 and Combat 2 session files.**  Parked: *The Last Class* has ended.  The start state shipped.  `tlc-combat-2` still needs a player-facing title before it ever ships.
- **2.4 Optional GM status line.**  Open.
- **2.5 Globe improvements.**  Open.  Cloud layer, mapping animations.

### Tier 3: Media Architecture

- **3.1 Secondary-feed playlists.**  Open.
- **3.2 Per-world media profiles.**  Open.
- **3.3 Asset manifest and preflight checks.**  Partial.  The build report and GM panel cover part of it.
- **3.4 Campaign prep screen for GM.**  Open.  Runs on the Mint box as a local page with a small Python helper that writes campaign files, plus a Build button.  The campaign folder structure is its storage.  Enemy data from COMP/CON exports.

### Tier 4: Campaign Expansion

- **4.1 World states and redactions.**  Open.
- **4.2 Recovered Files tab.**  Open.  Reveal triggers can already unlock a file per session.
- **4.3 Manufacturer skins.**  Open.  These become new `Style:` presets.
- **4.4 Further globe layers.**  Open.
- **4.5 COMP/CON pilot greeting.**  Open.
- **4.6 New worlds.**  Open.  Generation runs in the workshop at build time and gets checked against the canon firewall.

### New in 3.0 Planning (see ENHANCEMENTS.md)

Arm several triggers at once (OMNI-014), hack and transmission trigger styles (OMNI-015, OMNI-016), browser builder (OMNI-035), enemy comms intercept feed (OMNI-045), table-monitor mode (OMNI-080), GM window on the laptop for the "Battleship" setup (OMNI-081), tablet and monitors together (OMNI-082), Roll20 note (OMNI-083), airplane mode check (OMNI-094), workshop in git (OMNI-095).  COMP/CON work stays under OMNI-040 to OMNI-044.

### Tier 5: Polish and Housekeeping

- **5.1** Confirm or revise Halas's drafted planetary values.
- **5.2** Convert the pool worlds' em dashes to colons (76 remain in `library/worlds.md`).
- **5.3** Fix Veles's pronoun slips in *The Last Class*.
- **5.4** Normalize media: resolution, codecs, loop lengths, file sizes.  `halas-surface01.mp4` is about 60 MB.
- **5.5** Done.
- **5.6** Done.  The original ENHANCEMENTS.md turned up after a cleanup and was merged with the 3.0 items.  Original OMNI IDs are unchanged.

---

## 7. What I Will Provide

Upload these at the start of the thread:

1. **This file.**
2. **omnislate_<version>.zip**, the latest workshop folder, named for the engine version in `build.py` (such as `omnislate_3.6.zip`).  Zip the `omnislate/` folder itself, so the folder inside keeps the plain name `omnislate/`.  Videos can stay out.
3. **The session HTML from the tablet** when something about the table build matters.  It is the ground truth for what actually ran.
4. **Campaign documents** when relevant.  *The Last Class* has ended.  If none are provided, treat the work as generic engine work.
5. **Screenshots** of anything that looked wrong on the tablet or the table monitors.

As each upgrade comes up:

- **Hostile scans:** the NPC classes, templates, and counts for each fight (or COMP/CON exports), plus any mech art.
- **Rules questions:** the Lancer core book epub or the relevant expansion.
- **New worlds:** the world entry and an equirectangular map (2:1, plain ice or ocean along the top and bottom edges).
- **Feeds and sounds:** these stay in each chapter's (or umbrella's) `media/` and `sounds/` folders, named to the conventions above.  Assistants work with placeholders.

---

## 8. How to Work With Me on This

- Discuss first, then build.  When I say it's time to code, deliver complete tested files.
- Before changing the engine, confirm the zip's `app/display.html` matches the last table build.  Build 3.0 started with a stale template and was caught only because the video code was missing.
- The test scripts travel in the workshop's `dev/` folder (see `dev/README.txt`): pixel parity, functional checks, and the three ANDIS suites.
- Test in a headless browser before handing anything over: the screenshot comparison against the previous build, the trigger and start-state checks, and the 1920 × 1080 and 2560 × 1440 checks.  The sandbox can't play MP4 (H.264) or run Firefox, so say so when a feature depends on either.
- Keep changes surgical.  The table version works.  Protect it.
- At the end of every build, hand back the updated workshop zip (named `omnislate_<version>.zip`, with the version bumped in `build.py` when the engine changes), this handoff (revised), `ENHANCEMENTS.md`, and the built session files, so a new thread can pick up cleanly.
- Session prep runs on a two-week rhythm: week one for content and art, week two for a tablet dry run.
- Produced text (briefs, data files, handouts, docs) uses two spaces after periods, no em dashes, and no contrastive negation.
