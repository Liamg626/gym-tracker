# Gym Tracker

A personal strength-training tracker for exactly one lifter: logging workouts, body metrics and goals, and showing which muscles are recovered.

## Language

### Training

**Exercise**:
A named movement from the Exercise Library (e.g. "Seated Dumbbell Shoulder Press"), tagged with the Muscles it works.
_Avoid_: Movement, lift (as a noun for the catalogue entry)

**Exercise Library**:
The repo-owned catalogue of every Exercise the lifter does, with its Muscle tags.
_Avoid_: Exercise database, catalogue

**Workout**:
One gym session: an ordered list of Exercises performed, each with its Sets, from start to finish.
_Avoid_: Session, training, log

**Routine**:
A saved template of Exercises (e.g. "Push") that a Workout can be started from.
_Avoid_: Program, plan, split, template

**Set**:
One bout of an Exercise within a Workout, recorded as weight × reps, optionally with RIR and a note.
_Avoid_: Rep set, entry

**Warm-up Set**:
A Set flagged as warm-up; it never counts toward Volume, Recovery, PRs or Milestones.

**Working Set**:
Any Set that is not a Warm-up Set.
_Avoid_: Hard set, effective set

**RIR**:
Reps in reserve: how many more reps the lifter could have done at the end of a Set.
_Avoid_: RPE

**Volume**:
Sum of weight × reps across Working Sets, attributed to a Muscle or Exercise over a period.
_Avoid_: Tonnage, load

**Estimated 1RM**:
The single-rep max implied by a Working Set, using the Epley formula.
_Avoid_: Max, e1RM (in UI copy)

**Weekly Target**:
The number of Workouts the lifter aims to complete per week.

### Muscles and recovery

**Muscle**:
An anatomical region on the Recovery Map, at the finest anatomical detail the map supports (e.g. "biceps brachii, long head").
_Avoid_: Muscle group (except when explicitly rolling Muscles up for display)

**Primary Muscle / Secondary Muscle**:
The role a Muscle plays in an Exercise: the main mover, or an assisting one.

**Recovery State**:
A Muscle's readiness: **Fatigued** (red, just worked), **Recovering** (amber) or **Ready** (green).
_Avoid_: Fresh, sore, rested

**Recovery Map**:
The front-and-back body diagram that colours each Muscle by its Recovery State.
_Avoid_: Heatmap, body chart

### Body

**Weigh-in**:
A single body-weight reading the lifter types in, normally daily.

**Trend Weight**:
The 7-day rolling average of Weigh-ins; what goals and charts track.
_Avoid_: Average weight, smoothed weight

**Measurement Session**:
A weekly set of tape readings (neck, waist, chest, arms, thighs, shoulders) taken together.
_Avoid_: Check-in, measurements (as a noun for one occasion)

**Body Fat Estimate**:
Body fat percentage calculated from a Measurement Session with the US Navy formula.
_Avoid_: Body fat reading

### Goals and review

**Milestone**:
A lift goal written by the lifter as Exercise + weight × reps (e.g. Shoulder Press 100kg × 1).
_Avoid_: PR goal, target lift

**Body Goal**:
A target Trend Weight or Body Fat Estimate, with an optional deadline.

**PR**:
A new best for an Exercise: heaviest weight at a given rep count, or highest Estimated 1RM.
_Avoid_: PB, record

**Weekly Breakdown**:
The Monday–Sunday summary of Workouts, Volume, PRs, body changes, Watch Data and goal progress.
_Avoid_: Report, weekly summary

**Watch Data**:
Heart rate, sleep and activity figures imported from an uploaded Zepp (Amazfit) export.
_Avoid_: Health data, wearable sync
