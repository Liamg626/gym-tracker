# REC: Recovery Map and fatigue model

The feature that sets this app apart: a front/back body diagram colouring each Region by its Muscles' Recovery State: Fatigued (red), Recovering (amber) or Ready (green).

## Rules

- Recovery is driven by Working Sets only, using the Workout's performed time.
- No left/right split; both sides show the same state.
- All thresholds live in a config file in the repo, not in Settings.
- Volume for a Muscle Group counts each Working Set once, even when the Exercise tags several Muscles in that group.

### MVP rules (time-only)

| Since last Working Set | Primary Muscle | Secondary Muscle |
|---|---|---|
| < 24h | Fatigued | Recovering |
| 24–72h | Recovering | Recovering |
| > 72h | Ready | Ready |

### v1.2 researched model

Volume-weighted fatigue per Muscle that decays over a recovery window per Muscle, based on the research Task. The exact model will be decided after that research.

## Stories

**REC: Recovery State calculation (time-only)** (MVP, domain, TDD)
- Pure function: Workouts + Exercise Library + now → Recovery State per Muscle

**REC: Find a licensed anatomical SVG** (MVP, research Task)
- Findings in `docs/research/anatomical-svg.md`; source recorded in ADR-0007 (react-native-body-highlighter path data, MIT)

**REC: Anatomical Recovery Map** (MVP, blocked by the EXL Muscle taxonomy)
- Front/back diagram from the ADR-0007 artwork, legs widened, grey base; each Region carries one or more Muscle IDs and is coloured by the worst Recovery State among them, and a Region whose Muscles have no Working Sets yet stays grey (no state); tapping a Region lists each of its Muscles with its own state and when it was last trained (see `docs/research/muscle-taxonomy.md`); the same component renders on phone and dashboard
- The MIT notice is kept in the SVG file and the README third-party notices; the app's About screen carries a credit line

**REC: Research muscle fatigue and recovery** (v1.2, research Task)
- Primary sources on per-muscle recovery times and how fatigue scales with volume and RIR; the output is a findings doc plus a proposed model and config values

**REC: Volume-weighted fatigue model** (v1.2, blocked by the research)
- Replaces the time-only rules behind the same interface; the config file holds per-Muscle values
