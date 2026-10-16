# Research: an openly licensed anatomical front/back SVG for the Recovery Map

SCRUM-8 · [REC-001] · researched 2026-10-16

## Question

Which openly licensed front and back muscle-anatomy artwork can the **Recovery Map** use, given that the repo is public, we will split, recolour and add IDs to the artwork, and each region ID must match a **Muscle** ID (ADR-0006)? For each candidate: what licence, attribution and share-alike obligations apply, how many separately addressable muscle shapes it has, whether it suits a phone in dark mode, and how much work it takes to tag it with Muscle IDs. Fallback: existing React body-map libraries.

## Summary and recommendation

**Use Wikimedia Commons `Muscles front and back.svg`** (OpenStax, redrawn by Tomáš Kebert & umimeto.org, **CC BY-SA 4.0**) as the base artwork. It is the only candidate found that is real vector anatomy with **one closed path per muscle**. It holds 176 paths, and each figure is drawn once as a half that is mirrored with `<use>`. I count about 60–70 training-relevant muscle shapes across the two views, and the rest are face, hand, foot, bone and tendon shapes. (This count comes from a false-colour render. I did not tag each path, so treat it as an estimate.) The mirroring matches the REC rule "no left/right split". Its flat fills recolour cleanly, so it suits a dark theme.

- **Licence impact:** the modified SVG must stay CC BY-SA 4.0 and carry attribution. Keep it as a **separate file** that the component loads, not path data pasted into `.tsx` code. The repo's code then keeps its own licence: CC treats this as a collection, not an adaptation (see [Share-alike](#share-alike-does-a-cc-by-sa-asset-force-the-whole-repo)).
- **Taxonomy coverage:** most of the list maps directly: lats, infraspinatus, teres major, triceps long/lateral, brachialis, forearm muscles, rectus abdominis, external obliques, glute max, the quadriceps heads, the separate hamstrings, adductors, sartorius, both gastrocnemius heads, soleus and tibialis anterior. **We have to cut new shapes for:** the three deltoid heads, pec major clavicular vs sternal, trapezius upper/mid/lower and biceps long/short. **Gaps that can't honestly be shown on a superficial drawing:** triceps medial head, erector spinae (covered by the thoracolumbar fascia shape), rhomboids (only a sliver is visible), glute medius (only a sliver) and serratus anterior (drawn as stroke lines, not fillable areas). See [Recommendation](#recommendation).
- **Fallback:** `react-native-body-highlighter` path data (**MIT**). It is clean and stylised, but coarser: 23 named slugs, with sub-paths that can be re-tagged. `body-muscles` (**Apache-2.0**) already names finer regions (traps upper/mid/lower, triceps long/lateral and others), but its art is crude low-poly. Neither library documents where its artwork came from.

A draft ADR is at `docs/adr/0007-anatomical-svg-source.md` (Status: proposed).

## Comparison

