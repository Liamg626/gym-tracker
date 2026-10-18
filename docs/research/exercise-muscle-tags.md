# Research: Exercise → Muscle tags

SCRUM-22 · [REC-004] Phase 2 · researched 2026-10-17

## Question

Which Primary and Secondary Muscles, from the 48 in [muscle-taxonomy.md](muscle-taxonomy.md), does each Exercise in [exercise-list.md](exercise-list.md) work? Which Muscles does no Exercise train, and which Exercises light up only one side of the map?

## How the tags are made

- **Primary** = a main mover; **Secondary** = an assisting mover that takes real load. In the fatigue model a Secondary Muscle takes half the dose (CONTEXT.md). Pure stabilisers (e.g. the rotator cuff in a bench press) are **not** tagged, because tagging them would colour the map after almost every Workout.
- **No Secondary Muscle:** an empty Secondary list means the Exercise has no Secondary Muscle. This is isolation work (overhead triceps extensions, skull crushers, wrist curls, hip adduction and tibialis raises; 31 Exercises in the draft library). So "every Exercise has Primary and Secondary tags" means every Exercise has at least one Primary Muscle and an explicit, possibly empty, Secondary list.
- Tags are set **per family**, with **variant overrides** where a variant changes the target (incline vs decline fly, upright vs chest-lean dip, seated vs standing calf raise). Every one of the rows gets its own entry in the draft library.
- **Sources:** an EMG or training study where one exists (keys below); otherwise the Muscle's listed action in an anatomy reference ("anatomy: …"), which is weaker. "By analogy" means the study tested a close relative of the Exercise, not the Exercise itself.
- **Biceps heads:** both heads are always tagged together. No study shows the heads respond to different curls (muscle-taxonomy.md § Unverified), so "long-head" curls (incline, Bayesian) get no special tags.
- **Grip:** `forearm-flexors` are Secondary only on heavy hanging or pulling work (pull-ups, deadlifts, RDLs, hanging leg raises), not on every row.
- The data and the logic live in `scripts/exercise_tags.py`. It writes `docs/research/exercise-library.draft.json` and the tables below. Run `python scripts/exercise_tags.py` after any change.

## Draft library shape

`exercise-library.draft.json` uses the field names from the EXL "Library schema and validation" story, so the "Generate the library" story can pick it up directly:

```json
{ "id": "incline-dumbbell-press", "name": "Incline Dumbbell Press", "equipment": "Dumbbells, incline bench",
  "primaryMuscles": ["pectoralis-major-clavicular"], "secondaryMuscles": ["pectoralis-major-sternal", "deltoid-anterior", "..."] }
```

`bodyweight`, `countsBothSides` and the weight step are left to the "Generate the library" story; they are not Muscle tags.

## Tags

<!-- generated:start -->
333 Exercises tagged from 54 families. Every Exercise has at least one Primary Muscle and every tag is one of the 48 Muscle IDs.

### Family tags

