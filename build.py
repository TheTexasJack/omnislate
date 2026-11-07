#!/usr/bin/env python3
"""OMNISLATE: build self-contained session files for the table display.

Usage:
    python3 build.py                         pick a campaign from a menu
    python3 build.py errans-inter-astra      build every chapter in one campaign
    python3 build.py errans-inter-astra/remnant
                                             build one chapter
    python3 build.py campaigns/errans-inter-astra/halas/sessions/tlc-session-2.md
                                             build one session
    python3 build.py --all                   build every campaign

Each campaign lives in campaigns/<name>/.  A campaign can hold chapters:
any subfolder with its own campaign.md (folders starting with _ are skipped).
Chapters inherit the campaign's settings, worlds, briefs, images, sounds, and
media, and override whatever they set themselves.  Finished files land in
dist/<campaign>/<chapter>/ together with the media, so that one folder is all
the tablet needs.

Pillow (sudo apt install python3-pil) handles images.  Without it the
build still works, but images go in unconverted and map poles are not fixed.
"""
import base64
import datetime
import difflib
import hashlib
import html
import io
import json
import math
import re
import shutil
import sys
import traceback
from pathlib import Path

ENGINE = "3.6.3"
ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "app" / "display.html"
LIBRARY = ROOT / "library"
CAMPAIGNS = ROOT / "campaigns"
DIST = ROOT / "dist"

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


class BuildError(Exception):
    """A problem the GM can fix.  The message is shown as is, so keep it plain."""


def hint(name, options):
    m = difflib.get_close_matches(name, list(options), n=1, cutoff=0.6)
    return f"  Did you mean '{m[0]}'?" if m else ""


def rel(path):
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------- worlds

FIELDS = {
    "Slug": "slug",
    "Scan Tagline": "tagline",
    "Planet Type": "type",
    "Scan Class": "scanClass",
    "Description": "description",
    "Atmosphere": "atmosphere",
    "Natural Feature": "natural",
    "Settlements": "settlements",
    "Settlement Summary": "settlementSummary",
    "Anthropocentric Feature": "anthro",
    "Observed from Space": "observed",
    "Planetside Feature": "planetside",
    "Life": "life",
    "Moons": "moons",
    "Rings": "rings",
    "Primary": "primary",
    "Orbital Radius": "orbit",
    "Local Year": "year",
    "Mean Radius": "radius",
    "Surface Gravity": "gravity",
    "Mean Surface Temp": "temp",
}
SECTIONS = {"Thermal Survey": "thermal", "Surface Survey": "surface"}
FIELD_SECTIONS = {"Planetary Data"}
OPTIONAL = {"scanClass", "moons", "rings"}
REQUIRED = [k for k in FIELDS.values() if k not in OPTIONAL] + list(SECTIONS.values())
ALL_KEYS = list(FIELDS.values()) + list(SECTIONS.values())
LABEL_OF = {v: k for k, v in list(FIELDS.items()) + list(SECTIONS.items())}

DEPTHS = ["long range", "orbital", "planetside"]
DEPTH_KEYS = {
    "long range": {"slug", "tagline", "type", "scanClass", "atmosphere", "primary", "orbit",
                   "year", "radius", "gravity", "temp", "observed", "thermal", "moons", "rings"},
    "orbital": {"description", "natural", "settlements", "settlementSummary",
                "anthro", "surface"},
    "planetside": {"planetside", "life"},
}

IMAGE_SLOTS = {
    "map": "slug",
    "planet": "slug",
    "thermal": "thermal",
    "surface": "surface",
    "observed": "observed",
    "description": "description",
    "natural": "natural",
    "settlement": "settlements",
    "anthropocentric": "anthro",
    "planetside": "planetside",
    "life": "life",
}
IMAGE_EXTS = (".webp", ".png", ".jpg", ".jpeg")


def parse_worlds(path):
    """Read a worlds file.  Only structural problems stop the build.  Everything else becomes a warning."""
    text = path.read_text(encoding="utf-8")
    # HTML comments (the NEW WORLD TEMPLATE) are blanked out, keeping line numbers intact.
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    worlds = []
    current = None
    section = None
    skipping = False
    heading = re.compile(r"^## (\d+)\.\s+(.+?)\s*$")
    field = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        m = heading.match(line)
        if m:
            current = {"number": m.group(1), "name": m.group(2), "line": lineno, "warnings": []}
            section = None
            skipping = False
            worlds.append(current)
            continue
        if line.startswith("## "):
            current = None
            continue
        if current is None:
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            section = SECTIONS.get(title)
            # Unknown ### sections are GM notes.  They are skipped and never reach a session file.
            skipping = section is None and title not in FIELD_SECTIONS
            continue
        if skipping:
            continue
        m = field.match(line)
        if m:
            label, value = m.group(1), m.group(2).strip()
            key = FIELDS.get(label)
            if key is None:
                current["warnings"].append(f"line {lineno}: '{label}' is not a world field, so it was skipped."
                                           f"{hint(label, FIELDS)}")
                continue
            if key in current:
                current["warnings"].append(f"line {lineno}: '{label}' appears twice.  The first one is used.")
                continue
            current[key] = value.strip("`").strip()
            continue
        if section and line.strip():
            prev = current.get(section, "")
            current[section] = (prev + " " + line.strip()).strip()
    by_slug = {}
    for w in worlds:
        slug = w.get("slug", "")
        if not slug:
            raise BuildError(f"{rel(path)} line {w['line']}: {w['name']} has no Slug line.  "
                             "Every world needs one, for example: - **Slug:** `kestrel`")
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", slug):
            raise BuildError(f"{rel(path)}: {w['name']} has slug '{slug}'.  "
                             "Slugs use lowercase letters, numbers, and dashes only.")
        if slug in by_slug:
            raise BuildError(f"{rel(path)}: two worlds use the slug '{slug}'.")
        w["source"] = path
        by_slug[slug] = w
    return by_slug


def load_worlds(dirs):
    """Shared pool first, then the campaign, then the chapter.  Later files win on the same slug."""
    worlds = {}
    for f in [LIBRARY / "worlds.md"] + [d / "worlds.md" for d in dirs]:
        if f.exists():
            worlds.update(parse_worlds(f))
    return worlds


# ---------------------------------------------------------------- deep scan

GLITCHES = {
    "interference": "INTERFERENCE",
    "too distant": "TOO DISTANT",
    "bad scan": "BAD SCAN: RESAMPLE",
    "no return": "NO RETURN",
    "signal degraded": "SIGNAL DEGRADED",
}
SCAN_CLASSES = ("terrestrial", "ocean", "ice", "desert", "furnace", "barren", "tainted", "grave", "jovian", "shattered")
CLASS_WORDS = [
    ("jovian", ("jovian", "gas giant", "giant")),
    ("shattered", ("shatter", "crack", "dying", "fragment", "debris")),
    ("grave", ("grave", "dead", "gamma", "scoured", "necro", "ruin")),
    ("ice", ("ice", "icy", "frozen", "glacial", "snow")),
    ("ocean", ("ocean", "sea", "flood", "archipelago", "water", "aquatic")),
    ("desert", ("desert", "dune", "dry", "arid", "sand")),
    ("furnace", ("furnace", "lava", "volcan", "burn", "magma", "inferno")),
    ("tainted", ("tainted", "toxic", "choked", "fungal", "spore", "inhospitable")),
    ("barren", ("rocky", "barren", "airless", "symmetry", "asteroid", "stone")),
    ("terrestrial", ("vital", "temperate", "garden", "biosphere", "forest", "terrestrial", "old-growth", "jungle")),
]
ATMO_WORDS = [("breathable", "breathable"), ("ideal", "ideal"), ("marginal", "marginal"), ("toxic", "toxic"),
              ("corrosive", "corrosive"), ("none", "none"), ("thin", "none"), ("vacuum", "none")]
ATMO_LIST = "Breathable, Ideal, Marginal, Toxic, Corrosive, None / thin"
LIFE_WORDS = [("none detected", "none"), ("none", "none"), ("extinct", "extinct"), ("scarce", "scarce"),
              ("diverse", "diverse"), ("bountiful", "bountiful"), ("overrun", "overrun")]
LIFE_LIST = "None detected, Extinct, Scarce, Diverse, Bountiful, Overrun"
STAR_ORDER = "OBAFGKM"
STAR_LUM = [(0, 1e6), (10, 2e4), (20, 40), (30, 6.0), (40, 1.4), (42, 1.0), (50, 0.45), (55, 0.16),
            (60, 0.07), (65, 0.01), (69, 0.0015)]
