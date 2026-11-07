# REMNANT / Proxima Prime navigation scans / v1.0

**Based on:** `REMNANT_Campaign_Guide_Revised.v1.3.odt` (6 November 2026), supplied by the GM.  
**Deliverable date:** 7 November 2026.  
**Purpose:** editable, abstract shipboard navigation scans and GM encounter grids for the REMNANT chapter.

## Open these first

1. `NAVIGATION_INDEX.html` is the **offline image gallery** with clickable map previews. It requires no internet or JavaScript.
2. `scan_png/00_MASTER_PLAYER_SCAN.png` is the safe-to-show navigation overview.
3. `scan_svg/00_MASTER_PLAYER_SCAN.svg` is the corresponding vector master, editable in Inkscape.
4. `scan_png/00_MASTER_ROUTE_NETWORK.png` is the **GM-only** version with the intended route and scenario objectives.
5. `GM_ROUTE_CARD.md` provides connectivity, required and optional travel beats, and map usage notes.

The `scan_svg` and `scan_png` folders contain **18** sheets total: nine player-display scans and nine GM planning scans. The `encounter_svg` and `encounter_png` folders contain **five** GM-only hex references: one GAUNTLET, one pirate interception, and a Seam battle layout for **3, 4, or 5 PCs**. Every raster is 2560 px wide. All SVGs are standalone and have no scripts or external imagery.

## Map index

| Scan ID | Vessel | Area / purpose | Source status |
| --- | --- | --- | --- |
| `M-00` | Both | Master route/connection graph | Proposed routing connecting canonical places |
| `P-01` | Proxima | Damaged service hangar / mech boarding | Canon location, suggested subdivision |
| `P-02` | Proxima | Mech-scale transit and service galleries | Canon, with proposed junction labels |
| `P-03` | Proxima | Cargo-transfer gallery / pirate interception | Canon encounter; precise network position proposed |
| `P-04` | Proxima | Central engineering GAUNTLET / Lock 2 | Canon location and west/east control relationship |
| `P-05` | Proxima | Ship printer / fabrication and optional medical support | Printer beat canonical; exact location/medical branch proposed |
| `P-06` | Proxima | Local REM casket access | Canon host ship; exact access position proposed |
| `D-01` | Deimos | Docking spine / physical isolation interlock | Canon Lock 1; Deimos docked at Proxima nose |
| `D-02` | Deimos | Weapons-access route / RHANT cabinet | Canon host ship; exact corridor locations proposed |
| `D-03` | Deimos | Co-Consciousness Lance bay / final Seam battle | Canon host ship and scene |
| `D-04` | Deimos | Local RHANT casket access | Canon host ship; exact cabinet position proposed |

`P-06` and `D-04` are **branch nodes in the master and relevant sector maps**, not separately drawn floor sheets. They matter if a local manual cycle is required. They are intentionally not presented as an exact architectural deck number.

### Player versus GM sheets

- `*_PLAYER_SCAN` files are designed to be shown as sensor information before all revelations. These use neutral terms, such as **Research Bay** and **Secure Core Access**.
- `*_SECTOR_SCAN` files, plus `00_MASTER_ROUTE_NETWORK`, are **GM-only**, revealing locks, factions, casket identities, and the experimental bay.
- `encounter_*` files are all **GM-only**. They use tactical rules and spoiler labels.
- A player scan can be updated later to reveal more information by editing a duplicate of its SVG. Do not present a GM scan early unless the table has earned the reveal.

## Geometry rules and deliberate abstractions

**NOT TO SCALE.** The topology means **what connects to what**, not where a compartment physically lies in the hull or how many meters away it is. Functional bands are *not* actual ship deck counts and are *not* silhouettes. The ship's enormous real volume is implied by the long, repeated transit segments, gantries and industrial staging areas.

A line marked **MECH ROUTE** represents a mech-capable arterial connection; a dashed amber line represents a **pilot-only route** or narrow bypass. Isolated or hazardous elements are explicitly labeled and never rely on color alone. Connections between deck bands and the docking spine can involve lifts, pressure transfer, tram movements, or multiple changes of physical level; the map compresses those changes into a single graphic link.

Crucial canon: **Deimos docks at Proxima's nose**. The prototype **Co-Consciousness Lance is aboard Deimos**, not Proxima. Hell's Kraven controls or contests the **Proxima engineering enclosure**. The pirates independently occupy the **cargo-transfer gallery**. The final fight against the hitchhiker takes place in **Deimos's Lance bay**.

## Tactical encounter sheets

### `E-01_GAUNTLET`
- 26 hexes across x 16 deep, within the guide's 24–28 x 14–18 recommendation.
- West/left ADZ, east/right EDZ/CZ, two north and two south ingress zones.
- Fortified eastern objective area, movable machinery cover, and two clear Size 2 movement lanes as a design intent. Adjust cover for the actual PCs and rules of occupied spaces.
- Enemy reinforcements are the held half of the roster at the end of round 1. They are **not** extra units.

### `E-02_PIRATE_SALVAGE`
- 24 hexes across x 16 deep, within the guide's 22–26 x 14–16 recommendation.
- West arrival lift, Size 2 salvage hauler initially near center, east escape airlock.
- Six-segment escape clock. The hauler can be interdicted, seized, destroyed, or negotiated over. The gallery is deliberately distinct from the engineering GAUNTLET.

### `E-03_SEAM_3PCS / 4PCS / 5PCS`
- 29 x 21 hexes, generated to leave room for a central stationary Anchor/Body and peripheral devices.
- Exactly **one Coupler Cell per player**, each exactly **eight hexes** from the center; every two cells are more than **three hexes** apart. Positions are computed and tested using actual hex-coordinate distance, not visual approximation.
- The selected layout is a **proposed** playable space; the campaign guide fixes cell-spacing rules but does not prescribe a full bay shape or hex dimensions. The Body/Anchor overlap is represented by `A/B`.
- `S` marks **suggested** hostile escort starts, not mandatory deployments.

**These encounter maps are compact tactical references, not architectural cutaways or miniature placement guarantees.** Reposition generic cover, doors, or opponent starts as appropriate at the table.

## Art adaptation

Open the SVG in Inkscape to move nodes, recolor routes, replace text, or add overlays. Export PNGs at any target resolution. The Python generator is included if a consistent regeneration of all sheets is preferred. The generator requires `svgwrite`, `cairosvg`, and `Pillow` only; its SVG output has no runtime dependencies.

Suggested later scene pointers: a damaged service hangar, massive transit gallery, cargo hauler, central engineering enclosure, ship printer, med bay, docking interlock, RHANT casket area, and experimental chamber. These should be **standalone atmosphere images**, not pasted into the geometric scan. No user reference images or third-party stock imagery have been embedded.

## Attribution, quality, and security

- All maps and decorative shapes in this packet were drawn procedurally from scratch. No game-publisher art or text was copied into the artwork.
- Canon and scenario details were taken from the supplied GM guide; optional locations and invented routing are explicitly described as *proposed*.
- Generated SVG files have no `<script>`, `<foreignObject>`, external image references, network links, or event attributes. The offline gallery uses static markup/CSS, with no scripts or third-party sources.
- Treat the guide, GM-only scans, combat maps and route card as GM-secret until the players have learned the corresponding facts.
