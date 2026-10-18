# Research: the Muscle taxonomy for the Exercise Library and the Recovery Map

SCRUM-7 · [EXL-002] · researched 2026-10-17

## Question

Which skeletal **Muscles** should the app know about, and at what anatomical detail? For each Muscle: a stable kebab-case ID, a display name, the side of the **Recovery Map** it shows on (front, back or both) and a roll-up group for summaries. Where do common sources split muscles differently, and which convention do we follow? And because ADR-0006 says Muscle IDs must match region IDs in the Recovery Map artwork, how does each Muscle map onto the react-native-body-highlighter shapes chosen in ADR-0007, and what happens to a Muscle with no shape?

The rule used for "how much detail": split a muscle into heads or parts only where they can be **trained or fatigued differently** or are **visibly distinct on a front/back diagram**. Leave out muscles that can't be seen and can't be targeted on their own, or say why they stay.

## Summary and recommendation

- **46 Muscles in 11 groups** (41 in 9 before SCRUM-22; 48 after Phase 1; 46 since Liam merged the biceps heads and brachialis into `biceps-brachii` on 2026-10-18). Groups: chest, shoulders, back, biceps, triceps, forearms, core, hips, quads, hamstrings, lower legs. "Legs" is split four ways because 20 of the 48 Muscles are in the legs, and quads, hamstrings and hips respond to different exercises (e.g. squats grow the vasti, adductors and glutes but not the rectus femoris or hamstrings ([Kubo 2019][kubo2019])). One "legs" group would hide that.
- **Conventions:** deltoid in 3 parts (anterior/lateral/posterior); pectoralis major in 2 heads (clavicular, sternocostal; the small abdominal part goes with sternocostal); trapezius upper/middle/lower (= Terminologia Anatomica descending/transverse/ascending); latissimus dorsi as one Muscle; quadriceps shown as 3 (vastus intermedius left out, it is deep); hamstrings as 4 (biceps femoris long and short head, semitendinosus, semimembranosus); gastrocnemius medial and lateral head plus soleus; erector spinae as one Muscle; forearm as flexors, extensors and brachioradialis; external oblique only; adductors as one group Muscle. [Superseded where it differs: the vastus intermedius, rhomboids, teres minor, gluteus minimus, internal oblique, gracilis and supraspinatus bullets above were later added as Muscles by SCRUM-22 Phase 1, and "arms" is now Biceps, Triceps and Forearms.] Details and sources are in [Source disagreements](#source-disagreements-and-the-convention-we-follow).
- **Artwork fit** (written for the original 41; Phase 3 of SCRUM-22 confirms the reads). Re-tagging and cutting the existing react-native-body-highlighter shapes gives **38 of the 41** Muscles their own region. Brachialis gets one new sliver, and 2 Muscles share a neighbour's region. Several gaps from the SVG research turn out to have a shape after all: sartorius and gracilis look like sub-paths inside the `adductors` slug, the fibularis (peroneals) like the outer `calves` sub-path on the front, and infraspinatus and teres major are two of the three `upper-back` sub-paths.
- **No-shape Muscles (proposal for Liam).** Brachialis gets a small region cut from the biceps shape, since we are cutting the biceps anyway. Biceps femoris short head and iliopsoas share a neighbour's region. Rhomboids, vastus intermedius, gluteus minimus, teres minor, internal oblique and gracilis were first left out; SCRUM-22 Phase 1 added them back as Muscles that share a neighbour's Region, along with supraspinatus (see [Phase 1](#phase-1-every-gym-trained-muscle-visible-scrum-22-approved-by-liam-2026-10-17-and-applied-above)). See [No-shape recommendations](#no-shape-muscles-recommendation-per-muscle-proposal-for-liam).
- **This needs one change to how ADR-0006 is read.** "Muscle IDs must match region IDs" works only if a region may carry **more than one** Muscle ID, and the map shows the **worst** Recovery State among them. The proposal is to keep a mapping table (region → Muscle IDs) and test that every Muscle has at least one region and every region has at least one Muscle. Wording is in [Proposed doc changes](#proposed-doc-changes-for-liam-to-approve-not-applied).

## Proposed taxonomy

"Side" means which view of the Recovery Map shows the Muscle: front, back or both. "Art" is the short form of the react-native-body-highlighter mapping (full table in [Recovery Map region mapping](#recovery-map-region-mapping-scrum-22-phase-3)). Display names use the anatomical name first, with the gym name in brackets where it helps.

| # | ID | Display name | Side | Group | Art | Inclusion reason / source |
|---|---|---|---|---|---|---|
| 1 | `pectoralis-major-clavicular` | Pectoralis major, clavicular head (upper chest) | front | chest | cut from `chest` | Separate head that also flexes the arm on its own ([TeachMe pectoral][tma-pect]); peak EMG at a 30° incline ([Rodríguez-Ridao 2020][rr2020]); incline press grew upper-chest thickness more ([Chaves 2020][chaves2020]) |
| 2 | `pectoralis-major-sternal` | Pectoralis major, sternocostal head (mid and lower chest) | front | chest | cut from `chest` | Main head; middle and lower portions peak flat (0°) ([Rodríguez-Ridao 2020][rr2020]). Includes the small abdominal part ([Kenhub][kh-pect]) |
| 3 | `serratus-anterior` | Serratus anterior | front | chest | `obliques` sub-paths | Visible on the side of the ribcage; protracts and rotates the scapula ([TeachMe pectoral][tma-pect], [StatPearls][sp-serratus]) |
| 4 | `deltoid-anterior` | Deltoid, anterior part (front delt) | front | shoulders | cut from `deltoids` (front) | Flexion and medial rotation ([TeachMe shoulder][tma-shoulder]); most active in shoulder press ([Campos 2020][campos2020]) |
| 5 | `deltoid-lateral` | Deltoid, lateral part (side delt) | both | shoulders | cut from `deltoids` (front and back) | Main abductor ([TeachMe shoulder][tma-shoulder]); almost silent in bench press and flyes, high in lateral raise ([Campos 2020][campos2020]) |
| 6 | `deltoid-posterior` | Deltoid, posterior part (rear delt) | back | shoulders | cut from `deltoids` (back) | Extension and lateral rotation ([TeachMe shoulder][tma-shoulder]); its own exercises (reverse fly, face pull) |
| 7 | `infraspinatus` | Infraspinatus | back | shoulders | `upper-back` sub-path | The visible rotator cuff muscle; lateral rotation ([TeachMe shoulder][tma-shoulder], [OpenStax 11.5][os-115]). Teres minor folded in (same action) [superseded: `teres-minor` is its own Muscle, #45, SCRUM-22 Phase 1] |
| 8 | `trapezius-upper` | Trapezius, upper part (upper traps) | both | back | `trapezius` (front) + cut from `trapezius` (back) | Elevates the scapula (shrugs) ([TeachMe superficial back][tma-back]); TA "descending part" ([TA2][ta2-trap]) |
| 9 | `trapezius-middle` | Trapezius, middle part (mid traps) | back | back | cut from `trapezius` (back) | Retracts the scapula (rows) ([TeachMe superficial back][tma-back]); TA "transverse part" |
| 10 | `trapezius-lower` | Trapezius, lower part (lower traps) | back | back | cut from `trapezius` (back) | Depresses the scapula ([TeachMe superficial back][tma-back]); TA "ascending part" ([TA2][ta2-trap-asc]) |
| 11 | `latissimus-dorsi` | Latissimus dorsi (lats) | back | back | `upper-back` sub-path | Extends, adducts and medially rotates the arm ([TeachMe superficial back][tma-back]); pull-ups, rows |
| 12 | `teres-major` | Teres major | back | back | `upper-back` sub-path | Visible below the infraspinatus; extends, adducts and medially rotates the arm with the lats ([TeachMe shoulder][tma-shoulder], [StatPearls][sp-teresmajor]) |
| 13 | `erector-spinae` | Erector spinae (lower back) | back | back | `lower-back` sub-paths | Iliocostalis, longissimus and spinalis act together as one column to extend the spine ([TeachMe intrinsic back][tma-intrinsic], [StatPearls][sp-backmuscles]) |
| 14 | `biceps-brachii` | Biceps brachii (biceps) | front | biceps | `biceps` | The main elbow flexor and supinator, crossing the shoulder through its long head ([TeachMe upper arm][tma-arm]). Stands for both heads and for brachialis, which lies deep to it and is trained by every curl. Merged into one Muscle by Liam on 2026-10-18; earlier this row was three Muscles (long head, short head, brachialis) |
| 15 | — | (merged into `biceps-brachii`, 2026-10-18) | | | | |
| 16 | — | (merged into `biceps-brachii`, 2026-10-18) | | | | |
| 17 | `brachioradialis` | Brachioradialis | front | forearms | `forearm` (front) sub-path | Elbow flexor despite extensor origin ([TeachMe posterior forearm][tma-postfa]); its share changes with grip ([Kleiber 2015][kleiber2015], [Coratella 2023][coratella2023]) |
| 18 | `triceps-brachii-long-head` | Triceps brachii, long head | both | triceps | `triceps` (front) + `triceps` (back) sub-path | The only head that crosses the shoulder, so overhead work stretches it ([TeachMe upper arm][tma-arm]); overhead extensions grew it more than pushdowns did (+28.5% vs +19.6%), though the other heads gained too ([Maeo 2023][maeo2023]) |
| 19 | `triceps-brachii-lateral-head` | Triceps brachii, lateral head | back | triceps | `triceps` (back) sub-path | Visibly distinct; one-joint head ([StatPearls triceps][sp-triceps], [Maeo 2023][maeo2023]) |
| 20 | `triceps-brachii-medial-head` | Triceps brachii, medial head | both | triceps | `triceps` (back) sub-path + `triceps` (front), shared | Third head; mostly covered by the other two ([TeachMe upper arm][tma-arm]). Kept because the artwork has a third triceps shape |
| 21 | `forearm-flexors` | Forearm flexors (wrist and finger flexors) | front | forearms | `forearm` (front) sub-paths | Anterior compartment, flexes wrist and fingers ([TeachMe anterior forearm][tma-antfa], [OpenStax 11.5][os-115]); grip and wrist curls |
| 22 | `forearm-extensors` | Forearm extensors (wrist and finger extensors) | back | forearms | `forearm` (back) sub-paths | Posterior compartment ([TeachMe posterior forearm][tma-postfa], [OpenStax 11.5][os-115]); reverse curls, wrist extensions |
| 23 | `rectus-abdominis` | Rectus abdominis (abs) | front | core | `abs` sub-paths | One muscle segmented by tendinous intersections ([OpenStax 11.4][os-114]) |
| 24 | `external-oblique` | External oblique (obliques) | both | core | `obliques` sub-paths (front) + `lower-back` sub-path (back) | Superficial; twisting and side bending ([OpenStax 11.4][os-114]). Internal oblique folded in [superseded: `internal-oblique` is its own Muscle, #47, SCRUM-22 Phase 1] |
| 25 | `gluteus-maximus` | Gluteus maximus | back | hips | `gluteal` sub-path | Main hip extensor ([TeachMe gluteal][tma-glute]); grew with squats ([Kubo 2019][kubo2019]) |
| 26 | `gluteus-medius` | Gluteus medius | back | hips | `gluteal` sub-path | Abducts and medially rotates the hip ([TeachMe gluteal][tma-glute]); different exercises from maximus (abduction). Minimus folded in [superseded: `gluteus-minimus` is its own Muscle, #44, SCRUM-22 Phase 1] |
| 27 | `adductors` | Adductors (longus, brevis, magnus) | both | hips | `adductors` sub-paths (front and back) | Medial thigh group that adducts the hip ([OpenStax 11.6][os-116], [TeachMe medial thigh][tma-medthigh]); grew with full squats ([Kubo 2019][kubo2019]) |
| 28 | `iliopsoas` | Iliopsoas (hip flexors) | front | hips | no shape: shares the `rectus-femoris` region | Psoas major + iliacus, flexes the hip ([OpenStax 11.6][os-116], [TeachMe anterior thigh][tma-antthigh]); main mover in leg raises |
| 29 | `rectus-femoris` | Rectus femoris | front | quads | `quadriceps` sub-path | Only quadriceps head crossing the hip ([TeachMe anterior thigh][tma-antthigh]); no growth from squats ([Kubo 2019][kubo2019]) but the most growth from knee extensions ([Wakahara 2017][wakahara2017]) |
| 30 | `vastus-lateralis` | Vastus lateralis (outer quad) | both | quads | `quadriceps` (front) sub-path + `hamstring` (back) outer sub-path | Largest quadriceps component ([StatPearls VL][sp-vl]); visibly distinct |
| 31 | `vastus-medialis` | Vastus medialis (teardrop) | front | quads | `quadriceps` sub-path | Visibly distinct ("teardrop"); knee extensor ([OpenStax 11.6][os-116]) |
| 32 | `sartorius` | Sartorius | front | quads | `adductors` (front) sub-path | Visible strap across the thigh; anterior compartment; flexes hip and knee ([OpenStax 11.6][os-116], [TeachMe anterior thigh][tma-antthigh]) |
| 33 | `biceps-femoris-long-head` | Biceps femoris, long head | back | hamstrings | `hamstring` sub-path | Two-joint head; hip extension training grew it more than Nordics ([Bourne 2017][bourne2017]) |
| 34 | `biceps-femoris-short-head` | Biceps femoris, short head | back | hamstrings | no shape: shares the `biceps-femoris-long-head` region | Arises from the femur, so knee flexion only ([TeachMe hamstrings][tma-ham], [StatPearls hamstring][sp-ham]); hip hinges don't train it, leg curls do |
| 35 | `semitendinosus` | Semitendinosus | back | hamstrings | `hamstring` sub-path | Superficial medial hamstring ([TeachMe hamstrings][tma-ham]); grew more with isometric hip extension, a borderline result (p = 0.054) ([Carmichael 2022][carmichael2022]) |
| 36 | `semimembranosus` | Semimembranosus | back | hamstrings | `hamstring` inner sub-path, shared with gracilis | Deep to semitendinosus ([TeachMe hamstrings][tma-ham]); the artwork appears to draw a separate inner strip for it; grew with eccentric hip extension ([Carmichael 2022][carmichael2022]) |
| 37 | `gastrocnemius-medial-head` | Gastrocnemius, medial head | both | lower-legs | `calves` (back) sub-path + `calves` (front) inner sub-path | Two-joint; grows with straight-leg, not seated, calf raises ([Kinoshita 2023][kinoshita2023]) |
| 38 | `gastrocnemius-lateral-head` | Gastrocnemius, lateral head | back | lower-legs | `calves` (back) sub-path | As above; heads respond differently to foot position ([Nunes 2020][nunes2020]) |
| 39 | `soleus` | Soleus | both | lower-legs | `calves` (back) lower sub-paths | Deep to gastrocnemius, acts only at the ankle ([TeachMe posterior leg][tma-postleg]); bent-knee calf raises favour it ([Kassiano 2023][kassiano2023]) |
| 40 | `tibialis-anterior` | Tibialis anterior | front | lower-legs | `tibialis` | Visible on the shin; lifts the front of the foot ([OpenStax 11.6][os-116]); tib raises |
| 41 | `fibularis` | Fibularis (peroneus) longus and brevis | front | lower-legs | `calves` (front) outer sub-path | The lateral compartment; eversion ([TeachMe lateral leg][tma-latleg], [OpenStax 11.6][os-116]). Kept because the artwork appears to draw it |
| 42 | `rhomboids` | Rhomboids (major and minor) | back | back | shares `trapezius-middle` region | Deep to trapezius ([StatPearls rhomboids][sp-rhomboid]); every row and reverse fly. Added in SCRUM-22 Phase 1 |
| 43 | `vastus-intermedius` | Vastus intermedius | front | quads | shares `vastus-lateralis` region | Between the vasti, deep to rectus femoris ([OpenStax 11.6][os-116]); tag with the other vasti, never rectus femoris alone ([Kubo 2019][kubo2019]). SCRUM-22 Phase 1 |
| 44 | `gluteus-minimus` | Gluteus minimus | back | hips | shares `gluteus-medius` region | Same shape and function as medius ([TeachMe gluteal][tma-glute]). SCRUM-22 Phase 1 |
| 45 | `teres-minor` | Teres minor | back | shoulders | shares `infraspinatus` region | Rotator cuff, lateral rotation ([TeachMe shoulder][tma-shoulder]). SCRUM-22 Phase 1 |
| 46 | `supraspinatus` | Supraspinatus | back | shoulders | shares `infraspinatus` region | Rotator cuff; starts abduction ([OpenStax 11.5][os-115]). SCRUM-22 Phase 1 |
| 47 | `internal-oblique` | Internal oblique | front | core | shares `external-oblique` region | Twisting and side bending, under the external oblique ([OpenStax 11.4][os-114]). SCRUM-22 Phase 1 |
| 48 | `gracilis` | Gracilis | both | hips | shares `adductors` region (own Region in Phase 3 if the sliver confirms) | Adductor-group strap ([TeachMe medial thigh][tma-medthigh]). SCRUM-22 Phase 1 |

Group counts: chest 3, shoulders 6, back 7, biceps 1, triceps 3, forearms 3, core 3, hips 6, quads 5, hamstrings 4, lower-legs 5 (46 Muscles in 11 groups after the 2026-10-18 biceps merge; Phase 1 of SCRUM-22).

### The group set

| Group ID | Display name | Muscles |
|---|---|---|
| `chest` | Chest | 1–3 |
| `shoulders` | Shoulders | 4–7, 45, 46 |
| `back` | Back | 8–13, 42 |
| `biceps` | Biceps | 14 |
| `triceps` | Triceps | 18–20 |
| `forearms` | Forearms | 17, 21, 22 |
| `core` | Core | 23–24, 47 |
| `hips` | Glutes and hips | 25–28, 44, 48 |
| `quads` | Quads | 29–32, 43 |
| `hamstrings` | Hamstrings | 33–36 |
| `lower-legs` | Calves and shins | 37–41 |

Why this set:

- **Legs split four ways.** The leg groups get different exercises (squat vs leg curl vs calf raise) and grow differently: squats grew the vasti, adductors and gluteus maximus but not rectus femoris or the hamstrings ([Kubo 2019][kubo2019]). A single "legs" group in the Weekly Breakdown or the Exercise picker filter would lump 17 Muscles together [as first written; 20 after SCRUM-22 Phase 1] and hide a missed hamstring day.
- **"Hips" instead of "glutes".** The adductors and iliopsoas need a home. They act at the hip, so "Glutes and hips" fits better than putting them in quads or hamstrings.
- **Sartorius in quads.** It sits in the anterior compartment of the thigh with the quadriceps ([TeachMe anterior thigh][tma-antthigh]).
- **Serratus anterior in chest.** It is worked by pressing and push-ups and sits next to the pec on the diagram. Core would also be defensible.
- **Infraspinatus in shoulders, teres major in back.** Infraspinatus is rotator cuff (a shoulder rotator); teres major works with the lats.
- **Arms split three ways (SCRUM-22 Phase 1, Liam).** One "arms" group lumped 9 Muscles and hid a missed triceps day; Biceps, Triceps and Forearms are separate groups. Groups are only a roll-up, so this stays easy to change.

One catch for **Volume by group**: a Working Set of bench press is attributed to both pectoralis Muscles. If group Volume is a plain sum over Muscles, chest Volume counts that Set twice. Group Volume should count each Working Set once per group. This is flagged in [Proposed doc changes](#proposed-doc-changes-for-liam-to-approve-not-applied).

## Front and back visibility

| View | Muscles |
|---|---|
| **Front only** (16) | pectoralis-major-clavicular, pectoralis-major-sternal, serratus-anterior, deltoid-anterior, biceps-brachii, brachioradialis, forearm-flexors, rectus-abdominis, iliopsoas, rectus-femoris, vastus-medialis, sartorius, tibialis-anterior, fibularis, vastus-intermedius, internal-oblique |
| **Back only** (20) | deltoid-posterior, infraspinatus, trapezius-middle, trapezius-lower, latissimus-dorsi, teres-major, erector-spinae, triceps-brachii-lateral-head, forearm-extensors, gluteus-maximus, gluteus-medius, biceps-femoris-long-head, biceps-femoris-short-head, semitendinosus, semimembranosus, gastrocnemius-lateral-head, rhomboids, gluteus-minimus, teres-minor, supraspinatus |
| **Both** (10) | deltoid-lateral, trapezius-upper, triceps-brachii-long-head, triceps-brachii-medial-head, external-oblique, adductors, vastus-lateralis, gastrocnemius-medial-head, soleus, gracilis |

So: 16 front only + 20 back only + 10 both = 46 (after the Phase 3 region checks).

## Source disagreements and the convention we follow

> **Superseded in part (SCRUM-22 Phase 1, approved by Liam 2026-10-17).** This table is the 41-Muscle convention as first written for SCRUM-7. The [Phase 1 section](#phase-1-every-gym-trained-muscle-visible-scrum-22-approved-by-liam-2026-10-17-and-applied-above) overrides it where they differ (and since 2026-10-18 the biceps is one Muscle, `biceps-brachii`): for example teres minor, rhomboids, vastus intermedius, gluteus minimus, internal oblique, gracilis and supraspinatus are now their own Muscles (48 in total), and Arms is split into Biceps, Triceps and Forearms. Rows below that say "left out" or "folded in" are historical.

| Muscle | How sources split it | Our convention | Why |
|---|---|---|---|
| Deltoid | Anterior / middle / posterior fibres ([TeachMe shoulder][tma-shoulder]); clavicular / acromial / spinal parts ([Kenhub deltoid][kh-delt]); StatPearls entry: [Deltoid][sp-delt] | 3 Muscles: `deltoid-anterior`, `-lateral`, `-posterior` | The same three parts under two naming styles; gym names are clearer. The parts are trained differently: lateral deltoid at 5% MVIC in bench press vs 30% in lateral raise ([Campos 2020][campos2020]) |
| Pectoralis major | 2 heads, clavicular + sternocostal ([TeachMe pectoral][tma-pect], [StatPearls pec][sp-pect]); 3 parts incl. a small abdominal part ([Kenhub pec][kh-pect]); StatPearls notes 2–7 sternocostal segments | 2 Muscles; abdominal part counted with sternocostal | The clavicular head responds to incline ([Rodríguez-Ridao 2020][rr2020], [Chaves 2020][chaves2020]); the abdominal part is the smallest ([Kenhub pec][kh-pect]) and the artwork has one shape to cut, so a third cut adds little |
| Trapezius | Upper / middle / lower fibres ([TeachMe superficial back][tma-back]); TA2: pars descendens / transversa / ascendens ([TA2 trapezius][ta2-trap]); StatPearls entry: [Trapezius][sp-trap] | 3 Muscles, IDs `trapezius-upper/middle/lower` | Each part has a different action (elevate, retract, depress) and different exercises (shrug, row, Y-raise). Same parts as TA2, plainer names |
| Latissimus dorsi | One muscle in anatomy ([StatPearls lats][sp-lats]); some body-map libraries split it into upper/mid/lower regions (body-muscles, see [SVG research](anatomical-svg.md#k-body-muscles)) | 1 Muscle | No anatomical basis for a split and no training evidence found |
| Quadriceps | 4 muscles ([OpenStax 11.6][os-116], [TeachMe anterior thigh][tma-antthigh]); StatPearls describes five bellies ([StatPearls quads][sp-quads]) | 3 Muscles: rectus femoris, vastus lateralis, vastus medialis. Vastus intermedius left out | Rectus femoris behaves differently from the vasti ([Kubo 2019][kubo2019], [Wakahara 2017][wakahara2017]). Vastus intermedius lies deep to rectus femoris ([OpenStax 11.6][os-116]) and tracks the other vasti, so it has nothing to show |
| Hamstrings | "Three long muscles" ([OpenStax 11.6][os-116]); biceps femoris with long and short heads ([TeachMe hamstrings][tma-ham], [StatPearls hamstring][sp-ham]) | 4 Muscles | Short head crosses only the knee ([StatPearls hamstring][sp-ham]), so hip hinges miss it. Seated leg curls grew only the two-joint hamstrings more ([Maeo 2021][maeo2021]); different exercises favour BFlh vs semitendinosus ([Bourne 2017][bourne2017], [Carmichael 2022][carmichael2022]) |
| Calf (triceps surae) | Gastrocnemius with medial and lateral heads + soleus ([TeachMe posterior leg][tma-postleg]); OpenStax only gives gastrocnemius + soleus ([OpenStax 11.6][os-116]) | 3 Muscles | Straight-knee raises grew the gastrocnemius; seated did not, while soleus grew equally in both ([Kinoshita 2023][kinoshita2023]). Foot position shifted growth between the heads ([Nunes 2020][nunes2020]) |
| Erector spinae | One column of three muscles: iliocostalis, longissimus, spinalis ([TeachMe intrinsic back][tma-intrinsic], [StatPearls back muscles][sp-backmuscles]) | 1 Muscle | The three act together to extend the spine. No exercise targets one column, and the artwork has one lower-back strip per side |
| Rotator cuff | 4 muscles: supraspinatus, infraspinatus, teres minor, subscapularis ([OpenStax 11.5][os-115], [TeachMe shoulder][tma-shoulder]) | `infraspinatus` only (teres minor folded in) | Infraspinatus is the one visible on the back diagram; teres minor has the same action (lateral rotation). Supraspinatus and subscapularis are deep |
| Forearm | ~20 muscles in layers ([TeachMe anterior forearm][tma-antfa], [TeachMe posterior forearm][tma-postfa]); OpenStax groups them as anterior flexors and posterior extensors ([OpenStax 11.5][os-115]) | 3 Muscles: flexors, extensors, brachioradialis | Gym exercises train the flexor or extensor group, not single muscles. Brachioradialis is an elbow flexor ([TeachMe posterior forearm][tma-postfa], [OpenStax 11.5][os-115]) and is worked by curls, not wrist work |
| Obliques | External (superficial), internal (intermediate), transversus (deep) ([OpenStax 11.4][os-114]) | `external-oblique` only | Internal oblique has the same listed action (twisting, side bending) and lies under the external ([OpenStax 11.4][os-114]); nothing to show separately |
| Hip flexors | Iliopsoas = psoas major + iliacus ([OpenStax 11.6][os-116], [TeachMe anterior thigh][tma-antthigh]) | 1 Muscle `iliopsoas` | Psoas and iliacus share the action and the exercises |
| Glutes | Maximus, medius, minimus; minimus "similar in shape and function to the gluteus medius" ([TeachMe gluteal][tma-glute]) | Maximus and medius; minimus folded into medius | Minimus is deepest and smallest ([TeachMe gluteal][tma-glute]) |
| Adductors | OpenStax: adductor longus, brevis, magnus, pectineus and gracilis ([OpenStax 11.6][os-116]); TeachMe: gracilis, obturator externus, adductor brevis, longus, magnus (pectineus in the anterior compartment) ([TeachMe medial thigh][tma-medthigh]) | 1 Muscle `adductors` | The sources disagree on where pectineus belongs; one group Muscle avoids the question. Squats and the adductor machine both hit the group. Adductor magnus has a "hamstring part" that extends the hip ([TeachMe medial thigh][tma-medthigh]); it could be split later if Liam wants |
| Serratus anterior | One muscle with several digitations ([StatPearls serratus][sp-serratus]) | 1 Muscle | Digitations aren't trained separately |
| Rhomboids | Major + minor, deep to trapezius ([StatPearls rhomboids][sp-rhomboid], [TeachMe superficial back][tma-back]) | Left out (see [Excluded](#excluded-muscles)) | Can't be seen; retract the scapula with the middle trapezius |
| Teres major / minor, infraspinatus | Teres minor is rotator cuff; teres major is not ([TeachMe shoulder][tma-shoulder]) | Teres major own Muscle; teres minor folded into infraspinatus | Teres major's action (extend, adduct, medially rotate) matches the lats; teres minor's matches infraspinatus |
| Triceps | 3 heads ([StatPearls triceps][sp-triceps], [TeachMe upper arm][tma-arm]); OpenStax names no heads ([OpenStax 11.5][os-115]) | 3 Muscles | The long head alone crosses the shoulder ([TeachMe upper arm][tma-arm]); overhead work grew all heads more, the long head most ([Maeo 2023][maeo2023]); the artwork has 3 back sub-paths |
| Biceps | Long and short head ([TeachMe upper arm][tma-arm]) | 2 Muscles | Visibly distinct on the front diagram, and the long head crosses the shoulder. I found **no** hypertrophy study showing the heads respond to different exercises (see [Unverified](#unverified--limits)) |
| Rectus abdominis | One muscle, segmented ([OpenStax 11.4][os-114]) | 1 Muscle | No upper/lower split: the "segments" are one muscle in one sheath |

**Naming convention.** IDs are English kebab-case, anatomical name first, then the part: `deltoid-anterior`, `triceps-brachii-long-head`, `gastrocnemius-medial-head`. Where the gym name is far from the anatomical one, the display name carries both ("Deltoid, anterior part (front delt)"). Groups of muscles that are only ever trained together get a plural group-style ID (`adductors`, `forearm-flexors`).

## Excluded muscles

Each of these is left out of the taxonomy. Exercises that work them are tagged with the Muscle in the "Tag as" column. Because Muscle IDs only ever get added (see proposals), any of these can be added later.

| Muscle | Why left out | Tag as |
|---|---|---|
| Subscapularis | Deep rotator cuff ([OpenStax 11.5][os-115]); not visible; rarely a gym target (supraspinatus was added in Phase 1) | none |
| Transversus abdominis | Deep to the external oblique ([OpenStax 11.4][os-114]) | `rectus-abdominis` (internal oblique was added in Phase 1) |
| Quadratus lumborum | Deep posterior abdominal wall ([StatPearls QL][sp-ql]); side bending is tagged with obliques | `external-oblique` |
| Transversospinales (multifidus, rotatores, semispinalis) | Under the erector spinae ([TeachMe intrinsic back][tma-intrinsic]) | `erector-spinae` |
| Pectineus | Sources disagree on its compartment ([OpenStax 11.6][os-116] vs [TeachMe anterior thigh][tma-antthigh]); hip adduction and flexion | `adductors` |
| Deep hip rotators (piriformis, gemelli, obturators, quadratus femoris) | Deep to gluteus maximus; lateral rotation only ([TeachMe gluteal][tma-glute]) | `gluteus-maximus` |
| Tensor fasciae latae | Small, no shape; hip abduction with gluteus medius | `gluteus-medius` |
| Pectoralis minor, subclavius | Deep to pectoralis major ([TeachMe pectoral][tma-pect]) | `pectoralis-major-sternal` / `serratus-anterior` |
| Levator scapulae | Covered by trapezius ([TeachMe superficial back][tma-back]); elevates the scapula with upper trapezius | `trapezius-upper` |
| Brachialis | Deep to the biceps ([TeachMe upper arm][tma-arm]) and trained by every curl; merged into `biceps-brachii` with the two biceps heads (Liam, 2026-10-18) | `biceps-brachii` |
| Coracobrachialis, anconeus | Small, deep or hidden; trained with biceps / triceps | `biceps-brachii` / `triceps-brachii-lateral-head` |
| Deep posterior leg (tibialis posterior, popliteus, long toe flexors) | Deep compartment ([TeachMe posterior leg][tma-postleg]) | `soleus` |
| Neck muscles (sternocleidomastoid, splenius, scalenes) | ADR-0007 greys the neck as non-muscle; neck training is rare. Easy to add if Liam trains neck | `trapezius-upper` (shrugs) |
| Hand and foot intrinsics | Not trained in a strength gym; hands and feet are neutral in the artwork | none |

## Recovery Map region mapping (SCRUM-22 Phase 3)

The production artwork is `assets/recovery-map/recovery-map.svg`, built by `scripts/build_recovery_map.py` from react-native-body-highlighter at commit `8ed39ac`. The full Region → Muscle IDs table is generated next to it in `assets/recovery-map/regions.md` (59 Regions per side). The build fails if a Muscle has no Region, a Region has no Muscle, or a Muscle's side disagrees with this doc. That check stands in for the library-package test until the monorepo exists.

**Every "to confirm" read was checked** on 2026-10-17 against labelled false-colour renders of each source sub-path:

| Shape (source slug, sub-paths) | Read | Muscle IDs |
|---|---|---|
| front `obliques` 0, 1, 3 | upper finger-like blocks on the ribs | `serratus-anterior` |
| front `obliques` 2, 4–7 | blocks beside the abs and the flank | `external-oblique`, `internal-oblique` |
| front `adductors` 1 | diagonal strap from the hip crease to the inner knee | `sartorius` |
| front `adductors` 2 | short medial sliver; gracilis or an adductor, so shared | `gracilis`, `adductors` |
| front `calves` 0 | outermost lower-leg strip, lateral to tibialis | `fibularis` |
| front `calves` 1 | inner lower leg; gastrocnemius above, soleus below, so shared | `gastrocnemius-medial-head`, `soleus` |
| front `triceps` 0 | strip on the inner arm; long and medial heads both show there | `triceps-brachii-long-head`, `triceps-brachii-medial-head` |
| front `forearm` 0 | large thumb-side shape | `brachioradialis` |
| back `triceps` 2 | lower outer strip | `triceps-brachii-medial-head` |
| back `hamstring` outer thin strip | lateral to biceps femoris | `vastus-lateralis` |
| back `hamstring` inner thin strip | innermost, runs past the knee; semimembranosus or gracilis, so shared | `semimembranosus`, `gracilis` |
| back `lower-back` flank block | above the hip, under the lat wing | `latissimus-dorsi`, `external-oblique` (Liam: the lats reach the waist) |

**Cuts made on the source geometry** (Liam, 2026-10-17):

- **Deltoids:** curved bands parallel to the cap's outer edge. Front view: `deltoid-anterior` (inner, by the pec) and `deltoid-lateral` (outer). Back view: `deltoid-posterior` (inner) and `deltoid-lateral` (outer). All three heads are on the map, and the side delt shows on both views.
- **Back trapezius:** two Regions after a reference image Liam supplied. The upper traps are the back `neck` shapes plus the top of the trapezius shape above a diagonal from the shoulder to the spine. The strip below, down the spine, is `rhomboids` + `trapezius-middle` + `trapezius-lower`. The front `trapezius` wedge stays `trapezius-upper`.
- **Chest:** a diagonal from the sternum (upper) to the armpit (lower); above is `pectoralis-major-clavicular`, below `pectoralis-major-sternal`.
- **Biceps:** one Region carrying `biceps-brachii` (Liam, 2026-10-18: the biceps is one Muscle, `biceps-brachii`; the two heads and brachialis were merged into it). The earlier long-axis split into two heads and a brachialis sliver is gone.
- Cut pieces are inset so cuts show the same dark seam as the source's own gaps. The cut lines are a first pass and will be polished before the REC story builds on them.

**Tapping:** no Region can get a 44 px target on a body 150 px wide (the best cells are 3–23 px). Liam chose nearest-Region taps plus a "Nearby" list of 44 px rows; the SVG carries an invisible hit path per Region (`.hit`, `data-region`) for this. Every Region has its own hit path, so a tap on or near it selects it directly. The sheet lists that Region's Muscles plus the "Nearby" Regions as full-width 44 px rows, so a tap that lands on a neighbour is corrected with one more tap. Pinch-zoom on the body also works. See `docs/product/features/rec-recovery.md`.

## No-shape Muscles: recommendation per Muscle (proposal for Liam)

> **Superseded (dated 2026-10-17).** This SCRUM-7 proposal is superseded by SCRUM-22 Phase 1 (approved by Liam 2026-10-17: rhomboids, vastus intermedius, gluteus minimus, teres minor, supraspinatus, internal oblique and gracilis are Muscles sharing a Region) and by [Recovery Map region mapping](#recovery-map-region-mapping-scrum-22-phase-3) (SCRUM-22 Phase 3), which checked every read. The text below is kept as history; the (c) "leave out / fold in" recommendations and every "If ... turns out" fallback no longer apply.

**This is a proposal for Liam to approve, not a decision.** The options from the SVG research are (a) draw a small region, (b) borrow a neighbouring Muscle's region (the map shows the region's worst state; tapping lists each Muscle with its own state), (c) leave the Muscle out of the taxonomy.

| Muscle | Recommendation | Reason |
|---|---|---|
| Brachialis | **(a)**, cut a small sliver from the lower outer edge of the `biceps` shape | We cut the biceps anyway, so it costs one more line. It lies deep to the biceps ([TeachMe upper arm][tma-arm]); the sliver is a display choice, not an anatomical claim. Every curl works it, so sharing a biceps head region would be nearly always the same colour, but a sliver lets hammer and reverse curls show their own effect |
| Biceps femoris, short head | **(b)**, share the `biceps-femoris-long-head` region | It lies under the long head ([StatPearls hamstring][sp-ham]). Keeping it as a Muscle lets leg curls and RDLs be tagged honestly (RDL: long head only) |
| Iliopsoas | **(b)**, share the `rectus-femoris` region | Both are hip flexors at the front of the hip. Leg raises fatigue both. Squats barely grew rectus femoris ([Kubo 2019][kubo2019]); Kubo did not measure iliopsoas, so its pairing rests on shared function, not a source |
| Sartorius | Re-tag `adductors` front sub-path 1. **If** that strip turns out not to be sartorius: **(c)** | Rarely a Primary Muscle; not worth drawing |
| Gracilis | **(c)**, fold into `adductors` | Anatomically in the adductor group ([TeachMe medial thigh][tma-medthigh]); its sliver (front `adductors` 2) becomes part of the `adductors` region |
| Fibularis (peroneals) | Re-tag front `calves` sub-path 0. **If** that is wrong: **(c)** | Rarely trained in a gym |
| Rhomboids | **(c)**, tag rows with `trapezius-middle` | Deep to trapezius ([StatPearls rhomboids][sp-rhomboid]); would always show the same state as middle trapezius. If Liam wants "rhomboids" visible in the tap list, switch to (b) sharing the `trapezius-middle` region |
| Infraspinatus, teres major | Have shapes (`upper-back` sub-paths) | The SVG research's "one of infraspinatus / teres major / rhomboids" gap is the rhomboids |
| Vastus intermedius | **(c)** | Deep; sharing rectus femoris would mislead after squats ([Kubo 2019][kubo2019]) |
| Triceps brachii, medial head | Re-tag back `triceps` sub-path 2. **If** that is wrong: **(b)** share the lateral head region | Mostly covered by the other heads ([TeachMe upper arm][tma-arm]) |
| Gluteus minimus | **(c)**, fold into `gluteus-medius` | Same function ([TeachMe gluteal][tma-glute]) |
| Teres minor, internal oblique | **(c)** | See [Excluded](#excluded-muscles) |

Net effect (before SCRUM-22 Phase 1): 41 Muscles; 39 have their own region (38 from existing sub-paths or cuts of existing shapes, plus brachialis's new sliver); 2 share a region (biceps femoris short head, iliopsoas). [Superseded by SCRUM-22 Phase 3, which checked every read (see [Recovery Map region mapping](#recovery-map-region-mapping-scrum-22-phase-3)); the fallbacks in this paragraph and the "If ... turns out" rows above are no longer live.] If a "to confirm" read fails, that Muscle falls back as shown above. Three more fallbacks: if the upper `obliques` blocks are not serratus anterior, tag them `external-oblique` and leave serratus anterior out of the taxonomy; if the inner `hamstring` strip is not semimembranosus, semimembranosus shares the `semitendinosus` region (option b), and the strip is tagged `semitendinosus` (or `adductors` if it turns out to be gracilis), so every Region still carries a Muscle; if front `forearm` 0 is not brachioradialis, brachioradialis shares the `forearm-flexors` region (option b). In general, a shape whose Muscle falls back is tagged with its nearest neighbour in the same Muscle Group (e.g. front `forearm` 0 → `forearm-flexors`), so no Region is left without a Muscle.

## CONTEXT.md updates (approved by Liam and applied 2026-10-17)

Replace **Muscle** with:

> **Muscle**:
> A skeletal muscle, or a head or part of one, that the app tracks (e.g. "Biceps brachii, long head"). Each has a stable ID, a display name, the side of the Recovery Map it shows on (front, back or both) and one Muscle Group. Muscles are split only where the parts can be trained differently or are visibly distinct.
> _Avoid_: muscle group (say Muscle Group only for the roll-up), body part

Add:

> **Muscle Group**:
> A roll-up of Muscles for summaries and filters: Chest, Shoulders, Back, Arms, Core, Glutes and hips, Quads, Hamstrings, Calves and shins. Every Muscle belongs to exactly one.
> _Avoid_: Body part, muscle (for a group), split

(superseded by SCRUM-22 Phase 1: Biceps, Triceps and Forearms replace Arms; CONTEXT.md holds the live list)

> **Region**:
> One shape on the Recovery Map. A Region shows one or more Muscles and is coloured by the worst Recovery State among them.
> _Avoid_: Area, zone, body part

Amend **Recovery State**, adding a second sentence:

> A Muscle with no Working Sets yet has no Recovery State and is shown grey.

Amend **Recovery Map**:

> The front-and-back body diagram that colours each Region by the Recovery State of its Muscles.

## Doc changes (approved by Liam and applied 2026-10-17)

Applied as written below, with small wording changes from review: ADR-0006 was amended in place with a dated note and split into two sentences; the picker filter keeps "or equipment"; the REC Anatomical Recovery Map bullet was rewritten for Regions rather than adding a separate line.

**`docs/adr/0006-exercise-library-in-repo.md`** (or a short new ADR, if ADRs are not edited after acceptance). Replace "and Muscle IDs in the file must match region IDs in the Recovery Map SVG" with:

> and every Muscle ID in the file must appear on at least one Region of the Recovery Map, and every Region must carry at least one Muscle ID. A Region may carry several Muscle IDs. Muscle IDs are never removed or renamed, only added, so historical Workouts always resolve.

**`docs/product/features/exl-exercise-library.md`**

- **EXL: Muscle taxonomy**: replace the second bullet with:
  > - Findings and the proposed list in `docs/research/muscle-taxonomy.md`: 41 Muscles in 9 Muscle Groups, each mapped to one or more Recovery Map Regions (superseded by SCRUM-22 Phase 1: now 48 Muscles in 11 Muscle Groups)
- **EXL: Library schema and validation**: add bullets:
  > - The Muscle list (ID, display name, side, Muscle Group) lives in the library package alongside the Exercises
  > - A test fails if a Muscle has no Region or a Region has no Muscle (ADR-0006)
- **EXL: Exercise picker**: change "filter by Muscle group" to "filter by Muscle Group or Muscle".

**`docs/product/features/rec-recovery.md`**, **REC: Anatomical Recovery Map**: add
  > - A Region can carry several Muscle IDs and shows the worst Recovery State among them; tapping it lists each Muscle with its own state (see `docs/research/muscle-taxonomy.md`)

and under **Rules**:
  > - Volume for a Muscle Group counts each Working Set once, even when the Exercise tags several Muscles in that group

## Phase 1: every gym-trained Muscle visible (SCRUM-22, approved by Liam 2026-10-17 and applied above)

**Approved:** all 7 new Muscles, Arms split into Biceps/Triceps/Forearms, serratus anterior stays in Chest. The tables above already include them; the rest of this section is the reasoning. The rule from SCRUM-22: every gym-trained Muscle gets its own Region or a shared Region, so it appears in the tap list. A shared Region lists each Muscle with its own state when tapped, so folding a Muscle into a neighbour's Region costs no map space. No ID above is renamed or removed (ADR-0006), so Phase 1 only **adds** Muscles and edits display names.

### New Muscles (7, taking the total from 41 to 48)

| ID | Display name | Side | Group | Region | Why a Muscle now | Tag note |
|---|---|---|---|---|---|---|
| `rhomboids` | Rhomboids (major and minor) | back | back | shares `trapezius-middle` | Trained by every row and reverse fly, and a common "rhomboid" target in gym talk. Deep to trapezius ([StatPearls rhomboids][sp-rhomboid]), so there is no shape of its own | Rows tag both `trapezius-middle` and `rhomboids` |
| `vastus-intermedius` | Vastus intermedius | front | quads | shares `vastus-lateralis` | Trained by every knee extension and squat. Sits between the lateral and medial vasti, deep to rectus femoris ([OpenStax 11.6][os-116]). Sharing the rectus femoris Region (the old objection) would colour it after squats, which barely train rectus femoris ([Kubo 2019][kubo2019]); the vasti are the better neighbour | Tag with the other vasti, never with `rectus-femoris` alone |
| `gluteus-minimus` | Gluteus minimus | back | hips | shares `gluteus-medius` | Same shape and function as medius ([TeachMe gluteal][tma-glute]); trained by abduction and single-leg work | Tag with `gluteus-medius` |
| `teres-minor` | Teres minor | back | shoulders | shares `infraspinatus` | Rotator cuff, lateral rotation like infraspinatus ([TeachMe shoulder][tma-shoulder]); trained by face pulls and external rotations | Tag with `infraspinatus` |
| `supraspinatus` | Supraspinatus | back | shoulders | shares `infraspinatus` | Rotator cuff; starts shoulder abduction ([OpenStax 11.5][os-115]); trained by lateral raises and cuff work. Sits above the scapular spine, under trapezius | Lateral raises list it as Secondary |
| `internal-oblique` | Internal oblique | front | core | shares `external-oblique` | Twisting and side bending, under the external oblique ([OpenStax 11.4][os-114]); trained by every woodchop and side bend | Tag with `external-oblique` |
| `gracilis` | Gracilis | front | hips | shares `adductors` (own Region in Phase 3 if the front `adductors` 2 sliver confirms as gracilis) | Adductor-group strap ([TeachMe medial thigh][tma-medthigh]); trained by adductor work | Tag with `adductors` |

Display-name edits that go with this: `infraspinatus` drops "(with teres minor)", `gluteus-medius` drops "(with minimus)", `adductors` drops "gracilis" from its parenthesis.

Kept as they are: `biceps-femoris-short-head` and `iliopsoas` already share a Region, which satisfies the rule. `sartorius` and `fibularis` already have a Muscle; Phase 3 confirms their shapes.

Still excluded (not gym-trained or not reachable by any Exercise in the list): subscapularis, quadratus lumborum, transversus abdominis, transversospinales, pectineus, deep hip rotators, tensor fasciae latae, pectoralis minor, levator scapulae, coracobrachialis, anconeus, deep posterior leg, neck, hand and foot. Phase 2 will tell us if any Exercise needs one of these; IDs are add-only.

### Muscle Groups re-check

- **Serratus anterior:** stay in **chest**. It is worked by pressing and push-ups and sits beside the pec on the diagram. Core is defensible only for anti-rotation work, which is rare in this lifter's list.
- **Arms:** the open question. With 9 Muscles in one group, it lumps biceps, triceps and forearm Volume together, so "Weekly Sets: arms" cannot tell a missed triceps day from a missed biceps day. **Recommendation: split into Biceps (3: both heads, brachialis), Triceps (3), Forearms (3: brachioradialis, flexors, extensors)**, taking the group count from 9 to 11. Cost: two more rows in the Weekly Breakdown and picker filter. Group IDs are only a roll-up, so this stays easy to change.
- **Other groups unchanged.** Shoulders gains `teres-minor` and `supraspinatus`; hips gains `gluteus-minimus` and `gracilis`; quads gains `vastus-intermedius`; core gains `internal-oblique`; back gains `rhomboids`.

### Doc changes

- Add the 7 rows above to the taxonomy table (#42-48) and the group table, and move the matching rows out of **Excluded muscles**.
- `CONTEXT.md`: only if arms are split, update the **Muscle Group** list to the 11 names.
- `docs/product/features/exl-exercise-library.md` and `rec-recovery.md`: update "41 Muscles in 9 Muscle Groups" to the final numbers. (Superseded by SCRUM-22 Phase 1: the final numbers are 48 Muscles in 11 Muscle Groups.)

## Unverified / limits

- **Which sub-path is which muscle** comes from labelled renders of the artwork, not from any documentation. The former "to confirm" reads were checked in SCRUM-22 Phase 3; the three still ambiguous ones are shared Regions (see Recovery Map region mapping).
- **StatPearls pages could not be fetched directly** (NCBI served a bot check). Claims linked to StatPearls come from search-result excerpts of those pages; the load-bearing ones are also backed by TeachMeAnatomy or OpenStax, which I did fetch.
- **Biceps long vs short head:** I found anatomical reasons and visual distinctness but no hypertrophy study showing the heads respond to different exercises. They were kept for visibility until Liam merged them into one Muscle, `biceps-brachii`, on 2026-10-18. The brachioradialis evidence is mixed: one EMG study found its share differed with a pronated grip ([Kleiber 2015][kleiber2015]); another found it highest with a supinated grip ([Coratella 2023][coratella2023]).
- **Terminologia Anatomica:** the TA2 trapezius part names are confirmed from search results of the TA2 viewer (the viewer page itself renders client-side and I could not read it). The deltoid's TA part names were not confirmed; Kenhub's clavicular/acromial/spinal names were used instead.
- **Training studies** are small, mostly in untrained adults, and either run for weeks or measure one session (EMG, short-term swelling). They support "these parts can be trained differently", not exact effect sizes.
- **The group set is judgement**, not a standard. Arms could be split, serratus could sit in core.
- **Not checked:** Liam's actual Exercise list (EXL: Liam's exercise list is not written yet). If he does neck work, tibialis raises or no adductor work, Muscles can be added (IDs are add-only) or simply never tagged.

## Sources

Anatomy references
- [os-114]: OpenStax, *Anatomy and Physiology 2e*, 11.4 Axial Muscles of the Abdominal Wall and Thorax — https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax
- [os-115]: OpenStax, 11.5 Muscles of the Pectoral Girdle and Upper Limbs — https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs
- [os-116]: OpenStax, 11.6 Appendicular Muscles of the Pelvic Girdle and Lower Limbs — https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs
- [tma-pect]: TeachMeAnatomy, Muscles of the Pectoral Region — https://teachmeanatomy.info/upper-limb/muscles/pectoral-region/
- [tma-shoulder]: TeachMeAnatomy, Intrinsic Muscles of the Shoulder — https://teachmeanatomy.info/upper-limb/muscles/shoulder/intrinsic/
- [tma-back]: TeachMeAnatomy, Superficial Back Muscles — https://teachmeanatomy.info/back/muscles/superficial/
- [tma-intrinsic]: TeachMeAnatomy, Intrinsic Back Muscles — https://teachmeanatomy.info/back/muscles/intrinsic/
- [tma-arm]: TeachMeAnatomy, Muscles of the Upper Arm — https://teachmeanatomy.info/upper-limb/muscles/upper-arm/
- [tma-antfa]: TeachMeAnatomy, Anterior Forearm Muscles — https://teachmeanatomy.info/upper-limb/muscles/anterior-forearm/
- [tma-postfa]: TeachMeAnatomy, Posterior Forearm Muscles — https://teachmeanatomy.info/upper-limb/muscles/posterior-forearm/
- [tma-glute]: TeachMeAnatomy, Gluteal Region Muscles — https://teachmeanatomy.info/lower-limb/muscles/gluteal-region/
- [tma-antthigh]: TeachMeAnatomy, Anterior Thigh Muscles — https://teachmeanatomy.info/lower-limb/muscles/thigh/anterior-compartment/
- [tma-medthigh]: TeachMeAnatomy, Medial Thigh Muscles — https://teachmeanatomy.info/lower-limb/muscles/thigh/medial-compartment/
- [tma-ham]: TeachMeAnatomy, Hamstrings — https://teachmeanatomy.info/lower-limb/muscles/thigh/hamstrings/
- [tma-postleg]: TeachMeAnatomy, Posterior Leg Muscles — https://teachmeanatomy.info/lower-limb/muscles/leg/posterior-compartment/
- [tma-latleg]: TeachMeAnatomy, Lateral Leg Muscles — https://teachmeanatomy.info/lower-limb/muscles/leg/lateral-compartment/
- [kh-delt]: Kenhub, Deltoid muscle — https://www.kenhub.com/en/library/anatomy/the-deltoid-muscle
- [kh-pect]: Kenhub, Pectoralis major — https://www.kenhub.com/en/library/anatomy/major-pectoralis-muscle
- [ta2-trap]: TA2 Viewer, musculus trapezius (term 2226) — https://ta2viewer.openanatomy.org/?id=2226
- [ta2-trap-asc]: TA2 Viewer, ascending part of trapezius (term 2229) — https://ta2viewer.openanatomy.org/?id=2229

StatPearls (NCBI Bookshelf)
- [sp-pect]: Anatomy, Thorax, Pectoralis Major — https://www.ncbi.nlm.nih.gov/books/NBK525991/
- [sp-delt]: Anatomy, Shoulder and Upper Limb, Deltoid Muscle — https://www.ncbi.nlm.nih.gov/books/NBK537056/
- [sp-trap]: Anatomy, Back, Trapezius — https://www.ncbi.nlm.nih.gov/books/NBK518994/
- [sp-lats]: Anatomy, Back, Latissimus Dorsi — https://www.ncbi.nlm.nih.gov/books/NBK448120/
- [sp-rhomboid]: Anatomy, Back, Rhomboid Muscles — https://www.ncbi.nlm.nih.gov/books/NBK534856/
- [sp-serratus]: Anatomy, Thorax, Serratus Anterior Muscles — https://www.ncbi.nlm.nih.gov/books/NBK531457/
- [sp-teresmajor]: Anatomy, Shoulder and Upper Limb, Teres Major Muscle — https://www.ncbi.nlm.nih.gov/books/NBK580487/
- [sp-backmuscles]: Anatomy, Back, Muscles — https://www.ncbi.nlm.nih.gov/books/NBK537074/
- [sp-triceps]: Anatomy, Shoulder and Upper Limb, Triceps Muscle — https://www.ncbi.nlm.nih.gov/books/NBK536996/
- [sp-quads]: Anatomy, Bony Pelvis and Lower Limb: Thigh Quadriceps Muscle — https://www.ncbi.nlm.nih.gov/books/NBK513334/
- [sp-vl]: Anatomy, Bony Pelvis and Lower Limb: Vastus Lateralis Muscle — https://www.ncbi.nlm.nih.gov/books/NBK532309/
- [sp-ham]: Anatomy, Bony Pelvis and Lower Limb, Hamstring Muscle — https://www.ncbi.nlm.nih.gov/books/NBK546688/
- [sp-ql]: Anatomy, Abdomen and Pelvis, Quadratus Lumborum — https://www.ncbi.nlm.nih.gov/books/NBK535407/

Training studies
- [rr2020]: Rodríguez-Ridao D et al. Effect of Five Bench Inclinations on the Electromyographic Activity of the Pectoralis Major, Anterior Deltoid, and Triceps Brachii during the Bench Press Exercise. *Int J Environ Res Public Health* 2020;17(19):7339 — https://pubmed.ncbi.nlm.nih.gov/33049982/
- [chaves2020]: Chaves SFN et al. Effects of Horizontal and Incline Bench Press on Neuromuscular Adaptations in Untrained Young Men. *Int J Exerc Sci* 2020;13(6):859–872 — https://pubmed.ncbi.nlm.nih.gov/32922646/
- [campos2020]: Campos YAC et al. Different Shoulder Exercises Affect the Activation of Deltoid Portions in Resistance-Trained Individuals. *J Hum Kinet* 2020;75:5–14 — https://pubmed.ncbi.nlm.nih.gov/33312291/
- [maeo2023]: Maeo S et al. Triceps brachii hypertrophy is substantially greater after elbow extension training performed in the overhead versus neutral arm position. *Eur J Sport Sci* 2023;23(7):1240–1250 — https://pubmed.ncbi.nlm.nih.gov/35819335/
- [kleiber2015]: Kleiber T et al. Muscular coordination of biceps brachii and brachioradialis in elbow flexion with respect to hand position. *Front Physiol* 2015;6:215 — https://pubmed.ncbi.nlm.nih.gov/26300781/
- [coratella2023]: Coratella G et al. Biceps Brachii and Brachioradialis Excitation in Biceps Curl Exercise: Different Handgrips, Different Synergy. *Sports* 2023;11(3):64 — https://pubmed.ncbi.nlm.nih.gov/36976950/
- [kubo2019]: Kubo K et al. Effects of squat training with different depths on lower limb muscle volumes. *Eur J Appl Physiol* 2019;119(9):1933–1942 — https://pubmed.ncbi.nlm.nih.gov/31230110/
- [wakahara2017]: Wakahara T et al. Inter- and intramuscular differences in training-induced hypertrophy of the quadriceps femoris. *Clin Physiol Funct Imaging* 2017;37(4):405–412 — https://pubmed.ncbi.nlm.nih.gov/26576937/
- [maeo2021]: Maeo S et al. Greater Hamstrings Muscle Hypertrophy but Similar Damage Protection after Training at Long versus Short Muscle Lengths. *Med Sci Sports Exerc* 2021;53(4):825–837 — https://pubmed.ncbi.nlm.nih.gov/33009197/
- [bourne2017]: Bourne MN et al. Impact of the Nordic hamstring and hip extension exercises on hamstring architecture and morphology. *Br J Sports Med* 2017;51(5):469–477 — https://pubmed.ncbi.nlm.nih.gov/27660368/
- [carmichael2022]: Carmichael DS et al. Effect of an Isometric or Eccentric Hip Extension Exercise Intervention on Hamstring Strength, Architecture, and Morphology. *Med Sci Sports Exerc* 2022;54(12):2196–2207 — https://pubmed.ncbi.nlm.nih.gov/35941515/
- [kinoshita2023]: Kinoshita M et al. Triceps surae muscle hypertrophy is greater after standing versus seated calf-raise training. *Front Physiol* 2023;14:1272106 — https://pubmed.ncbi.nlm.nih.gov/38156065/
- [kassiano2023]: Kassiano W et al. Muscle Swelling of the Triceps Surae in Response to Straight-Leg and Bent-Leg Calf Raise Exercises in Young Women. *J Strength Cond Res* 2023;37(7):e438–e443 — https://pubmed.ncbi.nlm.nih.gov/37015022/
- [nunes2020]: Nunes JP et al. Different Foot Positioning During Calf Training to Induce Portion-Specific Gastrocnemius Muscle Hypertrophy. *J Strength Cond Res* 2020;34(8):2347–2351 — https://pubmed.ncbi.nlm.nih.gov/32735428/

Artwork
- [rnbh-repo]: react-native-body-highlighter — https://github.com/HichamELBSI/react-native-body-highlighter (assets `bodyFront.ts`, `bodyBack.ts`)

[os-114]: https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax
[os-115]: https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs
[os-116]: https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs
[tma-pect]: https://teachmeanatomy.info/upper-limb/muscles/pectoral-region/
[tma-shoulder]: https://teachmeanatomy.info/upper-limb/muscles/shoulder/intrinsic/
[tma-back]: https://teachmeanatomy.info/back/muscles/superficial/
[tma-intrinsic]: https://teachmeanatomy.info/back/muscles/intrinsic/
[tma-arm]: https://teachmeanatomy.info/upper-limb/muscles/upper-arm/
[tma-antfa]: https://teachmeanatomy.info/upper-limb/muscles/anterior-forearm/
[tma-postfa]: https://teachmeanatomy.info/upper-limb/muscles/posterior-forearm/
[tma-glute]: https://teachmeanatomy.info/lower-limb/muscles/gluteal-region/
[tma-antthigh]: https://teachmeanatomy.info/lower-limb/muscles/thigh/anterior-compartment/
[tma-medthigh]: https://teachmeanatomy.info/lower-limb/muscles/thigh/medial-compartment/
[tma-ham]: https://teachmeanatomy.info/lower-limb/muscles/thigh/hamstrings/
[tma-postleg]: https://teachmeanatomy.info/lower-limb/muscles/leg/posterior-compartment/
[tma-latleg]: https://teachmeanatomy.info/lower-limb/muscles/leg/lateral-compartment/
[kh-delt]: https://www.kenhub.com/en/library/anatomy/the-deltoid-muscle
[kh-pect]: https://www.kenhub.com/en/library/anatomy/major-pectoralis-muscle
[ta2-trap]: https://ta2viewer.openanatomy.org/?id=2226
[ta2-trap-asc]: https://ta2viewer.openanatomy.org/?id=2229
[sp-pect]: https://www.ncbi.nlm.nih.gov/books/NBK525991/
[sp-delt]: https://www.ncbi.nlm.nih.gov/books/NBK537056/
[sp-trap]: https://www.ncbi.nlm.nih.gov/books/NBK518994/
[sp-lats]: https://www.ncbi.nlm.nih.gov/books/NBK448120/
[sp-rhomboid]: https://www.ncbi.nlm.nih.gov/books/NBK534856/
[sp-serratus]: https://www.ncbi.nlm.nih.gov/books/NBK531457/
[sp-teresmajor]: https://www.ncbi.nlm.nih.gov/books/NBK580487/
[sp-backmuscles]: https://www.ncbi.nlm.nih.gov/books/NBK537074/
[sp-triceps]: https://www.ncbi.nlm.nih.gov/books/NBK536996/
[sp-quads]: https://www.ncbi.nlm.nih.gov/books/NBK513334/
[sp-vl]: https://www.ncbi.nlm.nih.gov/books/NBK532309/
[sp-ham]: https://www.ncbi.nlm.nih.gov/books/NBK546688/
[sp-ql]: https://www.ncbi.nlm.nih.gov/books/NBK535407/
[rr2020]: https://pubmed.ncbi.nlm.nih.gov/33049982/
[chaves2020]: https://pubmed.ncbi.nlm.nih.gov/32922646/
[campos2020]: https://pubmed.ncbi.nlm.nih.gov/33312291/
[maeo2023]: https://pubmed.ncbi.nlm.nih.gov/35819335/
[kleiber2015]: https://pubmed.ncbi.nlm.nih.gov/26300781/
[coratella2023]: https://pubmed.ncbi.nlm.nih.gov/36976950/
[kubo2019]: https://pubmed.ncbi.nlm.nih.gov/31230110/
[wakahara2017]: https://pubmed.ncbi.nlm.nih.gov/26576937/
[maeo2021]: https://pubmed.ncbi.nlm.nih.gov/33009197/
[bourne2017]: https://pubmed.ncbi.nlm.nih.gov/27660368/
[carmichael2022]: https://pubmed.ncbi.nlm.nih.gov/35941515/
[kinoshita2023]: https://pubmed.ncbi.nlm.nih.gov/38156065/
[kassiano2023]: https://pubmed.ncbi.nlm.nih.gov/37015022/
[nunes2020]: https://pubmed.ncbi.nlm.nih.gov/32735428/
[rnbh-repo]: https://github.com/HichamELBSI/react-native-body-highlighter