| Family | Primary | Secondary | Variant overrides | Source |
|---|---|---|---|---|
| Incline Chest Press | pectoralis-major-clavicular | pectoralis-major-sternal, deltoid-anterior, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | none | rr2020, chaves2020 |
| Chest Fly (Pec Deck) | pectoralis-major-clavicular, pectoralis-major-sternal | deltoid-anterior | *High-to-Low*: P pectoralis-major-sternal / S pectoralis-major-clavicular, deltoid-anterior; *Low-to-High*: P pectoralis-major-clavicular / S pectoralis-major-sternal, deltoid-anterior; *Incline*: P pectoralis-major-clavicular / S pectoralis-major-sternal, deltoid-anterior; *Decline*: P pectoralis-major-sternal / S pectoralis-major-clavicular, deltoid-anterior | anatomy: tma-pect |
| Dip | pectoralis-major-sternal, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | deltoid-anterior, pectoralis-major-clavicular | *Chest Lean*: P pectoralis-major-sternal / S triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, deltoid-anterior, pectoralis-major-clavicular; *Upright*: P triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head / S pectoralis-major-sternal, deltoid-anterior; *Bench Dip*: P triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head / S deltoid-anterior, pectoralis-major-sternal | anatomy: tma-pect, tma-arm |
| Flat Bench Press | pectoralis-major-sternal | pectoralis-major-clavicular, deltoid-anterior, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | none | rr2020 |
| Push-Up | pectoralis-major-sternal | pectoralis-major-clavicular, deltoid-anterior, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, serratus-anterior, rectus-abdominis | *Diamond*: P triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head / S pectoralis-major-sternal, deltoid-anterior, serratus-anterior, rectus-abdominis; *Decline*: P pectoralis-major-sternal, pectoralis-major-clavicular / S deltoid-anterior, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, serratus-anterior, rectus-abdominis | rr2020 (by analogy with the flat press); anatomy: sp-serratus |
| Decline Bench Press | pectoralis-major-sternal | deltoid-anterior, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | none | rr2020 |
| Shoulder Press | deltoid-anterior | deltoid-lateral, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, trapezius-upper, pectoralis-major-clavicular, serratus-anterior | *Push Press*: P deltoid-anterior / S deltoid-lateral, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, trapezius-upper, pectoralis-major-clavicular, serratus-anterior, vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus; *Behind-the-Neck*: P deltoid-anterior, deltoid-lateral / S triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, trapezius-upper, serratus-anterior; *Landmine*: P deltoid-anterior, pectoralis-major-clavicular / S triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, serratus-anterior | campos2020 |
| Lateral Raise | deltoid-lateral | supraspinatus, trapezius-upper, deltoid-anterior | *Y-Raise*: P deltoid-lateral / S supraspinatus, trapezius-upper, trapezius-lower | campos2020; anatomy: os-115 |
| Rear Delt Fly | deltoid-posterior | trapezius-middle, rhomboids, infraspinatus, teres-minor | none | anatomy: tma-shoulder, tma-back |
| Front Raise | deltoid-anterior | pectoralis-major-clavicular, deltoid-lateral, serratus-anterior | none | anatomy: tma-shoulder |
| Face Pull | deltoid-posterior, infraspinatus, teres-minor | trapezius-middle, rhomboids, trapezius-lower | none | anatomy: tma-shoulder, tma-back |
| Upright Row | deltoid-lateral, trapezius-upper | deltoid-anterior, supraspinatus, brachialis, brachioradialis | none | anatomy: tma-shoulder, tma-back |
| Lat Pulldown | latissimus-dorsi, teres-major | trapezius-lower, rhomboids, trapezius-middle, deltoid-posterior, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis | *Straight-Arm*: P latissimus-dorsi, teres-major / S triceps-brachii-long-head, deltoid-posterior, pectoralis-major-sternal | anatomy: tma-back, sp-teresmajor |
| Seated Row | latissimus-dorsi, trapezius-middle, rhomboids | teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis | *Wide-Grip*: P trapezius-middle, rhomboids, deltoid-posterior / S latissimus-dorsi, teres-major, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis | anatomy: tma-back |
| T-Bar Row | latissimus-dorsi, trapezius-middle, rhomboids | teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis | *Wide-Grip*: P trapezius-middle, rhomboids, deltoid-posterior / S latissimus-dorsi, teres-major, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis; *Landmine*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis, erector-spinae; *Meadows*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis, erector-spinae | anatomy: tma-back |
| Back Extension | erector-spinae | gluteus-maximus, biceps-femoris-long-head, semitendinosus, semimembranosus | *Seated Machine*: P erector-spinae / S gluteus-maximus; *Superman*: P erector-spinae / S gluteus-maximus | anatomy: tma-intrinsic |
| Pull-Up | latissimus-dorsi, teres-major | biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis, trapezius-lower, trapezius-middle, rhomboids, deltoid-posterior, forearm-flexors | none | anatomy: tma-back, sp-teresmajor |
| Bent-Over Row | latissimus-dorsi, trapezius-middle, rhomboids | teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis, erector-spinae | *Chest-Supported*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis; *Seal Row*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis; *Single-Arm*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis; *Inverted*: P latissimus-dorsi, trapezius-middle, rhomboids / S teres-major, deltoid-posterior, trapezius-lower, biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis, rectus-abdominis | anatomy: tma-back, tma-intrinsic |
| Deadlift | gluteus-maximus, erector-spinae, biceps-femoris-long-head, semitendinosus, semimembranosus | vastus-lateralis, vastus-medialis, vastus-intermedius, adductors, trapezius-upper, trapezius-middle, latissimus-dorsi, forearm-flexors | *Sumo*: P gluteus-maximus, adductors, vastus-lateralis, vastus-medialis, vastus-intermedius / S erector-spinae, biceps-femoris-long-head, semitendinosus, semimembranosus, trapezius-upper, latissimus-dorsi, forearm-flexors; *Trap Bar*: P vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus / S erector-spinae, biceps-femoris-long-head, semitendinosus, semimembranosus, trapezius-upper, forearm-flexors; *Rack Pull*: P erector-spinae, gluteus-maximus, trapezius-upper / S biceps-femoris-long-head, semitendinosus, semimembranosus, trapezius-middle, latissimus-dorsi, forearm-flexors | anatomy: tma-glute, tma-intrinsic, tma-ham |
| Overhead Triceps Extension | triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | none | none | maeo2023 |
| Triceps Pushdown | triceps-brachii-lateral-head, triceps-brachii-medial-head | triceps-brachii-long-head | none | maeo2023 |
| Preacher Curl | biceps-brachii-long-head, biceps-brachii-short-head, brachialis | brachioradialis, forearm-flexors | *Reverse-Grip*: P brachioradialis, brachialis / S biceps-brachii-long-head, biceps-brachii-short-head, forearm-extensors | anatomy: tma-arm |
| Bayesian Curl | biceps-brachii-long-head, biceps-brachii-short-head, brachialis | brachioradialis, forearm-flexors | *Hammer*: P brachialis, brachioradialis / S biceps-brachii-long-head, biceps-brachii-short-head | anatomy: tma-arm |
| Hammer Curl | brachialis, brachioradialis | biceps-brachii-long-head, biceps-brachii-short-head | none | kleiber2015, coratella2023 |
| Wrist Curl | forearm-flexors | none | none | anatomy: tma-antfa |
| Wrist Extension | forearm-extensors | none | none | anatomy: tma-postfa |
| Biceps Curl | biceps-brachii-long-head, biceps-brachii-short-head, brachialis | brachioradialis, forearm-flexors | *Reverse-Grip*: P brachioradialis, brachialis / S biceps-brachii-long-head, biceps-brachii-short-head, forearm-extensors; *Zottman*: P biceps-brachii-long-head, biceps-brachii-short-head, brachialis, brachioradialis / S forearm-flexors, forearm-extensors | anatomy: tma-arm |
| Lying Triceps Extension (Skull Crusher) | triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head | none | none | maeo2023 (by analogy) |
| Close-Grip Bench Press | triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head, pectoralis-major-sternal | deltoid-anterior, pectoralis-major-clavicular | *Crush Press*: P pectoralis-major-sternal, triceps-brachii-long-head, triceps-brachii-lateral-head, triceps-brachii-medial-head / S deltoid-anterior, pectoralis-major-clavicular | anatomy: tma-arm |
| Cable Crunch | rectus-abdominis | external-oblique, internal-oblique | *Oblique*: P external-oblique, internal-oblique / S rectus-abdominis | anatomy: os-114 |
| Leg Raise | rectus-abdominis, iliopsoas | rectus-femoris, sartorius, external-oblique, internal-oblique | *Oblique*: P external-oblique, internal-oblique, iliopsoas / S rectus-abdominis, rectus-femoris, sartorius; *Hanging*: P rectus-abdominis, iliopsoas / S rectus-femoris, sartorius, external-oblique, internal-oblique, forearm-flexors; *Reverse Crunch*: P rectus-abdominis / S external-oblique, internal-oblique, iliopsoas | anatomy: os-114, os-116 |
| Russian Twist | external-oblique, internal-oblique | rectus-abdominis, iliopsoas | *Landmine*: P external-oblique, internal-oblique / S rectus-abdominis, deltoid-anterior | anatomy: os-114 |
| Plank | rectus-abdominis | external-oblique, internal-oblique, deltoid-anterior, serratus-anterior | *Side Plank*: P external-oblique, internal-oblique / S gluteus-medius, gluteus-minimus, rectus-abdominis | anatomy: os-114 |
| Crunch and Sit-Up | rectus-abdominis | external-oblique, internal-oblique | *Bicycle*: P external-oblique, internal-oblique, rectus-abdominis / S iliopsoas; *Oblique*: P external-oblique, internal-oblique / S rectus-abdominis; *Sit-Up*: P rectus-abdominis / S external-oblique, internal-oblique, iliopsoas, rectus-femoris | anatomy: os-114 |
| Ab Wheel Rollout | rectus-abdominis | external-oblique, internal-oblique, latissimus-dorsi, serratus-anterior, deltoid-anterior | none | anatomy: os-114 |
| Hip Abduction | gluteus-medius, gluteus-minimus | gluteus-maximus | *Forward Lean*: P gluteus-medius, gluteus-minimus, gluteus-maximus | anatomy: tma-glute |
| Hip Adduction | adductors, gracilis | none | *Copenhagen*: P adductors, gracilis / S external-oblique, internal-oblique | anatomy: tma-medthigh |
| Hip Thrust and Glute Bridge | gluteus-maximus | biceps-femoris-long-head, semitendinosus, semimembranosus, gluteus-medius, gluteus-minimus | none | krause2020 |
| Step-Up | gluteus-maximus, vastus-lateralis, vastus-medialis, vastus-intermedius | rectus-femoris, gluteus-medius, gluteus-minimus, adductors | *Lateral*: P gluteus-maximus, gluteus-medius, gluteus-minimus, vastus-lateralis, vastus-medialis, vastus-intermedius / S rectus-femoris, adductors | krause2020 |
| Glute Kickback | gluteus-maximus | biceps-femoris-long-head, semitendinosus, semimembranosus | none | anatomy: tma-glute |
| Leg Press | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus | adductors | *Low, Narrow*: P vastus-lateralis, vastus-medialis, vastus-intermedius / S gluteus-maximus, adductors; *High, Wide*: P gluteus-maximus, adductors, vastus-lateralis, vastus-medialis, vastus-intermedius / S biceps-femoris-long-head, semitendinosus, semimembranosus | kubo2019 (by analogy with the squat) |
| Leg Extension | rectus-femoris, vastus-lateralis, vastus-medialis, vastus-intermedius | none | none | wakahara2017 |
| Pendulum Squat | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus | adductors | none | kubo2019 (by analogy) |
| Bulgarian Split Squat | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus | adductors, gluteus-medius, gluteus-minimus | none | krause2020 |
| Squat | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus, adductors | erector-spinae, gluteus-medius, gluteus-minimus | *Low-Bar*: P gluteus-maximus, adductors, vastus-lateralis, vastus-medialis, vastus-intermedius / S erector-spinae, biceps-femoris-long-head, semitendinosus, semimembranosus; *Front*: P vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus / S adductors, erector-spinae, rectus-abdominis; *Goblet*: P vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus / S adductors; *Bodyweight*: P vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus / S adductors | kubo2019 |
| Hack Squat | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus | adductors | *Barbell*: P vastus-lateralis, vastus-medialis, vastus-intermedius / S gluteus-maximus, adductors, erector-spinae, forearm-flexors | kubo2019 (by analogy) |
| Lunge | vastus-lateralis, vastus-medialis, vastus-intermedius, gluteus-maximus | adductors, gluteus-medius, gluteus-minimus | *Lateral*: P adductors, gracilis, gluteus-maximus, vastus-lateralis, vastus-medialis, vastus-intermedius / S gluteus-medius, gluteus-minimus | krause2020 |
| Hamstring Curl | biceps-femoris-long-head, biceps-femoris-short-head, semitendinosus, semimembranosus | gastrocnemius-medial-head, gastrocnemius-lateral-head, sartorius, gracilis | *Stability Ball*: P biceps-femoris-long-head, biceps-femoris-short-head, semitendinosus, semimembranosus / S gluteus-maximus, gastrocnemius-medial-head, gastrocnemius-lateral-head | maeo2021; anatomy: tma-ham |
| Romanian Deadlift | biceps-femoris-long-head, semitendinosus, semimembranosus, gluteus-maximus | erector-spinae, adductors, forearm-flexors | *Single-Leg*: P biceps-femoris-long-head, semitendinosus, semimembranosus, gluteus-maximus / S erector-spinae, adductors, gluteus-medius, gluteus-minimus, forearm-flexors; *B-Stance*: P biceps-femoris-long-head, semitendinosus, semimembranosus, gluteus-maximus / S erector-spinae, adductors, gluteus-medius, gluteus-minimus, forearm-flexors | anatomy: tma-ham, sp-ham |
| Nordic Hamstring Curl | biceps-femoris-long-head, biceps-femoris-short-head, semitendinosus, semimembranosus | gastrocnemius-medial-head, gastrocnemius-lateral-head | none | bourne2017 |
| Good Morning | biceps-femoris-long-head, semitendinosus, semimembranosus, erector-spinae, gluteus-maximus | adductors | none | anatomy: tma-ham, tma-intrinsic |
| Glute-Ham Raise | biceps-femoris-long-head, biceps-femoris-short-head, semitendinosus, semimembranosus | gluteus-maximus, gastrocnemius-medial-head, gastrocnemius-lateral-head, erector-spinae | none | anatomy: tma-ham |
| Calf Raise | gastrocnemius-medial-head, gastrocnemius-lateral-head, soleus | fibularis | *Seated*: P soleus / S fibularis | kinoshita2023, nunes2020 |
| Tibialis Raise | tibialis-anterior | none | none | anatomy: os-116 |

