# OMNISLATE Enhancement Suite

The running backlog for OMNISLATE.  Keep this file in the workshop folder beside `README.md` so it travels with the code to every Claudia and Mara thread.

**Statuses:** Idea, Planned, In Progress, Done, Parked, Research
**Tiers:** match the roadmap in `docs/OMNISLATE_Handoff_Prompt.md`.  The Roadmap column gives the matching roadmap ID where one exists.
**Rule:** Tier 1 always wins.  The table version works, so changes stay surgical.

*Merged 2026-10-26: the original suite (recovered after a cleanup moved it) plus the Build 3.0 planning items.  Original OMNI IDs are unchanged.  New items took the next free ID in their range.*

*Updated 2026-10-27: Hostile Scans design session with Nathan.  Decisions recorded in OMNI-017, OMNI-018, OMNI-020 to OMNI-029, and OMNI-040.  Still open before any build: where the Contacts screen lives and how it opens, the art treatment, and whether the sitrep becomes a brief.*

---

## Shipped

| Build | What shipped |
|---|---|
| M0 | Tablet proof: single file opens through File Manager+ into Firefox, fullscreen, wake lock, swipe, long-press trigger, 60 fps canvas globe |
| 1 | Build script, Halas overview, WebGL globe with drag and expand, polar fix, tap-to-expand panels, drone feed with static, Academy and GMS skins, Motion switch |
| 2 | Boot crest SVG, Briefs tab, brief library, hidden GM panel, arm-and-delay trigger, 06:47 sequence, alert state, fired state survives reload |
| 2.1 | Klaxon from `sounds/klaxon.mp3` or `klaxon.mp3` beside the file, Klaxon readout, Test klaxon, video and still feeds beside the file, Feeds readout |
| 2.2 | Surface drone 01 free-form feed, Thermal moved into the main feed, caption follows mode, landscape quick strip fix |
| 3.6 | ANDIS audio and video: `[A]` voice logs baked into the page with a live waveform and a typed transcript from a matching `.txt`, `[V]` videos from `media/` with a live 90s FMV look (CRT resolution, dithered 64 colors, interlace lines, about 10 frames a second).  Content always plays, the Sound switch covers effects.  Starter sample voice log and camera clip (OMNI-047, OMNI-048, OMNI-049) |
| 3.5 | ANDIS attachments: `### Attachments` in signals with tappable `[T]` text, `[I]` image, `[D]` print, and `[M]` folder tags.  Folders as a C64 disk directory with PRINT ALL.  ANDIS LP-4 dot-matrix printer prop with sound, a cue for the GM's paper handout.  `Routes: 0` for quick hacks.  Northwatch jailbreak signal.  OMNISLATE principle and Andi System lore in the handoff (OMNI-049 in part) |
| 3.4 | ANDIS terminal (OMNI-046): retro workstation opened from the top bar in sessions with signals.  Drag the cable to the SER port, CRT warm-up, on-screen breadbox keyboard, `LOAD "NAME",8,1` with C64 errors, loader stripes and drive knocks, signal-routing minigame with crossing penalties, real-clock countdown that survives reloads and game nights, scrub reveal of the decoded packet.  `signals/*.md` with Encoded and Decoded blocks, `Signals:` session line with `@decoded` and `@running`.  GM panel Skip, Pause, Add 10 min, Reset signal.  Own 5x7 pixel font.  Proxima Prime packet in Remnant and a BEACON sample in the starter |
| 3.3 | Chapters: a campaign folder holds chapter folders that inherit its `campaign.md` setting by setting and its worlds, briefs, images, sounds, and media file by file, and build into `dist/<campaign>/<chapter>/`.  A new folder appears on its own in the build report, the build page, and auto-build.  `_template` chapter in every umbrella, with a report note for badly named copies.  Errans Inter Astra restructured as the umbrella over `halas` (The Last Class), `remnant`, and `regulators`, under the PROMETHEUS crest.  `_starter` is an umbrella with `chapter-1`.  Build page groups session files by chapter.  No-script boot notice.  Auto-build catches edits saved before its first pass and saves made during a button build.  Server migration steps in `docs/SERVER_SETUP.md`.  README table of what is locked on the server, for whom, and why |
| 3.2 | unstableNHP server kit: `server/web.py` build page (per-GM logins with PBKDF2 hashes, campaign-scoped Build button, live report with session links, video range requests, auto-build about five seconds after a save, space meter, lockout after five bad passwords, Tailscale-only) and `server/omnictl.py` (install, add-gm, passwd, update with engine backup, autobuild, limit, fix-perms, status; Samba shares per campaign, ACL permissions, systemd service as the locked-down `omnibuild` user).  Server setup guide and Windows GM guide (OMNI-084) |
| 3.1 | Deep Scan tab (wireframe reconstruction, orbit and habitable-zone diagram, Cradle comparison bars, estimates, hazard flags).  Procedural wireframe planets seeded by slug, also used as the globe fallback when a world has no map.  `Atlas:` session line and a filterable world catalog.  NEW WORLD TEMPLATE with optional `Scan Class`, `Moons`, `Rings`.  Bad or missing world data shows in-fiction (INTERFERENCE, BAD SCAN, NO RETURN, TOO DISTANT) with GM warnings in the build report.  Unknown `###` sections and HTML comments in world files never ship.  Larkspur added to the pool (OMNI-070 in part) |
| 3.0 | Campaign-agnostic engine.  Campaign folders with `campaign.md` (name, motto, crest, Normal and Alert skins on `institutional` or `military` styles).  Shared world pool in `library/worlds.md`.  Named triggers with `attack` and `reveal` styles, per-trigger sound, trigger picker in the GM panel (OMNI-010, OMNI-011).  `Start: alert` for post-attack sessions.  Build stamp in the GM panel.  Plain-English build errors with typo suggestions.  `build.sh` launcher and desktop icon.  `_starter` sample campaign and `START-HERE.txt`.  Media copied into `dist/<campaign>/`.  Generated crest.  Player-facing screens verified pixel-identical to the 2.2 table file |

