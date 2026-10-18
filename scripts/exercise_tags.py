"""Exercise -> Muscle tags (SCRUM-22 Phase 2).

Reads every Exercise row from docs/research/exercise-list.md, tags it from the
family defaults and variant overrides below, writes the draft library JSON and
the tag tables in docs/research/exercise-muscle-tags.md, and prints the checks.

    python scripts/exercise_tags.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / "docs/research/exercise-list.md"
DOC = ROOT / "docs/research/exercise-muscle-tags.md"
OUT = ROOT / "docs/research/exercise-library.draft.json"

# The Muscles from docs/research/muscle-taxonomy.md: id -> (side, group).
MUSCLES = {
    "pectoralis-major-clavicular": ("front", "chest"),
    "pectoralis-major-sternal": ("front", "chest"),
    "serratus-anterior": ("front", "chest"),
    "deltoid-anterior": ("front", "shoulders"),
    "deltoid-lateral": ("both", "shoulders"),
    "deltoid-posterior": ("back", "shoulders"),
    "infraspinatus": ("back", "shoulders"),
    "teres-minor": ("back", "shoulders"),
    "supraspinatus": ("back", "shoulders"),
    "trapezius-upper": ("both", "back"),
    "trapezius-middle": ("back", "back"),
    "trapezius-lower": ("back", "back"),
    "latissimus-dorsi": ("back", "back"),
    "teres-major": ("back", "back"),
    "erector-spinae": ("back", "back"),
    "rhomboids": ("back", "back"),
    "biceps-brachii": ("front", "biceps"),
    "triceps-brachii-long-head": ("both", "triceps"),
    "triceps-brachii-lateral-head": ("back", "triceps"),
    "triceps-brachii-medial-head": ("both", "triceps"),
    "brachioradialis": ("front", "forearms"),
    "forearm-flexors": ("front", "forearms"),
    "forearm-extensors": ("back", "forearms"),
    "rectus-abdominis": ("front", "core"),
    "external-oblique": ("both", "core"),
    "internal-oblique": ("front", "core"),
    "gluteus-maximus": ("back", "hips"),
    "gluteus-medius": ("back", "hips"),
    "gluteus-minimus": ("back", "hips"),
    "adductors": ("both", "hips"),
    "iliopsoas": ("front", "hips"),
    "gracilis": ("both", "hips"),
    "rectus-femoris": ("front", "quads"),
    "vastus-lateralis": ("both", "quads"),
    "vastus-medialis": ("front", "quads"),
    "sartorius": ("front", "quads"),
    "vastus-intermedius": ("front", "quads"),
    "biceps-femoris-long-head": ("back", "hamstrings"),
    "biceps-femoris-short-head": ("back", "hamstrings"),
    "semitendinosus": ("back", "hamstrings"),
    "semimembranosus": ("back", "hamstrings"),
    "gastrocnemius-medial-head": ("both", "lower-legs"),
    "gastrocnemius-lateral-head": ("back", "lower-legs"),
    "soleus": ("both", "lower-legs"),
    "tibialis-anterior": ("front", "lower-legs"),
    "fibularis": ("front", "lower-legs"),
}

# Shorthands, expanded by m().
SETS = {
    "PC": "pectoralis-major-clavicular", "PS": "pectoralis-major-sternal",
    "SA": "serratus-anterior",
    "DA": "deltoid-anterior", "DL": "deltoid-lateral", "DP": "deltoid-posterior",
    "CUFF": "infraspinatus teres-minor", "SUP": "supraspinatus",
    "TU": "trapezius-upper", "TM": "trapezius-middle", "TL": "trapezius-lower",
    "RH": "rhomboids", "LAT": "latissimus-dorsi", "TMAJ": "teres-major",
    "ES": "erector-spinae",
    # brachialis is folded into biceps-brachii (Liam, 2026-10-18), so BR and BIC are the same Muscle
    "BIC": "biceps-brachii", "BR": "biceps-brachii",
    "TRI": "triceps-brachii-long-head triceps-brachii-lateral-head triceps-brachii-medial-head",
    "TRI1": "triceps-brachii-lateral-head triceps-brachii-medial-head",
    "TRIL": "triceps-brachii-long-head",
    "BRD": "brachioradialis", "FF": "forearm-flexors", "FE": "forearm-extensors",
    "RA": "rectus-abdominis", "OBL": "external-oblique internal-oblique",
    "GMAX": "gluteus-maximus", "GAB": "gluteus-medius gluteus-minimus",
    "ADD": "adductors", "GRA": "gracilis", "IP": "iliopsoas",
    "RF": "rectus-femoris", "VASTI": "vastus-lateralis vastus-medialis vastus-intermedius",
    "SAR": "sartorius",
    "HAM2": "biceps-femoris-long-head semitendinosus semimembranosus",
    "HAM": "biceps-femoris-long-head biceps-femoris-short-head semitendinosus semimembranosus",
    "GAS": "gastrocnemius-medial-head gastrocnemius-lateral-head", "SOL": "soleus",
    "TA": "tibialis-anterior", "FIB": "fibularis",
}


def m(spec):
    out = []
    for tok in spec.split():
        for mid in SETS[tok].split():
            if mid not in out:
                out.append(mid)
    return out


# Family -> (default primary, default secondary, source, [(name substrings, primary, secondary)]).
# The first override whose substrings all appear in the Exercise name wins.
ROW = "LAT TM RH"
ROW_S = "TMAJ DP TL BIC BR BRD"
FREE_ROW_S = ROW_S + " ES"
FAMILIES = {
    "Incline Chest Press": ("PC", "PS DA TRI", "rr2020, chaves2020", []),
    "Chest Fly (Pec Deck)": ("PC PS", "DA", "anatomy: tma-pect", [
        (["High-to-Low"], "PS", "PC DA"),
        (["Low-to-High"], "PC", "PS DA"),
        (["Incline"], "PC", "PS DA"),
        (["Decline"], "PS", "PC DA"),
    ]),
    "Dip": ("PS TRI", "DA PC", "anatomy: tma-pect, tma-arm", [
        (["Chest Lean"], "PS", "TRI DA PC"),
        (["Upright"], "TRI", "PS DA"),
        (["Bench Dip"], "TRI", "DA PS"),
    ]),
    "Flat Bench Press": ("PS", "PC DA TRI", "rr2020", []),
    "Push-Up": ("PS", "PC DA TRI SA RA", "rr2020 (by analogy with the flat press); anatomy: sp-serratus", [
        (["Diamond"], "TRI", "PS DA SA RA"),
        (["Decline"], "PS PC", "DA TRI SA RA"),
    ]),
    "Decline Bench Press": ("PS", "DA TRI", "rr2020", []),
    "Shoulder Press": ("DA", "DL TRI TU PC SA", "campos2020", [
        (["Push Press"], "DA", "DL TRI TU PC SA VASTI GMAX"),
        (["Behind-the-Neck"], "DA DL", "TRI TU SA"),
        (["Landmine"], "DA PC", "TRI SA"),
    ]),
    "Lateral Raise": ("DL", "SUP TU DA", "campos2020; anatomy: os-115", [
        (["Y-Raise"], "DL", "SUP TU TL"),
    ]),
    "Rear Delt Fly": ("DP", "TM RH CUFF", "anatomy: tma-shoulder, tma-back", []),
    "Front Raise": ("DA", "PC DL SA", "anatomy: tma-shoulder", []),
    "Face Pull": ("DP CUFF", "TM RH TL", "anatomy: tma-shoulder, tma-back", []),
    "Upright Row": ("DL TU", "DA SUP BR BRD", "anatomy: tma-shoulder, tma-back", []),
    "Lat Pulldown": ("LAT TMAJ", "TL RH TM DP BIC BR BRD", "anatomy: tma-back, sp-teresmajor", [
        (["Straight-Arm"], "LAT TMAJ", "TRIL DP PS"),
    ]),
    "Seated Row": (ROW, ROW_S, "anatomy: tma-back", [
        (["Wide-Grip"], "TM RH DP", "LAT TMAJ TL BIC BR BRD"),
    ]),
    "T-Bar Row": (ROW, ROW_S, "anatomy: tma-back", [
        (["Wide-Grip"], "TM RH DP", "LAT TMAJ TL BIC BR BRD"),
        (["Landmine"], ROW, FREE_ROW_S),
        (["Meadows"], ROW, FREE_ROW_S),
    ]),
    "Back Extension": ("ES", "GMAX HAM2", "anatomy: tma-intrinsic", [
        (["Seated Machine"], "ES", "GMAX"),
        (["Superman"], "ES", "GMAX"),
    ]),
    "Pull-Up": ("LAT TMAJ", "BIC BR BRD TL TM RH DP FF", "anatomy: tma-back, sp-teresmajor", []),
    "Bent-Over Row": (ROW, FREE_ROW_S, "anatomy: tma-back, tma-intrinsic", [
        (["Chest-Supported"], ROW, ROW_S),
        (["Seal Row"], ROW, ROW_S),
        (["Single-Arm"], ROW, ROW_S),
        (["Inverted"], ROW, ROW_S + " RA"),
    ]),
    "Deadlift": ("GMAX ES HAM2", "VASTI ADD TU TM LAT FF", "anatomy: tma-glute, tma-intrinsic, tma-ham", [
        (["Sumo"], "GMAX ADD VASTI", "ES HAM2 TU LAT FF"),
        (["Trap Bar"], "VASTI GMAX", "ES HAM2 TU FF"),
        (["Rack Pull"], "ES GMAX TU", "HAM2 TM LAT FF"),
    ]),
    "Overhead Triceps Extension": ("TRI", "", "maeo2023", []),
    "Triceps Pushdown": ("TRI1", "TRIL", "maeo2023", []),
    "Preacher Curl": ("BIC BR", "BRD FF", "anatomy: tma-arm", [
        (["Reverse-Grip"], "BRD BR", "BIC FE"),
    ]),
    "Bayesian Curl": ("BIC BR", "BRD FF", "anatomy: tma-arm", [
        (["Hammer"], "BR BRD", "BIC"),
    ]),
    "Hammer Curl": ("BR BRD", "BIC", "kleiber2015, coratella2023", []),
    "Wrist Curl": ("FF", "", "anatomy: tma-antfa", []),
    "Wrist Extension": ("FE", "", "anatomy: tma-postfa", []),
    "Biceps Curl": ("BIC BR", "BRD FF", "anatomy: tma-arm", [
        (["Reverse-Grip"], "BRD BR", "BIC FE"),
        (["Zottman"], "BIC BR BRD", "FF FE"),
    ]),
    "Lying Triceps Extension (Skull Crusher)": ("TRI", "", "maeo2023 (by analogy)", []),
    "Close-Grip Bench Press": ("TRI PS", "DA PC", "anatomy: tma-arm", [
        (["Crush Press"], "PS TRI", "DA PC"),
    ]),
    "Cable Crunch": ("RA", "OBL", "anatomy: os-114", [
        (["Oblique"], "OBL", "RA"),
    ]),
    "Leg Raise": ("RA IP", "RF SAR OBL", "anatomy: os-114, os-116", [
        (["Oblique"], "OBL IP", "RA RF SAR"),
        (["Hanging"], "RA IP", "RF SAR OBL FF"),
        (["Reverse Crunch"], "RA", "OBL IP"),
    ]),
    "Russian Twist": ("OBL", "RA IP", "anatomy: os-114", [
        (["Landmine"], "OBL", "RA DA"),
    ]),
    "Plank": ("RA", "OBL DA SA", "anatomy: os-114", [
        (["Side Plank"], "OBL", "GAB RA"),
    ]),
    "Crunch and Sit-Up": ("RA", "OBL", "anatomy: os-114", [
        (["Bicycle"], "OBL RA", "IP"),
        (["Oblique"], "OBL", "RA"),
        (["Sit-Up"], "RA", "OBL IP RF"),
    ]),
    "Ab Wheel Rollout": ("RA", "OBL LAT SA DA", "anatomy: os-114", []),
    "Hip Abduction": ("GAB", "GMAX", "anatomy: tma-glute", [
        (["Forward Lean"], "GAB GMAX", ""),
    ]),
    "Hip Adduction": ("ADD GRA", "", "anatomy: tma-medthigh", [
        (["Copenhagen"], "ADD GRA", "OBL"),
    ]),
    "Hip Thrust and Glute Bridge": ("GMAX", "HAM2 GAB", "krause2020", []),
    "Step-Up": ("GMAX VASTI", "RF GAB ADD", "krause2020", [
        (["Lateral"], "GMAX GAB VASTI", "RF ADD"),
    ]),
    "Glute Kickback": ("GMAX", "HAM2", "anatomy: tma-glute", []),
    "Leg Press": ("VASTI GMAX", "ADD", "kubo2019 (by analogy with the squat)", [
        (["Low, Narrow"], "VASTI", "GMAX ADD"),
        (["High, Wide"], "GMAX ADD VASTI", "HAM2"),
    ]),
    "Leg Extension": ("RF VASTI", "", "wakahara2017", []),
    "Pendulum Squat": ("VASTI GMAX", "ADD", "kubo2019 (by analogy)", []),
    "Bulgarian Split Squat": ("VASTI GMAX", "ADD GAB", "krause2020", []),
    "Squat": ("VASTI GMAX ADD", "ES GAB", "kubo2019", [
        (["Low-Bar"], "GMAX ADD VASTI", "ES HAM2"),
        (["Front"], "VASTI GMAX", "ADD ES RA"),
        (["Goblet"], "VASTI GMAX", "ADD"),
        (["Bodyweight"], "VASTI GMAX", "ADD"),
    ]),
    "Hack Squat": ("VASTI GMAX", "ADD", "kubo2019 (by analogy)", [
        (["Barbell"], "VASTI", "GMAX ADD ES FF"),
    ]),
    "Lunge": ("VASTI GMAX", "ADD GAB", "krause2020", [
        (["Lateral"], "ADD GRA GMAX VASTI", "GAB"),
    ]),
    "Hamstring Curl": ("HAM", "GAS SAR GRA", "maeo2021; anatomy: tma-ham", [
        (["Stability Ball"], "HAM", "GMAX GAS"),
    ]),
    "Romanian Deadlift": ("HAM2 GMAX", "ES ADD FF", "anatomy: tma-ham, sp-ham", [
        (["Single-Leg"], "HAM2 GMAX", "ES ADD GAB FF"),
        (["B-Stance"], "HAM2 GMAX", "ES ADD GAB FF"),
    ]),
    "Nordic Hamstring Curl": ("HAM", "GAS", "bourne2017", []),
    "Good Morning": ("HAM2 ES GMAX", "ADD", "anatomy: tma-ham, tma-intrinsic", []),
    "Glute-Ham Raise": ("HAM", "GMAX GAS ES", "anatomy: tma-ham", []),
    "Calf Raise": ("GAS SOL", "FIB", "kinoshita2023, nunes2020", [
        (["Seated"], "SOL", "FIB"),
    ]),
    "Tibialis Raise": ("TA", "", "anatomy: os-116", []),
}


def kebab(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read_exercises():
    family, rows = None, []
    for line in LIST.read_text(encoding="utf-8").splitlines():
        h = re.match(r"### (.+?) — ", line)
        if h:
            family = h.group(1)
            continue
        if line.startswith("## "):
            family = None
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if family and len(cells) == 5 and cells[4] == "option":
            rows.append({"name": cells[0], "family": family, "equipment": cells[1],
                         "unilateral": cells[2].startswith("Yes")})
    return rows


def tag(ex):
    p, s, _, overrides = FAMILIES[ex["family"]]
    for subs, op, os_ in overrides:
        if all(x in ex["name"] for x in subs):
            p, s = op, os_
            break
    primary = m(p)
    return primary, [x for x in m(s) if x not in primary]


def main():
    exercises = read_exercises()
    library, trained, primary_ever = [], set(), set()
    for ex in exercises:
        p, s = tag(ex)
        trained |= set(p) | set(s)
        primary_ever |= set(p)
        library.append({"id": kebab(ex["name"]), "name": ex["name"], "equipment": ex["equipment"],
                        "primaryMuscles": p, "secondaryMuscles": s})
        ex["views"] = {MUSCLES[x][0] for x in p + s}

    ids = [e["id"] for e in library]
    assert len(ids) == len(set(ids)), "duplicate Exercise id"
    assert set(trained) <= set(MUSCLES), set(trained) - set(MUSCLES)
    assert all(e["primaryMuscles"] for e in library)
    assert set(FAMILIES) == {e["family"] for e in exercises}, "family without tags"

    OUT.write_text(json.dumps(library, indent=2) + "\n", encoding="utf-8")

    untrained = [x for x in MUSCLES if x not in trained]
    secondary_only = [x for x in MUSCLES if x in trained and x not in primary_ever]
    one_view = {v: [e["name"] for e in exercises if e["views"] == {v}] for v in ("front", "back")}
    unilateral = [e["name"] for e in exercises if e["unilateral"]]

    fam_rows = ["| Family | Primary | Secondary | Variant overrides | Source |", "|---|---|---|---|---|"]
    for fam, (p, s, src, overrides) in FAMILIES.items():
        ov = "; ".join(f"*{' + '.join(subs)}*: P {', '.join(m(op))}"
                       + (f" / S {', '.join(x for x in m(os_) if x not in m(op))}" if os_ else "")
                       for subs, op, os_ in overrides) or "none"
        sec = ", ".join(x for x in m(s) if x not in m(p)) or "none"
        fam_rows.append(f"| {fam} | {', '.join(m(p))} | {sec} | {ov} | {src} |")

    counts = {x: [0, 0] for x in MUSCLES}
    for e in library:
        for x in e["primaryMuscles"]:
            counts[x][0] += 1
        for x in e["secondaryMuscles"]:
            counts[x][1] += 1
    cov_rows = ["| Muscle | Group | Primary in | Secondary in |", "|---|---|---|---|"]
    cov_rows += [f"| `{x}` | {MUSCLES[x][1]} | {c[0]} | {c[1]} |" for x, c in counts.items()]

    generated = "\n".join([
        f"{len(library)} Exercises tagged from {len(FAMILIES)} families. Every Exercise has at least one Primary Muscle and every tag is one of the {len(MUSCLES)} Muscle IDs.",
        "",
        "### Family tags",
        "",
        *fam_rows,
        "",
        "### Coverage per Muscle",
        "",
        *cov_rows,
        "",
        "### Checks",
        "",
        f"- **Muscles no Exercise trains:** {', '.join(untrained) or 'none'}",
        f"- **Muscles only ever Secondary:** {', '.join(secondary_only) or 'none'}",
        f"- **Exercises lighting only the front view:** {len(one_view['front'])}; **only the back view:** {len(one_view['back'])} (full lists printed by the script)",
        f"- **Unilateral Exercises:** {len(unilateral)}. The map mirrors left and right, so one-arm or one-leg Sets light both sides.",
    ])
    doc = DOC.read_text(encoding="utf-8")
    start, end = "<!-- generated:start -->", "<!-- generated:end -->"
    doc = doc[: doc.index(start) + len(start)] + "\n" + generated + "\n" + doc[doc.index(end):]
    DOC.write_text(doc, encoding="utf-8")

    print(f"{len(library)} Exercises, {len(FAMILIES)} families")
    print("untrained:", untrained)
    print("secondary only:", secondary_only)
    for v, names in one_view.items():
        print(f"{v} view only ({len(names)}):", ", ".join(names))
    print("unilateral:", len(unilateral))


if __name__ == "__main__":
    main()
