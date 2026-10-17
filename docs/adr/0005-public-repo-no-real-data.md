# Public repo, real health data never committed

The repo is public as a portfolio piece. Real Workouts, Weigh-ins and Measurement Sessions live only in D1 and on the device. Exports and any watch files are git-ignored, and secrets live in Cloudflare/Wrangler secrets. A generator produces made-up demo data for local development, tests, screenshots and any public demo. Previews use a separate shared D1 database that holds only generated demo data, and screenshots in pull requests come only from it. (Amended 2026-10-17, `docs/research/pr-testing.md`.)
