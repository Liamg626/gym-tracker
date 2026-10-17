# Research: getting Amazfit (Zepp) data into the app

SCRUM-10 · [WCH-001] · researched 2026-10-17

## Question

Can Watch Data (heart rate, resting HR, HRV, sleep, steps, workouts) from Liam's Amazfit watch reach the app at £0, from Windows, with no Mac and no paid Apple Developer Program, without breaking ADR-0001 (PWA, no HealthKit), ADR-0002 (Hono Worker + D1) or ADR-0005 (raw health files never stored or committed)?

- **Part A, direct integration (preferred):** an official Zepp developer API or partner program; a Zepp OS mini-app that posts daily figures to our Worker; a third party that Zepp syncs to and that has a web API a Worker can call.
- **Part B, export backup:** in-app export, an account data request, third-party export; format, fields, time zones, overlap between repeated exports.

Out of scope: the unofficial/reverse-engineered Zepp (Huami) API, and anything that breaks Terms of Service.

## Summary and recommendation

- **There is no official public Zepp cloud API for a personal project.** I found no developer API, auth scheme, rate limits or approval process for reading a user's health data from Zepp's cloud. A third-party aggregator says it integrates with Zepp ([Thryve][thryve]) and another says Zepp has no public API ([HAID][haid]); both are vendors, not primary sources, so this is "not found", not proven. Route A1: **NO**.
- **A Zepp OS mini-app is technically possible but unproven for this use.** The documented pieces exist: a watch app reads sensors, a side service running inside the Zepp phone app can call `fetch` to a server ([Side Service intro][ss-intro], [Fetch API][ss-fetch]), and a Zepp maintainer-labelled post shares a sample that uploads sleep data to a server ([Zepp discussion #276][gh276]). But: (a) Liam's watch model is unknown and the app needs Zepp OS API_LEVEL 2.0+ to 3.0+ depending on the sensor ([device list][devlist]); (b) no HRV sensor appears in the docs I could reach; (c) iOS support for developer-mode install and for the side service is **not stated** in the docs; (d) a background run is limited to 600 ms per execution unless a continuous service is approved ([App Service][app-service]); (e) there is no documented private-distribution route other than developer-mode QR install, and the public route needs a Zepp Console account, a privacy policy and 1 to 5 working days of review ([Distribute][distribute]). Liam has since confirmed his watch is an **Amazfit GTS 2**. The GTS 2 is not on Zepp's device list (the GTS 2 mini is, under non-Zepp OS) ([device list][devlist]); mini-apps are ruled out by that absence, not by a statement that names the GTS 2. Route A2: **NO for Liam's current watch**; it would only reopen if he moved to a Zepp OS 3.0+ watch.
- **Third-party sync to a web API: NO for the fields we want.** Strava is the only web API route that is not native-only, and it carries workouts only (heart rate summary per activity), not sleep, steps, resting HR or HRV, and Zepp's Strava sync is reported to cover outdoor activities only ([Amazfit support, Italian][amz-strava]). Apple Health and Health Connect are native-only and ruled out by ADR-0001.
- **Export is the route, and its format is now confirmed from Liam's real export (2026-10-17).** Zepp lists "Export data: Export personal data" as a data-subject right, reached from the app under Profile > Setting > "Exercising user rights" ([Zepp privacy support][zepp-priv]). No primary source documents the file, so the format below comes from **one real export Liam supplied**, inspected outside the repo and never committed (ADR-0005). It is a password-protected ZIP (WinZip AES, ZIP method 99 ([PKWARE APPNOTE][appnote], [WinZip AES][winzip-aes])) holding 11 folders of UTF-8 CSV files, one per data type, covering the account's whole history. See [Confirmed export format](#b2-confirmed-export-format).
- **Fields available:** daily steps, distance and calories; heart rate every 10 minutes (every minute during workouts); nightly sleep with deep, light and wake minutes, start and stop; minute-by-minute sleep stages; workouts with type code, start, duration and calories. **Not in the export:** HRV and resting HR. REM minutes are always 0 in Liam's file. Per-workout TCX/FIT files are also available but add only finer heart rate for single sessions, so they are skipped (Liam's call).
- **Recommendation: build the upload from the personal-data export.** Use these fields: daily steps, sleep (total, deep, light, wake, bed and wake times), daily heart rate (min, average, max from the 10-minute readings) and workouts (start, duration, calories, type). Resting HR is not in the file; a derived figure is proposed for Liam below. A made-up sample is in [`samples/zepp-export/`](samples/zepp-export/). The Zepp OS mini-app (route A2) is ruled out for the GTS 2, and the Apple Health export is kept only as a fallback if the Zepp export fails or changes (see B1).

## Part A: direct integration

### A1. Official Zepp developer API or partner programme

| Item | Finding |
|---|---|
| Public health-data cloud API | Not found. docs.zepp.com documents on-watch and phone-side APIs only (device app, side service, settings app) ([Zepp OS intro][zos-intro], [Device app intro][dev-intro]). The developer.zepp.com page I fetched rendered only a title ([developer.zepp.com][devsite]). |
| Auth, rate limits, approval | Not documented anywhere I could reach. |
| Partner programmes | Search snippets of developer.zepp.com mention IoT cooperation and health big-data collaboration, with no eligibility terms ([developer.zepp.com][devsite]). Treat as business-to-business and unusable by a personal project unless Zepp says otherwise. |
| Community confirmation | A community member replied on Zepp's own GitHub discussions that they were "not sure if it's possible to retrieve data from the Zepp website" and pointed to the watch-side sleep API instead ([discussion #522][gh522]). |

**Verdict: NO.** No documented route exists. The only way to confirm otherwise is to ask Zepp (privacy@zepp.com is the contact given for privacy matters, not for developer access ([Zepp privacy support][zepp-priv])).

### A2. Zepp OS mini-app (watch app + side service) posting to our Worker

How it fits together ([Side Service intro][ss-intro], [Fetch API][ss-fetch], [App Service][app-service]):

```
Watch (device app, JS) --BLE--> Side service (JS inside Zepp phone app) --HTTPS fetch--> Hono Worker --> D1
```

| Question | Finding |
|---|---|
| Can it send HTTPS to our Worker? | The side service "can communicate with the device app and server side" and has a Fetch API; only `url`, `method`, `headers`, `body` are supported; GET by default, POST shown in examples ([Side Service intro][ss-intro], [Fetch API][ss-fetch]). The docs do not state size limits, CORS behaviour or an HTTPS requirement. |
| Proof that sensor data can be sent to a server | A post labelled Maintainer (author MyoungXUE, in the zepp-health GitHub org) shares a sample where the device app reads sleep data and the side service posts it to a Node.js server; scheduled reporting uses the Alarm API with `setLaunchAppTimeout` ([discussion #276][gh276]). The Maintainer label is shown on the page; it does not say explicitly "Zepp staff". |
| Which watches | Zepp OS devices only. Non-Zepp-OS models (e.g. GTR 2, GTS 2 mini, T-Rex Pro, Pop, Zepp E) cannot run mini-apps. API_LEVEL is not listed for Band 7, GTR 3, GTR 3 Pro, GTS 3 and GTS 4 mini, so their support for 2.0+ apps is not confirmed ([device list][devlist]). Newer models (e.g. Balance, Active, T-Rex 3, GTR 4, Bip 5/6) support API_LEVEL 2.1 to 4.4 ([device list][devlist]). **Liam's model is the GTS 2 (confirmed by Liam 2026-10-17).** The GTS 2 is not on the device list (the GTS 2 mini is, under non-Zepp OS) ([device list][devlist]); mini-apps are ruled out by that absence, not by a statement that names the GTS 2. |
| Heart rate | `@zos/sensor` HeartRate, permission `data:user.hd.heart_rate`. `getToday()` returns per-minute values from midnight (2.0); `getResting()` and `getDailySummary()` (max HR and when) need API_LEVEL 3.0 ([HeartRate][s-hr]). |
| Resting HR | `getResting()`, API_LEVEL 3.0 ([HeartRate][s-hr]). |
| HRV | **No HRV method found** in the HeartRate page or search of docs.zepp.com ([HeartRate][s-hr]). The Zepp App privacy policy says HRV is collected in the app ([Zepp App privacy policy][zepp-app-pp]), so HRV may exist in Zepp's cloud but not be exposed to mini-apps. Unconfirmed. |
| Sleep | Sleep sensor, permission `data:user.hd.sleep`, API_LEVEL 2.0. `getInfo()` returns score, `deepTime`, `totalTime` (minutes), `startTime`, `endTime` (minutes since midnight); `getStage()` returns segments with `model` (wake/REM/light/deep constants), `start`, `stop`; `getNap()` from 3.0. The system refreshes sleep data every 30 minutes ([Sleep][s-sleep]). Minutes are "since midnight", so the time zone and the date must be added by our code (see time zones below). |
| Steps | Step sensor, permission `data:user.hd.step`, API_LEVEL 2.0: `getCurrent()` (current count) and `getTarget()` only ([Step][s-step]). Today's total only; no documented per-day history. |
| Workouts | Workout sensor, permission `data:user.hd.workout`: `getHistory()` returns only `startTime` and `duration` (3.0); `getStatus()` returns VO2 max, training load, recovery time ([Workout][s-workout]). No per-workout heart rate. |
| Background | An "App Service" can be woken by alarm, notification or system event, runs once and exits; one execution is limited to 600 ms; continuous service needs `device:os.bg_service` and user approval; v3+ only ([App Service][app-service]). So a daily push is feasible only with a model on Zepp OS 3.0+. |
| Install on iOS | Developer Mode in the Zepp app (Profile > Settings > About, tap the Zepp icon 7 times), then scan a QR code produced by `zeus preview` to install on the bound watch ([Zepp App Developer Mode][devmode], [Preview on a Watch][preview]). The docs **do not mention iOS or Android**, and do not say whether the installed app persists or expires ([Developer Mode][devmode], [Preview][preview]). `zeus` is a Node CLI ([Zeus CLI][zeus]); I did not verify it runs on Windows (this is probably fine, but unconfirmed). |
| Store publication | Not required for personal use if the QR preview install persists (unconfirmed). Public release: register in Zepp Console, upload a package, provide a privacy policy, 1 to 5 working days review ([Distribute][distribute]). |
| Cost | £0 (Zepp tooling is free as far as the docs show; no fee stated). |
| Effort | High relative to the feature: a watch app, a side service, a Worker endpoint and a token, plus a way to authenticate the watch to the Worker (ADR-0003 is single-passphrase auth; a device token would be new). |

**Verdict: NO for Liam's GTS 2** (not on the Zepp OS device list). For a future Zepp OS 3.0+ watch the route would be CONDITIONAL: it is YES against the £0, no Mac and no Apple fee limits on paper. It is NO to commit to until Liam confirms (1) the watch model is Zepp OS 3.0+, (2) developer-mode QR install works from his iPhone, (3) an installed mini-app keeps running, and (4) HRV is not needed, since no HRV API is documented. It also changes ADR-0001's consequence "Watch Data arrives by uploading export files", so it needs a new ADR (see below).

### A3. Third party that Zepp syncs to, with a web API

| Route | What Zepp sends | Web API callable from a Worker? | Verdict |
|---|---|---|---|
| **Strava** | Zepp uploads activities to Strava via Profile > Add accounts ([Amazfit support, Italian][amz-strava]); that page is for the Bip Lite, not the GTS 2, and says outdoor running, walking and cycling sync, and indoor, swimming, non-GPS and past activities do not. The Zepp App policy says Strava receives exercise period, distance, altitude, speed, pace, heart rate and stride data (South Korea addendum, with consent) ([Zepp App privacy policy][zepp-app-pp]). | Yes. OAuth API; activity summary has `has_heartrate`, `average_heartrate`, `max_heartrate`; heart-rate streams exist; no sleep, steps or resting HR endpoints ([Strava API reference][strava-ref]). Default limits 200 requests per 15 minutes and 2,000 per day (100 and 1,000 for non-upload); a new app has athlete capacity 1, which suits a personal project ([Strava rate limits][strava-rl]). | **NO** for the WCH fields: it gives workout heart rate only, and misses gym (indoor) sessions, which are the app's main use. Could be revisited for outdoor runs only. |
| **Apple Health** | Zepp can write to it (Profile > Add accounts > Health, per [StepsApp][steps-guide] and Sahha guides, non-primary) | No web API; HealthKit is native-only ([Apple HealthKit][hk]) | **NO**, ruled out (ADR-0001). |
| **Health Connect** | Zepp can link it (reported by [Gadgets & Wearables][gw-hc], non-primary) | Android on-device API only ([Health Connect][hc]) | **NO**, ruled out (native-only; Liam uses an iPhone). |
| **Google Fit / Fitbit** | Zepp App policy names Google Fit as a share target ([Zepp App privacy policy][zepp-app-pp]) | Not investigated further: the Google Fit APIs are being retired in favour of Health Connect (per Google's own notice; not fetched here), so I treat it as unavailable | **NO** (not verified, low value) |

### Part A route table

| Route | Limits check (£0, no Mac, no Apple fee, no ToS break) | Fields | Freshness | Effort | Verdict |
|---|---|---|---|---|---|
| A1 Official API | Cannot assess; none found | n/a | n/a | n/a | **NO** |
| A2 Mini-app + side service | £0 yes; no Mac needed; iOS support unconfirmed; needs Zepp OS 3.0+ for resting HR, apps service | HR (per minute), resting HR, sleep (score, stages, times), steps (today's total), workout start+duration; **no HRV** | Daily if alarm-triggered, near-live if continuous | High | **NO** (GTS 2 not on the device list); conditional only on a future 3.0+ watch |
| A3 Strava | £0 yes | Workout HR only | Minutes after sync | Medium | **NO** |
| A3 Apple Health / Health Connect | Native-only | n/a | n/a | n/a | **NO** |

## Part B: export backup

### B1. Ways to get data out of Zepp

| Way | What is confirmed (primary) | Format, layout, turnaround, repeatability |
|---|---|---|
| **Account data request ("Export personal data")** | Zepp's privacy support page lists "4. Export data: Export personal data" under exercising data subject rights, and gives the app path Zepp: App > Profile > Setting > "Exercising user rights" (Zepp Life: App > Profile > Setting > Account and Security). The page gives this path for exercising data subject rights, which lists Export personal data as item 4. It does not name the export menu item itself ([Zepp privacy support][zepp-priv]). The Zepp App privacy policy lists access and data-portability rights exercised through the Privacy Support portal ([Zepp App privacy policy][zepp-app-pp]). Zepp's website policy names a data protection officer (dpo@zepp.com) and says requests are processed "by applicable laws", with identity verification; no response time is given ([Zepp privacy policy][zepp-pp]). | **Confirmed from Liam's export:** a password-protected ZIP of CSV files covering the whole account history; layout in [B2](#b2-confirmed-export-format). Turnaround: not stated by Zepp; the GDPR default is one month ([GDPR Art. 12(3)][gdpr12], general law, not a Zepp statement). Repeatability: not stated; each export is the full history, so a repeat overlaps everything before it. The archive does contain a workout summary (`SPORT`), unlike an older unofficial report ([rolandsz][rs-post]). |
| **In-app export of workouts** | **Nothing primary.** Unverified: a search snippet of the App Store listing ([Zepp on the App Store][appstore]) and Android listings (non-primary) mention a storage permission used to "import/export your exercise data". No official support page found. | **Confirmed from Liam's files:** one workout at a time as TCX (Garmin Training Center Database v2 ([TCX schema][tcx])) or FIT ([FIT SDK][fit]). Liam's TCX has one lap with duration, calories, average and max HR, and a heart-rate trackpoint every few seconds in UTC; a strength session is `Sport="Other"` with `Notes` "Strength Training". Manual and per session, so **skipped** (Liam's call); the bulk export's minute-level heart rate during workouts is enough. |
| **Third-party export tools** | None are primary sources. The unofficial `Mi-Fit-and-Zepp-workout-exporter` script logs in with Zepp credentials against Zepp's undocumented API ([repo][rs-repo]). | **Out of scope** (reverse-engineered API). |
| **Apple Health export** | Zepp can write to Apple Health; Apple Health can export a ZIP containing `export.xml` ([Apple Health export][apple-export], via the Health app profile > Export All Health Data). | Only if Zepp is linked to Health on the iPhone. This is a user-side export, not a native app integration, so ADR-0001 does not rule it out: the PWA would parse the XML in the browser. **Unverified for this research**: I did not fetch Apple's page or confirm which Zepp fields land in Health. Kept as a fallback if the Zepp export fails or changes. |

Note on the Apple Health row: it is the one place where this research found a possibly workable path that the task did not list. It needs (a) Liam's Zepp account linked to Apple Health (Profile > Add accounts > Health per non-primary guides), and (b) a check of which categories Zepp writes (primary source needed). No longer needed now that the Zepp export is confirmed usable; kept as a fallback if Zepp changes the export.

### B2. Confirmed export format

Everything in this section comes from inspecting Liam's real export (2026-10-17) outside the repo. No primary source documents it, and Zepp could change it, so the parser should check headers and fail clearly on a mismatch.

**Archive:** `<userId>_<epoch ms>.zip`, encrypted with WinZip AES (ZIP method 99), password given to Liam by Zepp. Inside are 11 folders, each holding one file named `<FOLDER>_<epoch ms>.csv`. All files are UTF-8 **with a BOM**, LF line endings, comma-separated, with a header row. Days the watch was not worn are absent, not zero rows.

| Folder | Header | One row is | Time format | Use |
|---|---|---|---|---|
| `ACTIVITY` | `date,steps,distance,runDistance,calories` | a day | `date` local | **Yes:** daily steps, distance (m), calories |
| `ACTIVITY_MINUTE` | `date,time,steps` | a minute with steps (zero minutes left out) | local | No (the daily total is enough) |
| `ACTIVITY_STAGE` | `date,start,stop,distance,calories,steps` | a walking or moving block | local `HH:MM` | No |
| `SLEEP` | `date,deepSleepTime,shallowSleepTime,wakeTime,start,stop,REMTime,naps` | a night; `date` is the wake-up day | `start`/`stop` UTC (`YYYY-MM-DD HH:MM:SS+0000`) | **Yes:** minutes deep, light (`shallow`) and awake; bed and wake times. Deep + shallow + wake matched stop − start in Liam's file. `REMTime` was always 0. `naps` is empty or a quoted JSON array of `{start,end}` with backslash-escaped quotes. A night with start = stop and all zeros means no sleep recorded |
| `SLEEP_MINUTE` | `date,time,stage,hr,respiratory_rate` | a minute asleep | local `HH:MM`; see the date note below | Optional: stages `LIGHT`, `DEEP`, `WAKE` (no `REM` seen); `hr` filled about every 10 minutes; `respiratory_rate` always empty |
| `HEARTRATE` | `time,heartRate` | a manual measurement | UTC `+0000` | No (few rows) |
| `HEARTRATE_AUTO` | `date,time,heartRate` | an automatic reading: every 10 minutes, every minute during a workout | local | **Yes:** daily min, average, max |
| `SPORT` | `type,startTime,sportTime(s),maxPace(/meter),minPace(/meter),distance(m),avgPace(/meter),calories(kcal)` | a workout | `startTime` UTC | **Yes:** start, duration (s), calories, type. No heart rate. Type `52` is strength training (matched to Liam's TCX "Strength Training" session by start time and duration). Codes `6`, `8` and `10` are unmapped |
| `BODY` | `time,weight,height,bmi,fatRate,bodyWaterRate,boneMass,metabolism,muscleRate,visceralFat` | a weight entry in Zepp | UTC; unknown fields are the literal `null` | No: the app has its own Weigh-ins (BDY) |
| `HEALTH_DATA` | `date,time,arm,calf,chest,hip,thigh,waist` | a body measurement | n/a (empty in Liam's file) | No |
| `USER` | `userId,gender,height,weight,nickName,avatar,birthday` | the account | n/a | **Never read:** personal profile |

**The fields the ticket asked about:**

| Field | In the export? |
|---|---|
| Heart rate | Yes: `HEARTRATE_AUTO` (10-minute, 1-minute in workouts) and `SLEEP_MINUTE.hr` |
| Resting HR | **No.** Proposal for Liam: derive it as the lowest `HEARTRATE_AUTO` reading inside the night's `SLEEP` start–stop window (agent proposal, not a Zepp figure) |
| HRV | **No** |
| Sleep stages and duration | Yes: deep, light and awake minutes per night, plus per-minute stages. REM was always 0 on the GTS 2 |
| Steps | Yes: daily (`ACTIVITY`) and per minute |
| Workouts | Yes, `SPORT`: type, start, duration, calories; no heart rate (take it from `HEARTRATE_AUTO` in the workout window if needed) |

### B3. Time zones and overlap

- **Two time formats.** Columns holding a full timestamp (`SLEEP.start`/`stop`, `SPORT.startTime`, `HEARTRATE`, `BODY`) are UTC with a `+0000` suffix. Files with separate `date` and `time` columns (`ACTIVITY*`, `HEARTRATE_AUTO`, `SLEEP_MINUTE`) are **local time with no offset**. Checked by matching a workout's UTC start in `SPORT` and the TCX against the heart-rate rise in `HEARTRATE_AUTO`, which came one hour later, as expected for UK summer time. The parser needs the user's time zone (the browser's) to turn local rows into instants; DST changes make one local hour a year missing and one ambiguous.
- **`SLEEP_MINUTE` dates look one day late.** Each minute's `date` was one calendar day after the local date implied by `SLEEP.start`/`stop`, for both the evening and the morning part of a night. Seen in one export only. Use `SLEEP` for nightly figures and treat `SLEEP_MINUTE.date` with care.
- **`SLEEP.date` is the wake-up day** (a night starting on the 4th is dated the 5th).
- **A nap entry had a start date two years before its row's date.** Treat naps as unreliable and skip them.
- **Overlap:** each export is the full history, so every re-upload overlaps every earlier one. The existing WCH rule (overlapping dates update rather than duplicate) handles this: key daily rows on local calendar date, and workouts on UTC `startTime`.

### B4. Step by step on Liam's iPhone (recommended route: account data request)

Menu names come from Zepp's privacy page and may differ by app version; stop and tell Claude what you see if a step does not match. Liam has done this once and received the ZIP and its password.

1. Open the Zepp app your watch is paired with on the iPhone. If the menus below differ, report what you see.
2. Open **Profile**, then **Setting**, then **Exercising user rights** ([Zepp privacy support][zepp-priv]).
3. Choose **Export data** / **Export personal data**. If it is not there, open https://www.zepp.com/privacy-support in Safari and choose "Export data", signing in with the same Zepp account. If neither works, email privacy@zepp.com asking for a copy of your personal data in a machine-readable format (named as the privacy contact on [Zepp privacy support][zepp-priv]; the data protection officer is dpo@zepp.com ([Zepp privacy policy][zepp-pp])).
4. Note the date and time of the request and how long the data takes to arrive (Zepp does not state a time; GDPR default is one month ([GDPR Art. 12(3)][gdpr12])).
5. When it arrives, save the ZIP in **Files** on the iPhone, in a folder **outside the repo** (ADR-0005: never commit it).
6. Do **not** open it in the repo or paste it into chat. Follow [What Liam should provide](#what-liam-should-provide).

Steps 2 and 3 are the only part tied to a primary source. The page gives the "Exercising user rights" path for data subject rights, which lists Export personal data as item 4, but it does not name the export menu item itself.

## What Liam should provide

Received 2026-10-17: the watch model (GTS 2), a full personal-data export, and one workout as TCX and FIT. The format above is based on them. Still useful, none blocking:

1. How the export and its password arrived (email or in app), and how long it took. This goes into the upload screen's help text.
2. Which activities the `SPORT` type codes `6`, `8` and `10` were (for example a walk or the treadmill), so the codes can be mapped to names.

A made-up sample matching the real format is in [`samples/zepp-export/`](samples/zepp-export/).

## Data flow if direct integration is chosen later (route A2)

Only relevant if Liam moves to a Zepp OS 3.0+ watch; the GTS 2 cannot run it.

1. Watch app (Zepp OS 3.0+) wakes on an alarm once a day and reads the day's HR, resting HR, sleep and steps with the sensors above, then hands the figures to the side service over Bluetooth.
2. The side service posts them to a new Worker endpoint (for example `POST /api/watch-days`) over HTTPS with a device token.
3. The Worker upserts one row per calendar date in D1 (same upsert rule as the upload flow). No raw health file exists, so ADR-0005 holds.
4. The PWA reads those rows for the Weekly Breakdown.

**A new ADR would be needed**: it changes ADR-0001's consequence ("Watch Data arrives by uploading export files") and adds a second auth path beside ADR-0003's passphrase (a device token). Not drafted; for Liam to decide after the gate above.

## Proposed doc changes (for Liam to approve, not applied)

**`docs/product/features/wch-watch-data.md`**

- Intro: keep "no live sync (ADR-0001)". Change "uploading an export file" to "uploading a Zepp personal-data export (a password-protected ZIP of CSV files)".
- Rules: add "The ZIP is decrypted and parsed in the browser with the password Zepp gives; the password is never sent to the API or stored." Add "Key daily figures by local calendar date (the browser's time zone); key workouts by UTC start time."
- Under **WCH: Research the Zepp export**: add "Findings and format in `docs/research/zepp-export.md`; sample in `docs/research/samples/zepp-export/`."
- **WCH: Upload and parse a Zepp export**: no longer blocked by the research. List the figures: daily steps, distance and calories; sleep deep, light and awake minutes, bed and wake times; heart rate min, average and max; workouts (start, duration, calories, type). Leave out HRV (not in the export). Resting HR only if Liam accepts the derived figure.
- In the research story, change the field list "heart rate, resting HR, HRV, sleep, steps, workouts" to what the export has.

**`CONTEXT.md`**

- Amend **Watch Data**: "Daily heart rate, sleep, steps and Zepp workout figures imported from an uploaded Zepp (Amazfit) personal-data export."
- No new terms.

**ADRs**: none. The export route keeps ADR-0001 and ADR-0005 as they are. The parse story needs a browser ZIP library that handles WinZip AES (zip.js says it supports AES encryption ([zip.js][zipjs])); to confirm in that story.

## Unverified / limits

- **The export format comes from one real export**, not from Zepp documentation. Zepp may change it, other watch models may fill other fields (e.g. REM, respiratory rate), and the `SLEEP_MINUTE` date offset was seen once. Turnaround and repeat limits are still not stated by Zepp.
- **The Zepp privacy-support and developer.zepp.com pages** returned little text to my fetch tool, so I could not read any export instructions beyond the menu path and the list of options. The pages may hold more.
- **Zepp App privacy policy**: statements here came from a summarised fetch; it was truncated for length, and the Apple Health section was not seen.
- **No HRV API** in the sensor docs I reached; I could not fetch the sensor index page (404), so a method I did not find may exist.
- **Apple Health, Strava and Google Fit details** for Zepp come from non-primary support pages and guides where marked; the Google Fit retirement was not verified.
- **iOS behaviour** of Developer Mode, the side service and mini-app persistence is not covered by the docs I read.
- **Rate limits and approval** for any Zepp cloud API: none exist in what I found.
- **Terms of service** for developer-mode personal installs were not checked.
- **The mini-app sample** (discussion #276) is a post labelled Maintainer (author MyoungXUE, in the zepp-health GitHub org), not reference documentation.

## Sources

Zepp / Amazfit
- [zepp-priv]: Zepp, Privacy Protection Support (data subject rights, Export data) — https://www.zepp.com/privacy-support
- [zepp-pp]: Zepp, Privacy policy (website; DPO contact, portability) — https://www.zepp.com/privacy-policy
- [zepp-app-pp]: Zepp App privacy policy (data categories, rights, Strava/Google Fit sharing) — https://upload-cdn.zepp.com/tposts/8192
- [amz-strava]: Amazfit support (Italian), sync with Strava / Google Fit / Apple Health — https://support.amazfit.com/it/amazfit_bip_lite/docs/AtGHd91tuoOoVZxFdPuc5WXFnsf
- [appstore]: Zepp on the App Store — https://apps.apple.com/us/app/-/id1127269366
- [devsite]: Zepp developer site — https://developer.zepp.com/

Zepp OS docs
- [zos-intro]: Zepp OS introduction — https://docs.zepp.com/docs/intro/
- [dev-intro]: Device App introduction — https://docs.zepp.com/docs/guides/framework/device/intro/
- [devlist]: Device list (API_LEVEL by model) — https://docs.zepp.com/docs/reference/related-resources/device-list/
- [ss-intro]: Side Service introduction — https://docs.zepp.com/docs/guides/framework/side-service/intro/
- [ss-fetch]: Side Service Fetch API — https://docs.zepp.com/docs/reference/side-service-api/fetch/
- [app-service]: App Service — https://docs.zepp.com/docs/guides/framework/device/app-service/
- [s-hr]: HeartRate sensor — https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/HeartRate/
- [s-sleep]: Sleep sensor — https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Sleep/
- [s-step]: Step sensor — https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Step/
- [s-workout]: Workout sensor — https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Workout/
- [devmode]: Zepp App Developer Mode — https://docs.zepp.com/docs/guides/tools/zepp-app/
- [preview]: Preview on a Watch — https://docs.zepp.com/docs/guides/quick-start/preview/
- [zeus]: Zeus CLI — https://docs.zepp.com/docs/guides/tools/cli/
- [distribute]: How to submit an App — https://docs.zepp.com/docs/distribute/
- [gh276]: Zepp Health GitHub discussion #276, extract health data to a web server — https://github.com/orgs/zepp-health/discussions/276
- [gh522]: Zepp Health GitHub discussion #522, export smartwatch data — https://github.com/orgs/zepp-health/discussions/522

Third-party platforms
- [strava-ref]: Strava API v3 reference — https://developers.strava.com/docs/reference/
- [strava-rl]: Strava API rate limits — https://developers.strava.com/docs/rate-limits/
- [hk]: Apple, HealthKit — https://developer.apple.com/documentation/healthkit
- [apple-export]: Apple, share your health data (export) — https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios
- [hc]: Android, Health Connect — https://developer.android.com/health-and-fitness/guides/health-connect
- [gdpr12]: GDPR Article 12 — https://eur-lex.europa.eu/eli/reg/2016/679/oj

File formats
- [appnote]: PKWARE, ZIP APPNOTE (method 99, AE-x encryption) — https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
- [winzip-aes]: WinZip, AES encryption information — https://www.winzip.com/en/support/aes-encryption/
- [tcx]: Garmin, Training Center Database v2 schema — https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd
- [fit]: Garmin, FIT SDK — https://developer.garmin.com/fit/overview/
- [zipjs]: zip.js — https://gildas-lormeau.github.io/zip.js/

Non-primary (marked as such where used)
- [thryve]: Thryve, Zepp / Amazfit integration — https://www.thryve.health/supported-wearable-devices/zepp-amazfit
- [haid]: HAID, Amazfit integration — https://haid.app/en/integrations/amazfit
- [gw-hc]: Gadgets & Wearables, Zepp Health Connect — https://gadgetsandwearables.com/2025/01/24/zepp-health-connect/
- [steps-guide]: StepsApp, connect Amazfit — https://steps.app/en/support/pedometer/ios/other-smartwatches/how-do-i-connect-my-amazfit-to-stepsapp
- [rs-post]: Roland Szabó, Export Mi Fit and Zepp workout data — https://rolandszabo.com/posts/export-mi-fit-and-zepp-workout-data/
- [rs-repo]: rolandsz, Mi-Fit-and-Zepp-workout-exporter — https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter

[zepp-priv]: https://www.zepp.com/privacy-support
[zepp-pp]: https://www.zepp.com/privacy-policy
[zepp-app-pp]: https://upload-cdn.zepp.com/tposts/8192
[amz-strava]: https://support.amazfit.com/it/amazfit_bip_lite/docs/AtGHd91tuoOoVZxFdPuc5WXFnsf
[appstore]: https://apps.apple.com/us/app/-/id1127269366
[devsite]: https://developer.zepp.com/
[zos-intro]: https://docs.zepp.com/docs/intro/
[dev-intro]: https://docs.zepp.com/docs/guides/framework/device/intro/
[devlist]: https://docs.zepp.com/docs/reference/related-resources/device-list/
[ss-intro]: https://docs.zepp.com/docs/guides/framework/side-service/intro/
[ss-fetch]: https://docs.zepp.com/docs/reference/side-service-api/fetch/
[app-service]: https://docs.zepp.com/docs/guides/framework/device/app-service/
[s-hr]: https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/HeartRate/
[s-sleep]: https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Sleep/
[s-step]: https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Step/
[s-workout]: https://docs.zepp.com/docs/reference/device-app-api/newAPI/sensor/Workout/
[devmode]: https://docs.zepp.com/docs/guides/tools/zepp-app/
[preview]: https://docs.zepp.com/docs/guides/quick-start/preview/
[zeus]: https://docs.zepp.com/docs/guides/tools/cli/
[distribute]: https://docs.zepp.com/docs/distribute/
[gh276]: https://github.com/orgs/zepp-health/discussions/276
[gh522]: https://github.com/orgs/zepp-health/discussions/522
[strava-ref]: https://developers.strava.com/docs/reference/
[strava-rl]: https://developers.strava.com/docs/rate-limits/
[hk]: https://developer.apple.com/documentation/healthkit
[apple-export]: https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios
[hc]: https://developer.android.com/health-and-fitness/guides/health-connect
[gdpr12]: https://eur-lex.europa.eu/eli/reg/2016/679/oj
[appnote]: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
[winzip-aes]: https://www.winzip.com/en/support/aes-encryption/
[tcx]: https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd
[fit]: https://developer.garmin.com/fit/overview/
[zipjs]: https://gildas-lormeau.github.io/zip.js/
[thryve]: https://www.thryve.health/supported-wearable-devices/zepp-amazfit
[haid]: https://haid.app/en/integrations/amazfit
[gw-hc]: https://gadgetsandwearables.com/2025/01/24/zepp-health-connect/
[steps-guide]: https://steps.app/en/support/pedometer/ios/other-smartwatches/how-do-i-connect-my-amazfit-to-stepsapp
[rs-post]: https://rolandszabo.com/posts/export-mi-fit-and-zepp-workout-data/
[rs-repo]: https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter
