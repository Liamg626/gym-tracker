# graphify

[graphify](https://github.com/Graphify-Labs/graphify) turns the repo's code and docs into a knowledge graph that agents can query instead of grepping. Code is parsed locally with tree-sitter. Docs get a semantic pass that runs on the in-session model, so no API key is needed.

Only install the PyPI package `graphifyy` (double y). The other `graphify*` packages on PyPI have nothing to do with this project. The README also advertises a paid Graphify Cloud, which we don't need, and its benchmark numbers are self-reported.

## Licence

Apache-2.0, checked in the installed package (`graphifyy-0.9.92.dist-info`: `License-Expression: Apache-2.0`). Its `NOTICE` explains the second licence file: code contributed before the project was relicensed is still also available under MIT (`LICENSE-MIT`). Either way it is fine to use here.

## Setup

What the repo contains:

- [`.claude/skills/graphify/`](../../.claude/skills/graphify/): the project skill that `graphify install --project` writes. It adds `/graphify`.
- [`.graphifyignore`](../../.graphifyignore): keeps `node_modules`, build output, `.claude/`, and anything that could be real data out of the graph (exports, `*.zip`, `*.csv`, `.dev.vars`; see ADR-0005). graphify also reads `.gitignore`.
- `.gitignore` lists `graphify-out/`. The graph is a local build artifact, so each machine builds its own and nothing generated is committed.

On a new machine (Windows, needs Python 3.10+):

```
winget install astral-sh.uv
uv tool install graphifyy
uv tool update-shell        # puts ~/.local/bin on PATH; then restart the shell
```

Then run `/graphify .` in Claude Code to build the graph. Don't run `graphify install --project` again: the skill is already committed, and that command also turns on always-on mode (see below).

## Always-on mode: off

`graphify install --project` and `graphify claude install` also add two `PreToolUse` hooks to `.claude/settings.json` (`graphify hook-guard search` / `read`) and a rules section to `CLAUDE.md`. Together they steer every agent to the graph before it reads, globs or searches. We removed both. Querying stays **manual**: the repo is still mostly docs, and the hooks would change how every developer and reviewer agent explores it. We'll look at this again once the FND monorepo scaffold has landed.

The skill itself can still trigger on a codebase question when `graphify-out/graph.json` exists, because its description invites that. That is expected. Nothing forces it.

## When agents should query it

- To get oriented across many docs or packages, e.g. "which ADRs constrain the Recovery Map?" or "what depends on the Exercise Library?". Run `graphify query "<question>"`, `graphify path "<A>" "<B>"` or `graphify explain "<concept>"`.
- Don't use it for an exact string or a single file you already know. Grep or Read that directly.
- The graph can be stale. Before relying on an answer, check the cited `source_location` against the file.

## Refreshing

- `/graphify . --update` re-extracts only new or changed files (docs get a semantic pass again).
- `graphify update .` refreshes code only (AST, no model cost).
- To start again from scratch: delete `graphify-out/` and run `/graphify .`.

## Query log

graphify 0.9.92 writes **no** query log by default. Logging only starts if you set `GRAPHIFY_QUERY_LOG_ENABLE=1` or `GRAPHIFY_QUERY_LOG=<path>`. If you ever turn it on, the log goes to `~/.cache/graphify-queries.log`, outside the repo. `GRAPHIFY_QUERY_LOG_DISABLE=1` forces it off whatever else is set. We don't set any of these.

## Uninstall

1. `graphify uninstall --purge` removes graphify from every platform it detects and deletes `graphify-out/`. Afterwards, check that `.claude/settings.json` and `CLAUDE.md` have no graphify entries left.
2. Delete `.claude/skills/graphify/` and `.graphifyignore`, and drop `graphify-out/` from `.gitignore`.
3. `uv tool uninstall graphifyy`