### Coverage per Muscle

| Muscle | Group | Primary in | Secondary in |
|---|---|---|---|
| `pectoralis-major-clavicular` | chest | 22 | 45 |
| `pectoralis-major-sternal` | chest | 40 | 16 |
| `serratus-anterior` | chest | 0 | 34 |
| `deltoid-anterior` | shoulders | 21 | 73 |
| `deltoid-lateral` | shoulders | 14 | 18 |
| `deltoid-posterior` | shoulders | 14 | 36 |
| `infraspinatus` | shoulders | 4 | 8 |
| `teres-minor` | shoulders | 4 | 8 |
| `supraspinatus` | shoulders | 0 | 13 |
| `trapezius-upper` | back | 6 | 27 |
| `trapezius-middle` | back | 20 | 33 |
| `trapezius-lower` | back | 0 | 41 |
| `latissimus-dorsi` | back | 36 | 11 |
| `teres-major` | back | 18 | 20 |
| `erector-spinae` | back | 14 | 23 |
| `rhomboids` | back | 20 | 28 |
| `biceps-brachii-long-head` | biceps | 20 | 45 |
| `biceps-brachii-short-head` | biceps | 20 | 45 |
| `brachialis` | biceps | 29 | 41 |
| `triceps-brachii-long-head` | triceps | 24 | 56 |
| `triceps-brachii-lateral-head` | triceps | 32 | 46 |
| `triceps-brachii-medial-head` | triceps | 32 | 46 |
| `brachioradialis` | forearms | 10 | 60 |
| `forearm-flexors` | forearms | 4 | 44 |
| `forearm-extensors` | forearms | 3 | 3 |
| `rectus-abdominis` | core | 23 | 19 |
| `external-oblique` | core | 11 | 23 |
| `internal-oblique` | core | 11 | 23 |
| `gluteus-maximus` | hips | 58 | 18 |
| `gluteus-medius` | hips | 8 | 29 |
| `gluteus-minimus` | hips | 8 | 29 |
| `adductors` | hips | 11 | 39 |
| `iliopsoas` | hips | 6 | 11 |
| `gracilis` | hips | 5 | 7 |
| `rectus-femoris` | quads | 2 | 13 |
| `vastus-lateralis` | quads | 36 | 5 |
| `vastus-medialis` | quads | 36 | 5 |
| `sartorius` | quads | 0 | 13 |
| `vastus-intermedius` | quads | 36 | 5 |
| `biceps-femoris-long-head` | hamstrings | 25 | 20 |
| `biceps-femoris-short-head` | hamstrings | 12 | 0 |
| `semitendinosus` | hamstrings | 25 | 20 |
| `semimembranosus` | hamstrings | 25 | 20 |
| `gastrocnemius-medial-head` | lower-legs | 8 | 12 |
| `gastrocnemius-lateral-head` | lower-legs | 8 | 12 |
| `soleus` | lower-legs | 10 | 0 |
| `tibialis-anterior` | lower-legs | 4 | 0 |
| `fibularis` | lower-legs | 0 | 10 |

