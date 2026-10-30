# 30 Random World Templates

Shared world pool for every OMNISLATE campaign.  Any session in any campaign can scan these worlds.  Campaign-specific worlds (such as Halas) live in each campaign's own `worlds.md`.

These worlds blend the *Ironsworn: Starforged* planet oracles with the *Lancer* GM Toolkit world-building tables. Rolls were treated as prompts rather than shackles: contradictory or repeated results were reconciled, repeated ideas were altered, and a few worlds were deliberately pushed into stranger military, ecological, or humorous territory.

This file is the canonical data source for the tablet planet atlas. The descriptive world concept comes first; the astronomical numbers support that concept rather than overriding it. `Local Year` is expressed in Union Standard Years (`u`). Gravity is relative to Cradle standard (`g`). For gas giants, gravity and temperature use the indicated atmospheric reference level instead of pretending a Jovian has a convenient floor.

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

## Image Naming Convention

Each world's `Slug` is the canonical filename stem. The atlas may use these image assets when present:

- `{slug}-planet.webp` — main orbital/hero image
- `{slug}-thermal.webp` — true false-color infrared/thermal survey
- `{slug}-surface.webp` — visible-light planetside or low-atmosphere survey
- `{slug}-settlement.webp` — settlement image
- `{slug}-anthropocentric.webp` — major human-built feature
- `{slug}-life.webp` — native life, ecology, fossils, or other biological evidence

Missing optional images should be handled gracefully by the eventual HTML viewer rather than replaced with invented content.

## 01. Nacre

- **Slug:** `nacre`
- **Scan Tagline:** A living ocean beneath eternal ice.
- **Planet Type:** Ice World
- **Description:** Long-range scans resolve a bright cryovolcanic sphere wrapped in toxic haze. Polar geysers throw ice plumes above the atmosphere, while thermal returns beneath the crust suggest a surprisingly busy biosphere.
- **Atmosphere:** Toxic
- **Natural Feature:** 100-Year Storms — multi-year cryoblizzards periodically erase surface routes and expose fresh ice canyons.
- **Settlements:** Planetside settlement clustered around geothermal vents and a shielded launch basin.
- **Settlement Summary:** Planetside
- **Anthropocentric Feature:** Uplift Spaceport — a hardened surface-to-orbit port cut directly into the ice shelf.
- **Observed from Space:** Sky-breaching geyser plumes glitter in sunlight and leave temporary rings of ice debris.
- **Planetside Feature:** Vivid auroras ripple almost continuously over the polar regions.
- **Life:** Diverse — subglacial ecosystems include blind filter-feeders large enough to register on seismic sensors.

### Planetary Data

- **Primary:** K2 V
- **Orbital Radius:** 2.20 AU
- **Local Year:** 3.69u
- **Mean Radius:** 7,300 km
- **Surface Gravity:** 1.10 g
- **Mean Surface Temp:** −125 °C

### Thermal Survey

False-color infrared mapping shows a mostly frigid crust crossed by warm geothermal fractures. Strong heat returns beneath the polar ice are consistent with a global subglacial ocean and active vent systems.

### Surface Survey

Polar survey imagery shows cryovolcanic geysers punching through wind-carved ice fields while persistent auroras ripple above the horizon.

## 02. Icarus

- **Slug:** `icarus`
- **Scan Tagline:** A living planet beneath a veil of spores.
- **Planet Type:** Tainted World
- **Description:** The planet is hidden beneath a stagnant yellow-green cloud deck threaded with immense fungal blooms. A single encrypted industrial transponder answers hails from below, but no civilian registry claims the site.
- **Atmosphere:** Toxic
- **Natural Feature:** Remote — the system sits well outside normal traffic and requires a deliberate detour to reach.
- **Settlements:** No recognized civilian settlement; one sealed corporate enclave maintains permanent personnel.
- **Settlement Summary:** Corporate Enclave
- **Anthropocentric Feature:** Corpro-State Campus — a self-contained research and extraction complex buried beneath the cloud layer.
- **Observed from Space:** Stagnant cloud cover conceals nearly the entire surface.
- **Planetside Feature:** Kilometer-wide fungal shelves grow around deep basalt fissures and shed hallucinogenic spores.
- **Life:** Diverse — hardy fungal, microbial, and invertebrate analogues dominate.

### Planetary Data

- **Primary:** K5 V
- **Orbital Radius:** 0.54 AU
- **Local Year:** 0.48u
- **Mean Radius:** 6,900 km
- **Surface Gravity:** 0.97 g
- **Mean Surface Temp:** 34 °C

### Thermal Survey

Infrared scans show a warm, uneven surface beneath the cloud deck. The strongest heat islands coincide with deep basalt fissures and the sealed industrial enclave, with broader low-grade warmth tracing fungal megacolonies.

### Surface Survey

Low-atmosphere survey imagery reveals kilometer-wide fungal shelves rising from basalt chasms beneath a yellow-green sky, with the corporate campus sealed into higher ground.

## 03. Carcosa

- **Slug:** `carcosa`
- **Scan Tagline:** Something waits beneath the ice.
- **Planet Type:** Subglacial Ocean Ice World
- **Description:** A thick ice shell covers a dark global ocean. One enormous cryovolcano dominates the northern hemisphere, while quarantined habitation lights trace a narrow drilling corridor across its flank.
- **Atmosphere:** Corrosive
- **Natural Feature:** Quarantine — automated Union beacons prohibit unscheduled descent and refuse to state why.
- **Settlements:** One first-generation planetside settlement beneath the ice, currently under quarantine.
- **Settlement Summary:** 1 Quarantined
- **Anthropocentric Feature:** First-Generation Settlement — a young drilling colony built around geothermal bore shafts.
- **Observed from Space:** A supersized ice volcano rises above the surrounding plains and vents a persistent plume.
- **Planetside Feature:** Massive wind-packed snow drifts bury structures within hours unless actively cleared.
- **Life:** None detected

### Planetary Data

- **Primary:** K4 V
- **Orbital Radius:** 2.10 AU
- **Local Year:** 3.64u
- **Mean Radius:** 7,400 km
- **Surface Gravity:** 1.00 g
- **Mean Surface Temp:** −155 °C

### Thermal Survey

Infrared mapping shows a cold shell broken by one immense geothermal province beneath the northern cryovolcano. A narrow chain of artificial heat signatures marks the drilling corridor and buried colony.

### Surface Survey

