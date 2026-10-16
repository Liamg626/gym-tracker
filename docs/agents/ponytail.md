# ponytail

[ponytail](https://github.com/DietrichGebert/ponytail) (MIT) is a Claude Code plugin that pushes agents to write less code: reuse what exists, then the stdlib, then native platform features. It keeps validation, error handling, security and accessibility. It is on for every developer and reviewer agent working in this repo.

Only install it from `DietrichGebert/ponytail`. The benchmark numbers in its README are self-reported.

## Setup

It's enabled for the project in [`.claude/settings.json`](../../.claude/settings.json):

- `extraKnownMarketplaces.ponytail`: the GitHub marketplace `DietrichGebert/ponytail`
- `enabledPlugins["ponytail@ponytail"]: true`

On a new machine:

1. Put Node.js on the PATH of Claude Code's non-interactive shell, because the plugin's hooks run `node`. Check it with `node --version` from the Bash tool. Without Node the skills still work, but each hook prints `node: command not found`.
2. Open Claude Code in the repo and trust the folder. Accept the prompt to add the `ponytail` marketplace and install the plugin. If no prompt appears, run these as **two separate prompts**:
   ```
   /plugin marketplace add DietrichGebert/ponytail
   ```
   ```
   /plugin install ponytail@ponytail
   ```
3. Start a fresh session and run `/ponytail`. It should report the level (`full`).

The install may also ask for the plugin's `userConfig`. Keep the defaults: the **ledger** stays on and writes one local CSV row per task (cost, turns, tokens) to `~/.config/ponytail/band/<project>.csv`. Leave **webhook URL** empty so nothing leaves the machine.

## Mode

Agents run at the default level, `full`. Nothing needs to be set, so every machine and cloud session behaves the same.

To change it, there are two ways (highest priority first):

- `PONYTAIL_DEFAULT_MODE` (`off` / `lite` / `full` / `ultra`): commit it under `env` in `.claude/settings.json` to change it for the whole repo.
- `defaultMode` in the per-machine config file `%APPDATA%\ponytail\config.json` on Windows (`~/.config/ponytail/config.json` elsewhere). This is not in the repo, so it only changes one machine.

In a session, `/ponytail lite|full|ultra` switches the level, and `stop ponytail` turns it off.

## What it runs

Three Node hooks plus a band module:

- **SessionStart** injects the ruleset and a short codebase map.
- **SubagentStart** injects the ruleset into every subagent, including the reviewer agent.
- **UserPromptSubmit** tracks `/ponytail` mode switches.
- **band** writes the local ledger.

It also offers once to set up a status-line badge in your user `settings.json`. Saying no is fine.

## Uninstall

Order matters: the cleanup script lives inside the plugin, so run it first.

1. From the installed plugin directory (under `~/.claude/plugins/`), run `node scripts/uninstall.js`. It removes the mode flags, the config file, the status-line script and the `statusLine` entry ponytail added.
2. `/plugin remove ponytail`
3. Remove the `ponytail` entries from `.claude/settings.json`, or the next session will offer to install it again.
