# OMNISLATE campaign settings
# Copy the whole _starter folder, rename the copy (lowercase, dashes, no spaces), then edit this file.
# Lines that start with a single # are notes.  The build skips them, so keep or delete them as you like.
# Settings look like "Name: value".  Spelling of the setting name matters.  Capital letters do not.

# ---------------------------------------------------------------------------
# The basics
# ---------------------------------------------------------------------------

# Shown in the GM panel and around the edge of the generated crest.
Name: New Campaign

# Shown under the crest on the boot screen.  Delete the line for no motto.
Motto: Eyes Open, Steel Ready

# Your own crest: put the file in this folder and name it here.  SVG, PNG, JPG, and WebP all work.
# Leave this line commented out and the build draws a clean crest from Name, Motto, and Crest Text.
# Crest: crest.png

# The short word in the middle of the generated crest.  Defaults to the campaign's initials.
Crest Text: NEW

# ---------------------------------------------------------------------------
# Skins.  Normal is the everyday look.  Alert is the look after an attack.
# Style is institutional (rounded, gold, polished) or military (square, green, terminal).
# Network is the name in the top bar.
# Optional color overrides, each a hex color like #c9a24a:
#   Background, Bar, Panel, Panel Highlight, Line, Line Highlight, Text, Dim Text,
#   Accent, Alert Color, Boot Glow
# ---------------------------------------------------------------------------

## Normal Skin
Style: institutional
Network: Field Survey Network
# Accent: #c9a24a

## Alert Skin
Style: military
Network: Sensor Suite: emergency mode

### Boot Lines
# Shown on the boot screen when a session starts in alert mode ("Start: alert").
# Start a line with [red], [amber], or [green] to color it.  Plain lines are green.
- Sensor suite: emergency mode
- [red] Field survey network: no response
- [amber] Local sensor feed active

# ---------------------------------------------------------------------------
# Triggers.  Events the GM fires from the hidden GM panel.
# Each one starts with "## Trigger: some-id".  Sessions turn them on with "Triggers: some-id".
#
#   Label:     the name the GM sees in the GM panel
#   Style:     attack  (klaxon, the crest tears apart, signal lost, then the alert skin; every feed dies)
#              reveal  (quiet: hidden briefs appear, the Briefs tab flashes, an optional banner shows)
#   Reveals:   brief ids that stay hidden until this trigger fires (comma separated)
#   Sound:     a file in sounds/ to bake into the session, or "none".  Attack defaults to klaxon.mp3.
#              No file?  Attack plays a built-in alarm and reveal plays a built-in chime.
#   Lost Text: the big word during an attack's static (default "Signal lost")
#   Banner:    a short line that pops up on screen after the trigger fires
#   ### Lines: the terminal lines an attack prints after the static
# ---------------------------------------------------------------------------

## Trigger: example-intel
Label: Intel decrypted
Style: reveal
Reveals: example-intel
Banner: Encrypted packet recovered

## Trigger: example-attack
Label: Station attack
Style: attack
Reveals: example-emergency
Lost Text: Signal lost

### Lines
- Sensor suite: emergency mode
- [red] Field survey network: no response
- [red] Station defense grid: no response
- [amber] Switching to local sensor feed
- [amber] Priority message received
