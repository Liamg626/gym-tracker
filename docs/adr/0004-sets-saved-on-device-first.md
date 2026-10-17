# Sets are saved on the device first, then synced

During a Workout, every Set is written to the phone's local storage immediately and sent to the API from a background queue that retries until it succeeds. The UI never waits on the network. Gym signal is usually good (5G), so this is deliberately a lightweight outbound queue and not full offline-first sync: reads such as history and charts may need a connection.

Amended 2026-10-17: the queue covers every Workout and Set write (start, end, add, edit, delete), not only new Sets, so a dead spot at the door doesn't stop a Workout starting. IDs are UUIDs made on the phone, so retries are idempotent. Only one phone writes, so a conflict is settled by last write wins.