"Shapes" means separately addressable closed shapes. Counts come from inspecting the source (see each candidate's notes).

| Candidate | Source | Licence | Attribution | Share-alike impact | Addressable muscle shapes (front / back) | Granularity vs taxonomy | Dark-mode / phone fit | File size | Effort to add IDs |
|---|---|---|---|---|---|---|---|---|---|
| **A. Commons "Muscles front and back.svg"** | [Commons file page][c-mfb] | CC BY-SA 4.0 | Required: "OpenStax & Tomáš Kebert & umimeto.org", link, licence, note of changes | Our modified SVG must be BY-SA 4.0. Rest of repo unaffected if the SVG stays a separate file | 176 paths in total, half-figures mirrored. Roughly 35–40 muscle shapes front, 25–30 back (estimate) | **Best**: individual heads/muscles for quads, hamstrings, gastrocnemius, rotator cuff, forearm; deltoid/trap/pec/biceps need cutting | Good: flat fills, recolour per path; neutral shapes need restyling | 350 KB raw (≈119 KB of path data; Inkscape cruft removable) | Medium: name about 65 paths, cut about 5 shapes, strip gradients and path-effects |
| B. Commons "Muscular system.svg" / "-back.svg" (Termininja), also wger's base images | [front][c-ms], [back][c-msb] | CC BY-SA 3.0 | Required: Termininja + source files | As A (BY-SA) | Not addressable: 43 / 19 paths are posterised colour layers of a traced photo | None usable | Poor: photographic red-on-black texture | 3.9 MB / 3.3 MB | Full redraw |
| C. Commons Bouglé "Human muscular system, anterior-ca" | [Commons][c-bougle] | CC BY-SA 3.0 | Required: Jmarchn; Julien Bouglé plate | As A | 0: an embedded raster `<image>` with 316 label/leader paths on top | None usable | Poor: 19th-century plate, raster | 5.2 MB | Full redraw |
| D. Häggström "Muscles anterior/posterior labeled" | [anterior][c-ant], [posterior][c-post] | Public domain | None required (suggested citation given) | None | 0: PNG raster collage of Gray's plates | n/a | Poor: raster, labelled | 2.4 MB / 0.7 MB PNG | Full trace/redraw |
| E. OpenStax "1105 Anterior and Posterior Views of Muscles" | [Commons][c-openstax] | CC BY 4.0 | Required: OpenStax | None (BY only) | 0: JPG raster (A is the vector redraw of this) | n/a | Raster | 1.7 MB JPG | Full trace (already done by A) |
| F. Servier Medical Art "Musculature front/back" | [front][servier-front], [back][servier-back] | CC BY 4.0 | Required: "Image(s) provided by Servier Medical Art (https://smart.servier.com), licensed under CC BY 4.0" | None (BY only) | Unverified: PNG download (516×1356); vector only inside a PPTX kit made of thousands of freeform shading shapes | Unverified | Detailed fibre shading, poor for flat state colours | 0.36 MB PNG; 3.6 MB PPTX kit | High: convert PPTX freeforms → SVG, rebuild outlines |
| G. wger muscle SVGs | [repo][wger-repo] | Repo AGPL-3.0; the muscle images cite Termininja BY-SA 3.0 as source | Unclear (see notes) | Unclear | 15 muscles (wger API), one overlay SVG per muscle | Coarse | Photographic base (B) | 321 KB / 404 KB base + 16 × ~3 KB | High, and licence is ambiguous |
| H. react-native-body-highlighter | [repo][rnbh-repo] | MIT | Keep copyright + licence notice | None | 23 slugs; 159 paths across both sides (≈31 front / 25 back per side) | Medium: quads ×3, hamstrings ×4, calves ×4, upper-back ×3, triceps ×3 sub-paths, but deltoid/pec/trap are one shape each | Good: clean stylised shapes | 25 KB + 21 KB TS | Low–medium: re-tag sub-paths; React Native component, so reuse path data only |
| I. react-body-highlighter | [repo][rbh-repo] | MIT | Keep notice | None | 22 muscle names, 66 polygons | Coarse (older subset of H) | OK, polygonal | 6 KB | Low but coarse |
| J. react-muscle-highlighter | [repo][rmh-repo] | MIT (no copyright line) | Keep notice | None | Same assets as H (byte-identical) | As H | As H | As H | As H; prefer upstream H |
| K. body-muscles | [repo][bm-repo] | Apache-2.0 | Keep LICENSE + NOTICE, state changes | None | 89 named regions incl. left/right (40 front, 49 back) | Finest naming of the libraries (traps ×3, triceps ×2, hamstrings ×2, gastroc ×2 + soleus, glute med/max, serratus, erectors, QL) | Crude low-poly polygons with gaps | 12.8 KB + 11.9 KB TS | Low: rename/merge L/R; art quality is the cost |

## Per-candidate notes

### A. Commons "Muscles front and back.svg" (recommended)

- **Source and licence.** [File page][c-mfb]. Commons metadata (API `extmetadata`): `LicenseShortName: CC BY-SA 4.0`, `LicenseUrl: https://creativecommons.org/licenses/by-sa/4.0`, `AttributionRequired: true`. The wikitext of the page says: author `OpenStax & [[User:Nefronus|Tomáš Kebert]] & [https://www.umimeto.org umimeto.org]`; description "original drawing by OpenStax (File:1105_Anterior_and_Posterior_Views_of_Muscles.jpg), manually redrawn and modified (escpecially the back view) by Tomáš Kebert & umimeto.org"; licence template `{{self|cc-by-sa-4.0}}`; date 2020-09-13 ([page][c-mfb]). The OpenStax original is CC BY 4.0 ([E](#e-openstax-raster)). CC says BY works "may be incorporated into works that are licensed under CC BY-SA" ([CC FAQ][cc-faq]), so the BY-SA licence on the redraw is valid.
- **Attribution we owe** (CC BY-SA 4.0 §3(a)(1), quoted under [Licence terms](#licence-terms-quoted)): name the creators "OpenStax, Tomáš Kebert and umimeto.org", give the licence name and link, link to the Commons file, and state that we modified it ("split into regions, recoloured, IDs added").
- **Structure (inspected).** 350,482 bytes. Inkscape 1.0 file, `viewBox="0 0 406.99026 354.43411"` with both figures side by side. Element counts: 176 `<path>`, 15 `<g>`, 8 `<use>`, 174 Inkscape spiro `path-effect` defs and 89 `linearGradient`s. There are no `<image>` (raster) elements and no scripts. IDs are all auto-generated (`path1234`, `g2108`): no anatomical names. Each body is drawn as one half, and the other half is a `<use>` clone with `transform="matrix(-1,0,0,1,…)"`. The groups `g2108` (36 paths), `g2165` (57) and `g3482` (60) are cloned this way.
- **Shapes (from a false-colour render with one colour per path).** Each muscle is its own closed, filled path. Identified by eye: rectus abdominis as 4 segments per side, external oblique (front and back), pec major lower portion, deltoid (one shape per view), biceps with a separate dividing sliver, brachialis strip, about 8 forearm shapes, sartorius, rectus femoris, vastus lateralis, vastus medialis, 3 adductor shapes, tibialis anterior, peroneals, the gastrocnemius medial head (front); trapezius (one shape per half, neck to T12), lats, infraspinatus, teres major, triceps long and lateral heads, about 6 forearm extensor shapes, glute max, 4–5 separate hamstring strips (biceps femoris and semitendinosus/semimembranosus), gracilis, both gastrocnemius heads, soleus (back). The muscle ↔ path assignment above is my reading of the render, not a confirmed mapping, so confirm each path when tagging.
- **Quirks.** The upper chest is covered by the same green path as the deltoid (`path` index 69 in my render), so the deltoid and the clavicular pec must be cut apart. The serratus anterior is drawn as four stroke-only lines, so it isn't fillable. The erector spinae lies under a "fascia" strip. Gluteus medius is only a thin sliver.
- **Dark mode / phone.** Flat fills with a thin outline. Recolour muscle paths to the Recovery State colours and the bones, tendons and fascia (`#e5ecef`, `#dbd5c7`, `#fde8cc` today) to dark neutrals. The side-by-side layout (aspect ≈ 1.15:1) fits a phone width. The fingers and face are small but harmless.
- **Mirroring and IDs.** Because the second half is a `<use>` clone, setting `fill` on the original path (by ID) also colours the mirrored side. That is exactly the "both sides show the same state" rule, and region IDs stay unique. One catch: taps on the mirrored side hit the `<use>` element, not the path. Either flatten the clones into real duplicated paths that carry a `data-muscle` attribute, or resolve the tap by hit-testing. This is a build detail for the Anatomical Recovery Map story.

### B. Commons "Muscular system.svg" and "Muscular system-back.svg" (Termininja)

- [Front][c-ms] and [back][c-msb]: `CC BY-SA 3.0`, `AttributionRequired: true`, author Termininja, credited sources `Pectoralis major.png`, `Tibial anterior.png` / `Gastrocnemius.png`, `Latissimus dorsi.png`.
- Inspected: 3,922,457 bytes with 43 paths, and 3,321,999 bytes with 19 paths. The thumbnail shows a posterised trace of a photographic écorché on black, so the paths are colour layers, not muscles. Not usable as a region map.

### C. Commons Bouglé anterior (Catalan labels)

- [File page][c-bougle]: `CC BY-SA 3.0`, author Jmarchn, "Dibuix de Julien Bouglé". Inspected: 5,228,895 bytes, one embedded base64 `<image>` with 316 label/leader paths and 37 `<text>` on top. The artwork itself is raster, and there is only an anterior view in this file (a posterior one exists in the same category). Not usable.

### D. Häggström "Muscles anterior labeled.png" / "Muscle posterior labeled.png"

- [Anterior][c-ant] and [posterior][c-post]: `LicenseShortName: Public domain`, `AttributionRequired: false`. The page suggests the citation "Häggström, Mikael (2014). 'Medical gallery of Mikael Häggström 2014'. WikiJournal of Medicine 1 (2). DOI:10.15347/wjm/2014.008". These are a collage of Gray's Anatomy plates, PNG raster (1664×1632 and 1063×1297) with labels baked in. Public domain is the best licence available, but turning them into regions means tracing every muscle by hand: a redraw, not a split. I found no SVG version in Commons' `Category:SVG human muscular system` ([category][c-cat]).

### E. OpenStax raster

- [File page][c-openstax]: `CC BY 4.0`, artist OpenStax, from *Anatomy and Physiology* (2016). A 1304×3033 JPG, and the source drawing of A. Only relevant as A's upstream: A's attribution must keep OpenStax. `1105 … enko png.svg` (BY-SA 4.0) is that raster wrapped in an SVG with Korean/English labels (an embedded `<image>`, no paths).

### F. Servier Medical Art

- Licence on the site: "All Servier Medical Art illustrations are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)". Recommended credit: "Image(s) provided by Servier Medical Art (https://smart.servier.com), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)" ([how to cite][servier-cite]).
- [Musculature front][servier-front] and [back][servier-back] offer a PNG (`Monsieur_muscles_face.png`, 516×1356) and `SMART-Muscles.pptx`. The PPTX slides are vector freeforms: slides hold 223 to 5,442 shapes each, mostly fibre-shading strokes. **Unverified:** which slide holds the whole-body figures, and whether each muscle has one clean outline. CC BY with no share-alike is attractive, but the fibre-shaded style and the PPTX → SVG cleanup make it high effort.

### G. wger

- Repo licence `AGPL-3.0` (GitHub API, [LICENSE.txt][wger-license]). README: "Application Code: AGPL-3.0-or-later · Exercise/Ingredient Data: Creative Commons (see individual entries) · Documentation: CC-BY-SA-4.0" ([README][wger-readme]).
- `wger/core/static/images/muscles/SOURCES` lists only the two Termininja Commons files (B), so the base images are BY-SA 3.0 derivatives sitting in an AGPL repo. The repo states no separate licence for the per-muscle overlays (`main/muscle-1.svg` … `muscle-16.svg`, about 3 KB and 2 paths each). The wger API lists 15 muscles (anterior deltoid, biceps brachii, biceps femoris, brachialis, gastrocnemius, gluteus maximus, latissimus dorsi, external oblique, pectoralis major, quadriceps femoris, rectus abdominis, serratus anterior, soleus, trapezius, triceps brachii) ([API][wger-api]). Too coarse, and the overlay licence is ambiguous. Not recommended.

### H. react-native-body-highlighter (best library fallback)

- [LICENSE][rnbh-license]: "MIT License · Copyright (c) 2022 ELABBASSI Hicham". It is maintained: 296 stars, last push 2026-09-17, npm `3.2.0` published 2026-04-13 ([npm][rnbh-npm]).
- Source `assets/bodyFront.ts` / `bodyBack.ts` (25,205 / 21,468 bytes). The front has slugs chest, obliques, abs, biceps, triceps, neck, trapezius, deltoids, adductors, quadriceps, knees, tibialis, calves, forearm, hands, ankles, feet, head and hair. The back has neck, trapezius, deltoids, upper-back, triceps, lower-back, forearm, gluteal, adductors, hamstring, calves, ankles, feet, hands, head and hair. In total there are 159 path strings, and many slugs hold several sub-paths per side: quadriceps 3, adductors 3, abs 4, forearm 3–4, hamstring 4, calves 4 (back), triceps 3 (back), upper-back 3. Re-tagging those sub-paths gives rectus femoris / vastus lateralis / vastus medialis, separate hamstrings, the gastrocnemius heads and soleus, and triceps heads. Deltoid, chest and trapezius are a single shape per side.
- It is a React Native component (`react-native-svg`, viewBox `0 0 724 1448` per side), so for our web app we would copy the path data, not the component. MIT allows that if we keep the notice. The repo does not say where the artwork came from (unverified).

### I. react-body-highlighter

- [LICENSE][rbh-license]: "MIT License · Copyright (c) 2020 GV79". The README says "The SVG polygons were leveraged from the React Native package react-native-body-highlighter". Source `src/assets/index.ts`: 28 entries, 66 polygons, with 22 muscle names (`trapezius`, `upper-back`, `lower-back`, `chest`, `biceps`, `triceps`, `forearm`, `back-deltoids`, `front-deltoids`, `abs`, `obliques`, `adductor`, `abductors`, `hamstring`, `quadriceps`, `calves`, `gluteal`, `head`, `neck`, `knees`, `left-soleus`, `right-soleus`). The last npm release is `2.0.5`, published 2021-07-17 ([npm][rbh-npm]), although the repo had a push on 2026-09-20. Too coarse for "finest anatomical detail".

### J. react-muscle-highlighter

- [LICENSE][rmh-license] is MIT with **no copyright line**. Its `assets/bodyFront.ts` is **byte-identical** to H's (checked with `cmp`), and the README never mentions H or Hicham. If we used it, MIT's notice condition would point back to H's copyright anyway, so use H directly.

### K. body-muscles

- [LICENSE][bm-license] is Apache-2.0. [NOTICE][bm-notice]: "Body Muscles · Copyright 2024 Ivan Vulović". Apache §4 requires keeping the NOTICE and marking modified files. Vanilla TypeScript `BodyChart` (not React), npm `1.0.0` published 2026-04-14, 32 stars ([npm][bm-npm]).
- `src/data/muscles.front.ts` / `muscles.back.ts` define 40 + 49 named regions, split left/right. Examples: `traps-upper/mid/lower`, `deltoid-rear`, `shoulder-front`, `shoulder-side`, `chest-upper/lower`, `triceps-long/lateral`, `forearm-flexors/extensors`, `lats-upper/mid/lower`, `lower-back-erectors`, `lower-back-ql`, `gluteus-medius/maximus`, `hamstrings-medial/lateral`, `calves-gastroc-medial/lateral`, `calves-soleus`, `serratus-anterior`, `hip-flexor`, `tibialis-anterior`. The viewBox is only 35×93 units per view. The render shows angular low-poly polygons with white gaps, closer to a wireframe than anatomy. Good naming, weak art. The provenance of the shapes is not documented (unverified).

## Share-alike: does a CC BY-SA asset force the whole repo?

No, provided the artwork stays a distinct file.

- CC BY-SA 4.0 §1(a): "**Adapted Material** means material … derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor." ([legal code][cc-bysa])
- §3(b) applies share-alike only to Adapted Material: "if You Share Adapted Material You produce … The Adapter's License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License." ([legal code][cc-bysa])
- So our **split, recoloured, ID-tagged SVG is Adapted Material** and must be published as CC BY-SA 4.0 (or later).
- Our React component that loads it, and the rest of the repo, are not built from the drawing. Putting them next to it is a collection. CC FAQ: "All Creative Commons licenses … allow licensed material to be included in collections … You may choose a license for the collection, however this does not change the license applicable to the original material", and "CC licenses do not require the collection or the compilation itself to be made available under an SA license" ([CC FAQ][cc-faq]).
- Practical rules: keep the artwork in its own file (e.g. `apps/web/src/recovery-map/body.svg`) with a header comment and a `LICENSE`/`NOTICE` entry naming CC BY-SA 4.0. **Don't** paste its path data into a component `.tsx`, because that would blur the line. CC itself also recommends against CC licences for software ([CC FAQ][cc-faq]). Whether a given change counts as an adaptation "depends primarily on the applicable copyright law" ([CC FAQ][cc-faq]). This is a reading of the licence, not legal advice.

## Licence terms quoted

- **CC BY-SA 4.0 §3(a)(1) Attribution** ([legal code][cc-bysa]). "If You Share the Licensed Material (including in modified form), You must: retain the following if it is supplied by the Licensor … identification of the creator(s) of the Licensed Material …; a copyright notice; a notice that refers to this Public License; a notice that refers to the disclaimer of warranties; a URI or hyperlink to the Licensed Material to the extent reasonably practicable; indicate if You modified the Licensed Material and retain an indication of any previous modifications; and indicate the Licensed Material is licensed under this Public License, and include the text of, or the URI or hyperlink to, this Public License." §3(a)(2): this may be satisfied "in any reasonable manner based on the medium, means, and context … it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information."
- **CC BY-SA 4.0 §3(b) ShareAlike** quoted above, plus: "You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, Adapted Material that restrict exercise of the rights granted under the Adapter's License You apply."
- **CC BY 4.0** (OpenStax, Servier) has the same §3(a) attribution and no §3(b) ([legal code][cc-by]).
- **MIT** (H, I, J): "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." ([H LICENSE][rnbh-license])
- **Apache-2.0** (K) §4: carry prominent notices in modified files, retain copyright notices, and include the NOTICE file ([LICENSE][bm-license]).

## Recommendation

**Adopt A (Commons "Muscles front and back.svg", CC BY-SA 4.0).**

**Licence implications**

1. The tagged SVG lives as its own file under CC BY-SA 4.0. The repo's code licence is unchanged.
2. Attribution goes in three places. First, a comment at the top of the SVG. Second, a `NOTICE`/credits entry in the repo (README "Credits"). Third, an in-app credits line, e.g. on Settings/About, since the PWA "shares" the file:
   > Body diagram adapted from "Muscles front and back" by OpenStax, Tomáš Kebert & umimeto.org (https://commons.wikimedia.org/wiki/File:Muscles_front_and_back.svg), CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). Modified: split into regions, recoloured, IDs added.
3. Anyone may reuse our tagged SVG under BY-SA. That is fine for a portfolio repo.

**How much of the taxonomy it can show** (against the reference list in the ticket)

| Status | Muscles |
|---|---|
| Directly available as their own path(s): rename only | latissimus dorsi; infraspinatus; teres major; triceps long head; triceps lateral head; brachialis (thin strip); forearm flexors (group of ~8 front shapes); forearm extensors (group of ~6 back shapes); rectus abdominis; external oblique; gluteus maximus; rectus femoris; vastus lateralis; vastus medialis; sartorius; adductors (3 shapes); biceps femoris; semitendinosus; semimembranosus; gastrocnemius medial and lateral heads; soleus; tibialis anterior; peroneals |
| Available after we cut an existing shape | deltoid anterior / lateral / posterior (one shape per view today); pectoralis major clavicular vs sternal (the clavicular area shares the deltoid's path); trapezius upper / middle / lower (one shape); biceps long vs short head (one shape plus a dividing sliver) |
| **Gap**: not visible or not fillable in this superficial drawing | triceps medial head; erector spinae (under a thoracolumbar-fascia strip); rhomboids (small sliver under the trapezius); gluteus medius (thin sliver); serratus anterior (stroke lines only); any deep muscle (e.g. psoas, rotator cuff other than infraspinatus/teres) |

So roughly 25–28 of the ~35 reference Muscles work as-is or with a cut, and about 5 are gaps. **Open question for the EXL Muscle taxonomy (EXL-002):** ADR-0006 says Muscle IDs must match region IDs, so a hidden Muscle has no region. The options are: (a) draw a small region for it anyway (e.g. tint the fascia strip as erector spinae, or redraw the serratus as filled digitations), (b) let a hidden Muscle borrow the region of the muscle covering it, or (c) leave it out of the taxonomy. This needs a decision when the taxonomy is written.

**Splitting work** (for the Anatomical Recovery Map story, estimate about 1–2 days of SVG work)

1. Clean up: drop Inkscape metadata, 174 spiro path-effects, 89 gradients and the namedview, then run SVGO with reduced precision. The ~119 KB of raw path data should shrink well below that; I haven't measured the result.
2. Restyle: muscle paths get one class and no inline fill. Bone, tendon, fascia, face and hand shapes get a neutral class for the dark theme.
3. Tag: give each muscle path `id="<muscle-id>"` from the taxonomy (about 60–70 paths). Wrap multi-path Muscles such as forearm groups and rectus abdominis segments in `<g id="<muscle-id>">`.
4. Cut: split the deltoid (×2 views), trapezius, pec/deltoid path and biceps into new paths along anatomical lines.
5. Mirroring: keep the `<use>` clones (colouring the original colours both sides), or flatten them if tap-handling needs real elements.
6. Add a test that every Muscle ID in the Exercise Library has exactly one region in the SVG, and vice versa (ADR-0006).

**If A is rejected**, use H's path data (MIT). It gives clean art and about 30 shapes per view, but deltoid, pec and trapezius are each one shape, so the cuts listed above would be needed there too, and the shapes are more stylised.

## Proposed doc changes (for Liam to approve, not applied)

**`docs/product/roadmap.md`**

- In **MVP**, replace
  `- Recovery Map: **time-only** rules on a **placeholder** body diagram`
  with
  `- Recovery Map: **time-only** rules on the **anatomical** body diagram (licensed SVG, full Muscle detail; ADR-0007)`
- In **v1.1**, delete
  `- Anatomical Recovery Map (licensed SVG, full Muscle detail)`

**`docs/product/features/rec-recovery.md`** (Stories section)

- Delete the **REC: Placeholder Recovery Map** (MVP) story.
- Change **REC: Find a licensed anatomical SVG** to:
  > **REC: Find a licensed anatomical SVG** (MVP, research Task, done)
  > - Findings in `docs/research/anatomical-svg.md`; source recorded in ADR-0007 (Commons "Muscles front and back.svg", CC BY-SA 4.0)
- Change **REC: Anatomical Recovery Map** to:
  > **REC: Anatomical Recovery Map** (MVP, blocked by the EXL Muscle taxonomy)
  > - Front/back diagram from the ADR-0007 SVG; each region ID matches a Muscle ID; tapping a region lists its Muscles, their states and when they were last trained; the same component renders on phone and dashboard
  > - The SVG stays a separate CC BY-SA 4.0 file with attribution in the file, the README credits and the app's About screen

**`docs/product/features/exl-exercise-library.md`** (EXL: Muscle taxonomy story), add a bullet:
  > - Decide how Muscles hidden in the superficial diagram (e.g. triceps medial head, erector spinae, rhomboids, gluteus medius, serratus anterior) get a region; see `docs/research/anatomical-svg.md`

## Unverified / limits

- The muscle ↔ path assignments for A come from a visual read of a false-colour render and need confirming while tagging. The per-view shape counts are estimates.
- Servier: which PPTX slide holds the whole-body figures, and whether each muscle has one clean outline, was not checked.
- Provenance of the artwork in the H, I, J and K libraries: none of their repos states where the shapes came from.
- The licence of wger's per-muscle overlay SVGs is not stated separately from the AGPL repo.
- The size after SVGO cleanup was not measured.
- Commons search covered `Category:SVG human muscular system` and keyword searches. Other categories may hold further SVGs I didn't find.

## Sources

- [c-mfb]: https://commons.wikimedia.org/wiki/File:Muscles_front_and_back.svg (raw: https://upload.wikimedia.org/wikipedia/commons/e/ef/Muscles_front_and_back.svg)
- [c-ms]: https://commons.wikimedia.org/wiki/File:Muscular_system.svg
- [c-msb]: https://commons.wikimedia.org/wiki/File:Muscular_system-back.svg
- [c-bougle]: https://commons.wikimedia.org/wiki/File:Bougle,_Human_muscular_system,_anterior-ca.svg
- [c-ant]: https://commons.wikimedia.org/wiki/File:Muscles_anterior_labeled.png
- [c-post]: https://commons.wikimedia.org/wiki/File:Muscle_posterior_labeled.png
- [c-openstax]: https://commons.wikimedia.org/wiki/File:1105_Anterior_and_Posterior_Views_of_Muscles.jpg
- [c-cat]: https://commons.wikimedia.org/wiki/Category:SVG_human_muscular_system
- Commons metadata via https://commons.wikimedia.org/w/api.php (`prop=imageinfo&iiprop=extmetadata`, `prop=revisions`)
- [servier-front]: https://smart.servier.com/smart_image/musculature-front/
- [servier-back]: https://smart.servier.com/smart_image/musculature-back/
- [servier-cite]: https://smart.servier.com/how-to-cite-servier-medical-art/
- [wger-repo]: https://github.com/wger-project/wger
- [wger-license]: https://github.com/wger-project/wger/blob/master/LICENSE.txt
- [wger-readme]: https://github.com/wger-project/wger/blob/master/README.md
- wger SOURCES: https://github.com/wger-project/wger/blob/master/wger/core/static/images/muscles/SOURCES
- [wger-api]: https://wger.de/api/v2/muscle/
- [rnbh-repo]: https://github.com/HichamELBSI/react-native-body-highlighter
- [rnbh-license]: https://github.com/HichamELBSI/react-native-body-highlighter/blob/main/LICENSE
- [rnbh-npm]: https://registry.npmjs.org/react-native-body-highlighter
- [rbh-repo]: https://github.com/giavinh79/react-body-highlighter
- [rbh-license]: https://github.com/giavinh79/react-body-highlighter/blob/master/LICENSE
- [rbh-npm]: https://registry.npmjs.org/react-body-highlighter
- [rmh-repo]: https://github.com/soroojshehryar/react-muscle-highlighter
- [rmh-license]: https://github.com/soroojshehryar/react-muscle-highlighter/blob/main/LICENSE
- [bm-repo]: https://github.com/vulovix/body-muscles
- [bm-license]: https://github.com/vulovix/body-muscles/blob/main/LICENSE
- [bm-notice]: https://github.com/vulovix/body-muscles/blob/main/NOTICE
- [bm-npm]: https://registry.npmjs.org/body-muscles
- [cc-bysa]: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en
- [cc-by]: https://creativecommons.org/licenses/by/4.0/legalcode.en
- [cc-faq]: https://creativecommons.org/faq/

[c-mfb]: https://commons.wikimedia.org/wiki/File:Muscles_front_and_back.svg
[c-ms]: https://commons.wikimedia.org/wiki/File:Muscular_system.svg
[c-msb]: https://commons.wikimedia.org/wiki/File:Muscular_system-back.svg
[c-bougle]: https://commons.wikimedia.org/wiki/File:Bougle,_Human_muscular_system,_anterior-ca.svg
[c-ant]: https://commons.wikimedia.org/wiki/File:Muscles_anterior_labeled.png
[c-post]: https://commons.wikimedia.org/wiki/File:Muscle_posterior_labeled.png
[c-openstax]: https://commons.wikimedia.org/wiki/File:1105_Anterior_and_Posterior_Views_of_Muscles.jpg
[c-cat]: https://commons.wikimedia.org/wiki/Category:SVG_human_muscular_system
[servier-front]: https://smart.servier.com/smart_image/musculature-front/
[servier-back]: https://smart.servier.com/smart_image/musculature-back/
[servier-cite]: https://smart.servier.com/how-to-cite-servier-medical-art/
[wger-repo]: https://github.com/wger-project/wger
[wger-license]: https://github.com/wger-project/wger/blob/master/LICENSE.txt
[wger-readme]: https://github.com/wger-project/wger/blob/master/README.md
[wger-api]: https://wger.de/api/v2/muscle/
[rnbh-repo]: https://github.com/HichamELBSI/react-native-body-highlighter
[rnbh-license]: https://github.com/HichamELBSI/react-native-body-highlighter/blob/main/LICENSE
[rnbh-npm]: https://registry.npmjs.org/react-native-body-highlighter
[rbh-repo]: https://github.com/giavinh79/react-body-highlighter
[rbh-license]: https://github.com/giavinh79/react-body-highlighter/blob/master/LICENSE
[rbh-npm]: https://registry.npmjs.org/react-body-highlighter
[rmh-repo]: https://github.com/soroojshehryar/react-muscle-highlighter
[rmh-license]: https://github.com/soroojshehryar/react-muscle-highlighter/blob/main/LICENSE
[bm-repo]: https://github.com/vulovix/body-muscles
[bm-license]: https://github.com/vulovix/body-muscles/blob/main/LICENSE
[bm-notice]: https://github.com/vulovix/body-muscles/blob/main/NOTICE
[bm-npm]: https://registry.npmjs.org/body-muscles
[cc-bysa]: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en
[cc-by]: https://creativecommons.org/licenses/by/4.0/legalcode.en
[cc-faq]: https://creativecommons.org/faq/
