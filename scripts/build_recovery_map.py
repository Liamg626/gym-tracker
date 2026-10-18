"""Build the production Recovery Map SVG (SCRUM-22 Phase 3).

Fetches react-native-body-highlighter's male front/back path data at a pinned
commit (parsed as text, never executed), gives every Region its Muscle IDs, cuts
the chest, deltoids and trapezius on the source geometry, rotates the
legs 5 degrees outward at the hip (ADR-0007), and writes:

    assets/recovery-map/recovery-map.svg   front at x 0-724, back at x 724-1448
    assets/recovery-map/regions.md         Region -> Muscle IDs table

It fails if a Muscle has no Region, a Region has no Muscle, or a Muscle's side
in exercise_tags.MUSCLES disagrees with the map.

    pip install -r scripts/requirements.txt
    python scripts/build_recovery_map.py
"""
import re
import urllib.request
from pathlib import Path

from shapely import affinity
from shapely.geometry import MultiPolygon, Point, Polygon, box
from shapely.ops import polylabel, unary_union
from shapely.strtree import STRtree
from svgpathtools import parse_path

from exercise_tags import MUSCLES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/recovery-map"
CACHE = Path(__file__).resolve().parent / ".cache"
COMMIT = "8ed39ac2ae9cb46fb79d77eedec7e5b029a75174"
RAW = f"https://raw.githubusercontent.com/HichamELBSI/react-native-body-highlighter/{COMMIT}/"
VIEWS = {"front": ("assets/bodyFront.ts", 0, 362), "back": ("assets/bodyBack.ts", 724, 1086)}
LEG_SLUGS = {"adductors", "quadriceps", "hamstring", "knees", "tibialis", "calves", "ankles", "feet"}
LEG_ANGLE = 5
CUT_GAP = 6  # source units, about the width of the seams between source shapes
PHONE_PX_PER_UNIT = 150 / 724  # each view 150 px wide on the phone Recovery Map
HIT_MARGIN_PX = 8  # taps this close outside a Region still count