---

## Tier 2: Next Sessions

| ID | Enhancement | Status | Roadmap | Notes |
|---|---|---|---|---|
| OMNI-010 | Multiple GM events | Done (3.0) | 2.1 | Named triggers in `campaign.md`, each armed and fired on its own from the GM panel's trigger picker.  Remaining piece split out as OMNI-014 |
| OMNI-011 | Per-event sounds | Done (3.0) | 2.1 | `Sound:` line per trigger.  Order: embedded from `sounds/`, then the same name beside the file, then a built-in alarm (attack) or chime (reveal) |
| OMNI-012 | Combat 1 and Combat 2 session files | Parked | 2.3 | *The Last Class* has ended.  The start state they needed shipped in 3.0 (`Start: alert`).  `tlc-combat-2` needs a player-facing title before it ever ships, since the current one names the twist |
| OMNI-013 | GM status line | Idea | 2.4 | Fiction-facing timer or notice, such as "Keshar shuttle inbound."  The GM advances it by hand, so no clock drives a story beat |
| OMNI-014 | Arm several triggers at once | Idea | 2.1 | For example, a countdown on one trigger and "fire on Briefs" on another.  Today one trigger is armed at a time |
| OMNI-015 | Hack trigger style | Idea | new | Glitch and corruption, a foreign sigil taking over the screen (the PROMETHEUS sigil fits), then back to the current skin.  `Style: hack` is reserved and gives a "planned, not built yet" message |
| OMNI-016 | Transmission trigger style | Idea | new | Partly covered: the ANDIS (OMNI-046) handles incoming packets.  Still open as a quick on-screen call alert.  See OMNI-046 for the ANDIS decrypt, which covers incoming packets.  Incoming-call screen with sender ID and message, then back to normal.  `Style: transmission` is reserved |
| OMNI-017 | Reinforcement groups | Planned | 2.2 | Agreed 2026-10-27.  Optional `Group:` line on a contact, a free label the GM writes (Phase 1, Phase 2).  No Group line means on the field from the start.  Each group is its own collapsed bar under the main list, in file order, showing only its label.  Players tap a bar open when that wave arrives, in any order, so early arrivals need no timer.  Bars open and close freely: table honor covers peeking, and GMs sometimes give reinforcement counts in a briefing anyway.  Groups sit side by side and never nest |
| OMNI-018 | Sitrep as a brief | Idea | 2.2 | The COMP/CON encounter carries a sitrep (name, description, deployment, objective).  It could become a brief.  Undecided.  The encounter's own description never ships, since Nathan's export keeps campaign Key Events there |
| OMNI-020 | Hostile Contacts list | Planned | 2.2 | Design agreed 2026-10-27.  Every contact always shows its callsign, class, and template, the same information a Lancer GM gives when players ask.  Header reads `CONTACTS: 7 ACTIVE // 4 DESTROYED`.  Data comes from the contacts template (OMNI-026).  Still open: where the screen lives (its own tab or a trigger such as a `contacts` style) and how it first opens |
| OMNI-021 | Player Scan action | Planned | 2.2, 2.6 | Agreed 2026-10-27.  Scan is its own button on each contact card, with no limits programmed into OMNISLATE.  The GM says "go ahead and scan" and the rules stay at the table.  The button offers Full Statistics or Hidden Info.  A contact with no Hidden Info section answers NO ADDITIONAL RETURN |
| OMNI-022 | Scan snapshot stamp | Planned | 2.2, 2.6 | Result stays unlocked for the session, stamped "SCANNED 16:42 // DATA NOT LIVE" per the core book's Scan rule.  Stamps are per callsign, so scanning RON2 leaves RON3 unscanned.  Stamps survive a reload and clear on Reset session |
| OMNI-023 | Current HP on Scan | Research | 2.2 | Roster knows max HP only.  The COMP/CON encounter export holds prep-time HP (always full), so it does not solve this.  Options: GM says current HP aloud (Claudia's vote, fits "fiction here, mechanics in COMP/CON"), or a GM panel field sets it before the scan resolves |
| OMNI-024 | Scan log in GM panel | Idea | 2.2 | Shows what was scanned, which option, and when |
| OMNI-025 | Hostile art treatment | Planned | 2.2 | Hologram or targeting-return filter so mixed art generations read as one sensor source.  Halas attackers get custom shells labeled with ordinary NPC classes.  COMP/CON encounter exports carry no NPC portraits, so art always comes from the GM's own files.  Still open |
| OMNI-026 | Contacts template | Planned | 2.2 | Agreed 2026-10-27.  The base every GM uses, since Jarrett does not use COMP/CON.  `contacts/*.md` in a chapter or umbrella, one `## slug` entry per contact type, fill-in-the-blank like `worlds.md`.  Required: Class, Template, Size, Count.  Optional: Callsign, Code, Role, Tier, Group, HP, Armor, Evasion, E-Defense, Speed, Sensors, Save Target, Heat Cap, Structure, Stress, `### Loadout`, `### Hidden Info`.  `### GM Notes` and `#` comments never ship.  A missing stat shows NO RETURN on the scan.  Session line such as `Encounters: operation-halas-castigation`.  Build slice 1: template, parser, extractor, and the callsign list in the build report, with no player-facing change.  Slice 2: the display |
| OMNI-027 | COMP/CON encounter extractor | Planned | 2.2 | Agreed 2026-10-27.  Optional on-ramp for GMs who use COMP/CON.  Reads an encounter `.json` and writes the contacts template, run by `./build.sh import` or a build page button.  The table build only reads the `.md`, so a COMP/CON format change breaks the import step and never a session file.  Never overwrites: if the `.md` exists it writes `<name>.new.md` beside it and says so.  Merges matching units into one entry with Count.  Puts the COMP/CON name in a `#` comment so the real name stays off the tablet.  Leaves Callsign blank.  Loadout is names plus a one-line stat summary (`Heavy Assault Rifle: Main Rifle, Range 10, 6 Kinetic, +1 attack`), without the full rules text.  Unreadable parts (missing packs, renamed fields) are left blank with a plain-English note while the rest imports.  Nathan's `Operation_Halas_Castigation.json` is the reference export (11 combatants, packs marked MISSING already) |
| OMNI-028 | Contact callsigns | Planned | 2.2 | Agreed 2026-10-27.  Default callsign is the first three letters of the class plus a number: CAT1, CAT2, ASS1 (stays, Nathan's tokens already say it).  Numbering runs per prefix across the whole encounter, groups included, so a Ronin Marine and three Ronin Grunts are RON1 to RON4 and reinforcement Hives continue at HIV3.  `Code:` overrides the three-letter prefix when two classes collide, and the build warns and suggests one.  `Callsign:` names bosses and uniques outright (WARDEN, or WARDEN1 and WARDEN2 when Count is above 1).  Build checks every callsign is unique.  The build report prints the full list so tokens and minis match |
| OMNI-029 | Destroyed marker | Planned | 2.2 | Agreed 2026-10-27.  Mark destroyed on a contact card moves it to a collapsed DESTROYED group, dimmed with the callsign struck through.  One-tap Restore, no confirm dialog.  Wrecks stay scannable and keep their stamps.  Survives a reload, clears on Reset session.  No HP or status tracking and no COMP/CON sync: the GM's tracker stays the source of truth |

---

## Tier 3: Media Architecture and Prep Tools

| ID | Enhancement | Status | Roadmap | Notes |
|---|---|---|---|---|
| OMNI-030 | Surface drone 01 playlists | Idea | 3.1 | Cycle several clips or stills in the free-form channel |
| OMNI-031 | Per-world media profiles | Idea | 3.2 | Busy or lived-in, controlled, dead, frontier, hostile, industrial |
| OMNI-032 | Asset manifest and preflight | In Progress | 3.3 | 3.0 build report lists images and trigger sounds per session, and the GM panel lists what each feed found.  Remaining: one list of every expected media file per session, found or missing, before the session |
| OMNI-033 | Extra feed sensor modes | Idea | new | Lidar wireframe or night vision alongside Visible and Thermal |
| OMNI-034 | Campaign prep screen | Idea | 3.4 | Fill-in-the-blank page on the workshop machine (enemies, maps, free-form brief, brief number, campaign marker) with a small Python helper that writes campaign files, plus a Build button.  The 3.0 campaign folders are its storage.  The tablet keeps receiving finished files, so spoilers stay gated at build time |
| OMNI-035 | Browser builder | Idea | new | Drag a campaign folder into a page and get session files back with no Python install.  The long-term path for GMs on Windows.  Overlaps with OMNI-034 |
| OMNI-036 | Guided GM console | Idea | 3.4 | Build page steps: pick or create a chapter (no `_template` copying), a session form (world dropdowns with depth, brief and trigger checkboxes, Atlas toggle), media upload that names files from world and feed, then Build and Open or Download.  The browser becomes the only tool, so GMs skip the mapped drive.  Needs a narrow write path (own campaign, set file types, size limits) and a hand-edited-file warning.  Ask Jarrett which step lost him first.  Relates to OMNI-034 and OMNI-088 |
| OMNI-037 | `omnictl install-campaign` | Idea | new | One command to install a campaign shipped in a release zip: backup, swap, keep videos, fix-perms, and a diff of server-side edits.  Replaces the manual 3.3 migration steps |
| OMNI-038 | Build page conveniences | Idea | new | Download for tablet (zip of a chapter's pages and videos), auto-refresh of the report, warning count on each card, engine version on the page |
| OMNI-039 | Tailscale access rule for guest GMs | Done (2026-10-27) | new | Applied in the Tailscale admin console: Nathan's login gets everything, every other member gets only ports 80 and 445 on unstableNHP (`autogroup:member`).  Server config, no build.  Before inviting Jarrett: an access rule so guest members reach unstableNHP only, and Beast stays off limits.  Invite as Member, never Admin |

---

## Tier 4: Campaign Expansion

| ID | Enhancement | Status | Roadmap | Notes |
|---|---|---|---|---|
| OMNI-040 | COMP/CON capability review | Research | 4.5 | Encounter export reviewed 2026-10-27: per combatant it holds the GM's name, class and role, tier, templates, size, max stats, every feature with rules text, unit number, side, and reinforcement turn.  No portraits, and Hidden Info has no natural field.  Still to check: pilot exports, second-device display, and range support |
| OMNI-041 | Deployment roster | Idea | 4.5 | Import COMP/CON pilot exports.  Show callsign, frame, loadout, and art, with a scroll-through of frames.  No double entry |
| OMNI-042 | NPC roster import | Parked | 2.2, 3.4 | Folded into the COMP/CON encounter extractor (OMNI-027) |
| OMNI-043 | Frame stats from COMP/CON game data | Idea | 2.2 | Published as JSON.  Rule: never bundle Lancer game data in OMNISLATE.  Read each GM's own exports only |
| OMNI-044 | Boot screen pilot greeting | Idea | 4.5 | Callsign and frame from a pilot export |
| OMNI-045 | Enemy comms intercept feed | Idea | new | Partly covered: ANDIS signals can carry intercepted chatter as text, audio, or video.  Still open: the live radio-tuning receiver.  Optional hackable feed of NPC chatter seeded with GM-chosen facts, with a fake radio-tuning receiver (one live station, the rest looping).  Planned with Mara.  Critical clues stay with the GM.  Chat log posts to Discord after the session |
| OMNI-046 | ANDIS terminal and signal decrypt (v1) | Done (3.4) | new | Shipped in 3.4.  A separate retro-futurist workstation opened from a terminal icon in the top bar, only in sessions that list signals.  CRT monitor (C64 blue palette, scanlines, ANDIS UN.#30 badge, no Commodore branding) and a drawn breadbox keyboard.  Each hack starts with a loose wire the player drags to the keyboard port, where it snaps in, and the CRT warms up from a dot to a full raster with a degauss thunk.  Compact on-screen keyboard (Android keyboard suppressed), real keyboard on laptops, mouse and touch alike.  `LOAD "NAME",8,1` finds the signal (a few seconds of striped border and drive-head knocks while `LOADING`, never during the countdown), a wrong name gives `?FILE NOT FOUND  ERROR`, anything else `?SYNTAX  ERROR`.  `RUN` starts a simple signal-routing minigame (misses add time, never lock out), then a real-clock countdown from the signal's `Time:` with corruption % rolling down, then a scrub reveal of the decoded text or image.  Timer carries across sessions where the browser allows, and `Signals: id@decoded` or `id@running 00:45:00` sets it outright.  GM panel: Skip, Pause, Add time, Reset signal.  Files in `signals/`.  Kept simple so any GM's signals behave the same: the decoded text appears only at the end.  First packet: Proxima Prime (REMNANT) |
| OMNI-047 | Audio signal payloads | Done (3.6) | new | Voice logs with a live waveform and a transcript that types out as it plays.  Event Horizon use: the bridge answering in dead crew voices |
| OMNI-048 | Video signal payloads | Done (3.6) | new | Security footage in a CRT frame with static.  Sits beside the file like drone feeds, copied into `dist` only for sessions that list the signal |
| OMNI-049 | Signal attachments | Done (3.6) | 4.2 | Shipped: [T], [I], [D] print, [M] folders (3.5), [A] and [V] (3.6).  A decoded packet carries a list of recovered files (text, image, audio), each with its own viewer.  This is the path to the Recovered Files tab (OMNI-052).  Recovered files may carry text, since they are in-fiction documents.  The interface itself still never does |
| OMNI-050 | World states | Planned | 4.1 | `halas` academy and ashes.  Same drone 02 angle, ruins in frame |
| OMNI-051 | Redactions | Idea | 4.1 | Fields that display as classified text |
| OMNI-052 | Recovered Files tab | Done (3.6) | 4.2 | Delivered through ANDIS signal attachments instead of a separate tab: journals, logs, pictures, voice logs, and video as files in [M] folders.  A dedicated tab only if it is ever wanted.  *Ashes of Halas*.  Journals from cadets and staff, Science Wing logs, Veles's journal.  A reveal trigger can already unlock one file per session |
| OMNI-053 | Corrupted file restoration | Parked | 4.2 | The same file ships with more of it readable in later session files.  Candidate: the GRAVIS drift packet |
| OMNI-054 | Brief map images | Idea | new | Sitrep zone map attached to a brief.  Keep compatible with Roll20 (OMNI-083) |
| OMNI-055 | Partial decrypt stages | Idea | 4.2 | Stops such as 81.8%, 40%, 0% across sessions as the lance works at it.  Pairs with OMNI-053 |
| OMNI-056 | Terminal easter eggs and an explorable ANDIS | Idea | new | Grow the ANDIS into a system players can poke around in, ideally on its own device (Nathan's pink Chromebook has the right tactile size): C64 BASIC-style commands such as `LOAD "$",8` and `LIST`, a disk full of dummy files, tiny programs, and joke programs.  Already possible today with no new code: a signal with `Routes: 0`, `Time: 00:00:01`, and a video attachment works as a gag program, such as `LOAD "SKYRIM"` playing a GM-supplied clip.  Gag clips live in the GM's own `media/`.  Everything else stays `?SYNTAX  ERROR` until then |
| OMNI-057 | Standalone terminal page | Idea | new | The build also writes a terminal-only page so the ANDIS runs on its own device.  Nathan's idea: preload it on cheap old phones (no SIM) or an old Chromebook as table props, so players never install or load anything.  Notes: each device keeps its own timer state, so a second device needs `@running` or a GM skip to match; offline files avoid Wi-Fi trouble; a phone build makes OMNI-099 worth doing.  Pairs with OMNI-082 |
| OMNI-058 | Terminal options | Idea | new | Screen palette setting (C64 blue, amber, green phosphor).  Optional `LOAD` shortcut key that types `LOAD "`, off by default |
| OMNI-059 | Partial field reveal per world | Idea | new | Depth is all-or-nothing per world.  A session line such as `Known: life` would reveal single fields early, for charted core worlds |
| OMNI-063 | Paracausal terminal effects | Parked | new | Not yet, maybe later.  Ghost typing from the GM panel, first-received dates that flicker between each player's, sent dates after today |
| OMNI-064 | ANDIS hack words | Planned | new | Nathan's idea, 2026-10-27.  Optional signal fields `Hack Words:` (comma list, letters, numbers, spaces) and `Hack Time:` (HH:MM:SS taken off per word), with optional per-word times such as `PYRETICA=00:30:00`.  While the countdown runs, a `KEY:` line under the timer takes typed words.  A right word shows `KEY ACCEPTED  -00:01:00` with a chime and cuts the clock.  A wrong word shows `INVALID KEY` with no penalty.  A repeat shows `KEY ALREADY APPLIED`.  The screen shows `KEYS ACCEPTED: n` and never the total.  Keys never take the clock below about 10 seconds.  RETURN on an empty line still backs out to the prompt.  The GM panel lists the keys found (`KEYS: NHP, FART (2 of 4)`).  The GM hands out clues at the table, so no screen minigame is needed |
| OMNI-065 | Hack word likeness hint | Idea | new | Optional add-on to OMNI-064, off by default.  A wrong guess shows `LIKENESS: n`, how many letters sit in the right place compared with the closest key (the Fallout and Mastermind hint).  Only if the table wants more to chew on |
| OMNI-060 | Manufacturer skins | Idea | 4.3 | IPS-N, SSC, Harrison Armory, and HORUS (subtly wrong and glitchy).  In 3.0 these become new `Style:` presets any campaign skin can point at |
| OMNI-061 | Globe layers | Idea | 2.5, 4.4 | Drifting clouds (roadmap 2.5), terrain relief, night-side lights (4.4).  Clouds need a cloud-free map plus a clouds-only image |
| OMNI-062 | Season 2 umbrella crest reveal | Idea | new | Errans uses the PROMETHEUS sigil as its crest now.  When Pyretica returns in Season 2, a reveal or attack trigger could swap or corrupt the crest in fiction |
| OMNI-070 | New worlds | In Progress | 4.6 | 3.1 made adding worlds a copy-and-fill job with no art required, and added Larkspur.  Pool worlds and canon locations as the campaign travels.  Generation, if any, runs in the workshop at build time.  Canon firewall applies |
| OMNI-071 | ANDIS after-hours archive (Remnant) | Idea | new | About 20 easter eggs players explore between sessions once the buoy is decrypted: pre-accident crew manifest, repair logs with REMNANT follow-ups, a mess-hall food feud, episode-style shenanigans, Lancer nods, and a simple Asteroids-style game.  Rules (Nathan, 2026-11-07): hints and nods only, never copies; Lancer themed; SECCOM/HA crew have no aliens (they regard nonhumans as lesser); no table impact.  Next: Claudia drafts 20 titles with one-line pitches for approval |

---

## Table Hardware and Surfaces

| ID | Enhancement | Status | Roadmap | Notes |
|---|---|---|---|---|
| OMNI-080 | Table-monitor mode | Idea | new | The layout caps at 1500 px wide.  At 1920 × 1080 and 2560 × 1440 nothing breaks, but text reads small across a table.  Add a scale setting for big screens.  The tablet at 1088 × 680 stays the protected baseline |
| OMNI-081 | GM window on the laptop | Idea | new | The "Battleship" setup: the laptop runs the GM side and the tablet or table monitors face the players.  Today the GM panel is a hidden overlay on the player screen |
| OMNI-082 | Tablet and monitors together | Idea | new | The tablet passes around the table while the monitors show the globe or a scan.  Depends on OMNI-081 |
| OMNI-083 | Roll20 as the map surface | Idea | new | Roll20 will likely handle battle maps at the shop table.  Note only: keep future map features compatible, and keep the tablet able to show maps too |
| OMNI-084 | Windows build path | Done (3.2) | new | Chosen with Jarrett: the unstableNHP server.  GMs on any OS edit through a Samba drive over Tailscale and build from `http://unstablenhp/`.  No Python on Windows.  See `docs/SERVER_SETUP.md` and `docs/GM_SERVER_GUIDE.md` |
| OMNI-085 | Hosted OMNISLATE | Idea | new | OMNISLATE is private and proprietary for The Stoned Gnome, with no public release.  Only player-facing hosting inside the tailnet remains an idea.  GM-side hosting shipped in 3.2 as the Tailscale-only unstableNHP server.  Still open for players: A login protects files from strangers and leaves players able to read held briefs in page source, so hosted player pages need a backend that releases held content only when the GM fires.  Safe first slice: host the browser builder (OMNI-035), which carries no campaign data.  Use an existing login gate (such as Cloudflare Access) and never a homemade login.  The table tablet keeps running from local files.  Needs the security and public-release discussion first |
| OMNI-086 | Tailscale identity login | Idea | new | Replace build-page passwords with the Tailscale user identity, so a device on the tailnet is already logged in |
| OMNI-087 | Hard disk quotas | Idea | new | 3.2 shows a soft space meter per campaign.  Enforce real per-GM quotas on the filesystem if the box ever gets crowded |
| OMNI-088 | Web upload and file manager | Idea | new | Upload media and edit `.md` files from the build page, for devices that cannot map a network drive (tablets, Chromebooks) |
| OMNI-089 | Chapter cleanup in dist | Idea | new | A deleted or renamed chapter leaves its old `dist/<campaign>/<chapter>/` folder behind.  Offer a cleanup button on the build page, never an automatic delete |

---

## Tier 5: Polish and Housekeeping

| ID | Task | Status | Roadmap | Notes |
|---|---|---|---|---|
| OMNI-090 | Halas planetary values sign-off | Planned | 5.1 | Tagline, Vital World, Sparse Settlements, G4 V, 1.02 AU, 1.06u, 6,240 km, 0.98 g, 14 °C |
| OMNI-091 | Pool worlds em dashes to colons | Planned | 5.2 | Match the Halas entry.  76 remain in `library/worlds.md`.  The pool now ships to other GMs, so this matters more |
| OMNI-092 | Veles pronoun fix | Planned | 5.3 | *The Last Class* entry says "They uses" and "his" |
| OMNI-093 | Media normalization | Idea | 5.4 | Resolution, codecs, loop lengths, file sizes.  `halas-surface01.mp4` is about 60 MB |
| OMNI-094 | Airplane mode check | Planned | new | Open a session file offline once on the tablet |
| OMNI-095 | Workshop in git | Idea | new | Private GitHub repo so two GMs and two assistants share one history.  Doubles as Nathan's GitHub learning project |
| OMNI-096 | README retitle | Done (3.0) | 5.5 | Now titled OMNISLATE |
| OMNI-097 | ENHANCEMENTS.md back in the workshop | Done (3.0) | 5.6 | Original recovered and merged with the 3.0 planning items, roadmap IDs mapped |
| OMNI-098 | Assistant account on unstableNHP | Parked | new | Tabled 2026-10-26.  A desktop user `claudia` (no sudo) added as co-owner of Errans with `add-gm`, so an assistant could edit and build Errans only.  Check that the Claude desktop app runs on Mint first |
| OMNI-099 | Phone-width top bar | Idea | new | Low priority.  On a phone in portrait the top bar overflows since the ANDIS button joined it: the clock overlaps the network badge and Fullscreen is cut off.  The tablet is fine in both orientations.  Possible fix: hide the clock and shorten the button labels under about 520 px wide |

---

## Known Limits

- The build sandbox cannot play MP4 (H.264) or run Firefox.  MP4 playback and Firefox behavior are confirmed on the tablet only.
- The tablet cannot judge range or line of sight.  Those stay GM calls at the table.
- Fired triggers persist through reloads by design.  Use Reset session after every rehearsal.
- Big screens work, with small text, until OMNI-080 lands.
- Engine changes are checked by screenshot comparison against the previous table build (frozen clock, seeded randomness, static and globe canvases hidden).  Player-facing screens must match unless the change is meant to alter them.

---

## Adding an Entry

Give it the next free ID in its tier's range, a short title, a status, the roadmap ID if one exists, and one line of notes.  Move it to Shipped with the build number when it lands.

ID ranges: Tier 2 is 010 to 029, Tier 3 is 030 to 039, Tier 4 is 040 to 079, Table Hardware is 080 to 089, Tier 5 is 090 to 099.