STAR_COLOR = {"O": "#9fb6ff", "B": "#b4c8ff", "A": "#e6edff", "F": "#fff4d6", "G": "#ffe08a", "K": "#ffb35c", "M": "#ff7a4a"}


def seeded(slug, salt):
    return int(hashlib.md5(f"{slug}:{salt}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


def lead_word(text, words):
    low = text.lower().lstrip()
    for word, key in words:
        if low.startswith(word):
            return key
    return None


def first_number(text):
    t = text.replace("−", "-").replace("–", "-")
    m = re.search(r"(-?)\s*(\d[\d,]*(?:\.\d+)?)", t)
    if not m:
        return None
    try:
        return float(m.group(2).replace(",", "")) * (-1 if m.group(1) else 1)
    except ValueError:
        return None


def star_lum(cls, sub):
    idx = STAR_ORDER.index(cls) * 10 + sub
    for (a, la), (b, lb) in zip(STAR_LUM, STAR_LUM[1:]):
        if a <= idx <= b:
            t = (idx - a) / (b - a)
            return 10 ** (math.log10(la) + t * (math.log10(lb) - math.log10(la)))
    return STAR_LUM[-1][1]


def parse_stars(text):
    stars = []
    for cls, sub, lc in re.findall(r"\b([OBAFGKM])(\d(?:\.\d)?)?\s*(Ia|Ib|III|II|IV|VI|V|I)?\b", text):
        s = float(sub) if sub else 5.0
        stars.append({"cls": cls, "sub": s, "lc": lc or "V", "color": STAR_COLOR[cls], "lum": round(star_lum(cls, s), 4)})
    return stars


def guess_class(type_text):
    low = (type_text or "").lower()
    for cls, words in CLASS_WORDS:
        if any(w in low for w in words):
            return cls
    return None


def scan_world(src, allowed):
    """Gate a world by scan depth and turn bad data into in-fiction glitches.

    Returns (fields, glitch, deep, warnings).  Only values inside the allowed depth
    are ever read, so derived numbers cannot leak anything held back.
    """
    slug = src["slug"]
    warnings = list(src.get("warnings", []))
    fields, glitch = {}, {}
    for key in ALL_KEYS:
        if key not in allowed:
            if key not in OPTIONAL:
                glitch[key] = GLITCHES["too distant"]
            continue
        raw = src.get(key)
        if raw is None or raw == "":
            if key not in OPTIONAL:
                glitch[key] = GLITCHES["no return"]
                warnings.append(f"{LABEL_OF[key]} is missing.  The table shows NO RETURN.")
            continue
        token = re.fullmatch(r"\[\s*([a-z ]+?)\s*\]", raw.strip().lower())
        if token and token.group(1) in GLITCHES:
            glitch[key] = GLITCHES[token.group(1)]
            continue
        fields[key] = raw

    def bad(key, label, why):
        fields.pop(key, None)
        glitch[key] = label
        warnings.append(why)

    deep = {"seed": slug}

    # Leading words that drive the hazard flags and the halo.
    if "atmosphere" in fields:
        k = lead_word(fields["atmosphere"], ATMO_WORDS)
        if k:
            deep["atmo"] = k
        else:
            first = fields["atmosphere"].split()[0] if fields["atmosphere"].split() else ""
            bad("atmosphere", GLITCHES["bad scan"], f"Atmosphere starts with '{first}'.  Start it with one of: {ATMO_LIST}."
                f"{hint(first.capitalize(), ['Breathable', 'Ideal', 'Marginal', 'Toxic', 'Corrosive', 'None'])}  "
                "The table shows BAD SCAN: RESAMPLE.")
    if "life" in fields:
        k = lead_word(fields["life"], LIFE_WORDS)
        if k:
            deep["life"] = k
        else:
            first = fields["life"].split()[0] if fields["life"].split() else ""
            bad("life", GLITCHES["bad scan"], f"Life starts with '{first}'.  Start it with one of: {LIFE_LIST}."
                f"{hint(first.capitalize(), ['None', 'Extinct', 'Scarce', 'Diverse', 'Bountiful', 'Overrun'])}  "
                "The table shows BAD SCAN: RESAMPLE.")

    # Numbers.
    for key, out in (("radius", "radius"), ("gravity", "gravity"), ("temp", "temp"), ("year", "year")):
        if key in fields:
            v = first_number(fields[key])
            if v is None:
                bad(key, GLITCHES["interference"], f"{LABEL_OF[key]} '{fields.get(key, '')}' has no number in it.  "
                    "The table shows INTERFERENCE.")
            else:
                deep[out] = v
    if "gravity" in fields and "@" in fields["gravity"]:
        deep["gravityRef"] = fields["gravity"].split("@", 1)[1].strip()
    if "temp" in fields and "cloud" in fields["temp"].lower():
        deep["tempRef"] = "cloud tops"
    if "orbit" in fields:
        o = fields["orbit"]
        v = first_number(o)
        if v is None:
            bad("orbit", GLITCHES["interference"], f"Orbital Radius '{o}' has no number in it.  The table shows INTERFERENCE.")
        else:
            deep["orbit"] = v
            if "parent" in o.lower():
                deep["moonOf"] = True
                parts = re.split(r"/", o)
                if len(parts) > 1:
                    pk = first_number(parts[1])
                    if pk is not None:
                        deep["parentKm"] = pk
            if "circumbinary" in o.lower():
                deep["circumbinary"] = True
    if "primary" in fields:
        stars = parse_stars(fields["primary"])
        if stars:
            deep["stars"] = stars
            lum = sum(s["lum"] for s in stars)
            deep["hz"] = [round(math.sqrt(lum / 1.1), 3), round(math.sqrt(lum / 0.53), 3)]
        else:
            bad("primary", GLITCHES["interference"], f"Primary '{fields['primary']}' has no star class in it (such as G4 V).  "
                "The table shows INTERFERENCE.")

    # Scan class: explicit wins, then a guess from Planet Type.
    cls = None
    if "scanClass" in fields:
        c = fields["scanClass"].lower().strip()
        if c in SCAN_CLASSES:
            cls = c
        else:
            warnings.append(f"Scan Class '{fields['scanClass']}' is not one of: {', '.join(SCAN_CLASSES)}."
                            f"{hint(c, SCAN_CLASSES)}  The wireframe shows SIGNAL DEGRADED.")
            deep["degraded"] = True
        fields.pop("scanClass", None)
    if not cls and not deep.get("degraded"):
        cls = guess_class(fields.get("type"))
        if not cls and "type" in fields:
            warnings.append(f"Planet Type '{fields['type']}' does not suggest a Scan Class.  Add a Scan Class line.  "
                            "The wireframe shows SIGNAL DEGRADED.")
            deep["degraded"] = True
    deep["cls"] = cls
    if "moonOf" not in deep and "moon" in (fields.get("type") or "").lower():
        deep["moonOf"] = True

    # Text that is visible at this depth, for keyword flags.
    seen = " ".join(fields.get(k, "") for k in ("type", "tagline", "description", "natural", "observed",
                                                "planetside", "settlements", "thermal", "surface", "life")).lower()

    # Moons and rings: explicit wins, then keywords in visible text, then the seed.
    if "moons" in fields:
        v = first_number(fields.pop("moons"))
        if v is None:
            warnings.append("Moons should be a number.  The table shows NO RETURN.")
            glitch["moons"] = GLITCHES["no return"]
        else:
            deep["moons"] = int(max(0, v))
    else:
        if "royal court" in seen or "numerous moons" in seen or "dozens of small moons" in seen:
            deep["moons"] = 7
        elif re.search(r"\b(huge|large|broken|dominant|single) moon\b", seen):
            deep["moons"] = 1
        else:
            r = seeded(slug, "moons")
            deep["moons"] = int(3 + r * 4) if cls == "jovian" else (0 if deep.get("moonOf") else int(r * 2.6))
    if "rings" in fields:
        deep["rings"] = fields.pop("rings").strip().lower() in ("yes", "y", "true", "1", "ringed")
    else:
        deep["rings"] = bool(re.search(r"\bring(ed|s| system)\b", seen))
    deep["tilt"] = round(4 + seeded(slug, "tilt") * 28, 1)

    # Settlement signatures from the summary (orbital depth and deeper).
    s = (fields.get("settlementSummary") or "").lower()
    if "settlementSummary" in fields:
        if "abandon" in s or s.strip() in ("none", "none detected"):
            level = 0
        elif "metro" in s:
            level = 4
        elif any(w in s for w in ("multiple", "network", "arcolog", "subsurface", "military")):
            level = 3
        elif any(w in s for w in ("sparse", "colony", "settlement", "quarantin", "planetside", "new")):
            level = 2
        else:
            level = 1
        deep["settle"] = level
        deep["abandoned"] = "abandon" in s
        deep["orbitalOnly"] = any(w in s for w in ("orbital", "aerostat", "station")) and level <= 1

    # Hazard flags.
    hz = []
    atmo = deep.get("atmo")
    if atmo in ("toxic", "corrosive"):
        hz.append(f"{atmo.upper()} ATMOSPHERE")
    elif atmo == "none":
        hz.append("VACUUM OR TRACE ATMOSPHERE")
    elif atmo == "marginal":
        hz.append("MARGINAL ATMOSPHERE")
    t = deep.get("temp")
    if t is not None and deep.get("tempRef") is None:
        if t <= -60:
            hz.append("EXTREME COLD")
        elif t >= 60:
            hz.append("EXTREME HEAT")
    g = deep.get("gravity")
    if g is not None and cls != "jovian":
        if g >= 1.5:
            hz.append("HIGH GRAVITY")
        elif g <= 0.4:
            hz.append("LOW GRAVITY")
    if cls == "jovian":
        hz.append("NO SOLID SURFACE")
    for words, flag in ((("radiat", "radioactive", "irradiat", "gamma"), "RADIATION"),
                        (("quarantin",), "QUARANTINE"),
                        (("seismic", "earthquake", "tectonic", "fault"), "SEISMIC ACTIVITY"),
                        (("volcan", "lava", "caldera"), "VOLCANISM"),
                        (("superstorm", "cyclone", "blizzard", "lightning", "electrical storm", "ash storm", "100-year storm", "storm system", "flash flood"), "SEVERE WEATHER"),
                        (("spore", "hallucinogen"), "BIOLOGICAL AEROSOLS"),
                        (("debris", "impact plume", "meteor"), "DEBRIS FIELD"),
                        (("restrict", "prohibit", "exclusion"), "RESTRICTED APPROACH")):
        if any(w in seen for w in words):
            hz.append(flag)
    deep["hazards"] = hz

    # Derived estimates.
    r, g = deep.get("radius"), deep.get("gravity")
    if r is not None and g is not None and r > 0 and g > 0:
        deep["vesc"] = round(11.186 * math.sqrt(g * r / 6371), 1)
        if cls != "jovian":
            deep["density"] = round(g / (r / 6371), 2)
    if cls == "jovian":
        deep["hab"] = 0
    elif atmo and t is not None and g is not None:
        a = {"breathable": 1, "ideal": 1, "marginal": .55, "toxic": .2, "corrosive": .1, "none": .05}[atmo]
        tt = 1 if -10 <= t <= 35 else max(0, 1 - (abs(t - 12.5) - 22.5) / 70)
        gg = 1 if 0.6 <= g <= 1.3 else max(0, 1 - (min(abs(g - 0.6), abs(g - 1.3))) / 1.0)
        lf = {"none": .85, "extinct": .8, "scarce": .9, "diverse": 1, "bountiful": 1, "overrun": .85}.get(deep.get("life"), 1)
        deep["hab"] = int(round(100 * a * tt * gg * lf))
        deep["habPartial"] = "life" not in deep
    if deep.get("hz") and deep.get("orbit") is not None and not deep.get("moonOf"):
        lo, hi = deep["hz"]
        deep["zone"] = "inside" if deep["orbit"] < lo else ("outside" if deep["orbit"] > hi else "within")
    return fields, glitch, deep, warnings


# ---------------------------------------------------------------- briefs

BRIEF_FIELDS = {"Title": "title", "Type": "type", "Location": "location",
                "Issued By": "issued", "World": "world"}


def parse_briefs(folder):
    briefs = {}
    if not folder.is_dir():
        return briefs
    head = re.compile(r"^## ([a-z0-9][a-z0-9-]*)\s*$")
    field = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
    for path in sorted(folder.glob("*.md")):
        cur = None
        sec = None
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.rstrip()
            m = head.match(line)
            if m:
                bid = m.group(1)
                if bid in briefs:
                    raise BuildError(f"{rel(path)} line {lineno}: the brief id '{bid}' is used twice.")
                cur = {"id": bid, "sections": []}
                sec = None
                briefs[bid] = cur
                continue
            if line.startswith("## ") or line.startswith("# "):
                cur = None
                continue
            if cur is None or not line.strip():
                continue
            if line.startswith("### "):
                sec = {"title": line[4:].strip(), "items": []}
                cur["sections"].append(sec)
                continue
            m = field.match(line)
            if m and sec is None:
                label = m.group(1)
                if label not in BRIEF_FIELDS:
                    raise BuildError(f"{rel(path)} line {lineno}: '{label}' is not a brief field.  "
                                     f"Use {', '.join(BRIEF_FIELDS)}.{hint(label, BRIEF_FIELDS)}")
                cur[BRIEF_FIELDS[label]] = m.group(2).strip()
                continue
            if sec is None:
                continue
            if line.lstrip().startswith("- "):
                sec["items"].append({"t": "li", "text": line.lstrip()[2:].strip()})
            else:
                sec["items"].append({"t": "p", "text": line.strip()})
    for b in briefs.values():
        if not b.get("title"):
            raise BuildError(f"Brief '{b['id']}' has no Title line.")
    return briefs


# ---------------------------------------------------------------- campaign.md

STYLES = ("institutional", "military")
TRIGGER_STYLES = ("attack", "reveal")
FUTURE_STYLES = ("hack", "transmission")
COLOR_KEYS = {
    "Background": "--bg", "Bar": "--bg2", "Panel": "--panel", "Panel Highlight": "--panel-hi",
    "Line": "--line", "Line Highlight": "--line-hi", "Text": "--text", "Dim Text": "--dim",
    "Accent": "--accent", "Alert Color": "--alert", "Boot Glow": "--boot-glow",
}
TOP_KEYS = ("Name", "Motto", "Crest", "Crest Text")
SKIN_KEYS = ("Style", "Network") + tuple(COLOR_KEYS)
TRIGGER_KEYS = ("Label", "Style", "Reveals", "Sound", "Lost Text", "Banner")
TAGS = {"red": "bad", "amber": "amb", "green": ""}


def tagged(text, where):
    m = re.match(r"^\[(\w+)\]\s*(.*)$", text)
    if not m:
        return ["", text]
    tag = m.group(1).lower()
    if tag not in TAGS:
        raise BuildError(f"{where}: '[{m.group(1)}]' is not a line color.  Use [red], [amber], or [green].")
    return [TAGS[tag], m.group(2)]


# ---------------------------------------------------------------- signals (ANDIS terminal)

SIGNAL_FIELDS = {"Program": "program", "Title": "title", "Time": "time", "Corruption": "corruption",
                 "Routes": "routes", "Penalty": "penalty", "Image": "image"}
PROGRAM_RE = re.compile(r"^[A-Z0-9][A-Z0-9 ]{0,15}$")


def clock_seconds(text):
    m = re.fullmatch(r"\s*(\d{1,3}):([0-5]\d):([0-5]\d)\s*", text or "")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) if m else None


def parse_signals(folder):
    """signals/*.md: '## id', fields, then '### Encoded' and '### Decoded' blocks kept line for line."""
    sigs = {}
    if not folder.is_dir():
        return sigs
    head = re.compile(r"^## ([a-z0-9][a-z0-9-]*)\s*$")
    field = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
    for path in sorted(folder.glob("*.md")):
        text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
        cur = sec = None
        for lineno, raw in enumerate(text.splitlines(), 1):
            line = raw.rstrip()
            m = head.match(line)
            if m:
                sid = m.group(1)
                if sid in sigs:
                    raise BuildError(f"{rel(path)} line {lineno}: the signal id '{sid}' is used twice.")
                cur = {"id": sid, "where": f"{rel(path)} line {lineno}", "encoded": [], "decoded": [], "attachments": []}
                sigs[sid] = cur
                sec = None
                continue
            if line.startswith("## ") or line.startswith("# "):
                cur = sec = None
                continue
            if cur is None:
                continue
            if line.startswith("### "):
                name = line[4:].strip().lower()
                if name not in ("encoded", "decoded", "attachments"):
                    raise BuildError(f"{rel(path)} line {lineno}: '### {line[4:].strip()}' is not a signal section.  "
                                     "Use ### Encoded, ### Decoded, and ### Attachments.")
                sec = name
                continue
            if sec is None:
                if not line.strip():
                    continue
                m = field.match(line)
                if not m:
                    continue
                label = m.group(1).strip().title()
                if label not in SIGNAL_FIELDS:
                    raise BuildError(f"{rel(path)} line {lineno}: '{m.group(1)}' is not a signal field.  "
                                     f"Use {', '.join(SIGNAL_FIELDS)}.{hint(label, SIGNAL_FIELDS)}")
                cur[SIGNAL_FIELDS[label]] = m.group(2).strip()
                continue
            cur[sec].append((line, f"{rel(path)} line {lineno}"))
    for sig in sigs.values():
        sig["source"] = folder
    return sigs


def merged_signals(dirs):
    sigs = {}
    for d in dirs:
        sigs.update(parse_signals(d / "signals"))
    return sigs


ATTACH_KIND = {".png": "I", ".jpg": "I", ".jpeg": "I", ".webp": "I", ".md": "T", ".txt": "T",
               ".mp3": "A", ".wav": "A", ".ogg": "A", ".m4a": "A", ".mp4": "V", ".webm": "V"}
AUDIO_WARN_BYTES = 5 * 1024 * 1024


def color_lines(lines):
    out = []
    for t in lines:
        m = re.match(r"^\[(red|amber|green)\]\s?(.*)$", t, re.I)
        out.append([TAGS[m.group(1).lower()], m.group(2)] if m else ["", t])
    return out


def parse_attachments(sig, file_dirs, image_dirs, warns, media_dirs=(), sound_dirs=()):
    """'- NAME: print', '- NAME: file.png | caption', '- NAME:' with indented items below it for a folder."""
    out, folder = [], None
    top = re.compile(r"^- (.+?):\s*(.*)$")
    sub = re.compile(r"^\s{2,}- (.+?):\s*(.*)$")

    def item(name, value, where):
        name = name.strip().upper()[:16]
        value, _, caption = value.partition("|")
        value, caption = value.strip(), caption.strip()
        if value.lower() == "print":
            return {"name": name, "kind": "D"}
        ext = Path(value).suffix.lower()
        if ext not in ATTACH_KIND:
            warns.append(f"attachment {name} ({where}): '{value}' is not 'print' or a picture, text, audio, or video file, "
                         "so it is left out")
            return None
        kind = ATTACH_KIND[ext]
        dirs = {"I": image_dirs + file_dirs, "A": file_dirs + list(sound_dirs), "V": list(media_dirs)}.get(kind, file_dirs)
        p = next((d / value for d in dirs if (d / value).exists()), None)
        if not p:
            where_to = {"I": "images/ or signals/", "A": "signals/ or sounds/", "V": "media/"}.get(kind, "signals/")
            warns.append(f"attachment {name}: '{value}' was not found in {where_to}, so it is left out")
            return None
        a = {"name": name, "kind": kind, "caption": caption}
        if kind == "I":
            a["image"] = encode_image(p, "still")
        elif kind == "A":
            size = p.stat().st_size
            if size > AUDIO_WARN_BYTES:
                warns.append(f"attachment {name}: '{value}' is {size // (1024 * 1024)} MB, which makes the session file heavy.  "
                             "A shorter or lower-bitrate clip loads faster on the tablet")
            mime = SOUND_MIME.get(ext, "audio/mpeg")
            a["audio"] = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
            if "loop" in p.name.lower(): a["loop"] = True   # 3.6.2: *loop* files repeat
            tp = p.with_suffix(".txt")
            if tp.exists():
                a["transcript"] = color_lines([t.rstrip() for t in tp.read_text(encoding="utf-8").splitlines() if t.strip()])
        elif kind == "V":
            a["video"] = value
        else:
            text = re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf-8"), flags=re.S).splitlines()
            while text and not text[0].strip():
                text = text[1:]
            a["text"] = color_lines([t.rstrip() for t in text])
        return a

    for line, where in sig["attachments"]:
        if not line.strip():
            continue
        m = sub.match(line)
        if m:
            if folder is None:
                raise BuildError(f"{where}: an indented attachment needs a folder line above it, such as '- INCIDENTS:'.")
            if not m.group(2).strip():
                raise BuildError(f"{where}: folders can only go one level deep.  Give '{m.group(1)}' a file or 'print'.")
            a = item(m.group(1), m.group(2), where)
            if a:
                folder["items"].append(a)
            continue
        m = top.match(line)
        if not m:
            raise BuildError(f"{where}: attachments look like '- NAME: print' or '- NAME: file.png'.  Found '{line.strip()}'.")
        if not m.group(2).strip():
            folder = {"name": m.group(1).strip().upper()[:16], "kind": "M", "items": []}
            out.append(folder)
            continue
        folder = None
        a = item(m.group(1), m.group(2), where)
        if a:
            out.append(a)
    for a in out:
        if a["kind"] == "M" and not a["items"]:
            warns.append(f"attachment folder {a['name']} is empty")
    return [a for a in out if a["kind"] != "M" or a["items"]]


def finish_signal(sig, start, image_dirs, report, file_dirs=(), media_dirs=(), sound_dirs=()):
    """Check one signal and shape it for the page."""
    where = sig["where"]
    prog = (sig.get("program") or "").strip().upper()
    if not prog:
        raise BuildError(f"{where}: signal '{sig['id']}' needs a Program line, the name players type in LOAD \"NAME\",8,1.")
    if not PROGRAM_RE.match(prog):
        raise BuildError(f"{where}: Program '{sig['program']}' can only use letters, numbers, and spaces (16 at most), "
                         "because that is all the ANDIS keyboard has.")
    warns = []
    secs = clock_seconds(sig.get("time"))
    if secs is None:
        if sig.get("time"):
            warns.append(f"Time '{sig['time']}' is not HH:MM:SS, so it uses 01:00:00")
        secs = 3600
    pen = clock_seconds(sig.get("penalty") or "00:05:00")
    if pen is None:
        warns.append(f"Penalty '{sig['penalty']}' is not HH:MM:SS, so it uses 00:05:00")
        pen = 300
    try:
        corr = float((sig.get("corruption") or "100").rstrip("%"))
        corr = max(0.0, min(100.0, corr))
    except ValueError:
        warns.append(f"Corruption '{sig['corruption']}' is not a number, so it uses 100")
        corr = 100.0
    try:
        routes = int(sig.get("routes") if sig.get("routes") not in (None, "") else 3)
        routes = 0 if routes <= 0 else max(2, min(5, routes))
    except ValueError:
        warns.append(f"Routes '{sig['routes']}' is not a number, so it uses 3")
        routes = 3

    def block(lines):
        while lines and not lines[0][0].strip():
            lines = lines[1:]
        while lines and not lines[-1][0].strip():
            lines = lines[:-1]
        out = []
        for t, w in lines:
            m = re.match(r"^\[(red|amber|green)\]\s?(.*)$", t, re.I)
            out.append([TAGS[m.group(1).lower()], m.group(2)] if m else ["", t])
        return out
    enc, dec = block(sig["encoded"]), block(sig["decoded"])
    if not dec:
        raise BuildError(f"{where}: signal '{sig['id']}' has no ### Decoded text.  That is what the players earn.")
    image, img_note = None, ""
    if sig.get("image"):
        p = next((d / sig["image"] for d in image_dirs if (d / sig["image"]).exists()), None)
        if p:
            image = encode_image(p, "still")
            img_note = f"  image: {sig['image']}"
        else:
            warns.append(f"image '{sig['image']}' was not found in images/, so the decode is text only")
    attachments = parse_attachments(sig, list(file_dirs), image_dirs, warns, media_dirs, sound_dirs)
    state = {"mode": start[0], "left": start[1]}
    when = {"fresh": "starts encoded", "decoded": "starts decoded", "running": f"resumes with {fmt_clock(start[1])} left"}[start[0]]
    report.append(f"    Signal   {sig['id']:<22} LOAD \"{prog}\"  {fmt_clock(secs)}  "
                  f"{str(routes) + ' routes' if routes else 'no routing'}  {when}{img_note}")
    if attachments:
        report.append("    Attach   " + "  ".join(f"[{a['kind']}] {a['name']}" + (f" ({len(a['items'])})" if a["kind"] == "M" else "")
                                          for a in attachments))
    for w in warns:
        report.append(f"    Warn     signal {sig['id']} ({where}): {w}")
    return {"id": sig["id"], "program": prog, "title": sig.get("title", ""), "time": secs, "penalty": pen,
            "corruption": corr, "routes": routes, "encoded": enc, "decoded": dec, "image": image, "start": state,
            "attachments": attachments}


def fmt_clock(secs):
    return f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}"