# (Region name, slug, left index, right index, Muscle IDs, cut). Cuts are listed
# under cut(). Reads confirmed from labelled false-colour renders on 2026-10-17;
# see docs/research/muscle-taxonomy.md § Region mapping.
REGIONS = {
    "front": [
        ("chest-clavicular", "chest", 0, 0, ["pectoralis-major-clavicular"], ("above", .45, .25)),
        ("chest-sternal", "chest", 0, 0, ["pectoralis-major-sternal"], ("below", .45, .25)),
        ("deltoid-anterior", "deltoids", 0, 0, ["deltoid-anterior"], ("band", .5)),
        ("deltoid-lateral", "deltoids", 0, 0, ["deltoid-lateral"], ("band-rest", .5)),
        ("trapezius", "trapezius", 0, 0, ["trapezius-upper"], None),
        ("biceps", "biceps", 0, 0, ["biceps-brachii"], None),
        ("triceps", "triceps", 0, 0, ["triceps-brachii-long-head", "triceps-brachii-medial-head"], None),
        *[(f"serratus-{i}", "obliques", i, i, ["serratus-anterior"], None) for i in (0, 1, 3)],
        *[(f"obliques-{i}", "obliques", i, i, ["external-oblique", "internal-oblique"], None) for i in (2, 4, 5, 6, 7)],
        *[(f"abs-{i}", "abs", i, i, ["rectus-abdominis"], None) for i in range(4)],
        ("brachioradialis", "forearm", 0, 0, ["brachioradialis"], None),
        ("forearm-flexors-1", "forearm", 1, 1, ["forearm-flexors"], None),
        ("forearm-flexors-2", "forearm", 2, 2, ["forearm-flexors"], None),
        ("adductors", "adductors", 0, 0, ["adductors"], None),
        ("sartorius", "adductors", 1, 1, ["sartorius"], None),
        ("gracilis", "adductors", 2, 2, ["gracilis", "adductors"], None),
        ("rectus-femoris", "quadriceps", 0, 0, ["rectus-femoris", "iliopsoas"], None),
        ("vastus-lateralis", "quadriceps", 1, 1, ["vastus-lateralis", "vastus-intermedius"], None),
        ("vastus-medialis", "quadriceps", 2, 2, ["vastus-medialis"], None),
        ("tibialis-anterior", "tibialis", 0, 0, ["tibialis-anterior"], None),
        ("fibularis", "calves", 0, 0, ["fibularis"], None),
        ("calf-medial", "calves", 1, 1, ["gastrocnemius-medial-head", "soleus"], None),
    ],
    "back": [
        ("trapezius-upper-neck", "neck", 0, 0, ["trapezius-upper"], None),
        ("trapezius-upper", "trapezius", 0, 0, ["trapezius-upper"], ("above", .2, .34)),
        ("rhomboids", "trapezius", 0, 0, ["rhomboids", "trapezius-middle", "trapezius-lower"], ("below", .2, .34)),
        ("deltoid-posterior", "deltoids", 0, 0, ["deltoid-posterior"], ("band", .55)),
        ("deltoid-lateral", "deltoids", 0, 0, ["deltoid-lateral"], ("band-rest", .55)),
        ("infraspinatus", "upper-back", 0, 0, ["infraspinatus", "teres-minor", "supraspinatus"], None),
        ("teres-major", "upper-back", 2, 1, ["teres-major"], None),
        ("latissimus-dorsi", "upper-back", 1, 2, ["latissimus-dorsi"], None),
        ("triceps-lateral-head", "triceps", 0, 0, ["triceps-brachii-lateral-head"], None),
        ("triceps-long-head", "triceps", 1, 1, ["triceps-brachii-long-head"], None),
        ("triceps-medial-head", "triceps", 2, 2, ["triceps-brachii-medial-head"], None),
        *[(f"forearm-extensors-{i}", "forearm", i, i, ["forearm-extensors"], None) for i in range(4)],
        ("erector-spinae", "lower-back", 1, 0, ["erector-spinae"], None),
        ("latissimus-dorsi-lower", "lower-back", 0, 1, ["latissimus-dorsi", "external-oblique"], None),
        ("gluteus-medius", "gluteal", 0, 0, ["gluteus-medius", "gluteus-minimus"], None),
        ("gluteus-maximus", "gluteal", 1, 1, ["gluteus-maximus"], None),
        ("adductors", "adductors", 0, 0, ["adductors"], None),
        ("biceps-femoris", "hamstring", 2, 0, ["biceps-femoris-long-head", "biceps-femoris-short-head"], None),
        ("semitendinosus", "hamstring", 1, 1, ["semitendinosus"], None),
        ("semimembranosus", "hamstring", 3, 2, ["semimembranosus", "gracilis"], None),
        ("vastus-lateralis", "hamstring", 0, 3, ["vastus-lateralis"], None),
        ("gastrocnemius-lateral", "calves", 0, 0, ["gastrocnemius-lateral-head"], None),
        ("gastrocnemius-medial", "calves", 2, 1, ["gastrocnemius-medial-head"], None),
        ("soleus-1", "calves", 1, 2, ["soleus"], None),
        ("soleus-2", "calves", 3, 3, ["soleus"], None),
    ],
}


def fetch(rel):
    path = CACHE / COMMIT / rel
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(urllib.request.urlopen(RAW + rel, timeout=30).read())
    return path.read_text(encoding="utf-8")


def slugs(rel):
    out = {}
    for blk in re.split(r"\n  \{", fetch(rel))[1:]:
        slug = re.search(r'slug: "([^"]+)"', blk).group(1)
        out[slug] = {side: re.findall(r'"(M[^"]+)"', m.group(1))
                     for side in ("left", "right", "common")
                     if (m := re.search(side + r": \[(.*?)\]", blk, re.S))}
    return out


NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def spaced(d):
    """Rewrite compact path data (".5.5", glued arc flags) with plain spaces for svgpathtools."""
    out, i, cmd, argn = [], 0, None, 0
    while i < len(d):
        ch = d[i]
        if ch in " ,\n\t":
            i += 1
        elif ch.isalpha():
            cmd, argn = ch, 0
            out.append(ch)
            i += 1
        elif cmd in "aA" and argn % 7 in (3, 4):
            out.append(ch)  # arc flags are single digits, often glued to what follows
            argn += 1
            i += 1
        else:
            m = re.match(NUM, d[i:])
            out.append(m.group(0))
            argn += 1
            i += m.end()
    return " ".join(out)


def polygon(d, step=1.5):
    """Flatten an SVG path to a shapely polygon, sampling every ~step units."""
    rings = []
    for sub in parse_path(spaced(d)).continuous_subpaths():
        pts = []
        for seg in sub:
            n = max(2, int(seg.length() / step))
            pts += [seg.point(t / n) for t in range(n)]
        if len(pts) > 2:
            rings.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    return unary_union(rings)


