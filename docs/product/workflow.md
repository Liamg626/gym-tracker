# Delivery workflow

## Tickets

- Jira project `SCRUM`. Jira assigns the key (`SCRUM-14`).
- Titles start with an **area code + a number that counts up per area**: `[LOG-003] Log a Working Set`.
- Every ticket carries its area label in lowercase (`log`) for filtering.
- Epics: one per area. Stories: thin end-to-end slices Liam can test on his phone. Tasks: research and setup. Bugs: issue type `Bug`.
- Jira versions: MVP, v1.1, v1.2, v1.3. Sprints are one week, with no story points.

| Code | Area | Spec |
|---|---|---|
| FND | Foundations | [fnd-foundations.md](features/fnd-foundations.md) |
| EXL | Exercise Library | [exl-exercise-library.md](features/exl-exercise-library.md) |
| LOG | Workouts, Routines, history | [log-workouts.md](features/log-workouts.md) |
| BDY | Weigh-ins, measurements, body fat | [bdy-body.md](features/bdy-body.md) |
| REC | Recovery Map | [rec-recovery.md](features/rec-recovery.md) |
| GOL | Milestones, Body Goals, PRs | [gol-goals.md](features/gol-goals.md) |
| HOM | Home screen and widgets | [hom-home-widgets.md](features/hom-home-widgets.md) |
| INS | Charts, Weekly Breakdown | [ins-insights.md](features/ins-insights.md) |
| WCH | Watch Data | [wch-watch-data.md](features/wch-watch-data.md) |

## Statuses

To Do → In Progress → In Review → **Ready To Merge** → Done

## Implementing a ticket

Liam starts each ticket with the project `implement` skill and a `SCRUM-n` key.

Models: the skill itself runs on Sonnet (medium effort) and orchestrates; the code is written by the `implementer` subagent (Haiku, low; Sonnet, medium for the round-3 fixes) and reviewed by the `reviewer` subagent (Haiku, medium), both defined in `.claude/agents/`. Research and design tickets are done by the skill session itself.

ponytail (level `full`) is on for the skill session and both subagents through `.claude/settings.json`. Subagents get it through its SubagentStart hook. See [ponytail.md](../agents/ponytail.md).

1. **Skill session**: reads the ticket, moves it to In Progress and branches off `main` as `SCRUM-n-short-slug`. The **`implementer`** builds test-first (TDD) for domain logic and API, runs typecheck and tests, and commits with `SCRUM-n: …` messages. The skill session checks its evidence, pushes, opens a **draft PR** titled `SCRUM-n [AREA-nnn] …`, and moves the ticket to In Review.
2. **`reviewer`**: reviews the PR against the ticket's acceptance criteria and the repo docs, and leaves line comments on the draft PR. If changes are needed, the skill session sends them to a fresh `implementer` (the ticket stays In Review).
3. After **3** unsuccessful review rounds: label `ready-for-human`, comment on the ticket with what's blocking, stop.
4. When the reviewer approves: the **skill session** marks the PR ready for review, assigns Liam, posts the closing comment on the ticket, and moves the ticket to **Ready To Merge**.
5. **Liam** tests on the PR's Cloudflare preview URL and merges; the ticket moves to Done.

## Design gate

Each release (MVP, v1.1, v1.2, v1.3) has one **design ticket**, labelled `design`: FND-007 to FND-010 (SCRUM-16 to SCRUM-19). Each one produces two Claude Design artifacts, one for mobile and one for the web dashboard. Each design ticket publishes its **own new** artifacts, starting from a copy of the previous release's. A release's artifacts can still change after approval, until that release's Stories are sliced. From then on they are **frozen** for that release, because the Stories are built against them; any later change goes into the next release's design.

- **Gate:** each design ticket is blocked by the previous release's one. Every Story for a release gets an "is blocked by" link to that release's design ticket, created together with the Story. So no Story starts until its release's design is approved.
- **The design ticket's loop:** the agent posts the artifact links on the ticket and moves it to In Review. Liam gives feedback in artifact comments or Jira comments, and the agent republishes that ticket's artifacts to the same URLs. This repeats, with no round limit, until Liam approves. There is no branch, PR or reviewer agent. The closing comment's **Done** line holds the final artifact links, and the ticket moves to Done.
- **Sliced = frozen:** a release's design is frozen once it is approved **and** at least one Story with an "is blocked by" link to its design ticket exists, whichever happens later. If Stories are sliced before approval, the freeze comment is posted when Liam approves. Whoever triggers the freeze (creates that Story, or closes the design ticket when Stories already exist; Liam or an agent) adds a comment on the design ticket: "Design frozen for <release>", with the artifact links and their current version ids (the Artifact tool's version id, e.g. `1792235320-0528`).
- **Changes after approval, before slicing:** before republishing, the agent checks the design ticket for a "Design frozen" comment or a Story blocked by it. If either exists, the change goes to the next release's design ticket instead. Otherwise the agent republishes to the same URLs and adds a dated comment on the design ticket saying what changed; the ticket stays Done. If the next release's design ticket has already copied these artifacts, the change is applied there too.
- **Building a Story:** the `implementer` opens the artifacts named in the design ticket's "Design frozen" comment, for the device(s) the Story touches, and builds to match them. The reviewer checks the build against them too.

## Skills by ticket type

| Ticket type | Skill |
|---|---|
| Research Task | `mattpocock-skills:research`: findings go to `docs/research/<topic>.md` with sources; proposed design-doc changes are listed for Liam, never applied directly |
| Setup steps only Liam can do (machine installs) | `mattpocock-skills:wizard` for the human steps, then the agent finishes the repo side |
| Story / Bug | project `implement` skill: `tdd` during the build, `code-review` and `ponytail-review` by the reviewer agent |
| Task the agent can do itself (chore/setup: CI, deploys, config, demo data) | no extra skill; `tdd` for any logic, `code-review` and `ponytail-review` by the reviewer agent |
| Design prototype (label `design`) | the Artifact tool: `quickstart` with intent `design`, then publish and iterate. See § Design gate |
| Applying research to the design | `mattpocock-skills:grilling` + `mattpocock-skills:domain-modeling` |

## Closing comment (every ticket)

Before a ticket moves to Ready To Merge, or to Done if there is no PR, the agent posts one Jira comment in this format:

```
**Done:** 1–3 sentences on what was delivered and where (files/docs).
**PRs:** links, or "none".
**Q&A:**
- Q: <question asked during the work> → A: <answer> (<who answered: Liam / source / agent decision>)
**Follow-ups:** new tickets created, proposed doc changes awaiting approval, or "none".
```

Q&A includes every question put to Liam, every question the ticket set out to answer, and any judgement call the agent made on its own, so decisions stay traceable from Jira.

## Jira setup (done 2026-10-16)

- **Ready To Merge** status/column on the board
- **Bug** work type in the project (every work type shares the same five statuses)