Visible-light survey shows the cryovolcano venting continuously over a plain of wind-packed drifts; exposed structures are quickly buried unless heated or mechanically cleared.

## 04. Pelagos

- **Slug:** `pelagos`
- **Scan Tagline:** No land. No silence beneath the waves.
- **Planet Type:** Landless Ocean World
- **Description:** No continental landmass is visible. Strong tides raised by a huge moon drive moving belts of stormwater around the globe, and naval traffic concentrates around a chain of armored floating platforms.
- **Atmosphere:** Marginal
- **Natural Feature:** Royal Court — dozens of small moons crowd the sky around the dominant tidal satellite.
- **Settlements:** Multiple floating and orbital military settlements.
- **Settlement Summary:** Military Network
- **Anthropocentric Feature:** SysComm Naval Command — a regional naval headquarters built into mobile ocean platforms and orbital docks.
- **Observed from Space:** A large moon dominates the sky and visibly distorts global weather bands.
- **Planetside Feature:** Vast undersea cave systems honeycomb volcanic ridges beneath the open ocean.
- **Life:** Diverse — deep-water leviathans force naval sonar doctrine to distinguish wildlife from submarines.

### Planetary Data

- **Primary:** G3 V
- **Orbital Radius:** 1.05 AU
- **Local Year:** 1.07u
- **Mean Radius:** 6,800 km
- **Surface Gravity:** 1.05 g
- **Mean Surface Temp:** 12 °C

### Thermal Survey

Thermal imaging tracks warm equatorial currents, colder abyssal upwellings, and concentrated heat from mobile naval platforms. Several large moving subsurface returns are biological rather than mechanical.

### Surface Survey

Atmospheric survey shows armored floating bases riding heavy swells beneath an enormous moon, while sonar maps reveal cavern systems and leviathan-scale contacts below.

## 05. Ashfall

- **Slug:** `ashfall`
- **Scan Tagline:** A dead world still glowing with old mistakes.
- **Planet Type:** Grave World
- **Description:** The world presents as a dead industrial ruin under permanent overcast. Radiation blooms mark the old population centers, and orbital spectroscopy identifies layers of dumped reactor slag mixed into the upper crust.
- **Atmosphere:** Toxic
- **Natural Feature:** Monument of Shame — later powers used the abandoned world as a dumping ground for hazardous waste.
- **Settlements:** Abandoned planetside settlements; no confirmed permanent population.
- **Settlement Summary:** Abandoned
- **Anthropocentric Feature:** Union Embassy — the old diplomatic complex still stands intact inside an evacuated capital district.
- **Observed from Space:** Perpetual overcast broken only by the glow of contaminated storm systems.
- **Planetside Feature:** Radioactive hotspots surround collapsed industrial zones and dry canals.
- **Life:** Scarce — isolated extremophile colonies survive in sealed aquifers.

### Planetary Data

- **Primary:** K0 V
- **Orbital Radius:** 0.95 AU
- **Local Year:** 1.04u
- **Mean Radius:** 6,200 km
- **Surface Gravity:** 0.91 g
- **Mean Surface Temp:** −5 °C

### Thermal Survey

Infrared scans show weak natural heat and persistent artificial-looking hot zones around buried waste fields, failed reactors, and contaminated storm cells.

### Surface Survey

Ground survey finds collapsed industrial corridors, dry canals, black slag dunes, and radiation warning beacons surrounding the intact shell of a former Union embassy.

## 06. Dunwich

- **Slug:** `dunwich`
- **Scan Tagline:** A world that never stops burning.
- **Planet Type:** Furnace World
- **Description:** Ash clouds pulse with continuous lightning above a volcanically active surface. Despite the spectacle, the system is a routine shipping landmark, and a small orbital laboratory watches the planet like someone staring into an oven.
- **Atmosphere:** Marginal
- **Natural Feature:** Cosmopolitan — major shipping routes pass close enough for frequent resupply traffic.
- **Settlements:** Orbital research station only; the surface has no permanent civilian habitation.
- **Settlement Summary:** Orbital Station
- **Anthropocentric Feature:** Research Facility — a long-duration geophysics laboratory in low orbit.
- **Observed from Space:** Lightning-wracked ash clouds obscure much of the dayside.
- **Planetside Feature:** Steaming mineral mudflats occupy temporary basins between lava fields.
- **Life:** None detected

### Planetary Data

- **Primary:** G6 V
- **Orbital Radius:** 0.72 AU
- **Local Year:** 0.64u
- **Mean Radius:** 6,300 km
- **Surface Gravity:** 0.94 g
- **Mean Surface Temp:** 92 °C

### Thermal Survey

Infrared imaging is saturated by volcanic provinces, lava lakes, and fresh flows. Cooler islands between calderas form the only practical surface observation zones.

### Surface Survey

Survey craft record steaming mineral mudflats between active lava fields while electrical storms repeatedly strike ash columns rising above the horizon.

## 07. Ferrovia

- **Slug:** `ferrovia`
- **Scan Tagline:** Cities drift where the seas permit.
- **Planet Type:** Nitrogen-Ocean Flood World
- **Description:** A mild upper atmosphere hangs over dark nitrogen-rich seas and mobile forests of buoyant vegetation. Most inhabited platforms are sealed by quarantine barriers, including the fortified complex that serves as the system capital.
- **Atmosphere:** Ideal at inhabited elevations; hazardous near the ocean surface
- **Natural Feature:** Quarantine — traffic control permits orbital approach but tightly restricts atmospheric entry.
- **Settlements:** Multiple floating cities and orbital habitats, presently operating under quarantine protocols.
- **Settlement Summary:** Multiple / Quarantined
- **Anthropocentric Feature:** System Government Capital Complex — an armored administrative platform that migrates with the safest current.
- **Observed from Space:** Floating forests form continent-scale green rafts visible from orbit.
- **Planetside Feature:** Roaming icebergs of exotic volatiles drift through warmer equatorial waters.
- **Life:** Bountiful

### Planetary Data

- **Primary:** K1 V
- **Orbital Radius:** 0.85 AU
- **Local Year:** 0.86u
- **Mean Radius:** 7,100 km
- **Surface Gravity:** 1.08 g
- **Mean Surface Temp:** 8 °C

### Thermal Survey

Thermal scans reveal warm floating forests and inhabited platforms moving along stable current bands. The lower atmosphere and sea surface show colder, chemically hazardous zones.

