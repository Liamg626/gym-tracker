---
name: implement
description: "Take a SCRUM-n ticket from To Do to Ready To Merge: build, review, PR, closing comment."
disable-model-invocation: true
---

Implement the Jira ticket the user names (`SCRUM-n`). `docs/product/workflow.md` is the source of truth for statuses, naming, which skill fits which ticket type, the review loop and the closing-comment format. Read it before step 1, and follow it wherever this skill points to it.

Keep a **Q&A log** from the first step to the last: every question you put to Liam with his answer, every question the ticket sets out to answer with the answer you found, and every judgement call you made yourself. It becomes the closing comment.

## Tools

- Jira: the `atlassian` MCP server, cloudId `a751e4e3-ae82-407a-ac06-a7a1a5d0b722`. If its tools are missing, ask Liam to run `/mcp` and stop.
- GitHub: `gh`. On this machine it is often not on PATH; fall back to `"/c/Program Files/GitHub CLI/gh.exe"` (Bash).

## Steps

1. **Read the ticket.** Fetch it with its comments and links. State its title back to Liam. Then read `CONTEXT.md`, the feature spec for its area (`docs/product/features/`), and any ADR it touches. Done when you can name the ticket's type, its acceptance criteria and its spec.
2. **Gate it.** Stop and tell Liam if it has an unresolved "is blocked by" link, if it is `ready-for-human` with no agent-doable part, or if the acceptance criteria contradict the spec or an ADR (quote both). Ask Liam about anything ambiguous now, before any work starts, and log the Q&A.
3. **Start.** Move the ticket to In Progress. Branch off an up-to-date `main` as `SCRUM-n-short-slug`.
4. **Do the work** with the skill `workflow.md` assigns to this ticket type. For code, run typecheck and the touched test files as you go and the full suite at the end. Use the glossary's terms in code, docs and commits. Done when every acceptance criterion is met and you can point to the evidence for each.
5. **Open the draft PR.** Commit as `SCRUM-n: …`, push, and open a **draft** PR titled `SCRUM-n [AREA-nnn] <summary>`. The body lists each acceptance criterion with its evidence, and gives Liam test steps for the preview URL when there is something to try. If the ticket changed nothing in the repo, skip to step 8 and move it straight to Done. Otherwise move the ticket to In Review.
6. **Review.** Dispatch a fresh reviewer subagent with the ticket key, the PR number and `workflow.md`. Brief it to review the PR against the acceptance criteria, `CONTEXT.md` and the ADRs (stories and bugs also through the `code-review` skill), leave line comments on the PR (`gh pr review --comment` or `gh api` review comments; it cannot request changes on a PR from the same account), and return either **approved** or a list of required changes. Fix the required changes, push, and dispatch a fresh reviewer again.
   - **3 rounds without approval:** add the `ready-for-human` label, comment on the ticket with what is blocking, and go to step 8 without changing the status.
7. **Hand over.** On approval, run `gh pr ready`, assign Liam (`gh pr edit --add-assignee @me`), and move the ticket to Ready To Merge.
8. **Closing comment.** Post it on the ticket in the exact format from `workflow.md`, with the PR link and the full Q&A log. Then give Liam the same summary in chat. Done when the comment is posted and the ticket is in its final status for this run.
