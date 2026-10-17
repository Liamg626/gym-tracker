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

**FND: CI** (MVP)
- GitHub Actions on every PR and every push to `main`: lint, typecheck, test
- PR cannot merge while CI is red (branch protection)

**FND: Cloudflare deploys** (MVP)
- `apps/web` on Cloudflare Pages, `apps/api` on Workers, D1 database with Drizzle migrations
- Every PR gets a preview URL; merging to `main` deploys to production
- Secrets come only from Wrangler/Cloudflare secrets

**FND: Passphrase login** (MVP, ADR-0003)
- First visit on a device shows a passphrase screen; a correct passphrase returns a long-lived token stored on the device
- Every API route except login rejects requests without a valid token (401)
- A wrong passphrase is rate-limited

**FND: Installable PWA shell** (MVP)
- Manifest, icons and service worker; "Add to Home Screen" on iPhone opens full-screen
- Dark theme by default; Tailwind + shadcn/ui set up
- Phone layout plus wider dashboard layout; Workouts are started, logged (live or after the fact) and edited on the phone only; the dashboard shows them read-only and manages everything else (e.g. Routines, Weigh-ins, Measurement Sessions, Settings)

**FND: Settings** (MVP)
- Weekly Target, height (default 188cm), sex (default male), stored via the API
- v1.2 adds Working Set target ranges per Muscle

**FND: Demo data generator** (MVP, ADR-0005)
- Script that seeds a local/preview D1 with plausible made-up Workouts, Weigh-ins and Measurement Sessions
