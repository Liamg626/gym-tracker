# Research: an openly licensed anatomical front/back SVG for the Recovery Map

SCRUM-8 · [REC-001] · researched 2026-10-16, recommendation updated 2026-10-17 after Liam chose the fitness style

## Question

Which openly licensed front and back muscle-anatomy artwork can the **Recovery Map** use, given that the repo is public, we will split, recolour and add IDs to the artwork, and each region ID must match a **Muscle** ID (ADR-0006)? For each candidate: what licence, attribution and share-alike obligations apply, how many separately addressable muscle shapes it has, whether it suits a phone in dark mode, and how much work it takes to tag it with Muscle IDs. Fallback: existing React body-map libraries.

## Summary and recommendation

**Use the path data from [`react-native-body-highlighter`][rnbh-repo] (H, MIT)**, with the legs rotated outward at the hip for a wider stance, every original colour stripped, all muscles on one grey base and each Muscle coloured by its Recovery State. Liam chose this on 2026-10-17 from a side-by-side comparison of A and H, both greyed and state-coloured (the "Recovery Map artwork options" board in the MVP mobile design artifact). He wanted a **fitness style** like stock "athletic muscle chart" vectors (separated muscle blocks, legs apart), not a medical illustration. Stock art can't be used in a public repo, so it was only a style reference.