### Checks

- **Muscles no Exercise trains:** none
- **Muscles only ever Secondary:** serratus-anterior, supraspinatus, trapezius-lower, sartorius, fibularis
- **Exercises lighting only the front view:** 47; **only the back view:** 39 (full lists printed by the script)
- **Unilateral Exercises:** 84. The map mirrors left and right, so one-arm or one-leg Sets light both sides.
<!-- generated:end -->

## Findings

- **No Muscle is untrained** by the list (see Checks). Five are only ever Secondary, so they only ever take half doses:
  - `sartorius`: knee flexion (leg curls) and hip flexion (leg raises).
  - `fibularis`: plantarflexion in calf raises ([TeachMe lateral leg][tma-latleg]). The near miss "Banded Ankle Eversion" in exercise-list.md would train it directly.
  - `serratus-anterior`: push-ups, planks, overhead pressing, front raises. A direct exercise (e.g. push-up plus, scapular protraction) is not in the list.
  - `supraspinatus`: lateral and Y-raises, upright rows.
  - `trapezius-lower`: pulldowns, pull-ups, rows, face pulls, Y-raises. A prone Y-raise would make it Primary.
  
  Adding one direct Exercise for any of these is a choice for Liam, not a gap in the tags.
- **Vastus intermedius** is always tagged with the other two vasti, never alone and never with rectus femoris alone, as agreed in Phase 1.
- **Hamstrings:** hip hinges (RDL, good morning, deadlift) tag only the three two-joint hamstrings; leg curls, Nordics and the glute-ham raise add `biceps-femoris-short-head`, which crosses only the knee ([StatPearls hamstring][sp-ham]). Seated curls grew the two-joint hamstrings more than lying curls ([Maeo 2021][maeo2021]) but all four still work, so both versions tag all four as Primary.
- **Squats do not tag the hamstrings or rectus femoris**: squat training grew the vasti, adductors and gluteus maximus but not those ([Kubo 2019][kubo2019]). Leg extensions tag rectus femoris as Primary ([Wakahara 2017][wakahara2017]).
- **Seated calf raises tag soleus only**: seated training did not grow the gastrocnemius ([Kinoshita 2023][kinoshita2023]).
- **One side of the map:** most Exercises light only the front or only the back view, which is expected (a curl is front only, a row back only). Muscles drawn on both views (lateral deltoid, upper trapezius, triceps long head, external oblique, adductors, vastus lateralis, medial gastrocnemius) light both. Left and right are mirrored (SCRUM-22 Phase 3), so one-arm and one-leg Exercises colour both sides; the fatigue model counts a unilateral Set the same as a bilateral one.