def hex_color(value, where):
    v = value.strip()
    if not re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v):
        raise BuildError(f"{where}: '{value}' is not a color.  Colors look like #c9a24a.")
    return v


def soft(color, alpha):
    c = color.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def parse_campaign_raw(folder):
    path = folder / "campaign.md"
    if not path.exists():
        raise BuildError(f"{rel(folder)} has no campaign.md.  Copy the one from campaigns/_starter.")
    top = {}
    skins = {"normal": {}, "alert": {}}
    skin_lines = {"normal": [], "alert": []}
    triggers = {}
    section = ("top", None)
    sub = None
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        where = f"{rel(path)} line {lineno}"
        if not line:
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            low = title.lower()
            sub = None
            if low in ("normal skin", "alert skin"):
                section = ("skin", low.split()[0])
            elif low.startswith("trigger:"):
                tid = title.split(":", 1)[1].strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", tid):
                    raise BuildError(f"{where}: trigger id '{tid}' should be lowercase letters, numbers, and dashes.")
                if tid in triggers:
                    raise BuildError(f"{where}: there are two triggers called '{tid}'.")
                triggers[tid] = {"id": tid, "lines": [], "line": lineno}
                section = ("trigger", tid)
            else:
                raise BuildError(f"{where}: unknown section '## {title}'.  "
                                 "Use '## Normal Skin', '## Alert Skin', or '## Trigger: some-id'.")
            continue
        if line.startswith("### "):
            title = line[4:].strip().lower()
            if section[0] == "trigger" and title == "lines":
                sub = triggers[section[1]]["lines"]
            elif section == ("skin", "alert") and title == "boot lines":
                sub = skin_lines["alert"]
            else:
                raise BuildError(f"{where}: '{line}' does not belong here.  "
                                 "'### Lines' goes under a trigger.  '### Boot Lines' goes under '## Alert Skin'.")
            continue
        if line.startswith("#"):
            continue
        if line.startswith("- "):
            if sub is None:
                raise BuildError(f"{where}: a '- ' list line needs a '### Lines' or '### Boot Lines' heading above it.")
            sub.append(tagged(line[2:].strip(), where))
            continue
        if ":" not in line:
            raise BuildError(f"{where}: expected 'Setting: value' and found '{line}'.")
        key, value = (x.strip() for x in line.split(":", 1))
        key = " ".join(w.capitalize() for w in key.split())
        kind, name = section
        allowed = {"top": TOP_KEYS, "skin": SKIN_KEYS, "trigger": TRIGGER_KEYS}[kind]
        if key not in allowed:
            label = {"top": "the top of campaign.md", "skin": f"the {name} skin", "trigger": f"trigger '{name}'"}[kind]
            raise BuildError(f"{where}: '{key}' is not a setting for {label}.{hint(key, allowed)}  "
                             f"Allowed: {', '.join(allowed)}.")
        target = top if kind == "top" else skins[name] if kind == "skin" else triggers[name]
        target[key] = value
        sub = None
    for t in triggers.values():
        t["where"] = f"{rel(path)} trigger '{t['id']}' (line {t['line']})"
    crest_dir = folder if "Crest" in top else None
    return {"top": top, "skins": skins, "bootLines": skin_lines["alert"], "triggers": triggers,
            "path": path, "crestDir": crest_dir}


