# Hono on Cloudflare Workers with D1

The backend is a TypeScript REST API built with Hono, running on Cloudflare Workers, storing data in Cloudflare D1 (SQLite) through Drizzle ORM. The PWA is served as static assets by the same Cloudflare Worker that runs the API (Workers static assets), not from Cloudflare Pages. Cloudflare now tells new projects to start with Workers, and a single Worker gives each pull request one preview URL where the frontend and the API share an origin. (Amended 2026-10-17 after the PR testing research, `docs/research/pr-testing.md`.) A cloud backend was chosen over device-only storage so Liam learns backend work for the portfolio, and so the phone and dashboard share one source of truth.

## Considered Options

- **Node/Express on Render + Neon Postgres**: the free tier sleeps, and a 30–50s cold start in the middle of a set is unacceptable.
- **Supabase**: less backend code to write (less learning), and free projects pause after a week of inactivity.