### Surface Survey

Low-altitude imaging shows vast buoyant forests, armored civic platforms, and pale volatile icebergs drifting through dark equatorial seas.

## 08. Dykuma

- **Slug:** `dykuma`
- **Scan Tagline:** The router at the end of everything.
- **Planet Type:** Ancient White-Dune Sun World
- **Description:** The surface is a pale desert of eroded mountains and nearly airless dune fields. Deep scans find pre-Fall structures inside cliff caves, while the only active human signal comes from one stubborn omninet relay.
- **Atmosphere:** None / thin
- **Natural Feature:** Dust and Echoes — scattered pre-Fall ruins survive where stone overhangs shield them from erosion.
- **Settlements:** None; a rotating maintenance crew occasionally services the relay.
- **Settlement Summary:** None
- **Anthropocentric Feature:** Omninet Relay Node — the lone active installation, locally nicknamed 'the Router at the End of Everything.'
- **Observed from Space:** Dark rugged mountains protrude from otherwise white dune seas.
- **Planetside Feature:** Timeworn cliffside caves contain sheltered ruins and wind-polished access shafts.
- **Life:** None detected

### Planetary Data

- **Primary:** G6 V
- **Orbital Radius:** 0.48 AU
- **Local Year:** 0.35u
- **Mean Radius:** 4,800 km
- **Surface Gravity:** 0.52 g
- **Mean Surface Temp:** 115 °C

### Thermal Survey

Day-side infrared imaging shows extreme heating across exposed dunes and rock, while deeply shaded cave systems remain dramatically cooler and preserve traces of older structures.

### Surface Survey

Survey imagery shows white dune seas, black eroded mountains, and cliffside cave mouths surrounding the lone omninet relay installation.

## 09. Magnus

- **Slug:** `magnus`
- **Scan Tagline:** Cities suspended above a world without ground.
- **Planet Type:** Jovian World
- **Description:** A ringed gas giant radiates enough heat to glow faintly on infrared. Habitation consists of linked aerostat arcologies suspended above the lethal lower cloud decks, each riding predictable bands in the atmosphere.
- **Atmosphere:** Toxic
- **Natural Feature:** Ringed — dense bright rings create frequent eclipses across the upper atmosphere.
- **Settlements:** Multiple aerostat arcologies and supporting orbital stations.
- **Settlement Summary:** Aerostat Arcologies
- **Anthropocentric Feature:** Arcology Network — self-contained floating cities linked by shuttle corridors and atmospheric tugs.
- **Observed from Space:** The lower atmosphere is superheated and visibly luminous in thermal imaging.
- **Planetside Feature:** Intense radiation fields and charged-particle belts surround the deeper cloud layers.
- **Life:** None detected

### Planetary Data

- **Primary:** K3 V
- **Orbital Radius:** 3.70 AU
- **Local Year:** 8.27u
- **Mean Radius:** 58,000 km
- **Surface Gravity:** 1.90 g @ 1 bar
- **Mean Surface Temp:** −105 °C cloud tops

### Thermal Survey

Infrared imaging shows strong internal heat leaking through deeper cloud bands beneath much colder upper layers. Aerostat arcologies appear as narrow warm tracks riding stable atmospheric zones.

### Surface Survey

Upper-atmosphere survey shows linked floating arcologies beneath bright rings, with deeper cloud layers flashing from electrical storms and radiation events.

## 10. Janus

- **Slug:** `janus`
- **Scan Tagline:** Breathable air exists, but only where the world allows it.
- **Planet Type:** Choked-Valley Inhospitable World
- **Description:** High gravity presses a thick toxic atmosphere into lowlands, but a few elevated valleys contain breathable pockets. A new colony occupies one such refuge beside enormous fossil beds exposed by recent erosion.
- **Atmosphere:** Toxic globally; locally breathable in high valleys
- **Natural Feature:** High Gravity — surface gravity is substantially above Cradle standard.
- **Settlements:** One new planetside settlement in a naturally ventilated highland basin.
- **Settlement Summary:** New Colony
- **Anthropocentric Feature:** New Settlement — prefabricated habitats and construction subalterns still outnumber permanent residents.
- **Observed from Space:** A stagnant cloud deck hides the lowlands and leaves isolated mountain summits exposed.
- **Planetside Feature:** Fields of enormous weathered bones line the valley margins.
- **Life:** Diverse

### Planetary Data

- **Primary:** K0 V
- **Orbital Radius:** 0.90 AU
- **Local Year:** 0.96u
- **Mean Radius:** 8,400 km
- **Surface Gravity:** 1.80 g
- **Mean Surface Temp:** 27 °C

### Thermal Survey

Thermal mapping distinguishes hot, dense lowlands from cooler elevated basins. The colony occupies one of the few high valleys where atmospheric chemistry and temperature approach human tolerance.

### Surface Survey

Survey imagery shows a sealed new settlement overlooking enormous fossil beds while heavy toxic cloud fills the valleys below.

## 11. Mourn

- **Slug:** `mourn`
- **Scan Tagline:** A whole civilization, intact and empty.
- **Planet Type:** Grave World
- **Description:** Orbital imagery shows a planet-spanning municipal grid with no active power signatures. Roads, reservoirs, and cities remain geometrically intact around a colossal crater, but nothing living answers the scan.
- **Atmosphere:** Toxic
- **Natural Feature:** Dust and Echoes — dense pre-Fall urban remains preserve a nearly complete picture of the dead society.
- **Settlements:** None; every known municipality is abandoned.
- **Settlement Summary:** Abandoned
- **Anthropocentric Feature:** Municipal World, dead — hundreds of former cities and towns remain connected by intact infrastructure.
- **Observed from Space:** A massive impact basin interrupts the otherwise regular city grid.
- **Planetside Feature:** Radioactive hotspots flare around transit hubs and old power infrastructure.
- **Life:** None detected

### Planetary Data

- **Primary:** G8 V
- **Orbital Radius:** 0.95 AU
- **Local Year:** 0.99u
- **Mean Radius:** 6,100 km
- **Surface Gravity:** 0.91 g
- **Mean Surface Temp:** 4 °C

### Thermal Survey

Infrared scans find no active population centers, only residual heat from geothermal systems and intermittent power in isolated infrastructure nodes.

### Surface Survey

Street-level survey shows intact transit grids, silent reservoirs, and abandoned municipal towers beneath a sky stained by old atmospheric contamination.