def parse_campaign(target):
    """Merge campaign.md files from the campaign down to the chapter.  The chapter wins on anything it sets."""
    top, skins, boot, triggers, crest_dir, path = {}, {"normal": {}, "alert": {}}, [], {}, None, None
    for d in target["dirs"]:
        raw = parse_campaign_raw(d)
        top.update(raw["top"])
        for role in ("normal", "alert"):
            skins[role].update(raw["skins"][role])
        boot = raw["bootLines"] or boot
        triggers.update(raw["triggers"])
        crest_dir = raw["crestDir"] or crest_dir
        path = raw["path"]
    skin_lines = {"alert": boot}
    camp_id = target["id"]
    out = {"id": camp_id, "name": top.get("Name") or target["dirs"][-1].name.replace("-", " ").title(),
           "motto": top.get("Motto", ""), "crestFile": top.get("Crest", ""), "crestText": top.get("Crest Text", ""),
           "crestDir": crest_dir}
    defaults = {"normal": ("institutional", "Sensor Network"), "alert": ("military", "Sensor Suite: emergency mode")}
    for role in ("normal", "alert"):
        sk = skins[role]
        style = (sk.get("Style") or defaults[role][0]).lower()
        if style not in STYLES:
            raise BuildError(f"{rel(path)}: the {role} skin Style is '{sk.get('Style')}'.  Use institutional or military.")
        colors = {}
        for label, var in COLOR_KEYS.items():
            if sk.get(label):
                colors[var] = hex_color(sk[label], f"{rel(path)} ({role} skin, {label})")
        if "--accent" in colors:
            colors["--accent-soft"] = soft(colors["--accent"], .16)
        out[role] = {"style": style, "network": sk.get("Network") or defaults[role][1], "colors": colors}
    out["alert"]["bootLines"] = skin_lines["alert"] or [
        ["", out["alert"]["network"]], ["bad", "Primary network: no response"], ["amb", "Local sensor feed active"]]

    trig_out = {}
    for tid, t in triggers.items():
        where = t["where"]
        style = (t.get("Style") or "attack").lower()
        if style in FUTURE_STYLES:
            raise BuildError(f"{where}: the '{style}' style is planned but not built yet.  Use attack or reveal for now.")
        if style not in TRIGGER_STYLES:
            raise BuildError(f"{where}: Style is '{t.get('Style')}'.  Use attack or reveal.")
        sound = (t.get("Sound") or ("klaxon.mp3" if style == "attack" else "")).strip()
        lines = t["lines"] or ([["", out["alert"]["network"]], ["bad", "Primary network: no response"],
                                ["amb", "Switching to local sensor feed"], ["amb", "Priority message received"]]
                               if style == "attack" else [])
        trig_out[tid] = {
            "id": tid,
            "label": t.get("Label") or tid,
            "style": style,
            "reveals": [x.strip() for x in t.get("Reveals", "").split(",") if x.strip()],
            "sound": {"silent": True} if sound.lower() == "none" else ({"file": sound} if sound else {}),
            "lostText": t.get("Lost Text") or "Signal lost",
            "banner": t.get("Banner", ""),
            "lines": lines,
        }
    out["triggers"] = trig_out
    return out


