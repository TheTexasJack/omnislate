# OMNISLATE

*Portable Multimodal Survey, Intelligence, and Mission Display*

OMNISLATE turns a tablet or a table monitor into an in-fiction cockpit display: planetary scans, a live globe, drone feeds, mission briefs, and GM-fired events such as an attack or a decrypted intel drop.  The workshop folder (this one) holds the source files.  `build.py` turns them into one self-contained HTML file per session.  The tablet only opens the finished file.  No server, no install, no network.

Engine version 3.6.  Every campaign lives in its own folder, so any number of GMs can share one workshop.  A campaign holds one folder per chapter, and a new chapter folder shows up on its own.

## Folder

```text
omnislate/
├── START-HERE.txt          first stop for a new GM
├── app/display.html        the display engine (never edited per campaign)
├── build.py                the builder
├── build.sh                double-click launcher for build.py
├── library/
│   ├── worlds.md           shared world pool, available to every campaign
│   └── images/             art for pool worlds
├── campaigns/
│   ├── _starter/           copy this to start a new campaign
│   └── errans-inter-astra/ one folder per campaign
│       ├── campaign.md     name, crest, motto, skins, triggers (shared by every chapter)
│       ├── worlds.md       this campaign's own worlds
│       ├── images/         world art baked into the session file
│       ├── sounds/         trigger sounds baked into the session file
│       ├── media/          videos and stills that sit beside the file on the tablet
│       ├── briefs/         briefs every chapter shares
│       ├── signals/        coded messages for the ANDIS terminal (in a chapter too)
│       ├── notes/          recaps and prep (the build ignores this)
│       ├── halas/          one folder per chapter
│       │   ├── campaign.md the chapter's name, plus anything it overrides
│       │   ├── sessions/   one file per session
│       │   ├── briefs/     this chapter's briefs
│       │   └── media/      this chapter's videos
│       ├── remnant/
│       ├── regulators/
│       └── _template/      copy this to start a new chapter
├── dist/<campaign>/<chapter>/  finished files plus media, ready for the tablet
├── server/                 build web page and server installer (unstableNHP)
├── docs/                   handoff, server setup, GM server guide
└── ENHANCEMENTS.md         backlog
```

## First-time setup on a Linux Mint machine

1. Copy the whole `omnislate` folder somewhere permanent, such as your home folder.
2. Open a terminal in that folder and run these two lines once:

   ```bash
   sudo apt install python3-pil
   ./build.sh --install-launcher
   ```

3. A **Build OMNISLATE** icon appears on the desktop.  If Mint asks whether to trust it, say yes.

Python 3 already ships with Mint.  Pillow (`python3-pil`) handles image conversion and the globe's pole fix.

## Building

- **Desktop icon:** double-click **Build OMNISLATE**.  Pick a campaign if there is more than one.  The window lists every file it built and anything that needs attention, then waits for Enter.
- **Terminal:**

  ```bash
  ./build.sh                                  # menu
  ./build.sh errans-inter-astra               # one campaign, every chapter (the start of the name is enough)
  ./build.sh errans-inter-astra/remnant       # one chapter
  python3 build.py campaigns/errans-inter-astra/halas/sessions/tlc-session-2.md   # one session
  python3 build.py --all                      # every campaign
  ```

Build problems print in plain English with the file and line to fix, and a suggestion when a name looks like a typo.

Never edit a file in `dist/`.  Change the source and rebuild.  A hand edit disappears on the next build.

## What to open

Open the **session file**, never `app/display.html`.  The engine template is empty on its own.  Each session file in a chapter's `sessions/` becomes one page in `dist/<campaign>/<chapter>/`, named by its `Output:` line:

```text
halas/sessions/tlc-session-2.md   (Output: tlc-session-2)   ->   dist/errans-inter-astra/halas/tlc-session-2.html
```

On the laptop, double-click that `.html` file to open it in Firefox.  The build report lists every file it made under `OK`.

## On the tablet

Copy the chapter's `dist/<campaign>/<chapter>/` folder to the tablet, then open the session file from File Manager+ into Firefox.  Tap the boot screen to go fullscreen and hand it over.

Keep one folder per chapter on the tablet.  Video names follow world slugs, so two chapters in one folder could collide.

If the boot screen says "Sensor suite offline", the browser or a script blocker is blocking JavaScript.  Allow scripts for that page and reload.