## 12. Selene

- **Slug:** `selene`
- **Scan Tagline:** A quiet stone used to listen to distant stars.
- **Planet Type:** Rocky World
- **Description:** A small airless world shows broad barren plains cut by unnaturally regular mineral ridges. An orbital astrocartography station uses the quiet electromagnetic environment for extremely long-baseline observations.
- **Atmosphere:** None / thin
- **Natural Feature:** Inert Core — no meaningful magnetic field protects the surface from charged particles.
- **Settlements:** One orbital settlement attached to the survey station.
- **Settlement Summary:** Orbital Station
- **Anthropocentric Feature:** Astrocartography Station — telescopes and distributed sensor arrays map distant systems from orbit.
- **Observed from Space:** Featureless plains dominate the hemisphere facing the primary.
- **Planetside Feature:** Geometric mineral formations create straight ridges and polygonal basins over hundreds of kilometers.
- **Life:** None detected

### Planetary Data

- **Primary:** K1 V
- **Orbital Radius:** 0.72 AU
- **Local Year:** 0.67u
- **Mean Radius:** 2,900 km
- **Surface Gravity:** 0.28 g
- **Mean Surface Temp:** 10 °C mean

### Thermal Survey

Infrared scans show severe day-night temperature contrast across the airless surface. The only stable artificial heat signatures belong to the orbital survey complex.

### Surface Survey

Low passes reveal broad barren plains interrupted by unnaturally straight mineral ridges and immense polygonal basins.

## 13. Azula

- **Slug:** `azula`
- **Scan Tagline:** If it explodes here, that was probably the point.
- **Planet Type:** Young Lava-and-Lightning World
- **Description:** A massive supervolcano and constant electrical storms make the world an excellent place to test things nobody wants detonating near civilization. Surface telemetry is dominated by instrumented impact zones and hardened observation bunkers.
- **Atmosphere:** Corrosive
- **Natural Feature:** Remote — deliberate isolation made the planet attractive as a hazardous testing range.
- **Settlements:** No civilian settlement; rotating military and contractor crews occupy hardened installations.
- **Settlement Summary:** Military / Contractor
- **Anthropocentric Feature:** Proving Ground — weapons, chassis, armor systems, and experimental ordnance are tested on a planetary scale.
- **Observed from Space:** One supervolcano dominates the nightside in thermal scans.
- **Planetside Feature:** Scalding geyser fields occupy the few regions not covered by fresh lava.
- **Life:** Scarce — microbial extremophiles persist near cooler vents.

### Planetary Data

- **Primary:** F9 V
- **Orbital Radius:** 0.55 AU
- **Local Year:** 0.39u
- **Mean Radius:** 6,600 km
- **Surface Gravity:** 1.05 g
- **Mean Surface Temp:** 165 °C

### Thermal Survey

Infrared imagery is dominated by the supervolcano, fresh lava fields, and instrumented weapons-impact zones. Hardened observation bunkers appear as cool geometric voids amid the heat.

### Surface Survey

Survey imagery shows scalding geysers, lightning-struck ash plains, range markers, and reinforced test structures scattered between active lava channels.

## 14. Veil

- **Slug:** `veil`
- **Scan Tagline:** An ecosystem floating in the sky.
- **Planet Type:** Jovian World
- **Description:** This cool gas giant supports stable atmospheric layers where water-rich floating glaciers drift like islands. Biological signatures move between them in enormous slow formations, and a permanent uplift port hangs from a tethered aerostat.
- **Atmosphere:** Marginal
- **Natural Feature:** Monobiome — the habitable atmospheric band behaves as one continuous aerial ecosystem.
- **Settlements:** One major aerostat settlement with smaller service platforms.
- **Settlement Summary:** Aerostat Settlement
- **Anthropocentric Feature:** Uplift Spaceport — a high-altitude tether port services atmospheric craft and orbital shuttles.
- **Observed from Space:** Numerous moons produce a constantly changing sky.
- **Planetside Feature:** Floating glaciers carry whole microbial and plantlike ecologies through the upper clouds.
- **Life:** Diverse — kilometer-scale filter-feeders drift between the ice masses.

### Planetary Data

- **Primary:** K7 V
- **Orbital Radius:** 2.10 AU
- **Local Year:** 3.86u
- **Mean Radius:** 48,000 km
- **Surface Gravity:** 1.40 g @ 1 bar
- **Mean Surface Temp:** −95 °C cloud tops

### Thermal Survey

Infrared scans show a broad temperate atmospheric band warmed by internal heat. Floating glaciers and large airborne organisms register as cooler masses moving through warmer cloud currents.

### Surface Survey

Atmospheric survey shows inhabited aerostats tethered among drifting ice masses while kilometer-scale filter-feeders move slowly through the cloud sea.

## 15. Ory

- **Slug:** `ory`
- **Scan Tagline:** The planet repeats itself.
- **Planet Type:** Symmetry World
- **Description:** A low-gravity rocky planet exhibits repeating terrain at scales too large to dismiss as coincidence. Every major basin appears to mirror another across a single equatorial axis, making even routine mapping strangely unsettling.
- **Atmosphere:** None / thin
- **Natural Feature:** Low Gravity — weak surface gravity preserves delicate formations that would collapse on heavier worlds.
- **Settlements:** No civilian settlement; one forward post monitors the equatorial landmark.
- **Settlement Summary:** Forward Post
- **Anthropocentric Feature:** Checkpoint / Forward Post — a small garrison controls the only approved landing corridor.
- **Observed from Space:** The planet is visibly misshapen, with two broad lobes arranged around a central equatorial ridge.
- **Planetside Feature:** Straight-sided ravines and repeating hexagonal basins converge toward a black central mesa.
- **Life:** None detected

### Planetary Data

- **Primary:** G4 V
- **Orbital Radius:** 1.35 AU
- **Local Year:** 1.59u
- **Mean Radius:** 3,900 km
- **Surface Gravity:** 0.42 g
- **Mean Surface Temp:** −18 °C

### Thermal Survey

Infrared imaging shows the same broad thermal structures repeating across mirrored basins, reinforcing the planet's unsettling geometric symmetry.

### Surface Survey

Ground survey records straight-sided ravines, repeating hexagonal basins, and delicate stone formations converging on a black equatorial mesa.

## 16. Rasal

