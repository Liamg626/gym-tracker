# EXL: Exercise Library

The repo-owned catalogue of Exercises and the Muscles they work (ADR-0006).

## Stories

**EXL: Liam's exercise list** (MVP, Task, `ready-for-human`)
- Liam writes the list of Exercises he does, along with his gym's equipment
- Blocks the library generation story

**EXL: Muscle taxonomy** (MVP, Task)
- Research and define the list of Muscles at anatomical detail (e.g. biceps brachii long/short head), each with a stable ID, display name, front/back side and a roll-up group for summaries
- The IDs must match the region IDs in the Recovery Map SVG (REC)
- Decide how Muscles with no shape in the Recovery Map artwork (e.g. brachialis, sartorius, peroneals) get a region; see `docs/research/anatomical-svg.md`

**EXL: Library schema and validation** (MVP)
- JSON schema plus a typed loader in `packages/exercise-library`
- Each Exercise: stable ID, name, equipment, Primary Muscles, Secondary Muscles, `bodyweight` flag, `countsBothSides` flag, weight step (e.g. 1.25 / 2.5kg)
- A test fails if any Muscle ID is unknown, an ID is duplicated, or an Exercise has no Primary Muscle

**EXL: Generate the library** (MVP, blocked by the two stories above)
- Research each Exercise on Liam's list and write its entry, citing sources in the PR
- Exercises are never removed (ADR-0006)

**EXL: Exercise picker** (MVP)
- Search by name, filter by Muscle group or equipment, recently used Exercises first