## Unverified / limits

- **Most tags are action-based**, not measured. EMG studies cover the bench angle, deltoid parts, triceps position, curl grip, squat, knee extension, hamstring curls and calf raises; the rest rely on anatomy references.
- **Primary vs Secondary is a judgement** at the boundary (e.g. anterior deltoid in incline press, adductors in the squat). It only changes the fatigue dose by half a set.
- **Variant overrides match by name.** A new variant whose name doesn't match an override gets its family's default tags; check them when adding Exercises.

## Sources

- [rr2020]: Rodríguez-Ridao D et al. 2020, bench inclinations EMG — https://pubmed.ncbi.nlm.nih.gov/33049982/
- [chaves2020]: Chaves SFN et al. 2020, horizontal vs incline bench press — https://pubmed.ncbi.nlm.nih.gov/32922646/
- [campos2020]: Campos YAC et al. 2020, deltoid portions across shoulder exercises — https://pubmed.ncbi.nlm.nih.gov/33312291/
- [maeo2023]: Maeo S et al. 2023, overhead vs neutral triceps extension — https://pubmed.ncbi.nlm.nih.gov/35819335/
- [kleiber2015]: Kleiber T et al. 2015, biceps and brachioradialis by hand position — https://pubmed.ncbi.nlm.nih.gov/26300781/
- [coratella2023]: Coratella G et al. 2023, biceps curl handgrips — https://pubmed.ncbi.nlm.nih.gov/36976950/
- [kubo2019]: Kubo K et al. 2019, squat depth and muscle volumes — https://pubmed.ncbi.nlm.nih.gov/31230110/
- [wakahara2017]: Wakahara T et al. 2017, quadriceps hypertrophy after knee extension — https://pubmed.ncbi.nlm.nih.gov/26576937/
- [maeo2021]: Maeo S et al. 2021, seated vs lying leg curl — https://pubmed.ncbi.nlm.nih.gov/33009197/
- [bourne2017]: Bourne MN et al. 2017, Nordic vs hip extension — https://pubmed.ncbi.nlm.nih.gov/27660368/
- [kinoshita2023]: Kinoshita M et al. 2023, standing vs seated calf raise — https://pubmed.ncbi.nlm.nih.gov/38156065/
- [nunes2020]: Nunes JP et al. 2020, foot position in calf training — https://pubmed.ncbi.nlm.nih.gov/32735428/
- [krause2020]: Krause Neto W et al. 2020, gluteus maximus activation in common exercises (systematic review), J Sports Sci Med 19:195–203 — https://www.jssm.org/jssm-19-195.xml-abst
- Anatomy references (`tma-*`, `os-*`, `sp-*`): as listed in [muscle-taxonomy.md § Sources](muscle-taxonomy.md#sources).

[tma-latleg]: https://teachmeanatomy.info/lower-limb/muscles/leg/lateral-compartment/
[sp-ham]: https://www.ncbi.nlm.nih.gov/books/NBK546688/
[maeo2021]: https://pubmed.ncbi.nlm.nih.gov/33009197/
[kubo2019]: https://pubmed.ncbi.nlm.nih.gov/31230110/
[wakahara2017]: https://pubmed.ncbi.nlm.nih.gov/26576937/
[kinoshita2023]: https://pubmed.ncbi.nlm.nih.gov/38156065/