- **Slug:** `rasal`
- **Scan Tagline:** The capital died. Its systems did not.
- **Planet Type:** Grave World
- **Description:** The shattered remains of a moon trail the planet in a broad debris arc. Beneath it lies an abandoned planetary capital whose administrative center is still powered, though no living government claims it.
- **Atmosphere:** None / thin
- **Natural Feature:** Worldscar — an ancient impact excavated a basin large enough to alter the planet's silhouette.
- **Settlements:** None; the former capital complex is abandoned but partially functional.
- **Settlement Summary:** Abandoned
- **Anthropocentric Feature:** System Government Capital Complex — empty ministries, hardened archives, and autonomous civic systems remain online.
- **Observed from Space:** A broken moon and its debris stream dominate near orbit.
- **Planetside Feature:** Acoustic sensors occasionally register voice-like resonances moving through empty structures.
- **Life:** Extinct

### Planetary Data

- **Primary:** K2 V
- **Orbital Radius:** 0.90 AU
- **Local Year:** 0.97u
- **Mean Radius:** 5,200 km
- **Surface Gravity:** 0.62 g
- **Mean Surface Temp:** −35 °C

### Thermal Survey

Thermal survey shows an otherwise cold world punctuated by active power sources inside the abandoned capital complex and beneath several sealed archive districts.

### Surface Survey

Survey drones pass through empty ministry blocks and transit halls while a broken moon hangs above the impact-scarred horizon.

## 17. Harbinger

- **Slug:** `harbinger`
- **Scan Tagline:** A living world where the ground refuses to stay grounded.
- **Planet Type:** Vital World
- **Description:** A breathable biosphere lies beneath a brilliant ring system. Terrain mapping reveals floating stone shelves and frequent seismic shifts, while a discreet orbital SIGINT station quietly listens to traffic across the sector.
- **Atmosphere:** Breathable
- **Natural Feature:** Dreamland — isolated landmasses remain suspended above the surface by an unresolved geophysical effect.
- **Settlements:** One orbital settlement; small temporary expeditions operate planetside.
- **Settlement Summary:** Orbital Station
- **Anthropocentric Feature:** SIGINT Station — a low-profile signals intelligence post hidden among ring-monitoring satellites.
- **Observed from Space:** A complex ring system casts moving shadows across the surface.
- **Planetside Feature:** Frequent seismic activity rearranges valleys without disturbing the floating plateaus.
- **Life:** Bountiful

### Planetary Data

- **Primary:** G2 V
- **Orbital Radius:** 1.08 AU
- **Local Year:** 1.12u
- **Mean Radius:** 6,900 km
- **Surface Gravity:** 1.08 g
- **Mean Surface Temp:** 16 °C

### Thermal Survey

Thermal mapping shows ordinary biospheric heat interrupted by cool floating plateaus and active fault zones. The orbital SIGINT station is nearly invisible outside narrow communications windows.

### Surface Survey

Survey imagery shows forested valleys repeatedly reshaped by seismic activity beneath immense floating stone shelves.

## 18. Cinder Crown

- **Slug:** `cinder-crown`
- **Scan Tagline:** A habitable edge around a planetary furnace.
- **Planet Type:** Furnace World
- **Description:** Despite heavy volcanism, the upper atmosphere is breathable across limited highland zones. Ash storms flash with lightning around several active calderas, and a lonely deep-field relay occupies the most geologically stable plateau.
- **Atmosphere:** Breathable in highland regions
- **Natural Feature:** Royal Court — a swarm of small captured moons and debris fragments crowds local space.
- **Settlements:** No civilian settlement; a staffed relay and emergency shelter are the only permanent human presence.
- **Settlement Summary:** Relay Outpost
- **Anthropocentric Feature:** Deep-Field Relay — a hardened long-range sensor and communications site.
- **Observed from Space:** Lightning-wracked ash clouds spiral around a chain of active volcanic basins.
- **Planetside Feature:** Catastrophic earthquakes routinely open new vents and close old routes.
- **Life:** Scarce — heat-resistant lichen analogues cling to cooler highlands.

### Planetary Data

- **Primary:** K0 V
- **Orbital Radius:** 0.58 AU
- **Local Year:** 0.50u
- **Mean Radius:** 6,500 km
- **Surface Gravity:** 1.02 g
- **Mean Surface Temp:** 78 °C

### Thermal Survey

Infrared scans show linked volcanic basins separated by cooler highland refuges. The deep-field relay occupies one of the few thermally stable plateaus.

### Surface Survey

Ground survey shows ash storms, fresh fault scarps, and highland shelters overlooking incandescent calderas.

## 19. Lacuna

- **Slug:** `lacuna`
- **Scan Tagline:** Old rivers. New fractures. Cities overhead.
- **Planet Type:** Dry Temperate Paleo-River World
- **Description:** Broad plateaus and fossil river systems cover a dry temperate planet still undergoing active uplift. Human habitation has migrated into orbital arcologies after repeated quakes damaged the oldest surface settlements.
- **Atmosphere:** Marginal
- **Natural Feature:** Active Tectonics — fault lines continually reshape the old river basins.
- **Settlements:** Orbital arcology chain with seasonal surface work camps.
- **Settlement Summary:** Orbital Arcologies
- **Anthropocentric Feature:** Arcology Network — linked orbital habitats replaced several quake-damaged ground cities.
- **Observed from Space:** Vast plateaus are divided by the dark traces of ancient drainage systems.
- **Planetside Feature:** Timeworn cliff caves preserve evidence of repeated human occupation.
- **Life:** Diverse

### Planetary Data

- **Primary:** G7 V
- **Orbital Radius:** 1.03 AU
- **Local Year:** 1.10u
- **Mean Radius:** 6,200 km
- **Surface Gravity:** 0.94 g
- **Mean Surface Temp:** 14 °C

### Thermal Survey

Thermal scans trace active faults across broad plateaus and reveal seasonal work camps clustered near mineral-rich paleo-river deposits.

### Surface Survey

Survey imagery shows dry river canyons, uplifted plateaus, and cliff caves containing layers of abandoned human construction.

## 20. Palisade

