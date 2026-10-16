# Issue tracker: Jira

Issues and specs for this repo live in Jira, not GitHub Issues.

- **Site**: https://liamg626.atlassian.net
- **Project**: `SCRUM` (Scrum board: https://liamg626.atlassian.net/jira/software/projects/SCRUM/boards/1)
- **Access**: the `atlassian` MCP server (Atlassian Rovo MCP v2, `https://mcp.atlassian.com/v2/mcp`, configured in `.mcp.json`). If its tools aren't loaded, run `/mcp` and authenticate `atlassian`. Don't fall back to `gh issue`.

## Conventions

- **Create an issue**: create a Jira issue in project `SCRUM`. Use issue type `Story` for features, `Bug` for defects, `Task` for chores.
- **Read an issue**: fetch it by key (e.g. `SCRUM-12`), including its comments, labels and status.
- **List issues**: search with JQL, e.g. `project = SCRUM AND statusCategory != Done ORDER BY created DESC`. Add `AND labels = "<label>"` to filter by triage label.
- **Comment on an issue**: add a Jira comment to the issue.
- **Apply / remove labels**: edit the issue's `labels` field (Jira creates labels on first use).
- **Close**: transition the issue to `Done` (look up the available transitions first), with a comment explaining why.

Refer to issues by their Jira key (`SCRUM-12`), never by a bare `#12`.

## Linking code to Jira

Put the issue key in branch names, commit messages and PR titles (e.g. branch `SCRUM-12-log-workout`, commit `SCRUM-12: add workout form`). With the GitHub for Jira app installed, the branches, commits and PRs show up on the Jira issue.

## Pull requests as a triage surface

**PRs as a request surface: no.** Triage runs on Jira issues only.

## When a skill says "publish to the issue tracker"

Create a Jira issue in project `SCRUM`.

## When a skill says "fetch the relevant ticket"

Fetch the Jira issue by key, including comments.

## Wayfinding operations

Used by `/wayfinder`. The **map** is an Epic, and its **children** are the tickets.

- **Map**: a `SCRUM` Epic labelled `wayfinder-map`, whose description holds Notes / Decisions-so-far / Fog.
- **Child ticket**: an issue whose parent is the map Epic, labelled `wayfinder-<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, it's assigned to the driving dev.
- **Blocking**: a Jira issue link of type `Blocks` ("is blocked by"). A ticket is unblocked when every blocking issue is Done.
- **Frontier query**: JQL `parent = <map key> AND statusCategory != Done AND assignee IS EMPTY ORDER BY rank`, then drop any with an unresolved "is blocked by" link. The first one in rank order wins.
- **Claim**: assign the issue to yourself and move it to `In Progress`. This is the session's first write.
- **Resolve**: comment with the answer, transition to `Done`, then add a pointer (gist + key) to the map Epic's Decisions-so-far.