# ---------------------------------------------------------------- crest

def sanitize_svg(text, path):
    s = re.sub(r"<\?xml.*?\?>", "", text, flags=re.S)
    s = re.sub(r"<!DOCTYPE.*?>", "", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()
    bad = re.search(r"<\s*(script|foreignObject|iframe|object|embed)\b|\son\w+\s*=|javascript:", s, re.I)
    if bad:
        raise BuildError(f"{rel(path)} contains '{bad.group(0).strip()}', which is not allowed in a crest.  "
                         "Export it as a plain SVG or use a PNG instead.")
    m = re.match(r"<svg\b([^>]*)>", s)
    if not m:
        raise BuildError(f"{rel(path)} does not look like an SVG file.")
    attrs = m.group(1)
    if "viewbox" not in attrs.lower():
        raise BuildError(f"{rel(path)} needs a viewBox so it can scale.  Most editors add one on export.")
    if not re.search(r'\bclass="[^"]*\bcrest\b', attrs):
        if re.search(r'\bclass="', attrs):
            attrs = re.sub(r'\bclass="', 'class="crest ', attrs, count=1)
        else:
            attrs = ' class="crest"' + attrs
        s = "<svg" + attrs + ">" + s[m.end():]
    return s


def generated_crest(name, motto, label):
    """A clean default emblem built from the campaign name and motto."""
    esc = html.escape
    text = (label or "".join(w[0] for w in re.findall(r"[A-Za-z0-9]+", name))[:4] or "OMNI").upper()
    size = 30 if len(text) <= 5 else max(16, int(150 / len(text)))
    top = esc(name.upper())
    bottom = esc(motto.upper()) if motto else ""
    ticks = "".join(
        f'<path d="M{120 + 96 * math.cos(math.radians(a)):.1f} {120 + 96 * math.sin(math.radians(a)):.1f}'
        f'L{120 + 102 * math.cos(math.radians(a)):.1f} {120 + 102 * math.sin(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 10))
    parts = [
        f'<svg class="crest" viewBox="0 0 240 240" role="img" aria-label="{esc(name)} crest">',
        '<circle class="line" cx="120" cy="120" r="114" stroke-width="3"/>',
        '<circle class="line" cx="120" cy="120" r="106" stroke-width="1.2"/>',
        '<circle class="line" cx="120" cy="120" r="78" stroke-width="1.2"/>',
        f'<g class="line" stroke-width="1">{ticks}</g>' if not bottom else "",
        '<path class="acf" d="M120 52l5 9h-10zM120 188l5-9h-10z"/>',
        '<path class="ac" stroke-width="1.6" d="M66 92L120 64L174 92M66 148L120 176L174 148"/>',
        '<path class="line" stroke-width="1.4" d="M48 101H192M48 139H192"/>',
        '<path class="acf" d="M48 120l4-4 4 4-4 4zM184 120l4-4 4 4-4 4z"/>',
        f'<text class="ink" x="120" y="{120 + size * 0.36:.1f}" text-anchor="middle" '
        f'font-family="Georgia,\'Noto Serif\',\'DejaVu Serif\',serif" font-size="{size}" letter-spacing="4">{esc(text)}</text>',
        '<defs><path id="crestTop" d="M21 120A99 99 0 0 1 219 120"/><path id="crestArc" d="M19 120A101 101 0 0 0 221 120"/></defs>',
        f'<text class="ink" font-family="Georgia,\'Noto Serif\',\'DejaVu Serif\',serif" font-size="12.5" letter-spacing="2.4">'
        f'<textPath href="#crestTop" startOffset="50%" text-anchor="middle">{top}</textPath></text>',
    ]
    if bottom:
        parts.append(f'<text class="ink" font-family="Georgia,\'Noto Serif\',\'DejaVu Serif\',serif" font-size="12.5" '
                     f'letter-spacing="2.4"><textPath href="#crestArc" startOffset="50%" text-anchor="middle">{bottom}</textPath></text>')
    parts.append("</svg>")
    return "\n".join(p for p in parts if p)


def crest_markup(info):
    f = info["crestFile"]
    if not f:
        return generated_crest(info["name"], info["motto"], info["crestText"]), "generated from Name and Motto"
    path = info["crestDir"] / f
    if not path.exists():
        raise BuildError(f"campaign.md says 'Crest: {f}' but {rel(path)} does not exist.  "
                         "Put the file in the campaign folder, or delete the Crest line to use a generated crest.")
    ext = path.suffix.lower()
    if ext == ".svg":
        return sanitize_svg(path.read_text(encoding="utf-8"), path), f"{f} (SVG)"
    if ext in IMAGE_EXTS:
        if HAVE_PIL:
            img = Image.open(path)
            img.load()
            img = img.convert("RGBA")
            img.thumbnail((800, 800), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, "WEBP", quality=90, method=5)
            uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
        else:
            mime = {".webp": "image/webp", ".png": "image/png"}.get(ext, "image/jpeg")
            uri = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
        return f'<img class="crest" src="{uri}" alt="{html.escape(info["name"])} crest">', f"{f} (image)"
    raise BuildError(f"Crest file {f} should be .svg, .png, .jpg, or .webp.")


# ---------------------------------------------------------------- images and sounds

def find_image(slug, slot, folders):
    for folder in folders:
        for ext in IMAGE_EXTS:
            p = folder / f"{slug}-{slot}{ext}"
            if p.exists():
                return p
    return None


def fix_poles(img):
    """Resample polar rows to their true circumference and blend an ice cap.

    Features drawn at full width along the top or bottom edge collapse into
    starbursts on a sphere.  Squeezing each high-latitude row down to the
    width it really covers, then stretching it back, removes that.
    """
    img = img.convert("RGB")
    w, h = img.size
    out = img.copy()
    ice = (234, 240, 246)
    for y in range(h):
        lat = 90.0 - (y + 0.5) * 180.0 / h
        alat = abs(lat)
        if alat < 70:
            continue
        row = img.crop((0, y, w, y + 1))
        tiny = max(1, int(round(w * math.cos(math.radians(alat)))))
        row = row.resize((tiny, 1), Image.BOX).resize((w, 1), Image.BILINEAR)
        if lat > 0:
            t = min(1.0, max(0.0, (alat - 80.0) / 8.0))
            t = t * t * (3 - 2 * t)
            if t > 0:
                row = Image.blend(row, Image.new("RGB", (w, 1), ice), t)
        out.paste(row, (0, y))
    return out


_image_cache = {}


def encode_image(path, slot):
    key = (str(path), path.stat().st_mtime, slot)
    if key in _image_cache:
        return _image_cache[key]
    if not HAVE_PIL:
        mime = {".webp": "image/webp", ".png": "image/png"}.get(path.suffix.lower(), "image/jpeg")
        uri = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    else:
        img = Image.open(path)
        img.load()
        if slot == "map":
            img = fix_poles(img)
            if img.width > 4096:
                img = img.resize((4096, 2048), Image.LANCZOS)
        else:
            img = img.convert("RGB")
            img.thumbnail((1920, 1920), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=86, method=5)
        uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    _image_cache[key] = uri
    return uri


SOUND_MIME = {".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".wav": "audio/wav", ".m4a": "audio/mp4"}


def sync_media(dirs, out_dir):
    files = {}
    for d in dirs:
        src = d / "media"
        if src.is_dir():
            for f in sorted(src.iterdir()):
                files[f.name] = f
    copied = total = 0
    for f in files.values():
        if not f.is_file() or f.name.startswith(".") or f.name.lower().startswith("readme"):
            continue
        total += 1
        dst = out_dir / f.name
        st = f.stat()
        if dst.exists() and dst.stat().st_size == st.st_size and dst.stat().st_mtime >= st.st_mtime:
            continue
        shutil.copy2(f, dst)
        copied += 1
    return copied, total


# ---------------------------------------------------------------- session manifest

MANIFEST_KEYS = ("session", "output", "network", "start", "worlds", "atlas", "briefs", "triggers", "signals", "arm")


def parse_manifest(path):
    out = {}
    notes = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise BuildError(f"{rel(path)} line {lineno}: expected 'Setting: value' and found '{line}'.")
        k, v = line.split(":", 1)
        k = k.strip().lower()
        if k == "skin":
            notes.append("'Skin:' is retired.  Skins live in campaign.md now.  Use 'Start: alert' for an emergency-mode session.")
            continue
        if k == "held":
            raise BuildError(f"{rel(path)} line {lineno}: 'Held:' was replaced by 'Triggers:'.  "
                             "Define a trigger in campaign.md with a 'Reveals:' line for these briefs, "
                             "then list the trigger id here.")
        if k not in MANIFEST_KEYS:
            raise BuildError(f"{rel(path)} line {lineno}: '{k.title()}' is not a session setting.{hint(k, MANIFEST_KEYS)}  "
                             f"Allowed: {', '.join(x.title() for x in MANIFEST_KEYS)}.")
        out[k] = v.strip()
    if not out.get("worlds") and not out.get("atlas"):
        raise BuildError(f"{rel(path)}: needs a 'Worlds:' line, for example 'Worlds: nacre@orbital', "
                         "or an 'Atlas:' line, for example 'Atlas: long range'.")
    out.setdefault("worlds", "")
    out.setdefault("atlas", "")
    out.setdefault("session", path.stem)
    out.setdefault("output", path.stem)
    out.setdefault("network", "")
    out.setdefault("start", "normal")
    out.setdefault("briefs", "")
    out.setdefault("triggers", "")
    out.setdefault("signals", "")
    out.setdefault("arm", "90")
    out["start"] = out["start"].lower()
    if out["start"] not in ("normal", "alert"):
        raise BuildError(f"{rel(path)}: Start is '{out['start']}'.  Use normal or alert.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", out["output"]):
        raise BuildError(f"{rel(path)}: Output '{out['output']}' should be a plain file name with no spaces.")
    return out, notes


def ids(value):
    return [x.strip() for x in value.split(",") if x.strip()]


# ---------------------------------------------------------------- build

def build_session(target, manifest_path, ctx):
    manifest, notes = parse_manifest(manifest_path)
    info, worlds, all_briefs, crest = ctx["info"], ctx["worlds"], ctx["briefs"], ctx["crest"]
    layers = list(reversed(target["dirs"]))
    image_dirs = [d / "images" for d in layers] + [LIBRARY / "images"]
    brief_where = " or ".join(f"{rel(d / 'briefs')}/" for d in layers)
    report = []

    items = []
    for item in ids(manifest["worlds"]):
        slug, _, depth = item.partition("@")
        items.append((slug.strip(), (depth.strip() or "planetside").lower(), True))
    if manifest["atlas"]:
        adepth = manifest["atlas"].lower().strip()
        if adepth not in DEPTHS:
            raise BuildError(f"{rel(manifest_path)}: Atlas is '{manifest['atlas']}'.  Use a scan depth: {', '.join(DEPTHS)}.")
        listed = {i[0] for i in items}
        rest = sorted((w for sl, w in worlds.items() if sl not in listed), key=lambda w: (int(w["number"]), w["name"]))
        items += [(w["slug"], adepth, False) for w in rest]
    entries = []
    atlas_count = 0
    for slug, depth, listed in items:
        if slug not in worlds:
            raise BuildError(f"{rel(manifest_path)}: no world with slug '{slug}' in this campaign's worlds.md "
                             f"or library/worlds.md.{hint(slug, worlds)}")
        if depth not in DEPTHS:
            raise BuildError(f"{rel(manifest_path)}: '{slug}@{depth}' has an unknown scan depth.  "
                             f"Use {', '.join(DEPTHS)}.")
        allowed = set()
        for d in DEPTHS[: DEPTHS.index(depth) + 1]:
            allowed |= DEPTH_KEYS[d]
        src = worlds[slug]
        fields, glitch, deep, warns = scan_world(src, allowed)
        locked = [k for k in REQUIRED if k not in allowed]
        images, missing = {}, []
        for slot, needs in IMAGE_SLOTS.items():
            if needs not in allowed:
                continue
            p = find_image(slug, slot, image_dirs)
            if p:
                images[slot] = encode_image(p, slot)
            elif slot in ("map", "thermal", "surface"):
                missing.append(slot)
        entries.append({"name": src["name"], "number": src["number"], "depth": depth, "atlas": not listed,
                        "fields": fields, "glitch": glitch, "deep": deep, "locked": locked, "images": images})
        # 3.6.3: Audio signals.  media/{slug}-signal1 to -signal5 (.mp3 .ogg .wav .m4a) loop under Hazard flags.
        aud = []
        for n in range(1, 6):
            for d in target["dirs"]:
                hits = [h for h in sorted((d / "media").glob(f"{slug}-signal{n}.*")) if h.suffix.lower() in (".mp3", ".ogg", ".wav", ".m4a")]
                if hits:
                    aud.append(hits[0].name); break
        entries[-1]["audio"] = aud
        if listed:
            gaps = []
            if "map" in missing:
                gaps.append("no map, so the globe shows a wireframe")
            stills = [m for m in missing if m != "map"]
            if stills:
                gaps.append(f"no {'/'.join(stills)} still (videos beside the file still play)")
            report.append(f"    World    {src['name']:<14} {depth:<10}  images: {', '.join(sorted(images)) or 'none'}"
                          f"{'  [' + '; '.join(gaps) + ']' if gaps else ''}")
        else:
            atlas_count += 1
        for w in warns:
            report.append(f"    Warn     {src['name']} ({rel(src['source'])}): {w}")
    if atlas_count:
        report.append(f"    Atlas    {atlas_count} more world(s) at {manifest['atlas'].lower()}, browsable in Deep Scan")

    visible = ids(manifest["briefs"])
    for bid in visible:
        if bid not in all_briefs:
            raise BuildError(f"{rel(manifest_path)}: brief '{bid}' is listed under Briefs but is not in "
                             f"{brief_where}.{hint(bid, all_briefs)}")
    triggers, held = [], {}
    for tid in ids(manifest["triggers"]):
        if tid not in info["triggers"]:
            raise BuildError(f"{rel(manifest_path)}: trigger '{tid}' is not defined in campaign.md."
                             f"{hint(tid, info['triggers'])}")
        t = dict(info["triggers"][tid])
        for bid in t["reveals"]:
            if bid not in all_briefs:
                raise BuildError(f"campaign.md trigger '{tid}' reveals '{bid}', which is not in "
                                 f"{brief_where}.{hint(bid, all_briefs)}")
            if bid in visible:
                raise BuildError(f"{rel(manifest_path)}: brief '{bid}' is listed under Briefs and is also hidden by "
                                 f"trigger '{tid}'.  Take it out of Briefs so the trigger can reveal it.")
            if bid in held:
                raise BuildError(f"{rel(manifest_path)}: brief '{bid}' is revealed by both '{held[bid]}' and '{tid}'.  "
                                 "Pick one.")
            held[bid] = tid
        triggers.append(t)

    briefs = []
    for bid in visible:
        b = dict(all_briefs[bid])
        b["held"] = False
        briefs.append(b)
    for bid, tid in held.items():
        b = dict(all_briefs[bid])
        b["held"] = True
        b["trigger"] = tid
        briefs.append(b)

    sounds = {}
    for t in triggers:
        f = t["sound"].get("file")
        if not f:
            how = "silent" if t["sound"].get("silent") else "built-in " + ("alarm" if t["style"] == "attack" else "chime")
        else:
            sp = next((d / "sounds" / f for d in layers if (d / "sounds" / f).exists()), layers[0] / "sounds" / f)
            if sp.exists():
                if f not in sounds:
                    mime = SOUND_MIME.get(sp.suffix.lower(), "audio/mpeg")
                    sounds[f] = f"data:{mime};base64," + base64.b64encode(sp.read_bytes()).decode()
                how = f"{f} embedded ({sp.stat().st_size // 1024} KB)"
            else:
                how = f"{f} beside the file, else built-in"
        report.append(f"    Trigger  {t['id']:<22} {t['style']:<7} reveals: {', '.join(t['reveals']) or 'nothing'}"
                      f"  sound: {how}")

    signals, progs = [], {}
    all_sigs = ctx["signals"]
    sig_where = " or ".join(f"{rel(d / 'signals')}/" for d in layers)
    for item in ids(manifest["signals"]):
        sid, _, how = item.partition("@")
        sid, how = sid.strip(), how.strip().lower()
        if sid not in all_sigs:
            raise BuildError(f"{rel(manifest_path)}: signal '{sid}' is listed under Signals but is not in {sig_where}."
                             f"{hint(sid, all_sigs)}")
        if not how or how in ("encoded", "fresh"):
            start = ("fresh", 0)
        elif how == "decoded":
            start = ("decoded", 0)
        elif how.startswith("running"):
            left = clock_seconds(how[len("running"):])
            if left is None:
                raise BuildError(f"{rel(manifest_path)}: '{item}' needs the time left as HH:MM:SS, "
                                 f"for example '{sid}@running 00:45:00'.")
            start = ("running", left)
        else:
            raise BuildError(f"{rel(manifest_path)}: '{item}' is not a signal state.  "
                             f"Use {sid}, {sid}@decoded, or {sid}@running 00:45:00.")
        sig = finish_signal(all_sigs[sid], start, image_dirs, report, [d / "signals" for d in layers],
                            [d / "media" for d in layers], [d / "sounds" for d in layers])
        if sig["program"] in progs:
            raise BuildError(f"{rel(manifest_path)}: signals '{progs[sig['program']]}' and '{sid}' both use the program "
                             f"name {sig['program']}.  Give each its own.")
        progs[sig["program"]] = sid
        signals.append(sig)

    try:
        arm = max(5, int(manifest["arm"]))
    except ValueError:
        raise BuildError(f"{rel(manifest_path)}: Arm must be a number of seconds, for example 'Arm: 90'.")
    report.append(f"    Briefs   {', '.join(visible) or 'none'}")
    if manifest["start"] == "alert":
        report.append("    Start    alert (opens in emergency mode, feeds dead)")

    camp_info = {k: info[k] for k in ("id", "name", "motto", "normal", "alert")}
    payload = {
        "engine": ENGINE,
        "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "campaign": camp_info,
        "session": {"title": manifest["session"], "output": manifest["output"], "network": manifest["network"] or info["normal"]["network"],
                    "start": manifest["start"], "arm": arm},
        "triggers": triggers,
        "sounds": sounds,
        "worlds": entries,
        "briefs": briefs,
        "signals": signals,
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    page = ctx["template"].replace("<!--__CREST__-->", crest, 1).replace("/*__DATA__*/null", data, 1)
    out_dir = target["out"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{manifest['output']}.html"
    out.write_text(page, encoding="utf-8")
    return out, report, notes


def load_template():
    t = TEMPLATE.read_text(encoding="utf-8")
    for marker in ("/*__DATA__*/null", "<!--__CREST__-->"):
        if marker not in t:
            raise BuildError(f"app/display.html is missing the {marker} marker.  Restore it from the workshop zip.")
    return t


def merged_briefs(dirs):
    briefs = {}
    for d in dirs:
        briefs.update(parse_briefs(d / "briefs"))
    return briefs


def campaign_context(target):
    info = parse_campaign(target)
    crest, crest_note = crest_markup(info)
    return {"info": info, "worlds": load_worlds(target["dirs"]), "briefs": merged_briefs(target["dirs"]),
            "signals": merged_signals(target["dirs"]),
            "crest": crest, "crestNote": crest_note, "template": load_template()}


CHAPTER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def chapters_of(space):
    return [p for p in sorted(space.iterdir())
            if p.is_dir() and CHAPTER_RE.match(p.name) and (p / "campaign.md").exists()]


def skipped_chapters(space):
    """Folders that look like a chapter but will not build, usually a fresh copy of _template."""
    out = []
    for p in sorted(space.iterdir()):
        if not p.is_dir() or p.name in ("_template",) or p.name.startswith(".") or not (p / "campaign.md").exists():
            continue
        if not CHAPTER_RE.match(p.name):
            out.append(p)
    return out


def targets_of(space):
    """Everything buildable in one campaign folder: its own sessions/ (if any) and each chapter."""
    out = []
    if any((space / "sessions").glob("*.md")):
        out.append({"id": space.name, "label": space.name, "dirs": [space], "out": DIST / space.name})
    for ch in chapters_of(space):
        out.append({"id": f"{space.name}/{ch.name}", "label": f"{space.name} / {ch.name}",
                    "dirs": [space, ch], "out": DIST / space.name / ch.name})
    return out


def build_target(target, only=None):
    print(f"\n=== {target['label']} ===")
    ok = failed = 0
    try:
        ctx = campaign_context(target)
    except BuildError as e:
        print(f"  FAILED before any session was built:\n    {e}")
        return 0, 1
    print(f"  Campaign  {ctx['info']['name']}   crest: {ctx['crestNote']}")
    home = target["dirs"][-1]
    sessions = [only] if only else sorted((home / "sessions").glob("*.md"))
    if not sessions:
        print(f"  No session files in {rel(home / 'sessions')}/ yet.")
    made = set()
    for mp in sessions:
        try:
            out, report, notes = build_session(target, mp, ctx)
            ok += 1
            made.add(out.name)
            print(f"  OK      {rel(out)}  ({out.stat().st_size / 1048576:.2f} MB)  <- open this one")
            print("\n".join(report))
            for n in notes:
                print(f"    Note     {n}")
        except BuildError as e:
            failed += 1
            print(f"  FAILED  {mp.name}\n    {e}")
    if not only and target["out"].is_dir():
        # Session files whose source is gone (renamed or deleted) are removed so nobody opens a stale copy.
        for old in target["out"].glob("*.html"):
            if old.name not in made and not failed:
                old.unlink()
                print(f"  Removed {rel(old)}  (its session file is gone)")
    copied, total = sync_media(target["dirs"], target["out"]) if ok else (0, 0)
    if total:
        print(f"  Media     {total} file(s) in media/, {copied} copied into {rel(target['out'])}/")
    return ok, failed


def build_campaign(space, only=None):
    targets = targets_of(space)
    for p in skipped_chapters(space):
        print(f"\n  Skipped folder \"{p.name}\" in {rel(space)}/.  Rename it with lowercase letters, numbers, and dashes "
              f"(example: iron-tide) to build it as a chapter.")
    if only:
        targets = [t for t in targets if t["dirs"][-1] == only[0]]
    if not targets:
        print(f"\n=== {space.name} ===\n  Nothing to build yet.  Add sessions/ files, or copy _template into a chapter folder.")
        return 0, 0
    ok = failed = 0
    for t in targets:
        o, f = build_target(t, only[1] if only else None)
        ok += o
        failed += f
    root = DIST / space.name
    if not only and root.is_dir() and not any(t["out"] == root for t in targets):
        # Leftovers from before this campaign had chapters: files sitting directly in dist/<campaign>/.
        stale = [f for f in root.iterdir() if f.is_file()]
        for f in stale:
            f.unlink()
        if stale:
            print(f"\n  Cleaned {len(stale)} old file(s) from {rel(root)}/ (this campaign now builds into chapter folders)")
    return ok, failed


def list_campaigns(include_hidden=False):
    if not CAMPAIGNS.is_dir():
        return []
    return [p for p in sorted(CAMPAIGNS.iterdir())
            if p.is_dir() and (p / "campaign.md").exists() and (include_hidden or not p.name.startswith("_"))]


def choose_campaigns():
    camps = list_campaigns()
    if not camps:
        raise BuildError("No campaigns found.  Copy campaigns/_starter to campaigns/<your-campaign> to begin.")
    if len(camps) == 1 or not sys.stdin.isatty():
        return camps
    print("OMNISLATE build.  Which campaign?\n")
    for i, c in enumerate(camps, 1):
        print(f"  {i}) {c.name}")
    print("  A) all of them\n")
    pick = input("Type a number and press Enter: ").strip().lower()
    if pick in ("a", "all", ""):
        return camps
    if pick.isdigit() and 1 <= int(pick) <= len(camps):
        return [camps[int(pick) - 1]]
    raise BuildError(f"'{pick}' is not one of the choices.")


def main(argv):
    args = [a for a in argv if a not in ("--pause",)]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    targets = []
    if not args:
        targets = [(c, None) for c in choose_campaigns()]
    elif args[0] == "--all":
        targets = [(c, None) for c in list_campaigns()]
    else:
        for a in args:
            p = Path(a)
            if p.suffix == ".md" and p.exists():
                p = p.resolve()
                home = p.parent.parent
                if p.parent.name != "sessions" or not (home / "campaign.md").exists():
                    raise BuildError(f"{a} should sit in a campaign's sessions/ folder.")
                space = home if home.parent.resolve() == CAMPAIGNS.resolve() else home.parent
                targets.append((space, (home, p)))
            elif "/" in a.strip("/") and (CAMPAIGNS / a.strip("/")).is_dir():
                space_name, chapter = a.strip("/").split("/", 1)
                targets.append((CAMPAIGNS / space_name, (CAMPAIGNS / space_name / chapter, None)))
            elif (CAMPAIGNS / a).is_dir():
                targets.append((CAMPAIGNS / a, None))
            elif len([c for c in list_campaigns(True) if c.name.startswith(a)]) == 1:
                targets.append(([c for c in list_campaigns(True) if c.name.startswith(a)][0], None))
            else:
                names = [c.name for c in list_campaigns(True)]
                raise BuildError(f"'{a}' is not a campaign folder or a session file.{hint(a, names)}  "
                                 f"Campaigns: {', '.join(names) or 'none'}.")
    ok = failed = 0
    for camp, only in targets:
        o, f = build_campaign(camp, only)
        ok += o
        failed += f
    print(f"\nDone: {ok} built, {failed} failed.")
    if not HAVE_PIL:
        print("Note: Pillow is not installed.  Images went in unconverted and map poles were not fixed.")
        print("      Install it once with: sudo apt install python3-pil")
    return 2 if failed else 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except BuildError as e:
        print(f"\nBUILD FAILED: {e}")
        code = 2
    except KeyboardInterrupt:
        code = 1
    except Exception:
        print("\nSomething unexpected broke inside build.py.  Nothing you did should cause this.")
        print("Copy everything below this line and send it to whoever maintains your OMNISLATE workshop:\n")
        traceback.print_exc()
        code = 3
    sys.exit(code)
