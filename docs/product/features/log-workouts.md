# LOG: Workouts, Routines and history

Live logging at the gym is the core of the app. Everything else depends on this data.

## Rules

- A Workout starts when **Start Workout** is tapped and ends when **End Workout** is tapped. A small running clock shows elapsed time. There is **no rest timer**.
- If a Workout has no new Set for 3 hours, it auto-ends with its end time set to the time of the last Set. There is no cron: the phone checks when the app opens, everything that reads Workouts treats such a Workout as ended at its last Set, and the API stores that end time the next time the Workout is touched.
- Only one Workout can be open at a time.
- Ending a Workout with no Sets asks "Discard this Workout?" and deletes it. A Workout with only Warm-up Sets is kept but doesn't count towards the Weekly Target.
- Workout and Set writes (start, end, add, edit, delete) are saved on the device first and synced through a retrying queue (ADR-0004). IDs are UUIDs made on the phone, so a retried write is applied once.
- Warm-up Sets never count toward Volume, Recovery, PRs or Milestones.
- Bodyweight Exercises record **added** weight; Volume and Estimated 1RM use the latest Trend Weight on or before the Workout + added weight. With no Weigh-in ever, they use added weight only and the Workout shows a hint to log a Weigh-in.
- Dumbbell weight is entered **per dumbbell**; `countsBothSides` doubles Volume.
- Single-arm work counts as full Volume for the Muscle (no left/right split).

## Stories

**LOG: Start and end an empty Workout** (MVP)
- Start Workout creates a Workout with a start time; End Workout sets the end time; the clock shows elapsed time

**LOG: Add Exercises and log Sets** (MVP)
- Add an Exercise via the picker (EXL); log a Set as weight × reps with an optional RIR and note
- The weight stepper uses the Exercise's weight step; Sets can be marked as Warm-up Sets
- Each Exercise shows last time's Sets; one tap repeats last time's weight × reps

**LOG: Workout writes saved on the device first** (MVP, ADR-0004)
- Starting, logging, editing and ending a Workout work with the network off; queued Sets sync automatically when the network returns; nothing is lost if the app is closed mid-Workout
- A small indicator shows unsynced Sets

**LOG: Auto-end abandoned Workouts** (MVP)
- A Workout with no Set for 3h is ended at the time of its last Set, worked out on read (no cron; see Rules)
- Starting a Workout while one is open is not possible; the open one is shown instead

**LOG: Routines** (MVP)
- Create, edit, reorder and delete Routines; each entry is an Exercise + target Set count + rep range (e.g. 3 × 8–12)
- Start a Workout from a Routine; targets show as hints next to last time's Sets; Exercises can still be added or skipped
- A Workout keeps the Routine's ID plus a copy of its name and targets from when it started, so editing, renaming or deleting a Routine never changes history

**LOG: Workout history** (MVP)
- List of past Workouts (date, Routine, duration, Exercise count); open one to see every Set
- Edit or delete any Set or Workout (phone only; the dashboard's history is read-only)

**LOG: Log a Workout after the fact** (MVP, phone only)
- Create a Workout with a start and end time you type in, then add Sets; Recovery uses the Workout's performed time
