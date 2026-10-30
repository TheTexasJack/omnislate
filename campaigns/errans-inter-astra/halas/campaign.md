# The Last Class: chapter settings (Errans Inter Astra)
# Anything not set here comes from ../campaign.md.  Lines that start with a single # are notes.

Name: The Last Class
Motto: Unity Through Strength
Crest: crest.svg

## Normal Skin
# How the display looks before anything goes wrong.
Style: institutional
Network: Halas Academy Training Network

## Alert Skin
# How the display looks after an attack trigger fires, or from the start with "Start: alert".
Style: military
Network: GMS Sensor Suite: emergency mode

### Boot Lines
# Shown on the boot screen when a session uses "Start: alert".
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
