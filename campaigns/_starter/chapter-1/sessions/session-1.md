# One file per session.  One setting per line.  Lines that start with # are notes.
#
# Session:  the title (shows in the GM panel)
# Output:   the finished file name, no spaces (becomes dist/<campaign>/<chapter>/session-1.html)
# Network:  optional.  Overrides the Normal skin's network name for this session only.
# Start:    normal (default) or alert.  Alert opens straight into emergency mode with dead feeds.
# Worlds:   slug@depth, comma separated.  Depths: long range, orbital, planetside.
#           Anything past the chosen depth never goes into the file.
# Atlas:    optional.  Adds every other known world at this depth, browsable in Deep Scan.
# Briefs:   brief ids the players see from the start
# Triggers: trigger ids from campaign.md the GM can fire this session
# Signals:  optional.  Signal ids from signals/ the players can crack on the ANDIS terminal.
#           id@decoded opens already cracked.  id@running 00:45:00 resumes with 45 minutes left.
# Arm:      default countdown in seconds for the GM panel

Session: Session 1
Output: session-1
Worlds: kestrel@planetside, nacre@long range
Atlas: long range
Briefs: example-orders
Triggers: example-intel, example-attack
Signals: example-beacon
Arm: 60
