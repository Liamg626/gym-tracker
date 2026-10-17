# GOL: Milestones, Body Goals, PRs

All v1.1.

## Rules

- A Milestone is written by hand as Exercise + weight × reps (e.g. Shoulder Press 100kg × 1). It is achieved by a Working Set that meets or beats both the weight and the reps. For a bodyweight Exercise the weight is the **added** weight, as Sets are logged.
- Milestone progress = best Estimated 1RM ÷ Estimated 1RM of the target (Epley: `w × (1 + reps/30)`; when reps = 1, the Estimated 1RM is the weight itself). Only Sets of 1–12 reps have an Estimated 1RM. Dumbbell Exercises use the per-dumbbell weight as entered (doubling is for Volume only); bodyweight Exercises use Trend Weight + added weight (`log-workouts.md`).
- A Body Goal is a target Trend Weight or Body Fat Estimate with an optional deadline. On-track means a straight line fitted to the last 28 days of Trend Weight (or Body Fat Estimates), extended to the deadline, reaches the target. With less than 14 days of data the status is "not enough data".
- A PR is the heaviest weight at a given rep count (any rep count), or the highest Estimated 1RM, for an Exercise (Working Sets only).
- PRs are always worked out from the Sets, never stored, so editing or deleting a Set updates them.

## Stories

**GOL: Estimated 1RM and PR detection** (domain, TDD)

**GOL: PR celebration during a Workout**
- Logging a Set that beats the existing best shows a celebration straight away
- No celebration during an Exercise's first-ever Workout (every Set would be a PR)

**GOL: Milestones**
- Create/edit/delete; list with progress bars; marked achieved with the date and the Set that achieved it

**GOL: Body Goals**
- Create/edit/delete a weight or body fat target with an optional deadline; shows progress and on-track/behind