- **Slug:** `palisade`
- **Scan Tagline:** A city large enough to become geography.
- **Planet Type:** Ocean World
- **Description:** Low gravity and shallow global seas allowed one urban region to spread outward instead of upward. The result is a floating metroswathe hundreds of kilometers across, stitched together by causeways, docks, and mobile neighborhoods.
- **Atmosphere:** Marginal
- **Natural Feature:** Low Gravity — weak gravity produces unusually broad waves and long-lived airborne spray.
- **Settlements:** Multiple floating settlements merged into one immense urban belt.
- **Settlement Summary:** Metroswathe
- **Anthropocentric Feature:** Metroswathe — a continuous floating city-region home to billions, with very little agreement about where one district ends.
- **Observed from Space:** Scattered natural islands are almost lost inside the artificial city pattern.
- **Planetside Feature:** Enormous shallow-water plains extend far beyond the inhabited belt.
- **Life:** Diverse

### Planetary Data

- **Primary:** K1 V
- **Orbital Radius:** 0.78 AU
- **Local Year:** 0.76u
- **Mean Radius:** 5,100 km
- **Surface Gravity:** 0.63 g
- **Mean Surface Temp:** 19 °C

### Thermal Survey

Infrared imaging shows the floating metroswathe as a vast warm lattice over cooler shallow seas, with mobile districts producing slowly shifting heat patterns.

### Surface Survey

Low-altitude survey reveals causeways, floating neighborhoods, ship canals, and natural islands nearly swallowed by continuous urban development.

## 21. Navini

- **Slug:** `navini`
- **Scan Tagline:** The islands are alive, and they migrate.
- **Planet Type:** Ocean World
- **Description:** Semi-frozen oceans are broken by dark mobile 'islands' that change position between orbital passes. Close scans show they are colonial organisms, some large enough to carry entire forests and temporary research camps.
- **Atmosphere:** Marginal
- **Natural Feature:** Inert Core — weak magnetospheric protection produces harsh auroral radiation at high latitudes.
- **Settlements:** One planetside research settlement plus mobile scientific camps.
- **Settlement Summary:** Research Settlement
- **Anthropocentric Feature:** Research Facility — marine biologists and xenologists study the living islands and deep-ocean ecology.
- **Observed from Space:** Semi-frozen oceans form shifting belts of pack ice around warmer currents.
- **Planetside Feature:** Living islands migrate slowly across the ocean and occasionally collide with one another.
- **Life:** Overrun

### Planetary Data

- **Primary:** K3 V
- **Orbital Radius:** 0.86 AU
- **Local Year:** 0.93u
- **Mean Radius:** 6,500 km
- **Surface Gravity:** 0.98 g
- **Mean Surface Temp:** −12 °C

### Thermal Survey

Infrared mapping shows warm ocean currents threading beneath pack ice and large mobile biological heat signatures corresponding to the living islands.

### Surface Survey

Survey imagery shows research camps anchored atop dark colonial organisms carrying forests across semi-frozen seas.

## 22. Chitin

- **Slug:** `chitin`
- **Scan Tagline:** The biosphere is not sick. It only looks that way.
- **Planet Type:** Tainted World
- **Description:** Toxic seas and dense biological aerosols make the planet look diseased from orbit, but the biosphere is vigorous rather than dying. A young colony survives in a sealed cliff habitat above the worst of the weather.
- **Atmosphere:** Toxic
- **Natural Feature:** Ringed — dark rings rich in organic dust create frequent meteor showers.
- **Settlements:** One first-generation sealed planetside settlement.
- **Settlement Summary:** First-Generation Colony
- **Anthropocentric Feature:** First-Generation Settlement — colonists are adapting imported agriculture to an aggressively living environment.
- **Observed from Space:** Toxic seas reflect a dull metallic green beneath the cloud deck.
- **Planetside Feature:** Toxic rain can strip exposed coatings within hours.
- **Life:** Bountiful

### Planetary Data

- **Primary:** K6 V
- **Orbital Radius:** 0.46 AU
- **Local Year:** 0.39u
- **Mean Radius:** 6,700 km
- **Surface Gravity:** 0.98 g
- **Mean Surface Temp:** 31 °C

### Thermal Survey

Infrared scans show warm toxic seas and dense biological activity across coastal shelves. The sealed cliff colony stands out as a controlled cool zone amid vigorous native growth.

### Surface Survey

Survey imagery shows corrosive rain sweeping fungal coastlines below a sealed cliff habitat and reinforced agricultural modules.

## 23. Sif

- **Slug:** `sif`
- **Scan Tagline:** A forest tall enough to touch the weather.
- **Planet Type:** Old-Growth Temperate Biosphere
- **Description:** Orbital scans cannot find bare ground across most of the equatorial continent. Trees breach the cloud layer, waterfalls descend through stacked canopy levels, and the system administrator's residence occupies a deliberately tiny clearing.
- **Atmosphere:** Breathable
- **Natural Feature:** Hecatoncheires — mountain chains rise so high that several peaks project above the weather.
- **Settlements:** Sparse planetside settlements connected by air and orbital transit.
- **Settlement Summary:** Sparse Settlements
- **Anthropocentric Feature:** Union Administrator's Residence — a modest diplomatic enclave kept intentionally small to limit ecological disturbance.
- **Observed from Space:** Cloud-breaching trees form visible dark ridges across the equatorial canopy.
- **Planetside Feature:** Immense tiered waterfalls descend through kilometers of vegetation.
- **Life:** Bountiful — megafauna use the upper canopy like ordinary animals use open plains.

### Planetary Data

- **Primary:** G1 V
- **Orbital Radius:** 1.12 AU
- **Local Year:** 1.16u
- **Mean Radius:** 7,000 km
- **Surface Gravity:** 1.07 g
- **Mean Surface Temp:** 20 °C

### Thermal Survey

Thermal imagery shows a dense, continuous biosphere with strong warm signatures from megafauna moving through upper canopy corridors and cooler mountain spines above the weather.

### Surface Survey

Survey imagery reveals kilometer-deep stacked canopy, cloud-breaching trees, tiered waterfalls, and enormous animals moving across the upper branches.

## 24. Thalassa

- **Slug:** `thalassa`
- **Scan Tagline:** An ocean world built around an ancient wound.
- **Planet Type:** Ocean World
- **Description:** A breathable ocean planet carries the scar of a colossal ancient impact basin. Modern settlements cluster around scattered islands, while a SysComm naval complex occupies the deep central basin and the orbital space above it.
- **Atmosphere:** Breathable
- **Natural Feature:** Worldscar — a planetary impact basin forms the deepest ocean trench in the system.
- **Settlements:** Multiple island, floating, submarine, and orbital settlements.
- **Settlement Summary:** Multiple
- **Anthropocentric Feature:** SysComm Naval Command — fleet docks, submarine pens, and orbital logistics platforms dominate the central basin.
- **Observed from Space:** Scattered island chains trace the rim of an immense circular ocean basin.
- **Planetside Feature:** A sealed pre-Fall bunker complex is embedded in the trench wall beneath kilometers of water.
- **Life:** Diverse

