# Research: testing every PR on a Cloudflare preview URL on an iPhone

SCRUM-6 · [FND-001] · researched 2026-10-17

## Question

Liam tests each PR on its Cloudflare preview URL on an iPhone 15 Pro before merging (workflow.md step 5). What has to be true for that to work at £0 with a public repo and no real data (ADR-0005)?

1. How do per-PR previews work for a monorepo (`apps/web`, `apps/api`), and how does a preview frontend reach a preview API? Is Pages still the right product?
2. How does a preview get its own D1 database with demo data, so previews never touch production?
3. How are secrets (the passphrase) set per environment?
4. Can the PWA be installed from a preview URL, is it worth it versus Safari, and which iOS limits affect testing?
5. Does the free tier cover it?
6. What PR template tells Liam what to test?

Sources are primary only (Cloudflare docs and repos, WebKit, MDN, web.dev). Anything the docs do not settle is marked **not knowable without trying it**. No code exists yet (`apps/` is absent), so nothing here was run.

## Summary and recommendation

- **Use Cloudflare Workers, not Pages.** The Pages docs say "Start new projects with Workers" and "It is Cloudflare's primary platform for building applications" ([Pages home][cf-pages-home]); Workers lists "most Pages use cases" as supported ([Pages Vite guide][cf-pages-vite]). Pages has nothing we need that Workers lacks: the gaps are custom domains outside Cloudflare, Early Hints, file-based routing and Pages Plugins ([migration guide][cf-migrate]), and the project uses none. This contradicts ADR-0002 and FND "Cloudflare deploys" (both say Pages). See [Proposed doc changes](#proposed-doc-changes-for-liam-to-approve-not-applied).
- **Simplest preview shape: one Worker that serves both the API and the built web app** (Hono for `/api/*`, static assets for the PWA, SPA fallback). A preview is then one URL and the frontend calls its own origin, so there is no cross-origin wiring and no CORS. Workers static assets supports `not_found_handling = "single-page-application"` and `run_worker_first` route patterns ([static assets][cf-assets], [config][cf-wrangler-config]). The cost is that `apps/api`'s deploy bundles `apps/web/dist`, so the build order is web, then Worker. The alternative of two Workers is in [Frontend to API](#1-previews-in-a-monorepo-and-reaching-the-preview-api).
- **Use Workers Previews, not Version URLs.** Cloudflare says Previews are "the recommended way to test changes before production" and that Version URLs "run on production resources" ([compare workflows][cf-compare]). A Preview has its own vars, secrets and bindings, and does **not** inherit production settings ([Previews][cf-previews], [configuration][cf-prev-config]). Workers Builds runs `npx wrangler preview` on every non-production branch and comments the URL on the PR ([branches][cf-builds-branches], [GitHub integration][cf-builds-gh]). Previews are new: **whether they are available on the Free plan is not stated** in the pages read ([get started][cf-prev-start]). Verify in the first FND "Cloudflare deploys" run.
- **One shared preview D1 database, reseeded, rather than one per PR.** Previews that share a `database_id` share rows; a different ID isolates ([resources][cf-prev-res]). Free accounts get 10 databases ([D1 limits][cf-d1-limits]), so per-PR databases would need create and delete automation and would hit the cap with open PRs. A shared `gym-tracker-preview` database holds demo data only (ADR-0005), and a reseed script resets it. Trade-off: two open PRs that change the schema need the same database; see [D1](#2-a-d1-database-per-preview-that-never-touches-production).
- **Secrets:** set the preview passphrase once as a Preview base-config secret (`wrangler preview base-config secret put`); production uses `wrangler secret put`. They are different values, so a leaked preview passphrase opens nothing real ([secrets](#3-secrets-per-environment)).
- **iPhone:** test in Safari by default. Install to the Home Screen only for tickets that touch the PWA shell, service worker or offline behaviour, because each preview URL is its own origin with its own storage ([WebKit storage][wk-storage]), so the install and the login are per preview.
- **Cost:** within free limits on every number checked ([cost check](#5-free-tier-cost-check)); the tight ones are 1 concurrent build and 100 Previews per Worker, neither a problem for one developer.

## 1. Previews in a monorepo and reaching the preview API

### Pages (the current plan)

- A PR from the connected repo gets a preview URL that updates on each push; PRs from forks do not. Hash URL `<hash>.<project>.pages.dev` and a branch alias `<branch>.<project>.pages.dev` ([preview deployments][cf-pages-prev]).
- Previews are public by default; an access policy limits them to the Cloudflare account ([preview deployments][cf-pages-prev]).
- Monorepos: **one Pages project per app**, each with its own root directory and build command; build watch paths limit builds to relevant changes; maximum 5 Pages projects per repo; requires Build System V2 ([monorepos][cf-pages-mono]).
- Pages Functions run API code, but the docs steer Hono-style APIs to Workers; the "Functions" requests count against the Workers quota ([Pages limits][cf-pages-limits]).
- A Pages preview talks to a separate API Worker over its URL. Nothing in the Pages docs links a Pages preview to a matching Worker preview. **Not knowable without trying it:** how the Pages preview learns the API URL (a build-time `VITE_API_URL` pointing at a fixed staging Worker is the obvious route, and CORS would then be needed).

### Workers static assets and Workers Builds (recommended)

- Workers can serve a SPA with the API in the same Worker; "A request that matches a file is served without running Worker code" and unmatched requests go to the Worker or fall back to `index.html` in SPA mode ([static assets][cf-assets]).
- Pages-to-Workers comparison: both support preview URLs, rollbacks, D1 and the other bindings; Workers adds gradual deployments, the Vite plugin, Workers Logs and more; Pages adds custom domains outside Cloudflare zones, Early Hints, branch deploy controls with more options, and file-based routing ([migration guide][cf-migrate]). None of the Pages-only items are needed here.
- Workers Builds connects each Worker to the repo with a **root directory** and optional **build watch paths**; build and deploy commands run from the root directory; each Worker's status shows as a GitHub check run, and only Workers whose paths changed run a build ([advanced setups][cf-builds-adv], [GitHub integration][cf-builds-gh], [build configuration][cf-builds-conf]). The build-watch-path defaults are **not stated** on the pages read.
- Non-production branches run the **Preview command**, default `npx wrangler preview`; the PR gets a comment with the URL, later pushes update the same URL, and each deployment also has an immutable Deployment URL ([branches][cf-builds-branches], [GitHub integration][cf-builds-gh], [build configuration][cf-builds-conf]).
- Preview URL shape on `workers.dev`: `<preview-name>-<worker-name>.<subdomain>.workers.dev`, with `X-Robots-Tag: noindex` ([Previews][cf-previews]). Preview name defaults to the branch name.
- **Version URLs are the wrong tool:** they use "that Worker version's existing configuration and resources" (so production D1), cannot be viewed in Workers Logs or `wrangler tail`, and are public by default ([Version URLs][cf-version-urls]).

### Frontend to API

| Option | How the preview frontend reaches its API | For | Against |
|---|---|---|---|
| **A. One Worker: Hono + static assets** (recommended) | Same origin, `/api/*` | One URL per PR, one D1 binding, no CORS, one set of secrets | `apps/api` must see `apps/web/dist` at deploy time; web and API deploy together (fine for one user) |
| B. Two Workers (`web` with assets, `api`) | `web` calls `api`. A Preview's service binding to another Worker resolves to that Worker's **production** deployment ([resources: limitations][cf-prev-res]) | Separate deploys | A web Preview would reach the production API. Needs a fixed staging API URL and CORS. More moving parts |
| C. Pages + Worker | Build-time API URL | Matches current ADRs | Pages is no longer the recommended product; two build systems |

The Cloudflare docs do not show a monorepo with a web build feeding a Worker's `assets.directory`. **Not knowable without trying it:** whether Workers Builds with root directory at the repo root, `pnpm --filter web build` as the build command and `apps/api/wrangler.jsonc` pointing `assets.directory` at `../web/dist` works cleanly. The Cloudflare Vite plugin removes the need for `assets.directory` ([static assets][cf-assets]) and is an alternative if the layout is changed.

### Wrangler preview on Windows

Previews need Wrangler 4.135.0 or later installed as a project dependency ([get started][cf-prev-start]). Wrangler on Windows is not covered in the docs read. **Not knowable without trying it:** local `wrangler preview` from Windows. CI/Workers Builds is Linux anyway; local work uses `wrangler dev`.

## 2. A D1 database per preview that never touches production

### Mechanism

- Previews get their own bindings. The `previews` block in `wrangler.jsonc` lists preview bindings with the same binding name pointed at a preview-safe resource; "Previews do not inherit production settings" ([configuration][cf-prev-config]).
- D1: "Configure a shared staging database on the base branch"; to isolate one branch, change its Preview binding and migration config to a different database ([configuration][cf-prev-config]). Previews sharing a `database_id` share rows ([resources][cf-prev-res]).
- Previews migrate through a second config, `wrangler.preview-migrations.jsonc`, which "must point to the same physical database" as the Preview binding ([resources][cf-prev-res]). If several Previews share one database, run the migration for it only once ([resources][cf-prev-res]).
- The existing Pages equivalent (if Pages is kept): `[env.preview]` with its own `d1_databases`; bindings are not inherited, so every binding must be repeated in the environment block ([Pages Wrangler config][cf-pages-wrangler]).
- D1 migrations: `wrangler d1 migrations create/list/apply`; applied migrations are recorded in `d1_migrations`; `apply` takes `--local` and `--remote`; a failed migration rolls back ([migrations][cf-d1-mig], [commands][cf-d1-cmd]). Drizzle's one-folder-per-migration layout needs `migrations_pattern` alongside `migrations_dir` ([migrations][cf-d1-mig]).
- Seeding: `wrangler d1 execute <DB> --remote --file seed.sql`. Without `--local`, `d1 execute` targets the **remote** database ([local development][cf-d1-local], [commands][cf-d1-cmd]). That default is the danger: a mistyped command on the production binding writes to production.

### Per-PR versus shared preview database

| | Shared `gym-tracker-preview` | One database per PR |
|---|---|---|
| Isolation from production | Yes, as long as the `previews` binding never uses the production ID | Yes |
| Isolation between PRs | None: a schema-changing PR affects every open preview | Full |
| Setup | One `wrangler d1 create`, one reseed script | Create, migrate, seed on PR open; delete on close (the docs' cleanup example deletes Previews, not databases ([examples][cf-prev-auto])) |
| Free-tier fit | 2 databases of 10 | Open PRs plus production plus preview must stay under 10 ([D1 limits][cf-d1-limits]) |
| Fit for one developer and one PR at a time | Good | Over-built |

**Recommendation:** shared preview database, with the reseed as an npm script that drops the app tables, runs `d1 migrations apply --remote`, then runs the FND "Demo data generator" output (`d1 execute --file`). Move to per-PR only if two schema-changing PRs are routinely open together. Because migrations are applied to the shared database by the PR under test, a PR with a destructive migration must not be left open against it; reseed after each such PR.

### Guard rails so previews cannot hit production

- Production binding at top level of `wrangler.jsonc`, `previews.d1_databases` pointing to the preview database ID. IDs are not secrets, but the repo is public and holds no data (ADR-0005), so committing both IDs is fine.
- A test that reads `wrangler.jsonc` and fails if `previews.d1_databases[*].database_id` equals the top-level `database_id`.
- Seed and migrate scripts take the database **name** `gym-tracker-preview` as a fixed constant and never the production name.
- **Not knowable without trying it:** whether the default Workers Builds token can run `d1 migrations apply --remote` in the preview command. The default token is generated by Cloudflare ([build configuration][cf-builds-conf]); its D1 permissions are not documented on the pages read. Fallback: run migrations and seed from GitHub Actions with a scoped API token in a repo secret (fork PRs do not get repo secrets by default ([examples][cf-prev-auto]), which suits a public repo).

## 3. Secrets per environment

- Workers production: `npx wrangler secret put PASSPHRASE` creates and deploys a new version immediately; `wrangler versions secret put` creates a version without deploying ([secrets][cf-secrets]). Local: `.dev.vars` (already git-ignored, ADR-0005 and FND scaffold).
- Previews: secrets cannot live in the config file. `npx wrangler preview base-config secret put PASSPHRASE` sets it for every **new** Preview; "later changes to Base secrets apply only to new Previews, so active Previews remain unchanged"; `npx wrangler preview secret put PASSPHRASE --name <preview>` sets one ([configuration][cf-prev-config]).
- Practical result: give the preview the passphrase `preview-demo` (or similar throwaway) and keep the real one only on production. Rotating it needs a base-config change plus a new Preview, or the per-preview command.
- A `cloudflare/workers-sdk` pull request reports that in Wrangler 4.148.0 re-running `wrangler preview` on an existing Preview could drop its secrets; a fix is proposed in [workers-sdk#16102][gh-sdk-16102]. **Not knowable without trying it:** whether the installed version has the fix. If previews lose the passphrase, FND login will return 401 with a correct passphrase; check this first.
- Build variables and secrets in Workers Builds exist only at build time, not at runtime ([build configuration][cf-builds-conf]). The passphrase is a runtime secret, so it must not be put there.
- Pages (if kept): dashboard Settings > Variables and Secrets, then Encrypt; "Set secrets before the deployment that uses them" ([Pages bindings][cf-pages-bind]). Whether Pages secrets are scoped separately for production and preview, and the `wrangler pages secret put` flags, were **not documented on the pages read**.
- Preview URLs are public by default ([Previews][cf-previews]), so ADR-0003's login still guards the API on previews. An optional Cloudflare Access policy can restrict Previews to the account ([Previews][cf-previews]); not needed for demo data.

## 4. The PWA on the iPhone from a preview URL

### Can it be installed?

- Yes. Any website can be added from Safari's Share menu. It opens as an app (no browser UI) only if the manifest sets `display` to `standalone` or `fullscreen`; otherwise it is saved as a bookmark ([WebKit 16.4][wk-163]). Nothing requires a production domain. FND "Installable PWA shell" already specifies this.
- **Each preview URL is a separate origin.** WebKit storage is partitioned by origin ([WebKit storage][wk-storage]). Preview URLs differ by host (`<preview-name>-<worker>...`), so every PR is its own origin with its own token, IndexedDB and service worker. Installing PR 14 does not update an installed PR 13 icon; both icons would sit on the Home Screen.
- **Safari and the Home Screen app do not share storage** in the documented case of macOS Dock apps: Safari copies cookies at install and "does not copy over any other kind of local storage", after which no website data is shared ([WebKit Safari 17][wk-17]). For iOS Home Screen web apps the pages read confirm only that they "are not part of Safari and thus have their own counter of days of use" ([WebKit ITP][wk-itp]). **Not knowable without trying it:** that iOS keeps the same split. Plan for it: log in again after installing, and seed any local state again.
- Third-party browsers can offer Add to Home Screen from iOS 16.4 only with the web-browser entitlement ([WebKit 16.4][wk-163]); use Safari.

### Worth it versus Safari?

| Test | Safari tab on the preview URL | Installed from the preview URL |
|---|---|---|
| Layout, forms, API flows, login | Enough | Same |
| Safe-area insets, full-screen chrome, status bar, theme colour | Not visible | Needed |
| Service worker update and offline behaviour (ADR-0004: sets saved on device first) | Partial | Needed |
| Persistent storage behaviour | Best-effort; evictable | WebKit's persistent-storage heuristics weigh whether the site is a Home Screen web app ([WebKit storage][wk-storage]) |
| Cost | None | A new icon per PR, a new login, and the icon dies when the preview is deleted |

**Recommendation:** Safari is the default for every PR. Install to the Home Screen only on PRs that change the manifest, service worker, offline path or layout around the safe area (the FND "Installable PWA shell" ticket, and any later ticket that touches them), and delete the icon afterwards. Do a full installed check on production after merge for those tickets.

### iOS limits that affect testing

- **Stale builds from the service worker.** A new service worker installs and then **waits** while any page still uses the old one; it activates only once all pages controlled by the old worker are closed. `skipWaiting()` activates it sooner but old pages may then be served by both workers ([MDN service workers][mdn-sw], [web.dev lifecycle][webdev-sw]). A refresh does not release the old worker, because "the current service worker is always controlling a client during a refresh" ([web.dev][webdev-sw]). Browsers check for a new worker on navigation, at most every 24 hours for functional events, and the update only counts if the script differs byte for byte ([web.dev][webdev-sw]). Result: after pushing a fix to a PR, Liam may be looking at the previous build. Whether swiping the Home Screen app away in the iOS app switcher closes all its pages is **not knowable without trying it** (no primary source read).
  - Mitigation (proposed for FND "Installable PWA shell"): show the build commit SHA in Settings and on the login screen; give the worker `skipWaiting()` and `clients.claim()` on preview builds only; and use content-hashed asset names (Vite does by default).
- **7-day eviction.** Safari deletes a site's script-writable storage (IndexedDB, localStorage, service worker registrations and caches, and others) "after seven days of Safari use without user interaction on the site" ([WebKit ITP][wk-itp]). Home Screen web apps "have their own counter of days of use" and WebKit "do[es] not expect" their data to be deleted ([WebKit ITP][wk-itp]). The same article's wording is about Safari itself; the storage-policy article only says eviction can also follow "a site goes unused for some time" and is on an LRU, origin basis ([WebKit storage][wk-storage]). Effect on testing: a preview left in a Safari tab for a week may lose its token and any unsynced sets. Harmless for demo data, but an unsynced-sets test (ADR-0004) must be done within a session.
- **Quota.** Home Screen web apps have the same origin and overall quota as Safari ([WebKit storage][wk-storage]); not a testing constraint.
- **Push notifications** work only from the Home Screen app (ADR-0001); they cannot be tested from a Safari tab.
- **Preview URLs are deleted over time.** The oldest Preview is deleted when the Free-plan limit of 100 Previews per Worker is reached ([Previews][cf-previews]); deleted ones leave dead Home Screen icons.

## 5. Free-tier cost check

Checked 2026-10-17 against the current docs.

| Item | Free-plan limit | Our use | Source |
|---|---|---|---|
| Workers Builds minutes | 3,000 per month; 1 concurrent build; 20 min timeout | At an assumed 3 minutes per build, 3,000 minutes allows about 1,000 builds a month (**build time not measured**) | [Builds limits][cf-builds-limits] |
| Pages builds (if kept) | 500 builds per month | Each push to a PR counts as one | [Pages limits][cf-pages-limits] |
| Workers requests | 100,000 per day, reset 00:00 UTC | One user | [Workers limits][cf-workers-limits], [pricing][cf-workers-pricing] |
| Workers CPU time | 10 ms per HTTP request | Hono + Drizzle on D1; **not measured**, check heavy endpoints (Weekly Breakdown, imports) | [Workers limits][cf-workers-limits] |
| Static asset requests | "Free and unlimited" | The PWA bundle | [Workers pricing][cf-workers-pricing] |
| Static asset size | 20,000 files per version; 25 MiB per file | Small | [Workers limits][cf-workers-limits] |
| Secrets and env vars | 64 per Worker | A handful | [Workers limits][cf-workers-limits] |
| Previews | 100 per Worker, 100 deployments each; oldest auto-deleted | Few open PRs | [Previews][cf-previews] |
| D1 databases | 10 per account | Production plus preview = 2 | [D1 limits][cf-d1-limits] |
| D1 database size / storage | 500 MB each / 5 GB total | Single user | [D1 limits][cf-d1-limits], [D1 pricing][cf-d1-pricing] |
| D1 rows read / written | 5 million / 100,000 per day; beyond that queries error until 00:00 UTC | Preview and production counted together on one account | [D1 pricing][cf-d1-pricing] |
| D1 queries per Worker invocation | 50 | Batch writes in one request must stay within it | [D1 limits][cf-d1-limits] |

Notes:

- **Rows written is the tightest D1 number.** A demo-data reseed writes every seeded row. If the seed is a few thousand rows, a handful of reseeds a day is fine; a seed of 90 days of sets times 30 muscles tagged could add up. Keep the seed in the low thousands of rows. **Not measured.**
- The 100,000 daily-requests limit is account-wide across all Workers, previews included ([Workers limits][cf-workers-limits]).
- Whether Previews and Workers Builds are billed differently on the Free plan is **not stated** on the pages read.
- All figures are the current published limits and can change; the pages carry no end date.

## 6. PR template

Draft `.github/pull_request_template.md`. Not created. The `pr` skill writes the body, so the template mainly fixes the headings the skill fills in. Acceptance criteria come from the Jira ticket; the agent copies them as tickable steps.

```markdown
## What this does

<!-- 1-3 sentences. Ticket: SCRUM-n [AREA-nnn] -->

## Preview

- Preview URL: <!-- https://...workers.dev (also in the Cloudflare PR comment) -->
- Passphrase: preview passphrase (not the production one)
- Data: shared preview database, demo data only
- Build: <!-- commit SHA shown in Settings. Check it matches the last commit before testing -->

## Test on iPhone

Open the preview in Safari. Install to the Home Screen only if marked below.

- [ ] <!-- one step per acceptance criterion from the ticket, written as "do X, expect Y" -->
- [ ] <!-- ... -->
- [ ] Nothing else on the screen broke (quick look at the Log and Home screens)

Install to Home Screen needed: <!-- yes (why) / no -->

## Screenshots

<!-- iPhone-width screenshots or a short screen recording of each changed screen. Demo data only. -->

| Before | After |
|---|---|
| | |

## Notes for the reviewer

- Migrations: <!-- none / yes: list. A preview reseed is needed: yes/no -->
- New secrets or settings: <!-- none / list names only, never values -->
- Out of scope / follow-ups: <!-- ticket keys, or none -->
```

Rules the template relies on: screenshots and recordings use demo data only (ADR-0005); no secret values in the PR text; the PR is public.

## Proposed testing workflow

1. **PR opens (draft).** Workers Builds runs on the branch; it builds web and API and runs `wrangler preview`; a PR comment carries the URL and a check run shows build status ([GitHub integration][cf-builds-gh]). CI (lint, typecheck, test) runs separately in GitHub Actions (FND "CI"). Preview and CI are both required before Ready To Merge.
2. **Agent checks the preview before handing over.** The skill session opens the preview URL path `/api/health` (or equivalent) and confirms the commit SHA matches the branch head, then checks that a login with the preview passphrase works. This catches the dropped-secret and stale-build cases. If a migration changed, it reseeds the preview database first.
3. **PR is marked ready, ticket moves to Ready To Merge.** The PR description's "Test on iPhone" list is Liam's checklist (workflow.md step 4).
4. **Liam tests on the iPhone in Safari**, walking the ticket's steps. Home Screen install only if the PR says so. After a re-push he compares the SHA shown in the app with the PR's latest commit before testing.
5. **Liam merges.** Production deploys from `main`. For PWA-shell tickets he re-checks the installed production app.
6. **Cleanup.** Delete the PR's Preview (`wrangler preview delete --name <preview>`) when the PR closes, optionally with a GitHub Actions job as in the Cloudflare example ([examples][cf-prev-auto]); delete any Home Screen icon.

## Proposed doc changes (for Liam to approve, not applied)

These change nothing until Liam says so. Wording is exact.

**`docs/adr/0002-hono-cloudflare-workers-d1.md`.** ADRs are normally not edited after acceptance; add a dated note, as was done for ADR-0006, or write a new ADR superseding the Pages part. Replace "The PWA is hosted on Cloudflare Pages." with:

> The PWA is served as static assets by the same Cloudflare Worker that runs the API (Workers static assets), not from Cloudflare Pages. Cloudflare now tells new projects to start with Workers, and a single Worker gives each pull request one preview URL where the frontend and the API share an origin. *Amended 2026-10-17 (SCRUM-6).*

**`docs/product/features/fnd-foundations.md`, FND: Cloudflare deploys.** Replace the three bullets with:

> - `apps/api` is one Cloudflare Worker (Hono) that also serves the built `apps/web` PWA as static assets, with a D1 database and Drizzle migrations
> - Workers Builds deploys `main` to production and runs `wrangler preview` for every other branch; each PR gets a Preview URL, posted as a PR comment
> - A separate `gym-tracker-preview` D1 database, bound only in the `previews` block of `wrangler.jsonc`, holds demo data only; a test fails if its ID equals the production database ID
> - `pnpm db:reseed:preview` drops the preview tables, applies migrations and loads the demo data
> - Secrets come only from Wrangler/Cloudflare secrets: production with `wrangler secret put`, previews with `wrangler preview base-config secret put`. The preview passphrase is not the production one
> - The Settings screen and the login screen show the build commit SHA

**`docs/product/features/fnd-foundations.md`, FND: Installable PWA shell.** Add:

> - The service worker updates predictably on previews: it calls `skipWaiting()` and `clients.claim()` on preview builds, and the build SHA on screen shows which build is running

**`docs/product/features/fnd-foundations.md`, FND: Demo data generator.** Replace "seeds a local/preview D1" with:

> - Script that seeds a local D1 and the shared preview D1 (`gym-tracker-preview` only; it refuses any other database name) with plausible made-up Workouts, Weigh-ins and Measurement Sessions, in the low thousands of rows to stay under the D1 daily write limit

**`docs/product/features/fnd-foundations.md`, new story: FND: PR template** (MVP):

> **FND: PR template** (MVP)
> - `.github/pull_request_template.md` with: what this does, preview URL and passphrase, iPhone test steps from the ticket's acceptance criteria, screenshots, and notes on migrations and secrets
> - The `implement` skill fills it in; the `pr` skill's body follows its headings

**`docs/product/workflow.md`, "Implementing a ticket" step 4.** Append:

> Before it marks the PR ready, the skill session opens the preview, checks that the build SHA matches the branch head and that the preview passphrase logs in, and reseeds the preview database if a migration changed. The PR body's "Test on iPhone" list is Liam's checklist.

**`docs/product/workflow.md`, step 5.** Replace with:

> 5. **Liam** tests in Safari on the PR's preview URL, following the PR's "Test on iPhone" list, and merges; the ticket moves to Done. He installs the preview to the Home Screen only when the PR says so, and deletes the icon afterwards.

**`docs/product/workflow.md`, new section "Previews".**

> ## Previews
>
> Every non-production branch gets a Cloudflare Preview: one URL that serves the web app and the API, backed by the shared `gym-tracker-preview` database (demo data only) and its own passphrase. Previews never read production data or secrets. Two open PRs share one preview database, so a PR with a schema change reseeds it when it opens and after it closes.

**`docs/adr/0003-single-passphrase-auth.md`.** Add one sentence:

> Each Cloudflare Preview has its own throwaway passphrase, set as a Preview base-config secret, so no production secret is available to preview deployments.

**`docs/adr/0005-public-repo-no-real-data.md`.** Add one sentence:

> Previews use a separate shared D1 database that holds only generated demo data, and screenshots in pull requests come only from it.

**`docs/adr/0001-pwa-not-native.md`.** No change needed; add to Consequences if wanted:

> - Each preview URL is its own origin, so a Home Screen install and its login are per preview. Use Safari for most PR tests.

## Unverified / limits

- **Nothing was run.** There is no `apps/` yet. Every "works" claim is the docs' statement, not an experiment.
- **Workers Previews are new and I could not tell their status.** The docs read do not say if they are in beta or whether they are available on the Free plan ([get started][cf-prev-start]). If they are not, the fallback is Version URLs with a preview-alias (production resources, so the database guard rail would be lost) or GitHub Actions running `wrangler deploy --env preview` to a persistent staging Worker (Wrangler environments, [compare workflows][cf-compare]), which would then be a single shared preview rather than one per PR.
- **Marked "not knowable without trying it" above:** Pages-to-API wiring; the monorepo build layout feeding `assets.directory`; local `wrangler preview` on Windows; Workers Builds token permissions for D1 migrations; whether the secrets-drop fix ([#16102][gh-sdk-16102]) is in the installed Wrangler; whether the iOS Home Screen app's storage is separate from Safari's; whether the app switcher closes all pages of a Home Screen web app; Pages per-environment secrets; Workers Builds watch-path defaults; CPU time per request.
- **Third-party material used for one claim:** the secrets-drop issue comes from a GitHub pull request on `cloudflare/workers-sdk` (the vendor's own repo), read via search result excerpts only. It is treated as a warning, not as documented behaviour.
- **WebKit articles are dated.** The 7-day cap is from a 2020 article ([WebKit ITP][wk-itp]) and the storage article is from 2023 ([WebKit storage][wk-storage]). iOS may have changed since; test on the device.
- **Pages was researched only enough to compare.** If Liam keeps Pages, the Pages-specific facts above (per-project monorepo setup, `[env.preview]`, dashboard secrets) apply instead.

## Sources

Cloudflare Workers
- [cf-pages-home]: Cloudflare Pages docs home ("Start new projects with Workers") — https://developers.cloudflare.com/pages/
- [cf-pages-vite]: Pages, Deploy a Vite project ("Workers supports most Pages use cases") — https://developers.cloudflare.com/pages/framework-guides/deploy-a-vite3-project/
- [cf-migrate]: Migrate from Pages to Workers — https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- [cf-assets]: Workers static assets — https://developers.cloudflare.com/workers/static-assets/
- [cf-wrangler-config]: Wrangler configuration — https://developers.cloudflare.com/workers/wrangler/configuration/
- [cf-previews]: Workers Previews — https://developers.cloudflare.com/workers/previews/
- [cf-prev-config]: Previews, Configuration — https://developers.cloudflare.com/workers/previews/configuration/
- [cf-prev-res]: Previews, Resources and isolation — https://developers.cloudflare.com/workers/previews/resources/
- [cf-prev-start]: Previews, Get started — https://developers.cloudflare.com/workers/previews/get-started/
- [cf-prev-auto]: Previews, Examples (GitHub Actions) — https://developers.cloudflare.com/workers/previews/automation-examples
- [cf-compare]: Previews, Compare workflows — https://developers.cloudflare.com/workers/previews/compare-workflows/
- [cf-version-urls]: Workers, Version URLs — https://developers.cloudflare.com/workers/configuration/previews/
- [cf-builds-branches]: Workers Builds, Build branches — https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/
- [cf-builds-conf]: Workers Builds, Configuration — https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- [cf-builds-adv]: Workers Builds, Advanced setups (monorepos) — https://developers.cloudflare.com/workers/ci-cd/builds/advanced-setups/
- [cf-builds-gh]: Workers Builds, GitHub integration — https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/github-integration/
- [cf-builds-limits]: Workers Builds, Limits and pricing — https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/
- [cf-secrets]: Workers, Secrets — https://developers.cloudflare.com/workers/configuration/secrets/
- [cf-workers-limits]: Workers limits — https://developers.cloudflare.com/workers/platform/limits/
- [cf-workers-pricing]: Workers pricing — https://developers.cloudflare.com/workers/platform/pricing/
- [gh-sdk-16102]: cloudflare/workers-sdk pull request 16102, keep Preview secrets when deploying to an existing Preview — https://github.com/cloudflare/workers-sdk/pull/16102

Cloudflare Pages
- [cf-pages-prev]: Pages, Preview deployments — https://developers.cloudflare.com/pages/configuration/preview-deployments/
- [cf-pages-mono]: Pages, Monorepos — https://developers.cloudflare.com/pages/configuration/monorepos/
- [cf-pages-limits]: Pages limits — https://developers.cloudflare.com/pages/platform/limits/
- [cf-pages-wrangler]: Pages, Wrangler configuration — https://developers.cloudflare.com/pages/functions/wrangler-configuration/
- [cf-pages-bind]: Pages, Bindings (including secrets) — https://developers.cloudflare.com/pages/functions/bindings/

Cloudflare D1
- [cf-d1-limits]: D1 limits — https://developers.cloudflare.com/d1/platform/limits/
- [cf-d1-pricing]: D1 pricing — https://developers.cloudflare.com/d1/platform/pricing/
- [cf-d1-mig]: D1 migrations — https://developers.cloudflare.com/d1/reference/migrations/
- [cf-d1-cmd]: D1 Wrangler commands — https://developers.cloudflare.com/d1/wrangler-commands/
- [cf-d1-local]: D1 local development — https://developers.cloudflare.com/d1/best-practices/local-development/

WebKit and web platform
- [wk-163]: WebKit, Web Push for Web Apps on iOS and iPadOS — https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- [wk-itp]: WebKit, Full Third-Party Cookie Blocking and More (7-day cap) — https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
- [wk-17]: WebKit, News from WWDC23: WebKit in Safari 17.0 — https://webkit.org/blog/14205/news-from-wwdc23-webkit-in-safari-17-0/
- [wk-storage]: WebKit, Updates to Storage Policy — https://webkit.org/blog/14403/updates-to-storage-policy/
- [mdn-sw]: MDN, Using Service Workers — https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- [webdev-sw]: web.dev, The service worker lifecycle — https://web.dev/articles/service-worker-lifecycle

[cf-pages-home]: https://developers.cloudflare.com/pages/
[cf-pages-vite]: https://developers.cloudflare.com/pages/framework-guides/deploy-a-vite3-project/
[cf-migrate]: https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
[cf-assets]: https://developers.cloudflare.com/workers/static-assets/
[cf-wrangler-config]: https://developers.cloudflare.com/workers/wrangler/configuration/
[cf-previews]: https://developers.cloudflare.com/workers/previews/
[cf-prev-config]: https://developers.cloudflare.com/workers/previews/configuration/
[cf-prev-res]: https://developers.cloudflare.com/workers/previews/resources/
[cf-prev-start]: https://developers.cloudflare.com/workers/previews/get-started/
[cf-prev-auto]: https://developers.cloudflare.com/workers/previews/automation-examples
[cf-compare]: https://developers.cloudflare.com/workers/previews/compare-workflows/
[cf-version-urls]: https://developers.cloudflare.com/workers/configuration/previews/
[cf-builds-branches]: https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/
[cf-builds-conf]: https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
[cf-builds-adv]: https://developers.cloudflare.com/workers/ci-cd/builds/advanced-setups/
[cf-builds-gh]: https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/github-integration/
[cf-builds-limits]: https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/
[cf-secrets]: https://developers.cloudflare.com/workers/configuration/secrets/
[cf-workers-limits]: https://developers.cloudflare.com/workers/platform/limits/
[cf-workers-pricing]: https://developers.cloudflare.com/workers/platform/pricing/
[gh-sdk-16102]: https://github.com/cloudflare/workers-sdk/pull/16102
[cf-pages-prev]: https://developers.cloudflare.com/pages/configuration/preview-deployments/
[cf-pages-mono]: https://developers.cloudflare.com/pages/configuration/monorepos/
[cf-pages-limits]: https://developers.cloudflare.com/pages/platform/limits/
[cf-pages-wrangler]: https://developers.cloudflare.com/pages/functions/wrangler-configuration/
[cf-pages-bind]: https://developers.cloudflare.com/pages/functions/bindings/
[cf-d1-limits]: https://developers.cloudflare.com/d1/platform/limits/
[cf-d1-pricing]: https://developers.cloudflare.com/d1/platform/pricing/
[cf-d1-mig]: https://developers.cloudflare.com/d1/reference/migrations/
[cf-d1-cmd]: https://developers.cloudflare.com/d1/wrangler-commands/
[cf-d1-local]: https://developers.cloudflare.com/d1/best-practices/local-development/
[wk-163]: https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
[wk-itp]: https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
[wk-17]: https://webkit.org/blog/14205/news-from-wwdc23-webkit-in-safari-17-0/
[wk-storage]: https://webkit.org/blog/14403/updates-to-storage-policy/
[mdn-sw]: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
[webdev-sw]: https://web.dev/articles/service-worker-lifecycle
