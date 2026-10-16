# Single-passphrase auth, no user accounts

There is exactly one user, so there is no users table or login system. A single passphrase, stored as a Cloudflare secret, is exchanged once per device for a long-lived bearer token, and every API request must carry that token. The API is publicly reachable and the repo is public, so the API still needs protecting. A full account system would add code that serves no real user.
