# Vision

## What it is

A personal strength-training tracker for one lifter (Liam), used on an iPhone 15 Pro at the gym and on a larger screen as a dashboard for viewing and managing data (Workouts are logged on the phone). It is also a public portfolio piece, so the code, docs and workflow (Jira, ADRs, tests, CI) are part of the product.

## Why build it

- To have one that is entirely his own, with no paid tiers and personalised freely.
- To get features other apps don't have, starting with the **Recovery Map**.
- To practise React and learn a real cloud backend.

## Users

Exactly one, forever. There are no accounts, no sharing and no multi-user design. Anything that exists only to support other users is out of scope.

## Core capabilities

1. **Log Workouts live**, from Routines or ad hoc. Start and End stamp the duration (no rest timer), previous values are prefilled, and Warm-up Sets and RIR can be recorded.
1. **Customisable home screen** of widgets that can be moved and resized, like an iOS home screen.
2. **Recovery Map**: anatomical front/back diagram showing each Muscle as Fatigued / Recovering / Ready.
3. **Body tracking**: daily Weigh-ins and a weekly Measurement Session, with a Body Fat Estimate from the US Navy formula (male, 188cm).
4. **Goals**: hand-written Milestones (weight × reps) and Body Goals with optional deadlines.
5. **Progress over time**: Estimated 1RM per Exercise, Volume per Muscle, body trends.
6. **Weekly Breakdown** every Monday.
7. **Watch Data** (Amazfit via Zepp) brought in by uploading an export file.

## Constraints

- **£0 running cost.** No Apple Developer Program, and no Mac.
- **Public repo.** Real health data must never be committed.
- **Built by Claude**, with Liam overseeing and testing.

## Non-goals

- Cardio, classes and sport tracking (weights only)
- Native iOS app and live Apple Health integration
- AI-written coaching summaries
- Social features, sharing, multiple users
- An in-app "create exercise" screen (the Exercise Library is maintained in the repo)
- A full programme schedule with progression rules
