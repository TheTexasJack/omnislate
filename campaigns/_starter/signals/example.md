<!--
SIGNALS for the ANDIS terminal.  One signal per "## id" block.  Copy the block to add another.

  Program:     the name players type:  LOAD "BEACON",8,1
               Letters, numbers, and spaces only (16 at most), because that is all the ANDIS keyboard has.
  Title:       optional.  Shows while it decrypts.
  Time:        the real-clock countdown, HH:MM:SS.  It keeps running between game nights.
  Corruption:  optional.  The starting corruption %, counting down to 0.  Default 100.
  Routes:      optional.  How many carrier pairs the routing minigame has, 2 to 5.  Default 3.
  Penalty:     optional.  Time added each time a line crosses another, HH:MM:SS.  Default 00:05:00.
  Image:       optional.  A picture in images/ that comes with the decoded text.
  Routes: 0    skips the routing game, for quick hacks.

### Attachments is optional.  Files that come with the decoded message, each one a tag the players tap:
  - NAME: print                 [D] runs the ANDIS printer.  You hand over the real paper.
  - NAME: picture.png           [I] shows a picture on the screen (from images/ or signals/).
  - NAME: notes.txt | caption   [T] shows a text file on the screen.  Keep it in signals/ as a .txt.
  - NAME: log.mp3 | caption     [A] a voice log with a waveform (from signals/ or sounds/).
                                A .txt with the same name (log.txt) types along as the transcript.
  - NAME: clip.mp4              [V] a video on the CRT, aged to look like 90s footage.  Put it in media/.
  - NAME:                       [M] a folder.  Indent the files under it by two spaces.

### Encoded is what the players already have, shown while it decrypts.
### Decoded is what they earn.  Start a line with [red], [amber], or [green] to color it.
Everything between the two ### lines and the next ## is kept exactly as typed, blank lines too.

To use a signal in a session, list it in the session file:   Signals: example-beacon
  example-beacon@decoded            opens already decoded
  example-beacon@running 00:45:00   resumes with 45 minutes left
-->


## example-beacon
- **Program:** BEACON
- **Title:** Distress beacon
- **Time:** 00:10:00
- **Corruption:** 64.0

### Encoded
[PARTIAL DECRYPT // RELAY BEACON]
... MAYDAY ... ▒▓░ ... KESTREL ...
... SURVEY TEAM ... ▓▒▒ ... OVERDUE ...
[64.0% CORRUPTION]

### Decoded
[DECRYPT COMPLETE // RELAY BEACON]

This is survey team Hollis on Kestrel.  Our lander is down in the salt flats east of the station.
Two injured.  Water for four days.
[amber]Do not land in the flats after dark.  The ground moves.
[END PACKET]
[0.0% CORRUPTION]

### Attachments
- HOLLIS LOG: hollis-log.txt
- KESTREL: kestrel-map.png | Survey map, station marked
- SURVEY FILES:
  - HOLLIS DISTRESS: hollis-distress.mp3 | Distress call, day 4
  - LANDER CAM: lander-cam.webm
  - SALT FLATS MAP: print
  - CREW ROSTER: print