### Planetary Data

- **Primary:** G5 V
- **Orbital Radius:** 0.98 AU
- **Local Year:** 1.01u
- **Mean Radius:** 6,900 km
- **Surface Gravity:** 1.03 g
- **Mean Surface Temp:** 18 °C

### Thermal Survey

Thermal imaging shows strong equatorial currents and a conspicuous concentration of human activity around the central impact basin, including submarine and orbital infrastructure.

### Surface Survey

Survey imagery shows island settlements and naval platforms above an abyssal trench whose wall contains a sealed pre-Fall bunker complex.

## 25. Alecto

- **Slug:** `alecto`
- **Scan Tagline:** The life is gone. The radiation is not.
- **Planet Type:** Gamma-Scoured Burn World
- **Description:** The biosphere died after a historical radiation event and never recovered. The atmosphere remains chemically hostile, hot regions glow in infrared, and a forward checkpoint exists mainly to keep scavengers from entering the exclusion zone.
- **Atmosphere:** Toxic
- **Natural Feature:** Epochal Sunset — the planet is shifting from a hot post-catastrophe climate toward a colder geologic state.
- **Settlements:** No civilian settlement; one fortified checkpoint and rotating patrol force.
- **Settlement Summary:** Forward Post
- **Anthropocentric Feature:** Checkpoint / Forward Post — armed patrols enforce the exclusion perimeter and monitor unauthorized landings.
- **Observed from Space:** The upper atmosphere still shows persistent irradiation and abnormal ionization.
- **Planetside Feature:** Radioactive hotspots surround vitrified forests and burned continental margins.
- **Life:** Extinct

### Planetary Data

- **Primary:** F6 V
- **Orbital Radius:** 1.60 AU
- **Local Year:** 1.85u
- **Mean Radius:** 6,400 km
- **Surface Gravity:** 0.96 g
- **Mean Surface Temp:** 41 °C

### Thermal Survey

Infrared scans show broad cooling continents punctuated by persistent radioactive hot zones and vitrified regions that still retain unusual heat.

### Surface Survey

Survey imagery shows burned continental margins, glassed forests, exclusion markers, and a fortified patrol post overlooking contaminated wastes.

## 26. Morricone

- **Slug:** `morricone`
- **Scan Tagline:** A dead sea world waiting for the next storm.
- **Planet Type:** Desert World
- **Description:** Dry seabeds cover most of a breathable but biologically dead planet. Rare storms produce violent flash floods through old embassy districts, briefly turning empty diplomatic boulevards into rivers.
- **Atmosphere:** Breathable
- **Natural Feature:** Inert Core — the weak magnetic field leaves the surface exposed to hard solar weather.
- **Settlements:** No current settlement; the former diplomatic city is abandoned.
- **Settlement Summary:** Abandoned
- **Anthropocentric Feature:** Union Embassy — an intact but empty embassy complex remains from a failed settlement era.
- **Observed from Space:** Dry seabeds and retreat lines from vanished oceans cover most low elevations.
- **Planetside Feature:** Short rain events become destructive flash floods in ancient channels.
- **Life:** Extinct

### Planetary Data

- **Primary:** K0 V
- **Orbital Radius:** 0.82 AU
- **Local Year:** 0.84u
- **Mean Radius:** 6,300 km
- **Surface Gravity:** 0.95 g
- **Mean Surface Temp:** 26 °C

### Thermal Survey

Thermal mapping shows hot exposed seabeds, cooler canyon shadows, and brief sharp temperature drops where rare storm fronts form.

### Surface Survey

Survey imagery shows abandoned embassy avenues crossing dry seabeds; after storms, the same streets become violent temporary rivers.

## 27. Sunder

- **Slug:** `sunder`
- **Scan Tagline:** A planet in the process of becoming debris.
- **Planet Type:** Impact-Cracked Dying World
- **Description:** The planet is literally coming apart along old impact fractures. Weak gravity, exposed mantle caverns, and geomagnetic storms make navigation unreliable, but a Far-Field team maintains a tiny observation post on the largest stable fragment.
- **Atmosphere:** None / thin
- **Natural Feature:** Low Gravity — continuing mass loss has reduced surface gravity and destabilized debris orbits.
- **Settlements:** No civilian settlement; one Union Far-Field outpost.
- **Settlement Summary:** Far-Field Outpost
- **Anthropocentric Feature:** Union Far-Field Team Mission — a small scientific crew monitors the world's slow disassembly.
- **Observed from Space:** Geomagnetic storms flicker through a broad cloud of charged planetary debris.
- **Planetside Feature:** Exposed caverns open directly to space along kilometer-deep fractures.
- **Life:** Extinct

### Planetary Data

- **Primary:** K5 V
- **Orbital Radius:** 0.70 AU
- **Local Year:** 0.72u
- **Mean Radius:** 4,200 km
- **Surface Gravity:** 0.31 g
- **Mean Surface Temp:** 8 °C

### Thermal Survey

Infrared mapping shows heat leaking directly through open mantle fractures while the rest of the surface cools rapidly into vacuum.

### Surface Survey

Survey imagery shows exposed caverns, kilometer-deep cracks open to space, drifting crustal fragments, and the tiny Far-Field outpost anchored to stable rock.

## 28. Nephele

- **Slug:** `nephele`
- **Scan Tagline:** A storm large enough to define a hemisphere.
- **Planet Type:** Jovian World
- **Description:** A pale gas giant shows a permanent black polar cyclone surrounded by luminous cloud bands. Scientific aerostats track native airborne organisms while an orbital astrocartography station uses the planet's gravity well for precision observations.
- **Atmosphere:** Marginal in the upper cloud band
- **Natural Feature:** Hard Sun — upper-atmosphere habitats receive punishing ultraviolet exposure during the long local day.
- **Settlements:** One orbital settlement with several unmanned and temporary atmospheric platforms.
- **Settlement Summary:** Orbital Station
- **Anthropocentric Feature:** Astrocartography Station — a survey complex uses the stable orbital geometry to map distant systems.
- **Observed from Space:** A dark polar superstorm is large enough to be visible from the system's outer edge on good instruments.
- **Planetside Feature:** Crystalline rain falls through floating mineral aerosols in the habitable cloud band.
- **Life:** Diverse — buoyant ribbonlike organisms migrate along thermal currents.

