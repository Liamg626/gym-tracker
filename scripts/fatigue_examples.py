"""Worked examples for the fatigue model (SCRUM-22 Phase 4).

Runs three demo Workouts (push, pull, legs) through the MVP time-only rules and the
v1.2 volume-weighted model from docs/research/muscle-fatigue.md, using the Exercise
tags in docs/research/exercise-library.draft.json, and writes the tables into
muscle-fatigue.md between the generated markers. All numbers are demo data (ADR-0005).

    python scripts/fatigue_examples.py
"""
import json
from pathlib import Path

from exercise_tags import MUSCLES

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "docs/research/exercise-library.draft.json"
DOC = ROOT / "docs/research/muscle-fatigue.md"

# Mirrors FATIGUE_CONFIG in muscle-fatigue.md § Config shape.
ROLE_WEIGHT = {"primary": 1.0, "secondary": 0.5}
EFFORT_BY_RIR = {0: 1.0, 1: 0.52, 2: 0.42, 3: 0.32, 4: 0.25, 5: 0.2}
MIN_HOURS, MAX_HOURS, CAP_DOSE, FATIGUED_FRACTION = 12, 72, 4, 1 / 3
GROUP_SCALE = {g: 1.0 for _side, g in MUSCLES.values()}
HOURS = (12, 24, 48, 72)

# (Exercise name in the draft library, Working Sets, RIR)
WORKOUTS = {
    "Push": [("Barbell Bench Press", 4, 1), ("Incline Dumbbell Press", 3, 2),
             ("Seated Dumbbell Shoulder Press", 3, 1), ("Standing Dumbbell Lateral Raise", 3, 0),
             ("Cable Tricep Pushdown (Rope)", 3, 1)],
    "Pull": [("Wide-Grip Lat Pulldown", 4, 1), ("Seated Cable Row (V-Handle)", 4, 1),
             ("Standing Barbell Curl", 3, 1), ("Standing Cable Face Pull (Rope)", 3, 2),
             ("Standing Dumbbell Hammer Curl", 3, 1)],
    "Legs": [("High-Bar Barbell Back Squat", 4, 2), ("Barbell Romanian Deadlift", 3, 2),
             ("Seated Machine Leg Extension", 3, 0), ("Seated Machine Leg Curl", 3, 1),
             ("Standing Machine Calf Raise", 4, 1)],
}


def mvp_state(role, h):
    # elapsed time exactly at a boundary counts as the later state, as in Examples 1-4
    if h < 24:
        return "Fatigued" if role == "primary" else "Recovering"
    return "Recovering" if h < 72 else "Ready"


def v12_state(window, h):
    level = max(0.0, 1 - h / window)
    if level == 0:
        return "Ready"
    return "Fatigued" if level > 1 - FATIGUED_FRACTION else "Recovering"


def run(sets, library):
    dose, role = {}, {}
    for name, n, rir in sets:
        ex = library[name]
        for r, key in (("primary", "primaryMuscles"), ("secondary", "secondaryMuscles")):
            for m in ex[key]:
                dose[m] = dose.get(m, 0) + n * ROLE_WEIGHT[r] * EFFORT_BY_RIR[min(rir, 5)]
                if role.get(m) != "primary":
                    role[m] = r
    rows = []
    for m in sorted(dose, key=lambda m: (-dose[m], m)):
        window = GROUP_SCALE[MUSCLES[m][1]] * (MIN_HOURS + (MAX_HOURS - MIN_HOURS) * min(dose[m], CAP_DOSE) / CAP_DOSE)
        rows.append((m, role[m], dose[m], window,
                     [(mvp_state(role[m], h), v12_state(window, h)) for h in HOURS]))
    return rows


def weekly_sets(sets, library):
    """Each Working Set counts once per Muscle Group, at its highest role weight there."""
    totals = {}
    for name, n, _rir in sets:
        ex = library[name]
        best = {}
        for r, key in (("primary", "primaryMuscles"), ("secondary", "secondaryMuscles")):
            for m in ex[key]:
                g = MUSCLES[m][1]
                best[g] = max(best.get(g, 0), ROLE_WEIGHT[r])
        for g, w in best.items():
            totals[g] = totals.get(g, 0) + n * w
    return totals


def short(state):
    return {"Fatigued": "F", "Recovering": "R", "Ready": "G"}[state]


def main():
    library = {e["name"]: e for e in json.loads(LIBRARY.read_text(encoding="utf-8"))}
    out = ["States are written MVP → v1.2: **F** Fatigued, **R** Recovering, **G** Ready (green). "
           "Bold marks a Muscle whose two models disagree at that hour. U is the Fatigue Dose; D the Recovery Window.", ""]
    week = {}
    for title, sets in WORKOUTS.items():
        out += [f"#### {title}", "",
                "Working Sets: " + "; ".join(f"{name} {n} × RIR {rir}" for name, n, rir in sets) + ".", "",
                "| Muscle | Role | U | D (h) | " + " | ".join(f"{h} h" for h in HOURS) + " |",
                "|---|---|---|---|" + "---|" * len(HOURS)]
        for m, role, u, d, states in run(sets, library):
            cells = []
            for a, b in states:
                cell = f"{short(a)} → {short(b)}"
                cells.append(f"**{cell}**" if a != b else cell)
            out.append(f"| `{m}` | {role[0].upper()} | {u:.2f} | {d:.1f} | " + " | ".join(cells) + " |")
        out.append("")
        for g, v in weekly_sets(sets, library).items():
            week[g] = week.get(g, 0) + v
    out += ["#### Weekly Sets for the week (push + pull + legs once each)", "",
            "| Muscle Group | Weekly Sets | Against the 12-20 target |", "|---|---|---|"]
    for g in sorted(week, key=lambda g: -week[g]):
        v = week[g]
        verdict = "below the minimum (4)" if v < 4 else "below target" if v < 12 else "in target" if v <= 20 else "above target"
        out.append(f"| {g} | {v:g} | {verdict} |")
    start, end = "<!-- generated:examples:start -->", "<!-- generated:examples:end -->"
    doc = DOC.read_text(encoding="utf-8")
    doc = doc[: doc.index(start) + len(start)] + "\n" + "\n".join(out) + "\n" + doc[doc.index(end):]
    DOC.write_text(doc, encoding="utf-8")
    print("wrote worked examples:", ", ".join(WORKOUTS))


if __name__ == "__main__":
    main()
