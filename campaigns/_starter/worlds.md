# Campaign Worlds

Worlds that belong to this campaign.  The build reads this file first, then the shared pool in `library/worlds.md`, so every pool world is already available to your sessions.  A world here with the same slug as a pool world replaces it for this campaign only.

Copy the template below (or the Kestrel example) to add a world.  The template lists every field and its rules.  The `Slug` is the short name sessions use (`Worlds: kestrel@planetside`) and the start of every image and video file name for that world.

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

## 00. Kestrel

- **Slug:** `kestrel`
- **Scan Tagline:** A windswept waystation at the edge of charted space.
- **Planet Type:** Terrestrial World
- **Scan Class:** desert
- **Description:** Long-range scans resolve a cold, dry world of high plateaus and deep canyons under a thin, breathable atmosphere.  A single orbital beacon marks the system as an inhabited waystation.
- **Atmosphere:** Marginal; thin but breathable
- **Natural Feature:** Windward Shelf: a continent-long escarpment where steady winds blow day and night.
- **Settlements:** Kestrel Station, a refueling town of a few thousand people built into the canyon walls below the landing field.
- **Settlement Summary:** Single Outpost
- **Anthropocentric Feature:** Turbine Ridge: a line of wind turbines along the shelf that powers the station.
- **Observed from Space:** Rust-colored plateaus split by dark canyon systems, with thin white cloud streaming east.
- **Planetside Feature:** The landing field sits on a canyon rim, with the station's lights stacked down the cliff face below it.
- **Life:** Scarce: hardy lichens and burrowing grazers in the canyon floors.

### Planetary Data

- **Primary:** K2 V
- **Orbital Radius:** 0.81 AU
- **Local Year:** 0.79u
- **Mean Radius:** 5,120 km
- **Surface Gravity:** 0.86 g
- **Mean Surface Temp:** -4 °C

### Thermal Survey

Infrared mapping shows a cold world with warm seams along the canyon floors.  A tight cluster of heat marks Kestrel Station and the landing field above it.

### Surface Survey

Low-altitude survey imagery follows the Windward Shelf east, past the turbine line, to the station lights glowing on the canyon rim.
