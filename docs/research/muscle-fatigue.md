# Research: muscle fatigue, recovery time and weekly Working Sets

SCRUM-9 · [REC-002] · researched 2026-10-17

## Question

How long does a **Muscle** take to recover after resistance training, and how does that scale with the number of **Working Sets** and with effort (**RIR**)? How much fatigue should a **Secondary Muscle** take compared with a **Primary Muscle**? Which marker in the literature best means "ready to train again"? Can sleep, resting heart rate or HRV adjust recovery (context for future **Watch Data**)? And what weekly Working Set ranges per Muscle are supported (for the v1.2 insights and Settings)?

The output is a model for the v1.2 **Volume-weighted fatigue model** story, which replaces the time-only rules in `docs/product/features/rec-recovery.md` behind the same interface. The model may only use data the app records: Working Sets, reps, weight, RIR, time, Primary/Secondary Muscles. Every number in the config below is either traced to a source or marked **our own assumption**.

## Summary and recommendation

- **The literature gives time courses for a handful of Exercises, not a table of recovery times per Muscle.** The best-matched trials (resistance-trained adults, multi-set bench press and squat) show performance back to baseline in **about 6 h (far from failure, low volume) to 48-72 h (sets taken to failure, or 8 x 10)**. See [Q1](#q1-how-long-do-muscles-take-to-recover) and [Q2](#q2-how-recovery-scales-with-volume-and-effort).
- **Nothing retrieved supports different recovery times for large vs small Muscles or fast vs slow fibres.** The one direct comparison (untrained, eccentric-only) found arm muscles recovered *slower* than leg muscles ([Jamurtas 2005][jamurtas2005]). The proposed config therefore uses one recovery scale for every Muscle Group (1.0) and keeps the field so Liam can tune it.
- **Effort changes the immediate drop more clearly than the recovery.** Closer to failure means a bigger velocity loss right after the Working Set ([Refalo 2023][refalo2023]). The recovery difference is small: in Refalo 2023 velocity at 24 h was -3% for both failure and 1 RIR, and there was no significant difference at 48 h. Morán-Navarro 2017 compared 3 x 10 to failure with 6 x 5, which changes reps and effort together, so it cannot isolate proximity to failure ([Morán-Navarro 2017][moran2017]).
- **Secondary Muscle = 0.5 of a Primary set** is supported, but only for *training stimulus*, not for fatigue. A 2026 meta-regression of 67 studies found that counting indirect (synergist) sets as half a set predicted hypertrophy better than counting them as full sets or as zero (strength was not the basis of that finding) ([Pelland 2026][pelland2026]). No study retrieved measures fatigue or recovery in synergists against a fraction. One bench press study suggests triceps soreness lasts as long as chest soreness ([Nuckols 2026][nuckols2026]), which argues *against* 0.5 for recovery time.
- **Best marker for "ready to train again": recovery of force or velocity** (maximal voluntary contraction torque, lifting velocity), not soreness or creatine kinase ([Warren 1999][warren1999]). The app records none of these directly, so the model is anchored to performance studies and the doc proposes a cheap check against next-Workout Estimated 1RM.
- **Sleep, resting HR and HRV: do not use in v1.2.** There is no resistance-training evidence that would let us pick a number. See [Q5](#q5-sleep-resting-hr-and-hrv).
- **Weekly Working Sets per Muscle Group: 12-20 is the target range (Baz-Valle 2022), 4 is the minimum detectable gain, and gains keep rising past 20 with diminishing returns (Pelland 2026 preprint tiers).** Sources: [Baz-Valle 2022][bazvalle2022], [Pelland 2026][pelland2026] (tiers from the September 2024 preprint, not the published version). Schoenfeld 2017 shows a dose-response but its 10+ bin was not significant, so it is not the source of any number here. See [Q6](#q6-weekly-working-sets-per-muscle-group).
- **Proposed model** (details below): each Working Set adds `roleWeight x effort(RIR)` to a Muscle's **Fatigue Dose** for that Workout; the Fatigue Dose sets the **Recovery Window** (12 h for a trivial dose rising linearly to 72 h at a Fatigue Dose of 4 and above); Fatigue Level falls linearly from 1 to 0 across that window; **Fatigued** for the first third, **Recovering** until the end, then **Ready**. At the top of the range it reproduces the MVP's 24 h / 72 h boundaries.

## Findings

Evidence level: "full text" means I read the paper's results; "abstract" means I read the PubMed record (via Europe PMC) only. Where a number comes from an abstract I could not check tables.

### Q1: How long do Muscles take to recover

| Study | Who / what | Marker | Result |
|---|---|---|---|
| [Raastad 2000][raastad2000] (abstract) | 10 male strength athletes; squats, front squats and knee extensions for 90 min at 100% of 3RM (and 70% of that) | Isokinetic knee extension, evoked force, squat jump | Knee extension down 12-14% (high) vs 6-7% (moderate) afterwards. Back to baseline by **33 h** after the high protocol and **3 h** after the moderate one. Recovery was biphasic: fast in the first 11 h, then a plateau or second dip at 11-22 h |
| [Morán-Navarro 2017][moran2017] (full text, partly read) | 10 resistance-trained men; bench press and full squat, 3 x 5 reps, 6 x 5, or 3 x 10, each at a 10-rep maximum | Velocity at fixed weights, countermovement jump (CMJ), CK | 3 x 5 and 6 x 5 (stopping at 5 of a possible 10 reps): velocity back to baseline at **6 h**. 3 x 10 (to failure): velocity not fully restored until **48 h**, CMJ until **72 h**; CK was higher than the other protocols at 6 and 24 h. The paper's own text also says velocity at the 1 m/s weight was not fully recovered until 72 h and that this coincided with CK returning to baseline, so the end point is **48-72 h depending on the variable** |
| [Refalo 2023][refalo2023] (full text) | 24 resistance-trained adults (12 men, 12 women); 6 sets of bench press at 75% 1RM to failure, or stopping at 1 RIR or 3 RIR | Bench velocity at a fixed weight, soreness, perceived recovery | See Q2. Velocity back to within noise by **48 h** in all three conditions. Strength itself (1RM) was not measured |
| [Pareja-Blanco 2019][pareja2019] (full text) | 17 physically active men, not strength-trained; 3 sets of Smith machine squat at 60% or 80% 1RM, stopping at 20% or 40% velocity loss | Velocity at a fixed weight (V1), CMJ, 20 m sprint | V1 as % of baseline at 24 h / 48 h: 60%-20%: 92.2 / 95.5; 60%-40%: 92.6 / 93.0; 80%-20%: 95.9 / 100.8; 80%-40%: **89.2** (significant) / 95.9. Only 80%-20% had fully recovered by 48 h. CMJ stayed below baseline at 24 h for both 60% protocols |
| [Bartolomei 2017][bartolomei2017] (abstract) | 12 resistance-trained men; 8 x 10 vs 8 x 3 (leg extension, squat-type tests) | Isometric strength (MVIC), CMJ power, CK, LDH, myoglobin | Isometric leg extension strength still down at **72 h** after the 8 x 10 protocol, not after 8 x 3. Damage markers rose after both |
| [Soares 2015][soares2015] (abstract) | 16 highly resistance-trained men; elbow flexors, 8 x 10RM seated row vs 8 x 10RM preacher curl (opposite arms) | Isometric torque, soreness (DOMS) | Torque down 26.8% (curl) vs 15.1% (row) at 10 min. At 24 h the curl was still down 8.4%; the row was back to baseline. Soreness raised at 24, 48 and 72 h after the curl, back to baseline by 72 h after the row |
| [de Camargo 2022][decamargo2022] (abstract) | 10 resistance-trained men; 5 x 8RM back squat vs knee extension | Rectus femoris thickness, leg circumference, soreness | Soreness higher at 24 and 36 h after squats than after knee extensions. Measured to 36 h only |
| [Jamurtas 2005][jamurtas2005] (abstract) | 11 untrained men; 6 x 12 eccentric-only at 75% of maximal eccentric torque, knee extensors vs elbow flexors | ROM, soreness, CK, LDH, myoglobin, torque | Soreness and ROM changes similar in both. CK and myoglobin larger in the arms at 72 and 96 h. Torque still down at **96 h in the arms** and fully recovered by 96 h in the legs |
| [Nuckols 2026][nuckols2026] (full text) | 42 trained bench pressers (21 men, 21 women); sets of 5 at 75% 1RM, 90 s rest, to failure; tracked 72 h | Soreness of pectorals, triceps, anterior deltoids; Estimated 1RM from velocity | Pectoral and anterior deltoid soreness: 24 h > 48 h > 72 h. Triceps soreness: 24 h not different from 48 h, lower at 72 h. Estimated 1RM was still below the pre value at 48 h and 72 h on the paper's wording, which is ambiguous. No recovery point was defined. No difference between men and women |

What follows from these:

- **Anchors for the model.** Low effort, low dose: back to baseline within hours ([Morán-Navarro 2017][moran2017]). Moderate dose near failure (6 Working Sets at RIR 1, or 3 x 10 to failure): about 24-48 h for velocity, up to 72 h for jumping and CK. Larger dose (8 x 10, or sets to failure with lots of reps): 72 h or more for isometric strength ([Bartolomei 2017][bartolomei2017], [Nuckols 2026][nuckols2026]).
- **Muscle size.** The only head-to-head (untrained, eccentric only) went the opposite way to the "big Muscles take longer" rule ([Jamurtas 2005][jamurtas2005]). Nothing else retrieved compares Muscles at matched effort.
- **Exercise type, same Muscle.** Single-joint work on the elbow flexors cost more strength and took longer to recover than a multi-joint row at the same 8 x 10RM ([Soares 2015][soares2015]), but for the legs the multi-joint Exercise (back squat) left more soreness at 24 and 36 h than the single-joint one (knee extension) ([de Camargo 2022][decamargo2022]). The two disagree on which type is worse, so I do not add an Exercise-type term.
- **Fibre type: no usable source.** My search returned small studies and secondary summaries with conflicting conclusions (one linking slow-fibre dominance to worse repeated-bout outcomes, another linking fast fibres to soreness). I did not retrieve the primary papers, so I cite none and the config has no fibre-type term.
- **Eccentric emphasis.** Unaccustomed eccentric work causes damage and delayed soreness ([Hody 2019][hody2019], abstract) and is the usual protocol for the longest recoveries in the table (96 h+ in [Jamurtas 2005][jamurtas2005]). The app cannot see tempo or eccentric emphasis, so it is not modelled.
- **Training status / repeated bout effect.** A second bout of the same multi-joint exercise gives less soreness and CK (standardised mean difference 0.51-1.23 at 24 and 48 h) and less strength loss (SMD -0.27 to -0.40) than the first ([Doma 2023][doma2023], 20 studies). In a biopsy study of 10 young men, damage was highest after the first Workout of a training block, lower at week 3 and minimal at week 10 ([Damas 2016][damas2016]). A third bout of eccentric work added no further protection beyond the second ([Lindsay 2021][lindsay2021]). All the anchor studies above used resistance-trained or active adults, so the model describes someone on a familiar Routine. A new Exercise or a long layoff probably lengthens recovery, but I found no numbers, so the model has no novelty term.
- **Sex.** No difference in soreness or Estimated 1RM recovery over 72 h after bench press to failure ([Nuckols 2026][nuckols2026]). Women completed twice as many reps. Men lost more velocity right after the Working Sets under failure (-29% vs -21%) ([Refalo 2023][refalo2023]). The model has no sex term.
- **Doing more before recovery is complete.** Repeating 3 x 10 eccentric elbow flexor work 3 and 6 days after the first did not worsen damage or slow recovery in 12 untrained men ([Nosaka 1995][nosaka1995], abstract). So a Muscle that is not **Ready** is not necessarily off limits; the state is advice.

### Q2: How recovery scales with volume and effort

**Effort (proximity to failure)**

- Six bench Working Sets at 75% 1RM: velocity drop at 4 min was -25% (failure), -13% (1 RIR), -8% (3 RIR). At 24 h it was -3%, -3% and +2%; at 48 h the differences were no longer significant. Soreness at 24 h was higher for failure than for 1 RIR (effect size 0.79) or 3 RIR (1.16) ([Refalo 2023][refalo2023]).
- Failure is where the cost jumps. Velocity loss from the first to the last set was 22% (failure), 9% (1 RIR) and 6% (3 RIR) (same paper).
- With the same total reps, 3 x 10 to failure recovered slower than 6 x 5 at 24-48 h ([Morán-Navarro 2017][moran2017]). This is confounded: the two protocols differ in rep scheme as well as proximity to failure, so it is not evidence about effort alone.
- For gains: a meta-analysis found no significant difference between training to failure and not (hypertrophy effect size 0.22, 95% CI -0.11 to 0.55; strength -0.09, -0.22 to 0.05) ([Grgic 2022][grgic2022]); in trained participants alone, failure was slightly better for hypertrophy (0.15, 0.03 to 0.26). A meta-regression found hypertrophy rose as sets ended closer to failure while strength did not, but warned the RIR values were *estimated from study descriptions* ([Robinson 2024][robinson2024]).
- RIR itself is usable as a measure: resistance-trained men and women predicted 1 and 3 RIR on the bench press with a mean absolute error of 0.65 reps (SD 0.78) ([Refalo 2024][refalo2024], abstract). Bench press only.

**Volume (number of Working Sets in a Workout)**

- 8 x 10 vs 8 x 3 in trained men: larger drops in jump power and isometric strength, and isometric strength still down at 72 h only after 8 x 10 ([Bartolomei 2017][bartolomei2017]). The two protocols differ in reps *and* effort, so this is volume and effort together.
- In 17 active men, the authors concluded that a higher velocity loss (40%) and a lower relative weight (60% 1RM, more reps) gave more fatigue and slower recovery ([Pareja-Blanco 2019][pareja2019]); the 80%-40% protocol was the one still significantly down at 24 h.
- I did not find a study that varies *only* the number of sets at fixed effort and tracks recovery for 72 h. The scaling in the model (linear in Fatigue Dose, capped) is therefore **our own assumption** fitted through the anchors above, not a published relationship.

**Reps and weight.** The trials above are not consistent enough to let reps or weight set recovery on their own once effort is known. v1.2 uses sets and RIR only; weight and reps are stored but unused by the fatigue model.

### Q3: How much fatigue a Secondary Muscle should take

- **For training stimulus, 0.5 is the best-supported fraction.** [Pelland 2026][pelland2026] classified every set in 67 studies (2,058 participants, 79.1% male, mean age 25) as direct (the measured Muscle is the primary force generator) or indirect (a synergist). Indirect sets were counted as 1 ("total"), 0.5 ("fractional") or 0 ("direct only"). Fractional counting had the strongest support: for weekly hypertrophy volume, 2 x log(Bayes factor) was 9.48 against "total" (strong) and 10.29 against "direct" (very strong) (preprint tables; the published abstract confirms "fractional" was strongest). Their worked example: a biceps study with 5 sets of curls and 5 sets of rows counts as 7.5 fractional sets.
- **Limits.** Only three weightings were tried (1, 0.5, 0), so 0.5 is the best of three, not a fitted optimum. The authors say as much: "the 'fractional' quantification method suffers from the assumption that all indirect training should be quantified as half a set". Classifying sets as direct or indirect "was not wholly objective" ([Pelland 2026 preprint][pelland2024pre]). The outcome was growth or strength, not fatigue.
- **Supporting direction.** Adding direct elbow-flexor and triceps exercises to lat pulldown and bench press gave no extra elbow flexor growth in 29 untrained men (6.5% vs 7.04% muscle thickness), i.e. the pulling already trained the biceps ([Gentil 2013][gentil2013]). That shows indirect sets matter; it gives no fraction.
- **Evidence against 0.5 for recovery.** After bench press to failure, triceps soreness did not drop between 24 and 48 h while pectoral and anterior deltoid soreness did ([Nuckols 2026][nuckols2026]). Soreness is a weak recovery marker (Q4), but it is the only synergist data I found.
- **Recommendation.** Use 0.5 because it is the only number with any quantitative support and it matches how the weekly-set ranges in Q6 were derived. Treat it as a tunable; expect it to make Secondary Muscles look Ready too early (see the worked example).

### Q4: Markers: strength, soreness, creatine kinase

- **Strength / force-generating capacity is the recommended marker.** A review of measurement tools concluded that maximal voluntary contraction torque and range of motion are the best methods for quantifying the size and duration of muscle injury in humans, and that soreness ratings and blood protein levels "should be discouraged" for that purpose ([Warren 1999][warren1999], abstract).
- **Soreness tracks strength loss only loosely.** In 56 sedentary men after 60 eccentric reps, strength loss correlated with soreness at 48 h ([Konrad 2022][konrad2022], abstract), but this is a single time point after a damaging protocol, not a trained lifter's normal Workout. In [Refalo 2023][refalo2023] soreness was higher after failure but velocity recovered at the same time for failure and 1 RIR.
- **CK is the weakest candidate for "ready".** Its validity as a damage marker during exercise is "controversial" and it varies with ethnicity, age and sex ([Baird 2012][baird2012], abstract). In [Bartolomei 2017][bartolomei2017] CK rose after both the 8 x 10 and 8 x 3 protocols although only the first left strength down at 72 h. It does track velocity recovery in [Morán-Navarro 2017][moran2017], which called it the biochemical variable "most related" to the mechanical ones.
- **Damage is not the goal.** Early muscle protein synthesis after the first Workout of a block coincided with the most damage and did not relate to later growth ([Damas 2016][damas2016]). So "recovered from damage" is not what the lifter needs; "can produce normal force again" is.
- **What the app can measure.** Estimated 1RM and reps at a given weight are recorded. Comparing the model's state at the start of a Workout with that Exercise's Estimated 1RM versus the lifter's recent best would be a free sanity check on the thresholds (not a published method).

### Q5: Sleep, resting HR and HRV

- **Sleep and strength.** A systematic review (17 studies, quality rated "moderate" or "weak") found total sleep deprivation had little effect on strength, but consecutive nights of sleep *restriction* could lower force in multi-joint, not single-joint, movements ([Knowles 2018][knowles2018], abstract). One night without sleep cut muscle protein synthesis by 18% (n = 13), raised cortisol 21% and lowered testosterone 24% ([Lamon 2021][lamon2021], abstract). Neither gives a recovery-time multiplier.
- **HRV and resistance exercise.** Acute resistance exercise lowers parasympathetic modulation more than aerobic exercise, but resistance training has no effect on resting HRV in healthy young adults ([Kingsley 2016][kingsley2016], review abstract). A review of cardiac parasympathetic reactivation states it "does not appear to coincide with the recovery of all physiological systems (e.g. energy stores or the neuromuscular system)" and that data after strength work are limited ([Stanley 2013][stanley2013], abstract). HRV-guided training beat fixed training only by a small, non-significant margin for fitness and endurance performance, and all of that evidence is aerobic ([Manresa-Rocamora 2021][manresa2021], abstract).
- **Resting heart rate.** I found no resistance-training source that relates resting HR to local muscle recovery. It is not used.
- **Wearable accuracy.** A meta-analysis of 24 studies (798 people) found consumer wrist-worn trackers differ from polysomnography: total sleep time -16.9 min (95% CI -26.3 to -7.4), sleep efficiency -4.7 points, wake after sleep onset +13.3 min ([Lee 2025][lee2025], abstract). Huami Arc and Xiaomi Mi Band 5 were among the devices; I did not find a Zepp/Amazfit-specific validation.
- **Recommendation.** Keep **Watch Data** out of the v1.2 recovery model. The evidence supports sleep and HRV as context for the Weekly Breakdown, not as a number that shortens or lengthens a Recovery Window. If added later, the config has a reserved `watchAdjustment: null`.

### Q6: Weekly Working Sets per Muscle Group

| Source | Finding |
|---|---|
| [Schoenfeld 2017][schoenfeld2017] (meta-regression, 15 studies, 34 groups) | Each extra weekly set per Muscle Group was associated with +0.37% muscle gain (effect size +0.023). Higher vs lower volume within a study: +3.9%. Three-level split (<5, 5-9, 10+ sets) only a trend (p = 0.074). Few trained participants |
| [Schoenfeld 2019][schoenfeld2019] (trial, 34 resistance-trained men, 8 weeks, 3 Workouts a week) | 1, 3 or 5 sets per Exercise per Workout: strength gains similar; hypertrophy rose with volume at the elbow flexors, mid-thigh and lateral thigh |
| [Baz-Valle 2022][bazvalle2022] (systematic review, 7 studies, trained young men, at least 1 year) | Concluded 12-20 weekly sets per Muscle Group is a sensible standard for hypertrophy. No difference between moderate and high volume for quadriceps (p = 0.19) or biceps (p = 0.59); high was better for triceps (p = 0.01) |
| [Pelland 2026][pelland2026] (67 studies, fractional counting) | Hypertrophy rises with volume with diminishing returns, no clear plateau found. Tiers from the **September 2024 preprint** ([Pelland preprint][pelland2024pre]), not the published 2026 version (fractional sets per week): minimum detectable gain **4**; 5-10 efficient (about 6 more sets per detectable increment); 11-18 (about 8.5 more); 19-29 (about 10.75 more); 30-42 (about 12.5 more); 43+ unclear. Detectable means above 2.05% (hypertrophy). Strength plateaus far earlier (minimum 1 set, lower efficiency beyond about 5) |
| Frequency: [Schoenfeld 2016][schoenfeld2016], [Grgic 2019][grgic2019], [Pelland 2026][pelland2026] | Volume-equated, training a Muscle twice a week beat once; later reviews and the 2026 meta-regression find little independent effect of frequency on hypertrophy. Not used to gate targets |
| Maintenance: [Spiering 2021][spiering2021], [Bickel 2011][bickel2011] | Strength and size in young adults were kept for up to 32 weeks with one Workout per week and one set per Exercise at the same relative weight; a third of the original dose kept muscle size in the young. No weekly set figure to copy |

Limits: the tier table is from a **preprint dated September 2024**; I could not read the published 2026 version past its abstract, so numbers may have shifted. Short interventions (about 10 weeks on average), mostly young men, volumes counted as sets completed to an unclear proximity to failure (only about 30% of hypertrophy effects had a clear definition of momentary failure) ([Pelland 2026 preprint][pelland2024pre]). Group-specific targets are not supported by the evidence except weakly for triceps ([Baz-Valle 2022][bazvalle2022]), so the proposal uses one range for every Muscle Group.

## Proposed model

### Definitions

For one Muscle `m` and one Workout `w` performed at time `t_w`:

1. **Set weight.** For each Working Set `j` that tags `m`: `s_j = roleWeight[role_j] x effort[RIR_j]`.
   - `roleWeight`: Primary 1.0, Secondary 0.5 ([Pelland 2026][pelland2026]; used for stimulus; applied to fatigue is **our own assumption**).
   - `effort[RIR]` = `effortByRir[min(RIR, 5)]`, so RIR 6 or more uses the RIR 5 value.
   - The values for RIR 0, 1 and 3 (1.00, 0.52, 0.32) are **acute velocity-loss ratios**: the drop in bench velocity 4 min after the Set in [Refalo 2023][refalo2023] (failure -25%, 1 RIR -13%, 3 RIR -8%, divided by the failure drop, rounded). They are not recovery times. Using them as fatigue weights is **our own assumption** (S for the ratios, A for their use here).
   - RIR 2 -> 0.42 is the midpoint of the RIR 1 and RIR 3 values (**our own assumption**). RIR 4 -> 0.25 and RIR 5 or more -> 0.20 are **our own assumption** (no study tested RIR above 3 on this measure; [Morán-Navarro 2017][moran2017] stopped at 5 of 10 reps and recovered in about 6 h, so the value is small but not zero).
   - No RIR recorded: treat as RIR 1 (**our own assumption**: errs towards a longer window).
2. **Fatigue Dose** in the Workout: `U = sum of s_j` over the Workout's Working Sets for that Muscle. Warm-up Sets are excluded (existing rule).
3. **Recovery Window** (hours until Ready): `D = scale_m x (minHours + (maxHours - minHours) x min(U, capFatigueDose) / capFatigueDose)`, where `scale_m = muscleScale[m] ?? groupScale[group(m)]` and `group(m)` is the Muscle Group of `m`.
   - `maxHours = 72`: end of the 3 x 10-to-failure and 8 x 10 time courses ([Morán-Navarro 2017][moran2017], [Bartolomei 2017][bartolomei2017]) and the MVP's 72 h.
   - `minHours = 12`: **our own assumption**; trial values were about 6 h ([Morán-Navarro 2017][moran2017]) and I rounded up to avoid claiming instant recovery.
   - `capFatigueDose = 4`: **our own assumption**; chosen so 3 sets to failure (U = 3) gives 57 h, inside the 48-72 h seen in [Morán-Navarro 2017][moran2017], and 8 sets at RIR 1 (U = 4.16) reaches the 72 h cap.
   - Linear between those points: **our own assumption** (no study varies only volume).
   - `groupScale` and `muscleScale` default to 1.0 for every Muscle Group and Muscle (**our own assumption**; no supported difference, see Q1).
4. **Fatigue Level** from that Workout: `L_w(t) = max(0, 1 - (t - t_w) / D)`. It starts at 1 and falls linearly to 0 (linear decay is **our own assumption**; [Raastad 2000][raastad2000] saw a biphasic pattern the model ignores).
5. **Across Workouts:** `L(t) = max over Workouts of L_w(t)` (**our own assumption**: no compounding; a later small Workout does not extend an earlier large Workout's window. [Nosaka 1995][nosaka1995] is the only support, in untrained eccentric work).
6. **Recovery State**, from the combined `L(t)` (so the max rule decides which Workout counts):
   - **Fatigued** while `L > 1 - fatiguedUntilFraction`, i.e. the first third of a Workout's window (one third; **our own assumption**, chosen so a full-size Workout, D = 72 h, gives the MVP's 24 h Fatigued boundary).
   - **Recovering** while `0 < L <= 1 - fatiguedUntilFraction`.
   - **Ready** once `L = 0`.
   - No Working Sets ever on the Muscle: no state (grey), as today.

Weekly target counting (Q6): per Muscle Group per Monday-Sunday week, count each Working Set once, at the highest role weight among its tagged Muscles in that group (matches the existing "counts each Working Set once" rule). A Primary set counts 1, a Secondary-only set counts 0.5. All Working Sets count regardless of RIR (**our own assumption**, mirrors how [Pelland 2026][pelland2026] counted sets; `maxRirCounted` is provided if Liam wants a cutoff).

### Config shape

```ts
// Proposed shape for the fatigue config file named in rec-recovery.md.
// "Source" comments: S = traced to a paper, A = our own assumption.
export const FATIGUE_CONFIG = {
  version: 1,

  roleWeight: { primary: 1.0, secondary: 0.5 },          // S: Pelland 2026 (stimulus); A for fatigue

  // Lookup: effortByRir[min(RIR, 5)]. Values for RIR 0, 1, 3 are Refalo 2023's acute
  // velocity-loss ratios at 4 min (S: a measure of the immediate drop, NOT recovery time).
  // Using them as fatigue weights is A. RIR 2 (midpoint), 4 and 5+ are A.
  effortByRir: { 0: 1.0, 1: 0.52, 2: 0.42, 3: 0.32, 4: 0.25, 5: 0.2 },
  rirWhenMissing: 1,                                      // A

  recovery: {
    minHours: 12,                                         // A (trial: ~6 h, Moran-Navarro 2017)
    maxHours: 72,                                         // S: Moran-Navarro 2017, Bartolomei 2017; MVP
    capFatigueDose: 4,                                    // A (fatigue dose at which maxHours is reached)
    fatiguedUntilFraction: 1 / 3,                         // A (reproduces MVP 24 h at 72 h)
  },

  // Multiplier on the Recovery Window per Muscle Group. All 1.0 is A ("no supported
  // difference", Q1). Keys are taxonomy group IDs (muscle-taxonomy.md); CONTEXT.md names:
  //   chest = Chest, shoulders = Shoulders, back = Back, arms = Arms, core = Core,
  //   hips = Glutes and hips, quads = Quads, hamstrings = Hamstrings,
  //   'lower-legs' = Calves and shins.
  groupScale: {
    chest: 1.0, shoulders: 1.0, back: 1.0, arms: 1.0, core: 1.0,
    hips: 1.0, quads: 1.0, hamstrings: 1.0, 'lower-legs': 1.0,   // all A
  },
  muscleScale: {} as Record<string, number>,             // per Muscle ID overrides, empty by default (A)

  // Weekly Working Sets per Muscle Group (fractional: Secondary = 0.5). Same for every group.
  weeklySets: {
    min: 4,                                               // S: Pelland 2026 preprint (Sept 2024), minimum detectable gain
    targetLow: 12,                                        // S: Baz-Valle 2022 (12-20 per Muscle Group)
    targetHigh: 20,                                       // S: Baz-Valle 2022
    // Bands are lower bounds: a band runs from its `from` up to (not including) the next band's `from`.
    // Fractional totals (Secondary = 0.5) fall in the band whose `from` they are at or above.
    bands: [
      { from: 0, label: 'below minimum' },              // S: below Pelland 2026 preprint minimum detectable gain (4)
      { from: 4, label: 'detectable' },                  // S: Pelland 2026 preprint; 5-10 is its "efficient" tier
      { from: 11, label: 'tier 11-18' },                 // S: Pelland 2026 preprint tier
      { from: 19, label: 'tier 19-29' },                 // S: Pelland 2026 preprint tier
      { from: 30, label: 'tier 30-42' },                 // S: Pelland 2026 preprint tier
      { from: 43, label: 'unclear' },                    // S: Pelland 2026 preprint (no tier above 42)
    ],
    maxRirCounted: null as number | null,                 // A: null = count every Working Set
  },

  watchAdjustment: null,                                  // reserved; no supported number (Q5)
} as const
```

Weekly Working Set bands the UI could use, aligned with the tiers in the Sept 2024 [Pelland preprint][pelland2024pre] (the published 2026 version was not read past its abstract): under 4 = below the minimum detectable gain; 4-10 = detectable, efficient at 5-10 (**4 is the minimum detectable gain; "efficient" is the preprint's 5-10 tier**); 11-18; 19-29; 30-42; 43 or more = unclear. The **target** is a separate overlay of **12-20** from [Baz-Valle 2022][bazvalle2022] (a Muscle Group-agnostic range; not a Pelland tier). Targets are a goal, not a limit: [Pelland 2026][pelland2026] found no clear plateau.

## Worked examples

All numbers are made-up demo values (ADR-0005). Assumed tags for the bench press: Primary `pectoralis-major-sternal`; Secondary `pectoralis-major-clavicular`, `deltoid-anterior`, `triceps-brachii-lateral-head`, `triceps-brachii-medial-head`, `triceps-brachii-long-head`. Assumed tags for the incline press: Primary `pectoralis-major-clavicular`; Secondary `pectoralis-major-sternal`, `deltoid-anterior`. (The Exercise Library is not written yet; this is for illustration.) Config values as above; `t = 0` is the Workout's performed time. Recovery Windows are not rounded in the state checks; elapsed time exactly at a boundary counts as the later state.

### Example 1: 4 Working Sets of bench press at RIR 1

| Muscle | Role | U (Fatigue Dose) | Recovery Window `D` | Fatigued until |
|---|---|---|---|---|
| Pectoralis major, sternocostal | Primary | 4 x 1.0 x 0.52 = **2.08** | 12 + 60 x 2.08 / 4 = **43.2 h** | 43.2 / 3 = 14.4 h |
| Pectoralis major, clavicular part | Secondary | 4 x 0.5 x 0.52 = **1.04** | 12 + 60 x 1.04 / 4 = **27.6 h** | 9.2 h |
| Deltoid, anterior part | Secondary | 4 x 0.5 x 0.52 = **1.04** | 12 + 60 x 1.04 / 4 = **27.6 h** | 9.2 h |
| Triceps brachii, lateral head | Secondary | 1.04 | 27.6 h | 9.2 h |
| Triceps brachii, medial head | Secondary | 1.04 | 27.6 h | 9.2 h |
| Triceps brachii, long head | Secondary | 1.04 | 27.6 h | 9.2 h |

All three triceps heads are tagged Secondary, so they share the same U, D and states.

Fatigue Level `L = 1 - elapsed / D` and state:

| Muscle | 24 h | 48 h | 72 h |
|---|---|---|---|
| Sternocostal pec (P) | L = 1 - 24/43.2 = 0.44 -> **Recovering** | 48 >= 43.2 -> **Ready** | **Ready** |
| Clavicular pec (S) | L = 1 - 24/27.6 = 0.13 -> **Recovering** | **Ready** | **Ready** |
| Anterior deltoid (S) | L = 1 - 24/27.6 = 0.13 -> **Recovering** | **Ready** | **Ready** |
| Triceps lateral head (S) | **Recovering** (0.13) | **Ready** | **Ready** |
| Triceps medial head (S) | **Recovering** (0.13) | **Ready** | **Ready** |
| Triceps long head (S) | **Recovering** (0.13) | **Ready** | **Ready** |

Sanity check against the trial: [Refalo 2023][refalo2023] had 6 Working Sets at 1 RIR. U = 6 x 0.52 = 3.12, D = 12 + 60 x 3.12 / 4 = 58.8 h. The trial saw velocity within 3% of baseline at 24 h and back to baseline at 48 h; the model is a little more cautious than the data.

### Example 2: sensitivity, same 4 Working Sets

| Variant | Pec (P) at 24 / 48 / 72 h | Triceps (S) at 24 / 48 / 72 h |
|---|---|---|
| RIR 1 (Example 1) | Recovering / Ready / Ready | Recovering / Ready / Ready |
| RIR 0 (to failure): U_P = 4.00, D = 72 h; U_S = 2.00, D = 42 h | 24 h is exactly the Fatigued boundary (72/3) so **Recovering**; 48 h **Recovering** (L = 0.33); 72 h **Ready** | Recovering / Ready / Ready |
| RIR 3: U_P = 1.28, D = 31.2 h; U_S = 0.64, D = 21.6 h | Recovering (L = 0.23) / Ready / Ready | **Ready** at 24 h (24 >= 21.6) |
| RIR 1, Secondary weight 1.0 instead of 0.5 | unchanged | U = 2.08, D = 43.2 h: Recovering / Ready / Ready |

The Secondary Muscle result at 24 h is the weak point. [Nuckols 2026][nuckols2026] saw triceps soreness persist to 48 h after bench press to failure. If the app should show triceps as not Ready at 24 h after a Workout like Example 1, set `roleWeight.secondary` to 1.0 (then it matches the pec) or add a floor on Secondary Recovery Windows.

### Example 3: a small Workout after a large one (max rule)

Monday 18:00: 8 Working Sets of bench at RIR 1 on the sternocostal pec: U = 8 x 0.52 = 4.16, above the cap, so D = 72 h.
Tuesday 18:00 (t = 24 h): 2 Working Sets of incline press at RIR 3 (Primary on the clavicular head, but also Secondary on the sternocostal pec): sternocostal pec U = 2 x 0.5 x 0.32 = 0.32, D = 12 + 60 x 0.32 / 4 = 16.8 h.
At Wednesday 06:00 (t = 36 h after Monday, 12 h after Tuesday): Monday's L = 1 - 36/72 = 0.50; Tuesday's L = 1 - 12/16.8 = 0.29. `L = max = 0.50`, so **Recovering**; Tuesday's small Workout does not extend the window. Right after the Tuesday Workout (t = 24 h) the state is **Fatigued** from Tuesday's L = 1 for its first 5.6 h, even though the dose was tiny. That is a known quirk of the model: any Working Set starts a Fatigued period. A minimum-dose cutoff (for example ignore U below 0.5) would fix it but has no evidence behind it.

### Example 4: weekly Working Sets for the Chest group

Bench 4 sets (sternocostal Primary, clavicular Secondary) + incline press 3 sets (clavicular Primary, sternocostal Secondary) = 7 Working Sets at weight 1.0, each counted once for the Chest group even though two chest Muscles are tagged. The Shoulders group gets the same bench sets once at 0.5 (front-delt Secondary) = 2.0 plus incline 3 x 0.5 = 1.5. Chest: 7 (band 4-10, below the 12-20 target); Shoulders: 3.5 before any overhead work (under the 4 minimum).

## Proposed doc changes (for Liam to approve, not applied)

### `docs/product/features/rec-recovery.md`

Replace the **v1.2 researched model** section with:

> ### v1.2 researched model
>
> Volume-weighted fatigue per Muscle, from `docs/research/muscle-fatigue.md`. Each Working Set adds to the Fatigue Dose of every Muscle it tags: 1 for a Primary Muscle, 0.5 for a Secondary Muscle, multiplied by an effort factor from its RIR (1.0 at RIR 0, falling to 0.2 at RIR 5 or more; an unrecorded RIR counts as RIR 1). A Workout's Fatigue Dose sets the Muscle's Recovery Window, from 12 h up to 72 h, which is reached at a Fatigue Dose of 4. Fatigue Level falls linearly from 1 to 0 over the Recovery Window; the Muscle is Fatigued for the first third, Recovering until the end of the window, then Ready. When several Workouts overlap, the highest Fatigue Level wins. All numbers, including the Weekly Sets targets, live in the fatigue config file, not in Settings.

Add under **Rules**:

> - Weight and reps do not affect Recovery State; only Working Sets, role (Primary or Secondary), RIR and time do.
> - A Muscle that is not Ready is advice, not a restriction.

Replace the story **REC: Volume-weighted fatigue model**:

> **REC: Volume-weighted fatigue model** (v1.2, domain, TDD, blocked by the research)
> - Pure function: Workouts + Exercise Library + fatigue config + now -> Recovery State and Fatigue Level per Muscle, behind the same interface as the time-only rules
> - Config holds `version`, `roleWeight`, `effortByRir`, `rirWhenMissing`, `recovery`, `groupScale`, `muscleScale`, `weeklySets` and `watchAdjustment` (see `docs/research/muscle-fatigue.md` for values and sources)
> - Proposal: the config lives in one shared fatigue config module, e.g. `src/fatigue/fatigue.config.ts`, imported by both the fatigue model and the Weekly Sets insight so the targets and the Recovery Window share one source. The path is a suggestion; no `src/` module exists yet.
> - Tests cover the worked examples in the research doc and the MVP boundaries at the maximum dose

Add a story:

> **INS: Weekly Working Sets per Muscle Group** (v1.2)
> - Counts each Working Set once per Muscle Group per Monday-Sunday week (Primary 1, Secondary 0.5) and shows it against the bands in the config (below 4, 4-10, 11-18, 19-29, 30-42, 43+) with the 12-20 target marked

### `CONTEXT.md`

Add under **Muscles and recovery**:

> **Recovery Window**:
> The hours after a Workout until a Muscle is Ready, set by the Muscle's Fatigue Dose from that Workout (12 h at the lowest dose, 72 h at a Fatigue Dose of 4 or more).
> _Avoid_: Rest period, cooldown
>
> **Fatigue Dose**:
> How hard one Workout hit a Muscle: the sum over its Working Sets of 1 (Primary Muscle) or 0.5 (Secondary Muscle), times an effort factor from the Set's RIR. Internal to the fatigue model; not shown in the UI.
> _Avoid_: Effective sets
>
> **Fatigue Level**:
> A Muscle's remaining fatigue from 1 (just worked) to 0 (Ready), falling in a straight line across the Recovery Window. Recovery State is read from it: Fatigued for the first third of the window, Recovering after that, Ready at 0.
> _Avoid_: Fatigue score
>
> **Weekly Sets**:
> Working Sets per Muscle Group over a Monday-Sunday week, each counted once, with a Secondary Muscle counting half a set.
> _Avoid_: Hard sets, effective sets

Amend **Primary Muscle / Secondary Muscle**, adding:

> In the fatigue model a Secondary Muscle takes half the fatigue of a Primary Muscle for the same Working Set.

Amend **RIR**, adding:

> Optional; a Working Set with no RIR is treated as RIR 1 by the fatigue model.


## Decisions and open questions

Answered by Liam on 2026-10-17:

1. **Weekly Sets targets** live in the config file, not Settings (same as every other threshold in rec-recovery.md).
2. **Name for the internal fatigue unit:** Fatigue Dose (new glossary term; "effective set" stays avoided).
3. **Secondary weight for fatigue:** keep 0.5. Example 2 shows the trade-off; tune `roleWeight.secondary` later if needed.
4. **Minimum-dose cutoff:** none. Any Working Set counts (Example 3's quirk accepted).

Still open:

5. **Should RIR be mandatory?** The model depends on it; an unrecorded RIR defaults to 1, which lengthens Windows if most of your Working Sets are really RIR 3.
6. **Validation.** Are you happy to compare model state with the next Workout's Estimated 1RM and reps on your own data, locally (ADR-0005: demo data only in the repo)?

## Unverified / limits

- **Muscle-specific recovery times are not established.** All the time courses come from a few Exercises (bench, squat, knee extension, elbow flexor work) in small samples (10-24 people per trial). Using them for forearm flexors, soleus or erector spinae is extrapolation.
- **Abstract-only sources.** Most Q1, Q4, Q5 and Q6 citations were read as PubMed abstracts (via Europe PMC) because PubMed and several publisher pages returned bot checks. Full text read: Refalo 2023, Pareja-Blanco 2019, Nuckols 2026, the Pelland preprint, and the results section of Morán-Navarro 2017.
- **Pelland 2026** was read in full only as the September 2024 SportRxiv preprint; the published Sports Medicine version was read as an abstract. Tier numbers and Bayes factors are from the preprint. The preprint calls its comparison "Baz-Valle 2020"; the journal record is 2022.
- **Morán-Navarro 2017** text is internally inconsistent on when velocity recovers after 3 x 10 (48 h in one paragraph, 72 h in another); both are reported.
- **The effort values for RIR 0, 1, 3** come from one study of one Exercise (bench press, 24 people). They measure *acute* velocity loss at 4 min, not recovery time. At 24 h failure and 1 RIR were equal in velocity ([Refalo 2023][refalo2023]), so the model may overstate the gap between RIR 0 and 1.
- **The model has not been fitted or validated on any data.** The linear window, the cap at 4, the one-third Fatigued fraction, the max rule and the RIR 4-5 values are our own assumptions.
- **Excluded or unusable:** I found no primary source for fibre-type effects on recovery, for novelty (new Exercise) effects in hours, or for resting HR. A retracted study on single-joint additions (Barbalho) turned up in a search and is not cited. I could not read a 2026 paper on 7, 14 and 21-set lower-body Workouts (publisher bot check), so it is not used.

## Sources

Recovery time courses
- [raastad2000]: Raastad T, Hallén J. Recovery of skeletal muscle contractility after high- and moderate-intensity strength exercise. *Eur J Appl Physiol* 2000 — https://pubmed.ncbi.nlm.nih.gov/10929214/
- [moran2017]: Morán-Navarro R et al. Time course of recovery following resistance training leading or not to failure. *Eur J Appl Physiol* 2017;117(12):2387-2399 — https://pubmed.ncbi.nlm.nih.gov/28965198/
- [refalo2023]: Refalo MC, Helms ER, Hamilton DL, Fyfe JJ. Influence of resistance training proximity-to-failure, determined by repetitions-in-reserve, on neuromuscular fatigue in resistance-trained males and females. *Sports Med Open* 2023;9:10 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9908800
- [pareja2019]: Pareja-Blanco F et al. Time course of recovery following resistance exercise with different loading magnitudes and velocity loss in the set. *Sports (Basel)* 2019;7(3):59 — https://pmc.ncbi.nlm.nih.gov/articles/PMC6473797
- [bartolomei2017]: Bartolomei S et al. Comparison of the recovery response from high-intensity and high-volume resistance exercise in trained men. *Eur J Appl Physiol* 2017 — https://pubmed.ncbi.nlm.nih.gov/28447186/
- [soares2015]: Soares S et al. Dissociated time course of muscle damage recovery between single- and multi-joint exercises in highly resistance-trained men. *J Strength Cond Res* 2015 — https://pubmed.ncbi.nlm.nih.gov/25807025/
- [decamargo2022]: de Camargo JBB et al. Dissociated time course of indirect markers of muscle damage recovery between single-joint and multi-joint exercises in resistance-trained men. *J Strength Cond Res* 2022;36(8):2089-2093 — https://pubmed.ncbi.nlm.nih.gov/33394892/
- [jamurtas2005]: Jamurtas AZ et al. Comparison between leg and arm eccentric exercises of the same relative intensity on indices of muscle damage. *Eur J Appl Physiol* 2005 — https://pubmed.ncbi.nlm.nih.gov/16007451/
- [nuckols2026]: Nuckols GL, Overpeck CA, Hanson ED, Battaglini CL. The effects of biological sex on fatigue during and recovery from resistance exercise. *PeerJ* 2026;14:e20542 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12790778/
- [nosaka1995]: Nosaka K, Clarkson PM. Muscle damage following repeated bouts of high force eccentric exercise. *Med Sci Sports Exerc* 1995 — https://pubmed.ncbi.nlm.nih.gov/8531624/
- [hody2019]: Hody S et al. Eccentric muscle contractions: risks and benefits. *Front Physiol* 2019 — https://pubmed.ncbi.nlm.nih.gov/31130877/
- [doma2023]: Doma K et al. The repeated bout effect of multiarticular exercises on muscle damage markers and physical performances: a systematic review and meta-analyses. *J Strength Cond Res* 2023;37(12):2504-2515 — https://pubmed.ncbi.nlm.nih.gov/38015738/
- [lindsay2021]: Lindsay A et al. Muscle strength does not adapt from a second to third bout of eccentric contractions: a systematic review and meta-analysis of the repeated bout effect. *J Strength Cond Res* 2021;35(2):576-584 — https://pubmed.ncbi.nlm.nih.gov/33337696/
- [damas2016]: Damas F et al. Resistance training-induced changes in integrated myofibrillar protein synthesis are related to hypertrophy only after attenuation of muscle damage. *J Physiol* 2016;594(18):5209-5222 — https://pubmed.ncbi.nlm.nih.gov/27219125/

Effort, set counting and secondary Muscles
- [grgic2022]: Grgic J, Schoenfeld BJ, Orazem J, Sabol F. Effects of resistance training performed to repetition failure or non-failure on muscular strength and hypertrophy: a systematic review and meta-analysis. *J Sport Health Sci* 2022 — https://pubmed.ncbi.nlm.nih.gov/33497853/
- [robinson2024]: Robinson ZP et al. Exploring the dose-response relationship between estimated resistance training proximity to failure, strength gain, and muscle hypertrophy: a series of meta-regressions. *Sports Med* 2024 — https://pubmed.ncbi.nlm.nih.gov/38970765/
- [refalo2024]: Refalo MC et al. Accuracy of intraset repetitions-in-reserve predictions during the bench press exercise in resistance-trained male and female subjects. *J Strength Cond Res* 2024;38(3):e78-e85 — https://pubmed.ncbi.nlm.nih.gov/37967832/
- [pelland2026]: Pelland JC, Remmert JF, Robinson ZP, Hinson SR, Zourdos MC. The resistance training dose response: meta-regressions exploring the effects of weekly volume and frequency on muscle hypertrophy and strength gains. *Sports Med* 2026;56(2):481-505 (online Dec 2025), doi 10.1007/s40279-025-02344-w — https://pubmed.ncbi.nlm.nih.gov/41343037/
- [pelland2024pre]: Pelland J, Remmert J, Robinson Z, Hinson S, Zourdos M. The resistance training dose-response: meta-regressions exploring the effects of weekly volume and frequency on muscle hypertrophy and strength gain. SportRxiv preprint, not peer reviewed, last modified Sept 2024 — https://sportrxiv.org/index.php/server/preprint/view/460
- [gentil2013]: Gentil P et al. Effect of adding single-joint exercises to a multi-joint exercise resistance-training program on strength and hypertrophy in untrained subjects. *Appl Physiol Nutr Metab* 2013 — https://pubmed.ncbi.nlm.nih.gov/23537028/

Markers, sleep and HRV
- [warren1999]: Warren GL, Lowe DA, Armstrong RB. Measurement tools used in the study of eccentric contraction-induced injury. *Sports Med* 1999 — https://pubmed.ncbi.nlm.nih.gov/10028132/
- [konrad2022]: Konrad A et al. Relationship between eccentric-exercise-induced loss in muscle function to muscle soreness and tissue hardness. *Healthcare (Basel)* 2022 — https://pubmed.ncbi.nlm.nih.gov/35052259/
- [baird2012]: Baird MF et al. Creatine-kinase- and exercise-related muscle damage implications for muscle performance and recovery. *J Nutr Metab* 2012 — https://pubmed.ncbi.nlm.nih.gov/22288008/
- [knowles2018]: Knowles OE et al. Inadequate sleep and muscle strength: implications for resistance training. *J Sci Med Sport* 2018 — https://pubmed.ncbi.nlm.nih.gov/29422383/
- [lamon2021]: Lamon S et al. The effect of acute sleep deprivation on skeletal muscle protein synthesis and the hormonal environment. *Physiol Rep* 2021 — https://pubmed.ncbi.nlm.nih.gov/33400856/
- [kingsley2016]: Kingsley JD, Figueroa A. Acute and training effects of resistance exercise on heart rate variability. *Clin Physiol Funct Imaging* 2016 — https://pubmed.ncbi.nlm.nih.gov/25524332/
- [stanley2013]: Stanley J, Peake JM, Buchheit M. Cardiac parasympathetic reactivation following exercise: implications for training prescription. *Sports Med* 2013 — https://pubmed.ncbi.nlm.nih.gov/23912805/
- [manresa2021]: Manresa-Rocamora A et al. Heart rate variability-guided training for enhancing cardiac-vagal modulation, aerobic fitness, and endurance performance: a methodological systematic review with meta-analysis. *Int J Environ Res Public Health* 2021 — https://pubmed.ncbi.nlm.nih.gov/34639599/
- [lee2025]: Lee YJ et al. Performance of consumer wrist-worn sleep tracking devices compared to polysomnography: a meta-analysis. *J Clin Sleep Med* 2025;21(3):573-582 — https://pubmed.ncbi.nlm.nih.gov/39484805/

Weekly volume
- [schoenfeld2017]: Schoenfeld BJ, Ogborn D, Krieger JW. Dose-response relationship between weekly resistance training volume and increases in muscle mass: a systematic review and meta-analysis. *J Sports Sci* 2017 — https://pubmed.ncbi.nlm.nih.gov/27433992/
- [schoenfeld2019]: Schoenfeld BJ et al. Resistance training volume enhances muscle hypertrophy but not strength in trained men. *Med Sci Sports Exerc* 2019 — https://pubmed.ncbi.nlm.nih.gov/30153194/
- [bazvalle2022]: Baz-Valle E et al. A systematic review of the effects of different resistance training volumes on muscle hypertrophy. *J Hum Kinet* 2022 — https://pubmed.ncbi.nlm.nih.gov/35291645/
- [schoenfeld2016]: Schoenfeld BJ, Ogborn D, Krieger JW. Effects of resistance training frequency on measures of muscle hypertrophy: a systematic review and meta-analysis. *Sports Med* 2016 — https://pubmed.ncbi.nlm.nih.gov/27102172/
- [grgic2019]: Grgic J, Schoenfeld BJ, Latella C. Resistance training frequency and skeletal muscle hypertrophy: a review of available evidence. *J Sci Med Sport* 2019 — https://pubmed.ncbi.nlm.nih.gov/30236847/
- [spiering2021]: Spiering BA et al. Maintaining physical performance: the minimal dose of exercise needed to preserve endurance and strength over time. *J Strength Cond Res* 2021;35(5):1449-1458 — https://pubmed.ncbi.nlm.nih.gov/33629972/
- [bickel2011]: Bickel CS, Cross JM, Bamman MM. Exercise dosing to retain resistance training adaptations in young and older adults. *Med Sci Sports Exerc* 2011 — https://pubmed.ncbi.nlm.nih.gov/21131862/

[raastad2000]: https://pubmed.ncbi.nlm.nih.gov/10929214/
[moran2017]: https://pubmed.ncbi.nlm.nih.gov/28965198/
[refalo2023]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9908800
[pareja2019]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6473797
[bartolomei2017]: https://pubmed.ncbi.nlm.nih.gov/28447186/
[soares2015]: https://pubmed.ncbi.nlm.nih.gov/25807025/
[decamargo2022]: https://pubmed.ncbi.nlm.nih.gov/33394892/
[jamurtas2005]: https://pubmed.ncbi.nlm.nih.gov/16007451/
[nuckols2026]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12790778/
[nosaka1995]: https://pubmed.ncbi.nlm.nih.gov/8531624/
[hody2019]: https://pubmed.ncbi.nlm.nih.gov/31130877/
[doma2023]: https://pubmed.ncbi.nlm.nih.gov/38015738/
[lindsay2021]: https://pubmed.ncbi.nlm.nih.gov/33337696/
[damas2016]: https://pubmed.ncbi.nlm.nih.gov/27219125/
[grgic2022]: https://pubmed.ncbi.nlm.nih.gov/33497853/
[robinson2024]: https://pubmed.ncbi.nlm.nih.gov/38970765/
[refalo2024]: https://pubmed.ncbi.nlm.nih.gov/37967832/
[pelland2026]: https://pubmed.ncbi.nlm.nih.gov/41343037/
[pelland2024pre]: https://sportrxiv.org/index.php/server/preprint/view/460
[gentil2013]: https://pubmed.ncbi.nlm.nih.gov/23537028/
[warren1999]: https://pubmed.ncbi.nlm.nih.gov/10028132/
[konrad2022]: https://pubmed.ncbi.nlm.nih.gov/35052259/
[baird2012]: https://pubmed.ncbi.nlm.nih.gov/22288008/
[knowles2018]: https://pubmed.ncbi.nlm.nih.gov/29422383/
[lamon2021]: https://pubmed.ncbi.nlm.nih.gov/33400856/
[kingsley2016]: https://pubmed.ncbi.nlm.nih.gov/25524332/
[stanley2013]: https://pubmed.ncbi.nlm.nih.gov/23912805/
[manresa2021]: https://pubmed.ncbi.nlm.nih.gov/34639599/
[lee2025]: https://pubmed.ncbi.nlm.nih.gov/39484805/
[schoenfeld2017]: https://pubmed.ncbi.nlm.nih.gov/27433992/
[schoenfeld2019]: https://pubmed.ncbi.nlm.nih.gov/30153194/
[bazvalle2022]: https://pubmed.ncbi.nlm.nih.gov/35291645/
[schoenfeld2016]: https://pubmed.ncbi.nlm.nih.gov/27102172/
[grgic2019]: https://pubmed.ncbi.nlm.nih.gov/30236847/
[spiering2021]: https://pubmed.ncbi.nlm.nih.gov/33629972/
[bickel2011]: https://pubmed.ncbi.nlm.nih.gov/21131862/
