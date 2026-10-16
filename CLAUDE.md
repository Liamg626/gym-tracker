# CLAUDE.md

## Agent skills

### Issue tracker

Issues are tracked in Jira, project `SCRUM` at liamg626.atlassian.net (via the `atlassian` MCP server). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### ponytail

The ponytail plugin (write less code) is enabled for this project in `.claude/settings.json`. See `docs/agents/ponytail.md` for setup, mode and uninstall.

### graphify

The `/graphify` project skill builds a local knowledge graph of the repo in git-ignored `graphify-out/`. Querying is manual; always-on hooks are off. See `docs/agents/graphify.md` for when to query, refresh and uninstall.
