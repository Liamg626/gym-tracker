# REC: Recovery Map and fatigue model

The feature that sets this app apart: a front/back body diagram colouring each Muscle Fatigued (red), Recovering (amber) or Ready (green).

## Rules

- Recovery is driven by Working Sets only, using the Workout's performed time.
- No left/right split; both sides show the same state.
- All thresholds live in a config file in the repo, not in Settings.

### MVP placeholder rules (time-only)

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

**REC: Placeholder Recovery Map** (MVP)
- Simple front/back diagram with roughly a dozen rough regions; each anatomical Muscle maps onto one; tapping a region lists its Muscles, their states and when they were last trained

**REC: Find a licensed anatomical SVG** (v1.1, research Task)
- Find an openly licensed front + back anatomical SVG, confirm the licence allows public use with changes, and record it in an ADR; fallback: extend an existing React body-map library

**REC: Anatomical Recovery Map** (v1.1, blocked by the SVG research and the EXL Muscle taxonomy)
- Each region ID matches a Muscle ID; the same component renders on phone and dashboard

**REC: Research muscle fatigue and recovery** (v1.2, research Task)
- Primary sources on per-muscle recovery times and how fatigue scales with volume and RIR; the output is a findings doc plus a proposed model and config values

**REC: Volume-weighted fatigue model** (v1.2, blocked by the research)
- Replaces the time-only rules behind the same interface; the config file holds per-Muscle values