- **Licence impact:** MIT. Keep the copyright and permission notice with the artwork. There is no share-alike, so nothing about the repo's licence changes.
- **Taxonomy coverage:** against the provisional Muscle list in [Recommendation](#recommendation), 35 of 40 Muscles work as-is or after a cut. For 3 of those, which sub-path is which still has to be confirmed. 5 are gaps: brachialis, sartorius, gracilis, peroneals, and one of infraspinatus / teres major / rhomboids. Deltoid, pec major, trapezius and biceps are one shape each and need cutting into heads.
- **Runner-up:** A, Wikimedia Commons `Muscles front and back.svg` (OpenStax, redrawn by Tomáš Kebert & umimeto.org, **CC BY-SA 4.0**). It's finer medical anatomy with one closed path per muscle, but it's in a textbook style with the legs together, and share-alike applies. It remains the fallback if H's artwork provenance turns out to be a problem (see [Unverified](#unverified--limits)).

A draft ADR is at `docs/adr/0007-anatomical-svg-source.md` (Status: proposed).

## Comparison

"Shapes" means separately addressable closed shapes. Counts come from inspecting the source (see each candidate's notes).

| Candidate | Source | Licence | Attribution | Share-alike impact | Addressable muscle shapes (front / back) | Granularity vs taxonomy | Dark-mode / phone fit | File size | Effort to add IDs |
|---|---|---|---|---|---|---|---|---|---|
| A. Commons "Muscles front and back.svg" (runner-up) | [Commons file page][c-mfb] | CC BY-SA 4.0 | Required: "OpenStax & Tomáš Kebert & umimeto.org", link, licence, note of changes | Our modified SVG must be BY-SA 4.0. Rest of repo unaffected if the SVG stays a separate file | 176 paths in total, half-figures mirrored. Roughly 35–40 muscle shapes front, 25–30 back (estimate) | **Best**: individual heads/muscles for quads, hamstrings, gastrocnemius, rotator cuff, forearm; deltoid/trap/pec/biceps need cutting | Good: flat fills, recolour per path; neutral shapes need restyling | 350 KB raw (≈119 KB of path data; Inkscape cruft removable) | Medium: name about 65 paths, cut about 5 shapes, strip gradients and path-effects |
| B. Commons "Muscular system.svg" / "-back.svg" (Termininja), also wger's base images | [front][c-ms], [back][c-msb] | CC BY-SA 3.0 | Required: Termininja + source files | As A (BY-SA) | Not addressable: 43 / 19 paths are posterised colour layers of a traced photo | None usable | Poor: photographic red-on-black texture | 3.9 MB / 3.3 MB | Full redraw |
| C. Commons Bouglé "Human muscular system, anterior-ca" | [Commons][c-bougle] | CC BY-SA 3.0 | Required: Jmarchn; Julien Bouglé plate | As A | 0: an embedded raster `<image>` with 316 label/leader paths on top | None usable | Poor: 19th-century plate, raster | 5.2 MB | Full redraw |
| D. Häggström "Muscles anterior/posterior labeled" | [anterior][c-ant], [posterior][c-post] | Public domain | None required (suggested citation given) | None | 0: PNG raster collage of Gray's plates | n/a | Poor: raster, labelled | 2.4 MB / 0.7 MB PNG | Full trace/redraw |
| E. OpenStax "1105 Anterior and Posterior Views of Muscles" | [Commons][c-openstax] | CC BY 4.0 | Required: OpenStax | None (BY only) | 0: JPG raster (A is the vector redraw of this) | n/a | Raster | 1.7 MB JPG | Full trace (already done by A) |
| F. Servier Medical Art "Musculature front/back" | [front][servier-front], [back][servier-back] | CC BY 4.0 | Required: "Image(s) provided by Servier Medical Art (https://smart.servier.com), licensed under CC BY 4.0" | None (BY only) | Unverified: PNG download (516×1356); vector only inside a PPTX kit made of thousands of freeform shading shapes | Unverified | Detailed fibre shading, poor for flat state colours | 0.36 MB PNG; 3.6 MB PPTX kit | High: convert PPTX freeforms → SVG, rebuild outlines |
| G. wger muscle SVGs | [repo][wger-repo] | Repo AGPL-3.0; the muscle images cite Termininja BY-SA 3.0 as source | Unclear (see notes) | Unclear | 15 muscles (wger API), one overlay SVG per muscle | Coarse | Photographic base (B) | 321 KB / 404 KB base + 16 × ~3 KB | High, and licence is ambiguous |
| **H. react-native-body-highlighter (chosen)** | [repo][rnbh-repo] | MIT | Keep copyright + licence notice | None | 23 slugs; 159 paths across both views (per side: 29 front / 25 back muscle paths) | Medium: quads ×3, hamstrings ×4, calves ×4, upper-back ×3, triceps ×3 sub-paths, but deltoid/pec/trap are one shape each | Good: clean stylised shapes | 25 KB + 21 KB TS | Low–medium: re-tag sub-paths; React Native component, so reuse path data only |
| I. react-body-highlighter | [repo][rbh-repo] | MIT | Keep notice | None | 22 muscle names, 66 polygons | Coarse (older subset of H) | OK, polygonal | 6 KB | Low but coarse |
| J. react-muscle-highlighter | [repo][rmh-repo] | MIT (no copyright line) | Keep notice | None | Same assets as H (byte-identical) | As H | As H | As H | As H; prefer upstream H |
| K. body-muscles | [repo][bm-repo] | Apache-2.0 | Keep LICENSE + NOTICE, state changes | None | 89 named regions incl. left/right (40 front, 49 back) | Finest naming of the libraries (traps ×3, triceps ×2, hamstrings ×2, gastroc ×2 + soleus, glute med/max, serratus, erectors, QL) | Crude low-poly polygons with gaps | 12.8 KB + 11.9 KB TS | Low: rename/merge L/R; art quality is the cost |

## Per-candidate notes

### A. Commons "Muscles front and back.svg" (runner-up)

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

### H. react-native-body-highlighter (chosen)

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

This only matters if we fall back to A; H is MIT. In short: no, provided the artwork stays a distinct file.

- CC BY-SA 4.0 §1(a): "**Adapted Material** means material … derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor." ([legal code][cc-bysa])
- §3(b) applies share-alike only to Adapted Material: "if You Share Adapted Material You produce … The Adapter's License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License." ([legal code][cc-bysa])
- So our **split, recoloured, ID-tagged SVG is Adapted Material** and must be published as CC BY-SA 4.0 (or later).
- Our React component that loads it, and the rest of the repo, are not built from the drawing, so under CC's FAQ putting them next to it should count as a collection, though the FAQ notes this depends on the applicable copyright law. CC FAQ: "All Creative Commons licenses … allow licensed material to be included in collections … You may choose a license for the collection, however this does not change the license applicable to the original material", and "CC licenses do not require the collection or the compilation itself to be made available under an SA license" ([CC FAQ][cc-faq]).
- Practical rules: keep the artwork in its own file (e.g. `apps/web/src/recovery-map/body.svg`) with a header comment and a `LICENSE`/`NOTICE` entry naming CC BY-SA 4.0. **Don't** paste its path data into a component `.tsx`, because that would blur the line. CC itself also recommends against CC licences for software ([CC FAQ][cc-faq]). Whether a given change counts as an adaptation "depends primarily on the applicable copyright law" ([CC FAQ][cc-faq]). This is a reading of the licence, not legal advice.

## Licence terms quoted

- **CC BY-SA 4.0 §3(a)(1) Attribution** ([legal code][cc-bysa]). "If You Share the Licensed Material (including in modified form), You must: retain the following if it is supplied by the Licensor … identification of the creator(s) of the Licensed Material …; a copyright notice; a notice that refers to this Public License; a notice that refers to the disclaimer of warranties; a URI or hyperlink to the Licensed Material to the extent reasonably practicable; indicate if You modified the Licensed Material and retain an indication of any previous modifications; and indicate the Licensed Material is licensed under this Public License, and include the text of, or the URI or hyperlink to, this Public License." §3(a)(2): this may be satisfied "in any reasonable manner based on the medium, means, and context … it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information."
- **CC BY-SA 4.0 §3(b) ShareAlike** quoted above, plus: "You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, Adapted Material that restrict exercise of the rights granted under the Adapter's License You apply."
- **CC BY 4.0** (OpenStax, Servier) has the same §3(a) attribution and no §3(b) ([legal code][cc-by]).
- **MIT** (H, I, J): "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." ([H LICENSE][rnbh-license])
- **Apache-2.0** (K) §4: carry prominent notices in modified files, retain copyright notices, and include the NOTICE file ([LICENSE][bm-license]).

## Recommendation

**Adopt H: the `react-native-body-highlighter` path data (MIT), restyled.** Liam chose it on 2026-10-17 from a greyed, state-coloured comparison with A, preferring its fitness style and a wider stance.

**What we do to it**

1. **Copy the path data, not the component.** It's a React Native component, so we take only the shapes from `assets/bodyFront.ts` / `bodyBack.ts` into our own SVG file (e.g. `apps/web/src/recovery-map/body.svg`).
2. **Widen the stance.** Rotate every leg shape (quadriceps, adductors, knees, tibialis, calves, ankles, feet, hamstring) about 5° outward around its hip, and bake the transform into the paths. The comparison board used 5°.
3. **Strip the original colours.** Every muscle starts on one grey base (`#4A515C`). Head, hair, neck, hands, feet, knees and ankles get a darker neutral (`#262B33`). Stroke in the card background colour, so the dark gaps between the muscle blocks read as separations.
4. **Colour by Recovery State at runtime.** Each region carries its Muscle ID. The component sets the fill from the Muscle's Recovery State (Fatigued, Recovering, Ready), and a Muscle with no data stays grey. No state colours live in the SVG file.
5. **Left and right sides.** H draws both sides as separate paths (`left` / `right` arrays). Both get the same Muscle ID (e.g. via `data-muscle`), so both colour together, which fits the "no left/right split" rule.

**Licence implications**

1. MIT: "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." ([LICENSE][rnbh-license])
2. Keep the notice (`Copyright (c) 2022 ELABBASSI Hicham` plus the MIT permission text) in a comment at the top of the SVG file, and in a third-party notices section of the README. Build tools (SVGO, inlining, upload sanitisers) strip comments, so the README notice and the in-app line are what cover the shipped copy. Because the PWA ships the file, also list it on an in-app About/licences line:
   > Body diagram adapted from react-native-body-highlighter by ELABBASSI Hicham (https://github.com/HichamELBSI/react-native-body-highlighter), MIT licence. Modified: legs repositioned, recoloured, regions split and tagged with Muscle IDs.
3. No share-alike: the modified file can sit under the repo's own licence, and the [Share-alike](#share-alike-does-a-cc-by-sa-asset-force-the-whole-repo) section only applies if we ever fall back to A.

**How much of the taxonomy it can show**

The Muscle taxonomy (EXL-002, SCRUM-7) isn't written yet. The list below is this doc's own **provisional** list of 40 Muscles, and coverage must be rechecked against the real taxonomy.

| Status | Muscles (count) |
|---|---|
| Re-tag an existing sub-path | latissimus dorsi; triceps long, lateral and medial heads (3 back sub-paths); forearm flexors (front, 3 sub-paths); forearm extensors (back, 4); rectus abdominis (4 segments); external oblique (front sub-paths); gluteus maximus and gluteus medius (2 gluteal sub-paths); rectus femoris, vastus lateralis and vastus medialis (3 quadriceps sub-paths); adductors (3); biceps femoris, semitendinosus and semimembranosus (4 hamstring sub-paths); gastrocnemius medial and lateral heads and soleus (4 back calf sub-paths); tibialis anterior; erector spinae (2 lower-back sub-paths). **22** |
| Probably available, sub-path to confirm | two of infraspinatus / teres major / rhomboids (the 2 non-lat upper-back sub-paths); serratus anterior (the upper of the 8 front oblique sub-paths look like digitations). **3** |
| Available after we cut an existing shape | deltoid anterior / lateral / posterior (one shape per view); pectoralis major clavicular vs sternal (one shape); trapezius upper / middle / lower (one shape per view); biceps long vs short head (one shape). **10** |
| **Gap**: no shape in H | brachialis; sartorius; gracilis; peroneals; the third of infraspinatus / teres major / rhomboids. **5** |

So **35 of the 40 provisional Muscles** can be shown, 3 of them pending confirmation, and 5 are gaps. **Open question for EXL-002:** ADR-0006 says Muscle IDs must match region IDs, so a Muscle without a shape needs a decision. The options are: (a) draw a small region for it, (b) let it borrow the region of a neighbouring muscle (e.g. brachialis with biceps), or (c) leave it out of the taxonomy.

**Splitting work** (for the Anatomical Recovery Map story; estimate about 1 day of SVG work)

1. Extract the paths into one SVG with a front view and a back view, apply the leg rotation, drop H's colours and the `hair` shapes if unwanted.
2. Tag: give each region its Muscle ID; group multi-path Muscles (e.g. rectus abdominis segments) under one ID.
3. Cut: split deltoid (×2 views), chest, trapezius (×2 views) and biceps along anatomical lines.
4. Add a test that every Muscle ID in the Exercise Library has a region in the SVG, and vice versa (ADR-0006).

**If H has to be dropped** (e.g. its artwork provenance turns out to be a problem), fall back to A: CC BY-SA 4.0, kept as a separate file with attribution (see A's notes and the Share-alike section). The credit would read "Body diagram adapted from 'Muscles front and back' by OpenStax, Tomáš Kebert & umimeto.org, redrawn from OpenStax *Anatomy and Physiology* (CC BY 4.0); CC BY-SA 4.0; modified".

## Proposed doc changes (for Liam to approve, not applied)

**`docs/product/roadmap.md`**

- In **MVP**, replace
  `- Recovery Map: **time-only** rules on a **placeholder** body diagram`
  with
  `- Recovery Map: **time-only** rules on the **anatomical** body diagram (fitness-style front/back SVG, ADR-0007)`
- In **v1.1**, delete
  `- Anatomical Recovery Map (licensed SVG, full Muscle detail)`

**`docs/product/features/rec-recovery.md`** (Stories section)

- Delete the **REC: Placeholder Recovery Map** (MVP) story.
- Change **REC: Find a licensed anatomical SVG** to:
  > **REC: Find a licensed anatomical SVG** (MVP, research Task)
  > - Findings in `docs/research/anatomical-svg.md`; source recorded in ADR-0007 (react-native-body-highlighter path data, MIT)
- Change **REC: Anatomical Recovery Map** to:
  > **REC: Anatomical Recovery Map** (MVP, blocked by the EXL Muscle taxonomy)
  > - Front/back diagram from the ADR-0007 artwork, legs widened, grey base; each region ID matches a Muscle ID and is coloured by its Recovery State, and a Muscle with no Working Sets yet stays grey (no state); tapping a region lists its Muscles, their states and when they were last trained; the same component renders on phone and dashboard
  > - The MIT notice is kept in the SVG file, the README third-party notices and the app's About screen

**`docs/product/features/exl-exercise-library.md`** (EXL: Muscle taxonomy story), add a bullet:
  > - Decide how Muscles with no shape in the Recovery Map artwork (e.g. brachialis, sartorius, peroneals) get a region; see `docs/research/anatomical-svg.md`

## Unverified / limits

- **H's artwork provenance:** the repo doesn't say where the shapes came from. MIT is only as good as the author's right to grant it. If a source with conflicting terms turns up, fall back to A.
- Which of H's sub-paths is which muscle (e.g. the upper-back and oblique sub-paths) comes from the slug names and a render, and needs confirming while tagging.
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
