# No Watch Data: the app does not import from the watch

Status: accepted (Liam, 2026-10-17)

The app no longer brings in data from Liam's Amazfit watch, either by a direct connection or by uploading Zepp exports, and the v1.3 Watch Data release is dropped. The research (`docs/research/zepp-export.md`) found no direct route for the GTS 2:
- there is no official Zepp API
- the watch can't run Zepp OS mini-apps
- Strava has workouts only
- Apple Health and Health Connect are native-only

The only route left is Zepp's personal-data export. It is a password-protected ZIP that has to be requested by hand each time. It has no HRV and no resting HR, so of the planned figures it gives only sleep, which would have filled a single line of the Weekly Breakdown. Liam judged that not worth the hassle of getting each export. Training data comes only from what is logged in the app.

## Consequences

- There is no WCH area, `wch-watch-data.md` spec, v1.3 release or v1.3 design ticket.
- The Weekly Breakdown has no Watch Data section.
- If a future watch offers a real web sync, start from the research doc rather than reopening this ADR silently.