### Planetary Data

- **Primary:** F5 V
- **Orbital Radius:** 4.50 AU
- **Local Year:** 8.07u
- **Mean Radius:** 61,000 km
- **Surface Gravity:** 2.00 g @ 1 bar
- **Mean Surface Temp:** −120 °C cloud tops

### Thermal Survey

Infrared survey shows warm upwellings wrapped around the permanent polar cyclone and migrating heat traces from large airborne organisms in the temperate cloud layers.

### Surface Survey

Atmospheric survey reveals luminous cloud bands, crystalline precipitation, floating mineral aerosols, and scientific aerostats skirting the black polar storm.

## 29. Vesper

- **Slug:** `vesper`
- **Scan Tagline:** Four climates under two suns.
- **Planet Type:** Vital World
- **Description:** Two suns illuminate a densely inhabited world of violently contrasting biomes. Orbital imaging shows desert, rainforest, tundra, and inland sea meeting across abrupt boundaries beneath a sprawling metropolitan belt.
- **Atmosphere:** Ideal
- **Natural Feature:** Under Twin Suns — the binary primary produces long, complex day-night cycles.
- **Settlements:** Multiple planetside settlements dominated by one enormous metropolitan region.
- **Settlement Summary:** Metroswathe
- **Anthropocentric Feature:** Metroswathe — billions inhabit a continuous urban corridor crossing several climate zones.
- **Observed from Space:** Vibrantly colored landscapes produce sharp bands visible from orbit.
- **Planetside Feature:** Biomes meet in abrupt, chaotic boundaries with little transitional terrain.
- **Life:** Diverse

### Planetary Data

- **Primary:** G8 V + K2 V binary
- **Orbital Radius:** 1.45 AU circumbinary
- **Local Year:** 1.36u
- **Mean Radius:** 7,100 km
- **Surface Gravity:** 1.06 g
- **Mean Surface Temp:** 22 °C

### Thermal Survey

Thermal imaging shows unusually abrupt temperature boundaries between neighboring biomes, with the metroswathe forming a bright inhabited belt across several climate zones.

### Surface Survey

Survey imagery shows desert, rainforest, tundra, and inland sea meeting across hard ecological boundaries beneath a complex double-sun sky.

## 30. Nix

- **Slug:** `nix`
- **Scan Tagline:** The moon that takes the hits.
- **Planet Type:** Icy Impact-Buffer Moon
- **Description:** This marginally habitable moon intercepts a steady stream of debris that would otherwise strike its parent giant. Settlements are buried beneath mobile pack ice, and local seismology is complicated by both tectonics and fresh impacts.
- **Atmosphere:** Marginal
- **Natural Feature:** Active Tectonics — tidal flexing keeps the moon geologically restless beneath its frozen crust.
- **Settlements:** Multiple stable subsurface settlements linked by tunnels and under-ice transit.
- **Settlement Summary:** Subsurface Settlements
- **Anthropocentric Feature:** Stable Settlement — several generations now regard the buried ice cities as home.
- **Observed from Space:** Fresh impact plumes and captured debris create a faint, constantly renewed dust wake.
- **Planetside Feature:** Shattered plains of pack ice drift over a warmer subsurface ocean.
- **Life:** Bountiful — the under-ice sea supports dense chemosynthetic ecosystems.

### Planetary Data

- **Primary:** G7 V
- **Orbital Radius:** 6.40 AU stellar / 620,000 km from parent
- **Local Year:** 17.07u
- **Mean Radius:** 3,100 km
- **Surface Gravity:** 0.36 g
- **Mean Surface Temp:** −95 °C

### Thermal Survey

Infrared scans show tidal heating beneath the fractured ice, with strong warm bands under the largest settlements and along active under-ice ridges.

### Surface Survey

Survey imagery shows fresh impact plumes, drifting pack ice, buried access towers, and a dusty debris wake continually renewed by intercepted objects.

## 31. Larkspur

- **Slug:** `larkspur`
- **Scan Tagline:** A quiet coastal world with more buried history than its population knows.
- **Planet Type:** Temperate Archipelago World
- **Description:** Larkspur is a breathable, lightly populated world of forested continents, shallow inland seas, long island chains, and broad stretches of unsettled interior. Most habitation follows old coastal roads and river valleys around Greyhaven, the planet's only major starport. The Aster Compact maintained the Ravelin Training and Security Center well outside the main population belt. Much of the world remains only lightly surveyed, leaving isolated settlements, abandoned infrastructure, and older subsurface sites scattered beyond routine traffic.
- **Atmosphere:** Breathable
- **Natural Feature:** Remote — Larkspur lies away from major shipping routes, and most offworld traffic exists because of Greyhaven Starport and the former Compact security presence.
- **Settlements:** Greyhaven serves as the primary port and administrative center. Smaller towns include Bellweather, Marrowfield, and Northwatch, with additional farming, fishing, and service communities spread along the coast and interior road network.
- **Settlement Summary:** Sparse Settlements
- **Anthropocentric Feature:** Ravelin Training and Security Center — a Compact pilot-training, security, and logistics installation located beyond the main civilian population belt.
- **Observed from Space:** Green coastal belts and island chains divide broad blue seas, with only a few concentrated night-side population clusters.
- **Planetside Feature:** Black basalt headlands, forested ridges, sea caves, and abandoned survey roads make large regions difficult to monitor from the ground.
- **Life:** Diverse — temperate forests, wetlands, coastal shallows, and open grasslands support a mature biosphere.

### Planetary Data

- **Primary:** G8 V
- **Orbital Radius:** 0.96 AU
- **Local Year:** 1.00u
- **Mean Radius:** 6,480 km
- **Surface Gravity:** 1.00 g
- **Mean Surface Temp:** 17 °C

### Thermal Survey

Infrared mapping shows a mild global profile with concentrated artificial heat around Greyhaven and smaller signatures at the scattered towns. Ravelin appears as a distinct but isolated installation. The island chains southeast of Eider Point show little modern activity despite extensive subsurface voids and old engineered cavities.

### Surface Survey

Low-altitude survey imagery shows forested coastal roads, small town clusters, river crossings, abandoned training ranges, and chains of basalt islands cut by caves and narrow beaches.
