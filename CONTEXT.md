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
Reps in reserve: how many more reps the lifter could have done at the end of a Set. Optional; a Working Set with no RIR is treated as RIR 1 by the fatigue model.
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
A skeletal muscle, or a head or part of one, that the app tracks (e.g. "Biceps brachii, long head"). Each has a stable ID, a display name, the side of the Recovery Map it shows on (front, back or both) and one Muscle Group. Muscles are split only where the parts can be trained differently or are visibly distinct.
_Avoid_: muscle group (say Muscle Group only for the roll-up), body part

**Muscle Group**:
A roll-up of Muscles for summaries and filters: Chest, Shoulders, Back, Biceps, Triceps, Forearms, Core, Glutes and hips, Quads, Hamstrings, Calves and shins. Every Muscle belongs to exactly one.
_Avoid_: Body part, muscle (for a group), split

**Region**:
One shape on the Recovery Map. A Region shows one or more Muscles and is coloured by the worst Recovery State among them; Muscles with no state are ignored, and a Region where none has a state is grey.
_Avoid_: Area, zone, body part

**Primary Muscle / Secondary Muscle**:
The role a Muscle plays in an Exercise: the main mover, or an assisting one. In the fatigue model a Secondary Muscle takes half the fatigue of a Primary Muscle for the same Working Set.

**Recovery State**:
A Muscle's readiness: **Fatigued** (red, just worked), **Recovering** (amber) or **Ready** (green).
A Muscle with no Working Sets yet has no Recovery State and is shown grey.
_Avoid_: Fresh, sore, rested

**Recovery Map**:
The front-and-back body diagram that colours each Region by the Recovery State of its Muscles.
_Avoid_: Heatmap, body chart

**Fatigue Dose**:
How hard one Workout hit a Muscle: the sum over its Working Sets of 1 (Primary Muscle) or 0.5 (Secondary Muscle), times an effort factor from the Set's RIR. Internal to the fatigue model; not shown in the UI.
_Avoid_: Effective sets

**Recovery Window**:
The hours after a Workout until a Muscle is Ready, set by the Muscle's Fatigue Dose from that Workout (12 h at the lowest dose, 72 h at a Fatigue Dose of 4 or more).
_Avoid_: Rest period, cooldown

**Fatigue Level**:
A Muscle's remaining fatigue from 1 (just worked) to 0 (Ready), falling in a straight line across the Recovery Window. Recovery State is read from it: Fatigued for the first third of the window, Recovering after that, Ready at 0.
_Avoid_: Fatigue score

**Weekly Sets**:
Working Sets per Muscle Group over a Monday-Sunday week, each counted once, with a Secondary Muscle counting half a set.
_Avoid_: Hard sets, effective sets

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
The Monday–Sunday summary of Workouts, Volume, PRs, body changes and goal progress.
_Avoid_: Report, weekly summary

