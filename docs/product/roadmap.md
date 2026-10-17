# Roadmap

Releases map to Jira versions. Sprints are one week long, with no story points.

## MVP: usable at the gym

- Monorepo, CI, Cloudflare deploys with per-PR preview URLs
- Passphrase login (ADR-0003)
- Exercise Library, generated from Liam's own exercise list (ADR-0006)
- Routines: create, edit, start a Workout from one
- Live Workout logging: Start/End Workout with an elapsed clock (no rest timer), prefill from last time, Warm-up Sets, RIR, notes, per-exercise weight step; Sets saved on the device first (ADR-0004); auto-end after 3h with no Sets
- Home screen widgets in a fixed default layout (Start Workout on the phone only, Recovery Map, Quick Weigh-in, This week, Last Workout, Latest Body Fat Estimate, Weight and Body Fat chart)
- Settings: Weekly Target, height, sex
- Workout history: view, edit, delete, log after the fact
- Weigh-ins (one per day) and Trend Weight
- Measurement Sessions and the Body Fat Estimate (US Navy, male, 188cm)
- Recovery Map: **time-only** rules on the **anatomical** body diagram (fitness-style front/back SVG, ADR-0007)

## v1.1: progress and goals

- Customisable home screen: edit mode, move/resize to set sizes, add/remove widgets, layouts per device saved to the API
- PR detection, with a celebration during the Workout
- Milestones (weight × reps) and Body Goals (optional deadline, on-track indicator)
- Charts: Estimated 1RM per Exercise, Trend Weight, Body Fat Estimate, tape measurements, Workout calendar

## v1.2: insights

- Weekly Breakdown (Monday–Sunday, every metric listed in the vision)
- Volume per Muscle views, Working Sets per Muscle against a target range
- Researched, volume-weighted fatigue model replaces the time-only rules

## v1.3: Watch Data

- Upload a Zepp export into the app; extract heart rate, resting HR, HRV, sleep and steps
- Watch Data in the Weekly Breakdown

## Defaults

kg only · weeks run Monday–Sunday · Europe/London · dark mode · no backups (decided)