def cut(shape, spec, mid):
    """Cut types (all mirror for the right-hand copy):
    above/below (o, i): keep the part above/below a straight line from height
        fraction o on the edge away from the midline to i on the edge towards it.
    band/band-rest (k): the shape squeezed sideways to k of its width towards the
        midline, clipped to the shape (band), or the shape minus that (band-rest);
        the cut runs parallel to the outer contour."""
    if spec is None:
        return shape
    kind, a = spec[0], spec[1]
    x0, y0, x1, y1 = shape.bounds
    right = (x0 + x1) / 2 > mid
    outer_x, inner_x = (x1, x0) if right else (x0, x1)
    if kind in ("above", "below"):
        o, i = y0 + (y1 - y0) * a, y0 + (y1 - y0) * spec[2]
        edge = y0 - 10 if kind == "above" else y1 + 10
        pad = 10 if right else -10
        return shape.intersection(Polygon([(outer_x + pad, o), (inner_x - pad, i), (inner_x - pad, edge), (outer_x + pad, edge)]))
    band = shape.intersection(affinity.scale(shape, xfact=a, yfact=1, origin=(inner_x, (y0 + y1) / 2)))
    return band if kind == "band" else shape.difference(band)


def d_of(geom, nd=1):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.simplify(.35).coords)[:-1]
            out.append("M" + " ".join(f"{x:.{nd}f} {y:.{nd}f}" for x, y in pts) + "Z")
    return "".join(out)


def build_view(view):
    rel, x_off, mid = VIEWS[view]
    paths = slugs(rel)
    used, regions, neutral = set(), [], []
    for name, slug, li, ri, muscles, spec in REGIONS[view]:
        for side, i in (("left", li), ("right", ri)):
            src = paths[slug][side][i]
            used.add((slug, side, i))
            # cut pieces are inset so a cut shows the same dark gap as the source's own seams
            geom = src if spec is None else cut(polygon(src), spec, mid).buffer(-CUT_GAP / 2, join_style=2)
            regions.append({"id": f"{view}-{name}-{side[0]}", "slug": slug, "side": side,
                            "muscles": muscles, "d": geom if isinstance(geom, str) else d_of(geom),
                            "geom": polygon(src) if spec is None else geom})
    for slug, sides in paths.items():
        for side, ds in sides.items():
            neutral += [{"slug": slug, "side": side, "d": d} for i, d in enumerate(ds) if (slug, side, i) not in used]
    # leg pivots: top centre of each leg's outline, so the legs rotate outward at the hip
    pivots = {}
    for side in ("left", "right"):
        legs = unary_union([r["geom"] for r in regions if r["slug"] in LEG_SLUGS and r["side"] == side])
        x0, y0, x1, y1 = legs.bounds
        pivots[side] = ((x0 + x1) / 2, y0)
    return regions, neutral, pivots, mid


def leg_transform(side, pivots, mid):
    px, py = pivots[side]
    angle = LEG_ANGLE if px > mid else -LEG_ANGLE  # feet move away from the midline
    return f"rotate({angle} {px:.1f} {py:.1f})", angle, (px, py)


def hit_cells(regions, pivots, mid):
    """A tap selects the nearest Region (Liam, 2026-10-18). Returns each Region's hit
    cell (the points nearer to it than to any other Region, within HIT_MARGIN_PX of the body
    at phone size) and the diameter in phone px of the largest circle inside it."""
    geoms = []
    for r in regions:
        g = r["geom"]
        if r["slug"] in LEG_SLUGS:
            _, angle, origin = leg_transform(r["side"], pivots, mid)
            g = affinity.rotate(g, angle, origin=origin)
        geoms.append(g)
    body = unary_union(geoms).buffer(HIT_MARGIN_PX / PHONE_PX_PER_UNIT)
    # assign a grid of points to their nearest Region, then measure each Region's cell
    step = 4
    x0, y0, x1, y1 = body.bounds
    pts = [Point(x, y) for x in range(int(x0), int(x1), step) for y in range(int(y0), int(y1), step)]
    pts = [p for p in pts if body.contains(p)]
    nearest = STRtree(geoms).query_nearest(pts, return_distance=False, all_matches=False)[1]
    cells = {k: [] for k in range(len(geoms))}
    for p, k in zip(pts, nearest):
        cells[k].append(box(p.x - step / 2, p.y - step / 2, p.x + step / 2, p.y + step / 2))
    out = {}
    for k, boxes in cells.items():
        cell = unary_union(boxes)
        best = max((cell.geoms if isinstance(cell, MultiPolygon) else [cell]), key=lambda q: q.area)
        size = 2 * polylabel(best, tolerance=1).distance(best.boundary) * PHONE_PX_PER_UNIT
        out[regions[k]["id"]] = (cell.simplify(4), size)
    return out


