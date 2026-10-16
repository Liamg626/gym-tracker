# Sets are saved on the device first, then synced

During a Workout, every Set is written to the phone's local storage immediately and sent to the API from a background queue that retries until it succeeds. The UI never waits on the network. Gym signal is usually good (5G), so this is deliberately a lightweight outbound queue and not full offline-first sync: reads such as history and charts may need a connection.