## Deep Scan and the world atlas

The **Deep Scan** tab turns any world's data into a sensor readout with no art needed: a rotating wireframe reconstruction drawn from the world's data, an orbit diagram with the habitable zone, Cradle comparison bars for gravity, radius, and temperature, readouts with estimates, and hazard flags.  A world without a map shows the same wireframe on the Scan tab, and a session whose first world has no map opens on Deep Scan.

Add `Atlas: long range` (or `orbital`, or `planetside`) to a session file to include every other known world at that depth.  The Deep Scan catalog lists them all with a filter box.

New worlds: copy the NEW WORLD TEMPLATE at the top of any `worlds.md`.  It lists every field and its rules.  Bad or missing values never stop the build.  The table shows them as INTERFERENCE, BAD SCAN: RESAMPLE, NO RETURN, or TOO DISTANT, and the build report lists each one under `Warn` so you can fix it.  Type `[interference]` (or `[too distant]`, `[bad scan]`, `[no return]`) as a value to hide it on purpose.  Any `###` section the template does not list is treated as GM notes and never reaches the screen.

## The unstableNHP server

The workshop can also run on a small always-on Mint box (unstableNHP) shared over Tailscale.  GMs edit through a shared drive from any computer, Windows included, and build from a web page at `http://unstablenhp/`.  Setup: `docs/SERVER_SETUP.md`.  GM guide: `docs/GM_SERVER_GUIDE.md`.  Server code: `server/web.py` (build page) and `server/omnictl.py` (install, users, updates).

### What is locked on the server, and why

| Place | Nathan (admin) | Other GMs | Build service | Why |
|---|---|---|---|---|
| `campaigns/<campaign>/` | Read and write | Read and write their own only | Read only | Each GM owns their campaign.  Nobody else can open it.  The build service reads it and writes nothing there. |
| `app/`, `build.py`, `server/`, `docs/`, `library/`, `campaigns/_starter/` | Read and write | Read only | Read only | The engine stays the same for everyone.  New releases arrive through `omnictl update`, which backs up the old engine first. |
| `dist/` | Read only | Through the build page only, their own campaigns | Read and write | Finished pages are always made by a build, so a hand edit can never drift from the source.  The next build would overwrite it anyway. |
| `/etc/omnislate/gms.json` | Root only | No access | Read only | Holds the hashed passwords and who owns which campaign. |
| `/var/lib/omnislate/` | Root only | No access | Read and write | Build reports and auto-build state. |

Shares: `omnislate-admin` is the whole workshop for Nathan.  `omnislate` is a read-only reference copy for every GM, and it hides anything that GM cannot read, `dist/` included.  Each campaign share (such as `errans-inter-astra`) is just that campaign folder.

Need to change something locked?  Use `sudo` on unstableNHP, then run `sudo python3 /srv/omnislate/server/omnictl.py fix-perms`.  Files made with `sudo` belong to root, and the build service cannot replace or delete them until fix-perms gives them back.  Edits to `dist/` still disappear on the next build, so make lasting changes in `campaigns/`.

## Starting a new campaign

Copy `campaigns/_starter`, rename the copy, and follow `campaigns/_starter/README.md`.  Folder names use lowercase letters, numbers, and dashes.  Folders that start with `_` are skipped by the menu and by `--all`.

## Chapters

A campaign folder can hold any number of chapter folders, each with its own `campaign.md`.  To add one, copy `_template` inside the campaign and rename the copy.  Errans Inter Astra is the umbrella with The Last Class (`halas`), Remnant, and The Regulators as chapters.

- **Settings** in the chapter's `campaign.md` override the campaign's, one setting at a time.  Skins merge setting by setting.  Triggers merge by id.
- **Files** (worlds, briefs, images, sounds, media, crest) are looked up in the chapter first, then the campaign, then `library/`.
- **Output** goes to `dist/<campaign>/<chapter>/`, one list per chapter on the build page.
- A campaign with its own top-level `sessions/` still builds straight into `dist/<campaign>/`, so 3.2 campaigns keep working unchanged.
- A chapter folder with spaces or capitals in its name (such as `_template - Copy`) is skipped, and the build report says so.

## The ANDIS terminal (signals)

An old workstation the lance can plug into.  A session that lists signals shows an **ANDIS** button in the top bar.  The players:

1. Drag the loose cable down to the SER port on the keyboard.  The screen powers on.  Every new hack starts unplugged.
2. Type `LOAD "NAME",8,1` on the on-screen keyboard (or a real one), then `RUN`.  A wrong name gives `?FILE NOT FOUND  ERROR`, anything else `?SYNTAX  ERROR`.
3. Play signal routing: link each pair of matching carriers without crossing lines.  A crossed line costs the signal's Penalty on the clock.
4. Wait out the countdown.  It runs on the real clock, so it keeps going when the terminal is closed, the tablet sleeps, or the session ends.  The ANDIS button shows progress and pulses when the decode is ready.
5. Read the decoded packet.  It scrubs in out of the noise, then scrolls with a finger drag.
6. Tap the attachment tags under it: `[T]` text, `[I]` a picture, `[D]` a document that runs the ANDIS printer (that is your cue to hand over the real paper), and `[A]` a voice log with a live waveform and a transcript that types along, `[V]` a video aged on the fly to look like 90s FMV, and `[M]` a folder shown as a disk directory with PRINT ALL.  RETURN or `[BACK]` goes back.  Tap to pause or play audio and video.

Audio files go in `signals/` (or `sounds/`) and are baked into the page.  A `.txt` with the same name becomes the transcript.  Videos go in the chapter's `media/` folder, like the drone feeds.  Voice logs and videos always play: the GM panel Sound switch only mutes effects.  For full-quality video, use the Surface drone 01 feed (Expand) or play it separately.

Signals live in `signals/*.md` in the campaign or a chapter.  Each `## id` block has `Program` (the LOAD name: letters, numbers, spaces), `Time` (HH:MM:SS), and optional `Title`, `Corruption`, `Routes`, `Penalty`, and `Image`, then a `### Encoded` block (what they already have), a `### Decoded` block (what they earn), and an optional `### Attachments` list.  `Routes: 0` skips the routing game, for quick hacks such as a 15 second jail records breach.  Both blocks keep every line as typed.  The comments at the top of `campaigns/_starter/signals/example.md` explain each field.

In a session file: `Signals: remnant-buoy`.  Add `@decoded` to open already cracked, or `@running 00:45:00` to resume with 45 minutes left.  The timer also carries over by itself when sessions open the same way (both from the server, or both from the tablet).

GM panel, ANDIS SIGNALS: pick a signal, then Skip to decoded, Pause or Resume, Add 10 min, or Reset signal.  Reset session leaves signals alone, so a test attack never wipes a real decode.

## Display controls

- **Motion:** turns all animation on or off.  This switch overrides the tablet's reduce-motion setting on purpose.
- **Fullscreen:** enters or leaves fullscreen.
- **Globe:** drag to rotate, Expand for full screen.
- **Panels:** tap to open full screen.  Back returns.
- **Surface feed:** Visible and Thermal modes, plus Expand.

## GM panel (hidden)

Open it by holding the network badge in the top-left corner for about one second, or press Ctrl+Shift+G on a laptop.

- **Build stamp:** engine version, campaign, session, and build time.  Check this first when a file misbehaves.
- **Sound in use:** which sound the selected trigger will play and where it came from.
- **Feeds:** what each drone feed found beside the file.
- **Trigger:** when a session has more than one trigger, pick which one the arm and fire buttons control.
- **Arm:** a countdown, or "Fire when player opens Briefs."  The badge dot turns hollow while armed.
- **Fire now, Disarm, Reset session.**  Fired triggers survive a page reload until Reset session.
- **ANDIS signals:** Skip to decoded, Pause, Add 10 min, Reset signal.
- **Sound on or off, Test sound, Preview skin** (Normal or Alert).  Sound covers the terminal's clicks and drive noises too.

## Media beside the file

| Feed | Where it shows | File names |
|---|---|---|
| Surface drone 02 | Main feed, Visible mode | `{slug}-surface.mp4` / `.webm` |
| Thermal | Main feed, Thermal mode | `{slug}-thermal.mp4` / `.webm` |
| Surface drone 01 | Second feed panel, no caption | `{slug}-surface01.mp4` / `.webm` |

Put these in the chapter's `media/` folder (or the campaign's, to share them).  Every build copies them into `dist/<campaign>/<chapter>/`.  Each feed tries a video, then a still with the same name (`.webp`, `.png`, `.jpg`), then an image embedded by the build, then static.  After an attack trigger, or in a session with `Start: alert`, every feed shows FEED LOST.