NOTICE = """react-native-body-highlighter, https://github.com/HichamELBSI/react-native-body-highlighter
(commit {commit}), male front and back path data.

MIT License

Copyright (c) 2022 ELABBASSI Hicham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Modified for Gym Tracker (SCRUM-22): original colours removed, shapes tagged
with Muscle IDs, chest, deltoids and trapezius cut into Regions, legs
rotated 5 degrees outward at the hip. Generated by scripts/build_recovery_map.py."""


def main():
    views = {v: build_view(v) for v in VIEWS}

    # coverage and side checks
    on_map = {}
    for v, (regions, *_rest) in views.items():
        for r in regions:
            assert r["muscles"], f"{r['id']} has no Muscle"
            for m in r["muscles"]:
                assert m in MUSCLES, f"{r['id']}: unknown Muscle {m}"
                on_map.setdefault(m, set()).add(v)
    missing = [m for m in MUSCLES if m not in on_map]
    assert not missing, f"Muscles with no Region: {missing}"
    for m, vs in on_map.items():
        side = "both" if len(vs) == 2 else vs.pop()
        assert MUSCLES[m][0] == side, f"{m}: exercise_tags says {MUSCLES[m][0]}, map says {side}"

    body, hits = [], {}
    for v, (regions, neutral, pivots, mid) in views.items():
        hits[v] = hit_cells(regions, pivots, mid)
        body.append(f'  <g id="{v}">')
        for side in ("left", "right"):
            groups = {"body": [], "legs": []}
            for n in neutral:
                if n["side"] in (side, "common" if side == "left" else None):
                    groups["legs" if n["slug"] in LEG_SLUGS else "body"].append(
                        f'      <path class="base" d="{n["d"]}"/>')
            for r in regions:
                if r["side"] == side:
                    groups["legs" if r["slug"] in LEG_SLUGS else "body"].append(
                        f'      <path class="region" id="{r["id"]}" data-muscles="{" ".join(r["muscles"])}" d="{r["d"]}"/>')
            body.append(f'    <g class="side-{side}">')
            body += groups["body"]
            body.append(f'      <g class="legs" transform="{leg_transform(side, pivots, mid)[0]}">')
            body += ["  " + line for line in groups["legs"]]
            body += ["      </g>", "    </g>"]
        body.append('    <g class="hits">')
        body += [f'      <path class="hit" data-region="{rid}" d="{d_of(cell, 0)}"/>' for rid, (cell, _s) in hits[v].items()]
        body += ["    </g>", "  </g>"]
    svg = "\n".join([
        f"<!--\n{NOTICE.format(commit=COMMIT)}\n-->",
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1448 1448">',
        "  <style>.base{fill:#262B33}.region{fill:#3A414B;stroke:#0D0F12;stroke-width:2}.hit{fill:transparent}</style>",
        *body, "</svg>", ""])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "recovery-map.svg").write_text(svg, encoding="utf-8")

    rows = ["| Region (id without -l/-r) | View | Muscle IDs |", "|---|---|---|"]
    seen = set()
    for v, (regions, *_r) in views.items():
        for r in regions:
            key = r["id"][:-2]
            if key not in seen:
                seen.add(key)
                rows.append(f"| `{key}` | {v} | {', '.join(f'`{m}`' for m in r['muscles'])} |")
    n_regions = len(seen)
    (OUT / "regions.md").write_text("\n".join([
        "# Recovery Map Regions",
        "",
        "Generated by `scripts/build_recovery_map.py` from `recovery-map.svg`. Every Region exists as a",
        "left (`-l`) and right (`-r`) copy that carry the same Muscle IDs and always show the same state.",
        "A Region with several Muscles is coloured by the worst Recovery State among them.",
        "",
        f"{n_regions} Regions per side; all {len(MUSCLES)} Muscles appear on at least one.",
        "",
        *rows, ""]), encoding="utf-8")

    print(f"wrote recovery-map.svg ({len(svg) // 1024} KB) and regions.md: {n_regions} Regions per side, {len(MUSCLES)} Muscles covered")
    for v, cells in hits.items():
        sizes = sorted(s for k, (_c, s) in cells.items() if k.endswith("-l"))
        print(f"{v}: nearest-Region hit cells {sizes[0]:.0f}-{sizes[-1]:.0f} px across at phone size; "
              "the Nearby list gives every Region a 44 px row")


if __name__ == "__main__":
    main()
