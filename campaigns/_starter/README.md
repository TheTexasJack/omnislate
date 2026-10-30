# Setting Up a Campaign

This folder is a working sample campaign.  Build it once to see what everything looks like, then make it yours.  You only ever edit text files.  No code.

## How a campaign is laid out

A campaign is one folder.  Inside it, each **chapter** (a story arc, a season, a separate group of players) gets its own folder.  Every chapter shows up on its own on the build page and in the build report.

```text
_starter/                 the campaign
├── campaign.md           crest, motto, skins, triggers: shared by every chapter
├── worlds.md             worlds every chapter can use
├── images/  sounds/      shared art and sounds
├── chapter-1/            one chapter
│   ├── campaign.md       the chapter's name, plus anything it changes
│   ├── sessions/         one file per game session
│   ├── briefs/           this chapter's mission briefs
│   └── media/            this chapter's drone videos
└── _template/            copy this to start another chapter
```

Finished files land in `dist/<campaign>/<chapter>/`, such as `dist/iron-tide/chapter-1/session-1.html`.

A chapter inherits everything from the campaign folder above it.  Set something in the chapter's own `campaign.md`, or drop a file with the same name into the chapter's folders, and the chapter's version wins.  So Remnant can have its own crest and network name while still sharing the campaign's worlds and klaxon.

## 1. Copy this folder

Copy `_starter` and rename the copy after your campaign: lowercase letters, numbers, and dashes, such as `iron-tide`.  On the unstableNHP server Nathan does this step for you.

## 2. Add a chapter

`chapter-1` is ready to use.  Rename it if you like (lowercase, numbers, dashes).  For another chapter:

1. Copy `_template` and paste it in the same place.
2. Rename the copy, such as `season-2`.  Windows names it `_template - Copy`: that name is skipped until you rename it, and the build report says so.
3. Open `campaign.md` in the copy and set `Name:`.

The new chapter builds on its own a few seconds later on the server, or the next time you press Build.  Folders whose names start with `_` are always skipped.

## 3. Edit `campaign.md`

The campaign's `campaign.md` is the look and feel of every chapter.  A chapter's `campaign.md` uses the same settings, and anything it leaves out comes from the campaign.

| Setting | What it does |
|---|---|
| `Name` | Campaign name.  Shows in the GM panel and on the generated crest. |
| `Motto` | Line under the crest on the boot screen.  Delete it for none. |
| `Crest` | Your own crest file in this folder (SVG, PNG, JPG, or WebP).  Leave it out for a generated crest. |
| `Crest Text` | Short word in the middle of the generated crest. |

**Skins.**  `## Normal Skin` is the everyday look.  `## Alert Skin` is the look after an attack, or from the start in an alert session.  Each skin takes:

- `Style:` institutional (rounded, gold, polished) or military (square, green, terminal)
- `Network:` the name in the top bar
- Optional colors as hex codes: `Background`, `Bar`, `Panel`, `Panel Highlight`, `Line`, `Line Highlight`, `Text`, `Dim Text`, `Accent`, `Alert Color`, `Boot Glow`

The alert skin can also carry `### Boot Lines`, the terminal lines on the boot screen when a session starts in alert mode.

**Triggers.**  Events you fire from the hidden GM panel.  Each starts with `## Trigger: some-id`.

| Setting | What it does |
|---|---|
| `Label` | Name you see in the GM panel. |
| `Style` | `attack`: klaxon, the crest tears apart, SIGNAL LOST, terminal lines, then the alert skin, and every feed dies.  `reveal`: quiet.  Hidden briefs appear, the Briefs tab flashes, and an optional banner pops up. |
| `Reveals` | Brief ids that stay hidden until this trigger fires. |
| `Sound` | A file in `sounds/` to bake into the session, or `none`.  Attack defaults to `klaxon.mp3`.  With no file, attack plays a built-in alarm and reveal plays a built-in chime. |
| `Lost Text` | The big word during an attack's static.  Default: Signal lost. |
| `Banner` | A short line that pops up after the trigger fires. |
| `### Lines` | The terminal lines an attack prints after the static.  Start a line with `[red]`, `[amber]`, or `[green]` to color it. |

