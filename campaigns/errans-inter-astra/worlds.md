# Errans Inter Astra: Campaign Worlds

Worlds that belong to this campaign.  The build checks this file first, then the shared pool in `library/worlds.md`.  A world here with the same slug as a pool world replaces the pool version for this campaign only.

Format: see `library/worlds.md`.  Each world starts with `## NN. Name`.

<!--
=== NEW WORLD TEMPLATE ===
Copy everything between the dashed lines to the bottom of this file, delete the guide text after each value, and fill it in.
This block is a comment.  The build skips it.

Rules:
- Every field is required unless it says (optional).
- One line per field.  Sensor data only.  Campaign secrets belong in your campaign notes.
- Bad or missing values never stop the build.  They show at the table as INTERFERENCE, BAD SCAN, or NO RETURN,
  and the build report lists each one so you can fix it.
- To hide a value on purpose, type [interference], [too distant], [bad scan], or [no return] as the value.
- Any ### section that is not listed here is treated as GM notes and never reaches the screen.
-----------------------------------------------------------------
## 00. World Name

- **Slug:** `world-name`  (lowercase letters, numbers, and dashes; unique; also the start of every image and video file name)
- **Scan Tagline:** One short sentence.
- **Planet Type:** Free-text flavor, such as Nitrogen-Ocean Flood World.
- **Scan Class:** terrestrial | ocean | ice | desert | furnace | barren | tainted | grave | jovian | shattered  (optional; drives the wireframe; guessed from Planet Type when left out)
- **Description:** Two or three sentences about what long-range scans see.
- **Atmosphere:** Start with Breathable, Ideal, Marginal, Toxic, Corrosive, or None / thin.  Add detail after a semicolon.
- **Natural Feature:** Label: one sentence.
- **Settlements:** One or two sentences.
- **Settlement Summary:** Two to four words, such as Sparse Settlements, Orbital Station, Abandoned, Metroswathe.
- **Anthropocentric Feature:** Label: one sentence.
- **Observed from Space:** One sentence.
- **Planetside Feature:** One sentence.
- **Life:** Start with None detected, Extinct, Scarce, Diverse, Bountiful, or Overrun.  Optional ": detail" after it.
- **Moons:** A number.  (optional; guessed from the text and the slug when left out)
- **Rings:** yes or no.  (optional; guessed from the text when left out)

### Planetary Data

- **Primary:** Spectral class, such as G4 V.  Binary: G8 V + K2 V binary
- **Orbital Radius:** 1.02 AU  (moons: 6.40 AU stellar / 620,000 km from parent)
- **Local Year:** 1.06u
- **Mean Radius:** 6,240 km
- **Surface Gravity:** 0.98 g  (gas giants: 1.90 g @ 1 bar)
- **Mean Surface Temp:** 14 °C  (gas giants: -105 °C cloud tops)

### Thermal Survey

Two sentences.  Players can read this at long range, so keep spoilers out.

### Surface Survey

One or two sentences.  Players can read this at orbital depth.
-----------------------------------------------------------------
-->

## 00. Halas

- **Slug:** `halas`
- **Scan Tagline:** A quiet world no faction calls home.
- **Planet Type:** Vital World
- **Description:** Long-range scans resolve a temperate, breathable world of broad continents, inland seas, and a small northern ice cap.  Union's footprint is thin: one omninet relay, a modest administrative office, a handful of aid workers, and periodic naval traffic.  Registry records list a faction-neutral military academy on the southern continent.
- **Atmosphere:** Breathable
- **Natural Feature:** Remote: Halas lies near the Cascade Line, well off the major shipping lanes, and sees little traffic beyond periodic Union naval patrols.
- **Settlements:** Scattered diasporan towns along the southern river valleys, anchored by Keshar, a spaceport town of roughly twelve thousand with a militia and no mech capability.
- **Settlement Summary:** Sparse Settlements
- **Anthropocentric Feature:** Halas Academy: a faction-neutral Lancer academy on a plateau above the Verath River, twenty kilometers west of Keshar.
- **Observed from Space:** Broad savannah belts and river valleys cover the southern continent, broken by long mountain ranges and slow-turning ocean storms.
- **Planetside Feature:** The Verath River cuts a green valley through golden savannah, with the academy plateau rising above the valley floor.
- **Life:** Diverse: savannah grasslands, river valleys, and coastal shallows support a stable, well-surveyed biosphere.

### Planetary Data

- **Primary:** G4 V
- **Orbital Radius:** 1.02 AU
- **Local Year:** 1.06u
- **Mean Radius:** 6,240 km
- **Surface Gravity:** 0.98 g
- **Mean Surface Temp:** 14 °C

### Thermal Survey

Infrared mapping shows a temperate heat profile, warmest across the southern savannahs and coolest over the northern ice cap and high ranges.  Small, steady heat signatures mark Keshar's spaceport and the academy plateau above the Verath valley.

### Surface Survey

Low-altitude survey imagery shows the Verath River winding through savannah toward Keshar, with the academy plateau and its training yard visible above the valley.
