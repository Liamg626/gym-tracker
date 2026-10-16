# WCH: Watch Data (Amazfit via Zepp)

v1.3, low priority. There is no live sync (ADR-0001): data arrives by uploading an export file.

## Rules

- The export file is read **in the browser**; only the extracted daily figures are sent to the API. The raw file is never stored or committed (ADR-0005).

## Stories

**WCH: Research the Zepp export** (Task)
- How to export from Zepp (in-app or data-request), the file format, and which fields are available: heart rate, resting HR, HRV, sleep, steps, workouts. Include a made-up sample file for tests. If no usable export exists, recommend closing the area.

**WCH: Upload and parse a Zepp export** (blocked by the research)
- Pick a file, preview the date range and figures found, confirm, then send to the API; re-uploading overlapping dates updates them rather than duplicating them

**WCH: Watch Data in the Weekly Breakdown**