A campaign with no triggers is fine.  The GM panel simply hides those controls.

## 4. Add worlds

Every world in `library/worlds.md` is already available.  Add your own to the campaign's `worlds.md` (shared by every chapter), or give a chapter its own `worlds.md`, by copying the NEW WORLD TEMPLATE at the top of that file (or the Kestrel example).  The template lists every field and its rules.  The `Slug` is the short name sessions and file names use.

No art?  No problem.  The Deep Scan tab draws a wireframe of every world from its data.  A typo never breaks the build: the table shows a sensor glitch such as INTERFERENCE, and the build report lists it under `Warn` so you can fix it.

World art goes in `images/` as `{slug}-map.png` (2:1 map for the globe, plain ice or ocean along the top and bottom edges), plus optional stills.  See `images/README.txt`.

Images and video are artwork only.  The display draws every label, number, and caption itself.

## 5. Write briefs

Briefs live in `briefs/*.md`, in the chapter (or in the campaign folder for briefs every chapter shares).  Each starts with `## brief-id`, then fields (`Title`, `Type`, `Location`, `Issued By`, `World`), then `###` sections of paragraphs or `- ` list items.  Everything in a brief can end up on the table screen, so keep GM secrets out.

## 6. Write a session file

One file per session in the chapter's `sessions/` folder.  The comments at the top of `chapter-1/sessions/session-1.md` explain every line.  The important ones:

```text
Session: Session 1
Output: session-1
Worlds: kestrel@planetside, nacre@long range
Briefs: example-orders
Triggers: example-intel, example-attack
```

`Worlds` takes `slug@depth`.  Depths are `long range`, `orbital`, and `planetside`.  Anything past the chosen depth never goes into the file, so players cannot find it.

Add `Start: alert` for a session that opens already in emergency mode, such as the fight right after an attack.

Add `Atlas: long range` to let players browse every other known world in the Deep Scan catalog.  They only see what a long-range scan would show.

## 7. Build and test

Double-click **Build OMNISLATE** and pick your campaign (on the server, press its Build button).  Every chapter builds.  Read the output: it lists each world, which images it found, each trigger and its sound, and anything that needs fixing.

Open the finished session file in Firefox on the laptop first: `dist/<your-campaign>/<chapter>/session-1.html` (the name comes from the `Output:` line).  The engine file `app/display.html` is an empty template, so skip that one.  Hold the network badge (or press Ctrl+Shift+G) to open the GM panel and test each trigger.  Reset session puts everything back.

## 8. Signals for the ANDIS terminal

Coded messages the players crack on an old terminal: plug in the cable, `LOAD "NAME",8,1`, `RUN`, route the carriers, wait out the timer, read the message.  Write them in `signals/*.md`.  The sample `signals/example.md` (LOAD "BEACON") is used by `chapter-1/sessions/session-1.md`, so build the starter and try it.  Its notes explain every field.  List a signal in a session with `Signals: example-beacon`.

A signal can carry attachments the players tap after it decodes: text files, pictures, documents that run the ANDIS printer (you hand over the real paper), and folders.  The sample has one of each, including a voice log and a short camera clip in its SURVEY FILES folder.  `Routes: 0` skips the routing game for quick hacks.

## 9. Media for the table

Videos for the drone feeds go in the chapter's `media/` folder (or the campaign's, to share them), named after the world slug (`kestrel-surface.mp4`, `kestrel-thermal.mp4`, `kestrel-surface01.mp4`).  Each build copies them into `dist/<your-campaign>/<chapter>/`, so copying that one folder to the tablet carries everything for that chapter.
