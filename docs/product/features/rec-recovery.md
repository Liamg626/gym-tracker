# REC: Recovery Map and fatigue model

The feature that sets this app apart: a front/back body diagram colouring each Region by its Muscles' Recovery State: Fatigued (red), Recovering (amber) or Ready (green).

## Rules

- Recovery is driven by Working Sets only, using the Workout's performed time.
- No left/right split; both sides show the same state.
- All thresholds live in a config file in the repo, not in Settings.
- Volume for a Muscle Group counts each Working Set once, even when the Exercise tags several Muscles in that group.
- Weight and reps do not affect Recovery State; only Working Sets, role (Primary or Secondary), RIR and time do.
- A Muscle that is not Ready is advice, not a restriction.

### MVP rules (time-only)

| Since last Working Set | Primary Muscle | Secondary Muscle |
|---|---|---|
| < 24h | Fatigued | Recovering |
| 24–72h | Recovering | Recovering |
| > 72h | Ready | Ready |

### v1.2 researched model

Volume-weighted fatigue per Muscle, from `docs/research/muscle-fatigue.md`. Each Working Set adds to the Fatigue Dose of every Muscle it tags: 1 for a Primary Muscle, 0.5 for a Secondary Muscle, multiplied by an effort factor from its RIR (1.0 at RIR 0, falling to 0.2 at RIR 5 or more; RIR is optional, and an unrecorded RIR counts as RIR 1). A Workout's Fatigue Dose sets the Muscle's Recovery Window, from 12 h up to 72 h, which is reached at a Fatigue Dose of 4. Fatigue Level falls linearly from 1 to 0 over the Recovery Window; the Muscle is Fatigued for the first third, Recovering until the end of the window, then Ready. When several Workouts overlap, the highest Fatigue Level wins. All numbers, including the Weekly Sets targets, live in the fatigue config file, not in Settings.

## Stories

**REC: Recovery State calculation (time-only)** (MVP, domain, TDD)
- Pure function: Workouts + Exercise Library + now → Recovery State per Muscle

**REC: Find a licensed anatomical SVG** (MVP, research Task)
- Findings in `docs/research/anatomical-svg.md`; source recorded in ADR-0007 (react-native-body-highlighter path data, MIT)

**REC: Anatomical Recovery Map** (MVP, blocked by the EXL Muscle taxonomy)
- Front/back diagram from the ADR-0007 artwork, legs widened, grey base; each Region carries one or more Muscle IDs and is coloured by the worst Recovery State among them, and a Region whose Muscles have no Working Sets yet stays grey (no state); tapping a Region lists each of its Muscles with its own state and when it was last trained (see `docs/research/muscle-taxonomy.md`); the same component renders on phone and dashboard
- The MIT notice is kept in the SVG file and the README third-party notices; the app's About screen carries a credit line
- The artwork is `assets/recovery-map/recovery-map.svg` (built by `scripts/build_recovery_map.py`; Regions and their Muscle IDs in `assets/recovery-map/regions.md`). A tap selects the nearest Region, using the SVG's invisible hit paths, and the sheet lists that Region's Muscles plus a "Nearby" list of the Regions within a finger's reach as full-width 44 px rows, so every Region is reachable in two taps at most; pinch-zoom on the body also works (Liam, 2026-10-18: no Region can get a 44 px target on a 150 px-wide body)

**REC: Research muscle fatigue and recovery** (v1.2, research Task)
- Primary sources on per-muscle recovery times and how fatigue scales with volume and RIR; the output is a findings doc plus a proposed model and config values

**REC: Volume-weighted fatigue model** (v1.2, domain, TDD, blocked by the research)
- Pure function: Workouts + Exercise Library + fatigue config + now → Recovery State and Fatigue Level per Muscle, replacing the time-only rules behind the same interface
- Config holds `version`, `roleWeight`, `effortByRir`, `rirWhenMissing`, `recovery`, `groupScale`, `muscleScale`, `weeklySets` and `watchAdjustment` (values and sources in `docs/research/muscle-fatigue.md`), in one shared fatigue config module (suggested path `src/fatigue/fatigue.config.ts`) that the Weekly Sets insight also imports
- Tests cover the worked examples in the research doc and the MVP boundaries at the maximum dose
