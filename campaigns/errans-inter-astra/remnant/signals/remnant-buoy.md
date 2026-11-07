<!--
SIGNALS for the ANDIS terminal.  One signal per "## id" block.  Copy the block to add another.

  Program:     the name players type:  LOAD "REMNANT",8,1
               Letters, numbers, and spaces only (16 at most), because that is all the ANDIS keyboard has.
  Title:       optional.  Shows while it decrypts.
  Time:        the real-clock countdown, HH:MM:SS.  It keeps running between game nights.
  Corruption:  optional.  The starting corruption %, counting down to 0.  Default 100.
  Routes:      optional.  How many carrier pairs the routing minigame has, 2 to 5.  Default 3.
  Penalty:     optional.  Time added each time a line crosses another, HH:MM:SS.  Default 00:05:00.
  Image:       optional.  A picture in images/ that comes with the decoded text.

### Encoded is what the players already have, shown while it decrypts.
### Decoded is what they earn.  Start a line with [red], [amber], or [green] to color it.
Everything between the two ### lines and the next ## is kept exactly as typed, blank lines too.

To use a signal in a session, list it in the session file:   Signals: remnant-buoy
  remnant-buoy@decoded            opens already decoded
  remnant-buoy@running 00:45:00   resumes with 45 minutes left
-->

## remnant-buoy
- **Program:** REMNANT
- **Title:** OmniNet drift packet
- **Time:** 02:00:00
- **Corruption:** 81.8

### Encoded
[PARTIAL DECRYPT // OMNINET DRIFT PACKET]
[AUTH: LANCER-ID: CORRUPTED. ORIGIN: OUTER SYSTEM RELAY BUOY]

IF THIS ... ◍T̸̘q̷̬Z̵̡v̶̯2̸̲⨕8̴̖⪺ WAS A SCIENTIFIC …
THAT WAS THE ... SEALED UNDER [REDACTED].
... TEAM, ... THE TEAM STOPPED …
TRANSMITTING BLIND REPEAT …
LEAVE. IMMEDIATELY.
[END PACKET]
[81.8% CORRUPTION]

### Decoded
[DECRYPT COMPLETE // OMNINET DRIFT PACKET]
[AUTH: LANCER-ID: VERIFIED. ORIGIN: OUTER SYSTEM RELAY BUOY]

If this message reaches [LANCER], understand that what happened aboard the Proxima Prime was a scientific experiment of a new origin, authorized by Harrison Armory.
That was the official explanation before we discovered what had been sealed under the primary engineering deck.
We sent an investigation team, followed by a security detail. The first team reported something impossible. The second team stopped responding entirely.
We have lost contact with the bridge. Internal communications are unreliable. Someone is answering our calls using the identities of crew members we know are dead. Records show that these conversations occurred years ago.
We are transmitting BLIND REPEAT through the outer system relay network. We cannot confirm that our messages are being received.
If you received this message, do not trust any transmission originating from Proxima Prime.
[red]DO NOT ATTEMPT TO BOARD.
[red]Leave! Immediately!
[END PACKET]
[0.0% CORRUPTION]

### Attachments
- PULSE: remnant-pulse-loop.mp3 | Carrier pulse, recovered.  Repeating.
