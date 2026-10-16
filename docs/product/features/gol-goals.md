# GOL: Milestones, Body Goals, PRs

All v1.1.

## Rules

- A Milestone is written by hand as Exercise + weight × reps (e.g. Shoulder Press 100kg × 1). It is achieved by a Working Set that meets or beats both the weight and the reps.
- Milestone progress = best Estimated 1RM ÷ Estimated 1RM of the target (Epley: `w × (1 + reps/30)`; when reps = 1, the Estimated 1RM is the weight itself).
- A Body Goal is a target Trend Weight or Body Fat Estimate with an optional deadline. On-track means the projected trend reaches the target by the deadline.
- A PR is the heaviest weight at a given rep count, or the highest Estimated 1RM, for an Exercise (Working Sets only).

## Stories

**GOL: Estimated 1RM and PR detection** (domain, TDD)

**GOL: PR celebration during a Workout**
- Logging a Set that is a PR shows a celebration straight away; the PR is recorded on the Set

**GOL: Milestones**
- Create/edit/delete; list with progress bars; marked achieved with the date and the Set that achieved it

**GOL: Body Goals**
- Create/edit/delete a weight or body fat target with an optional deadline; shows progress and on-track/behind
