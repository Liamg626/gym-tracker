# FND: Foundations

Repo, tooling, deploys, auth and the agent workflow. Everything else builds on this.

## Stories

**FND: Monorepo scaffold** (MVP)
- pnpm workspaces: `apps/web` (React + Vite PWA), `apps/api` (Hono), `packages/domain`, `packages/exercise-library`
- TypeScript strict, ESLint, Prettier, Vitest wired in every package
- `pnpm typecheck`, `pnpm test`, `pnpm lint` work from the root
- `.gitignore` covers exports, Zepp files, `.dev.vars` and wrangler state (ADR-0005)

**FND: Project implement skill** (MVP)
- `.claude/skills/implement/SKILL.md`, based on Liam's `claude/.agents/skills/implement`, extended with the flow in [workflow.md](../workflow.md)
- Given a `SCRUM-n` key, it runs the whole developer → reviewer → PR loop

**FND: PR template** (MVP)
- `.github/pull_request_template.md` with: what this does, preview URL and passphrase, iPhone test steps from the ticket's acceptance criteria, screenshots, and notes on migrations and secrets
- The `implement` skill fills it in; the `pr` skill's body follows its headings

**FND: CI** (MVP)
- GitHub Actions on every PR and every push to `main`: lint, typecheck, test
- PR cannot merge while CI is red (branch protection)

**FND: Cloudflare deploys** (MVP)
- `apps/api` is one Cloudflare Worker (Hono) that also serves the built `apps/web` PWA as static assets, with a D1 database and Drizzle migrations
- Workers Builds deploys `main` to production and runs `wrangler preview` for every other branch; each PR gets a Preview URL, posted as a PR comment
- A separate `gym-tracker-preview` D1 database, bound only in the `previews` block of `wrangler.jsonc`, holds demo data only; a test fails if its ID equals the production database ID
- `pnpm db:reseed:preview` drops the preview tables, applies migrations and loads the demo data
- Secrets come only from Wrangler/Cloudflare secrets: production with `wrangler secret put`, previews with `wrangler preview base-config secret put`. The preview passphrase is not the production one
- The Settings screen and the login screen show the build commit SHA

**FND: Passphrase login** (MVP, ADR-0003)
- First visit on a device shows a passphrase screen; a correct passphrase returns a long-lived token stored on the device
- Every API route except login rejects requests without a valid token (401)
- A wrong passphrase is rate-limited

**FND: Installable PWA shell** (MVP)
- Manifest, icons and service worker; "Add to Home Screen" on iPhone opens full-screen
- Dark theme by default; Tailwind + shadcn/ui set up
- The service worker updates predictably on previews: it calls `skipWaiting()` and `clients.claim()` on preview builds, and the build SHA on screen shows which build is running
- Phone layout plus wider dashboard layout; Workouts are started, logged (live or after the fact) and edited on the phone only; the dashboard shows them read-only and manages everything else (e.g. Routines, Weigh-ins, Measurement Sessions, Settings)

**FND: Settings** (MVP)
- Weekly Target and height (default 188cm), stored via the API. There is no sex setting: the one lifter is male and only the male US Navy formula is used
- Weekly Sets targets are not in Settings; they live in the fatigue config file (`rec-recovery.md`)

**FND: Demo data generator** (MVP, ADR-0005)
- Script that seeds a local D1 and the shared preview D1 (`gym-tracker-preview` only; it refuses any other database name) with plausible made-up Workouts, Weigh-ins and Measurement Sessions, in the low thousands of rows to stay under the D1 daily write limit
