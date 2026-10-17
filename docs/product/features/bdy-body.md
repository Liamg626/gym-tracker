# BDY: Weigh-ins, Measurement Sessions, Body Fat Estimate

## Rules

- One Weigh-in per day, in kg, entered by hand. Entering again the same day overwrites it.
- Trend Weight on a day = the mean of the Weigh-ins in the 7 days ending that day. With no Weigh-in in those 7 days, that day has no Trend Weight.
- Measurement Session: normally weekly but not enforced; any date, at most one per day (logging again that day overwrites it, like a Weigh-in); in cm. Neck and waist are **required**; chest, shoulders, right arm and right thigh are optional.
- Body Fat Estimate uses the US Navy formula (male): `495 / (1.0324 − 0.19077·log10(waist − neck) + 0.15456·log10(height)) − 450`, using height from Settings.

## Stories

**BDY: Navy body fat calculation** (MVP, domain-only, TDD)
- A pure function in `packages/domain`, tested against published worked examples

**BDY: Log a Weigh-in** (MVP)
- Quick entry (also used by the home widget); overwrites today's entry; shows today's value and Trend Weight

**BDY: Weigh-in history** (MVP)
- List with edit/delete; Trend Weight calculated in `packages/domain`

**BDY: Log a Measurement Session** (MVP)
- Form with required neck/waist and optional fields; saving shows the Body Fat Estimate
- History list with edit/delete

**BDY: Body charts** (v1.1, see INS)
