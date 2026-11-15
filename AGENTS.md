# AGENTS.md

GluonStack (formerly IsotoneStack) is a portable Windows development stack: Apache, PHP, MariaDB, PostgreSQL and Mailpit, run as Windows services, with a WPF control panel, a web dashboard, PowerShell scripts that configure and control it, and an Inno Setup installer. This repository follows the Conclave-SDK 3-agent conventions.

## The project

- **Governing plan:** [docs/plans/2026-11-15-gluonstack-modernisation.md](./docs/plans/2026-11-15-gluonstack-modernisation.md). It holds the decisions (names, framework, components) every section follows. The live plan is [todo/implementation-plan.md](./todo/implementation-plan.md), generated from the TODO files.
- **Design contract:** [docs/design/SPEC.md](./docs/design/SPEC.md), from the owner's choice in [docs/design/direction.md](./docs/design/direction.md). Every user-facing surface is built against it. Values come from `docs/design/tokens.json` through `python scripts/generate-ui-tokens.py`; icons come from `assets/brand/svg/` through `python scripts/build-brand-assets.py`. Neither generated output is edited by hand.
- **Where the code lives:** the control panel in `iso-control/` (`gluon-control/` once D00 T01 §1 ships), the web dashboard in `default/`, product scripts in `scripts/*.ps1` with their `.bat` launchers, configuration templates in `config/`, brand assets and fonts in `assets/`.
- **Two kinds of file share `scripts/`:** the product's PowerShell, which ships to users and follows [.agent/rules/core-rules.md](./.agent/rules/core-rules.md) (a template, a matching `.bat`, ASCII output, logging), and agent tooling in Python (`todo-graph.py`, `campaign_guard.py`, `review-dispatch.py`, the generators), which never ships.
- **Component binaries are not in git.** `apache24/`, `php/`, `mariadb/`, `mailpit/`, `phpmyadmin/`, `pwsh/` and `bin/` are ignored and exist only on a machine that installed them. A section that needs a running service checks for it and says so when it is absent.
- **Verify:** `dotnet build iso-control/Isotone.csproj` (0 errors) until D00 T02 §1 makes it `dotnet build GluonStack.slnx -warnaserror`; `python scripts/todo-graph.py validate` and `plan --check`; `python scripts/generate-ui-tokens.py --check` and `python scripts/build-brand-assets.py --check`. D00 T03 §1 gathers these into `pwsh scripts/check-all.ps1`. Run full builds and test suites through `bosun run --` where Bosun is installed.
- **Versions are never written from memory.** "Latest" is what the upstream feed reports on the day; D01 T01 builds the resolver and the manifest that records it.

## Autonomy and ambition

The owner's standing directive, binding on every agent and every run in this repository, attended or not.

- **Decide and act.** A task assigned is a task authorised: do it, then report. Never stop to ask a question that the repository, its governing documents or sound engineering judgment already answers.
- **Ask only what cannot be decided here.** Ask before something that cannot be put back (dropping data, creating or exposing a credential, a force-push, deleting outside the repository) or that needs business context the repository lacks. Every other choice is made, recorded with what reversing it would cost, and built. An unattended run never asks: it takes the conventional option and records it in the run file.
- **Heal what breaks.** A red gate, a failed tool, a stalled run or a wrong plan is work, not a stop: find the cause and fix it at its owning layer, with a test that would have caught it.
- **Improve the means as well as the product.** The plan, the gate and the tooling are changed whenever they slow the work or let a defect through.
- **Be the best of its kind.** Measure GluonStack against XAMPP, Laragon, WampServer and Herd, and close what falls short.
- **A person is needed only for what no tool can do.** A row waits on `operator`, `attended` or `owner-decision` only for a business decision the repository cannot make or an act no program can perform.
- **Finish.** Done means the work runs end to end, the checks pass, the documentation matches the code and nothing is left as a placeholder.
- **This machine is the owner's workstation.** Never stop, unregister or reconfigure a Windows service that is not named `Gluon*` or `Isotone*`, never change a port another program holds, and never delete under `www\`, `backups\` or a database data folder.

## Working rules

- Verify files, routes, schemas, tools, and commands before relying on them. A path someone mentions is a hypothesis until it is on disk.
- Inspect existing patterns, imports, the package manager, the framework, and the test commands before editing. Do not infer architecture or tool schemas from memory when the repository can answer.
- Resolve a tool by capability before path. Prefer explicit config, then discovery, then a setup-required state. Store discovered paths only in ignored local config and never hardcode user-specific absolute paths.
- Prefer global or user-level tool installs. Add repo-scoped wrappers only when they encode project-specific behavior or reproducible commands.
- Real data only. Demo or seed data stays behind an explicit demo mode and is labeled as such.
- Run the relevant typecheck, lint, and tests after a change.
- Fix at the owning layer: a setting in its setting, behaviour in the code that produces it, data in the data. No output filters that hide a problem. Code changes end the report with a `Layer:` line.
- Markdown prose is never hard-wrapped: one line per paragraph and per list item. Every Markdown table row stays `<= 120` characters so raw `.md` files never wrap.
- Never use em dashes or en dashes anywhere: prose, code, comments, commit messages and generated files.
- Temporary files and full logs go to scratch, never the repository: `R:\scratch` on Windows, `/mnt/r/scratch` on WSL (the same folder), or the session scratchpad when one is given.

## Safety

- Local reversible work in the repository needs no confirmation.
- Ask the operator once before anything that sends, deletes, or changes something outside the repository: mail, production systems, cloud changes, SQL writes, dropping data, credentials.
- When a command needs sudo, give the operator the exact command to run with `! sudo ...`. Never store the sudo password.
- Never print, log, or commit a secret value.

## Skills

- Antigravity skills live in `.agents/skills/<name>/`, Claude skills in `.claude/skills/<name>/`, and Codex skills in `.codex/skills/<name>/`, all as real files, never symlinks. Change all three together.
- Follow [Agent Skills and Rules Structure](./docs/agent-skills-and-rules-structure.md) before adding or moving skills.
- Name a skill for its capability, not with a project prefix.
- Each agent reads and runs only its own directory (`.agents/` for Antigravity, `.claude/` for Claude Code, `.codex/` for Codex) and never edits another agent's skills unless asked.

## Subagents

- Delegate mechanical subtasks to subagents. Claude subagents pin an explicit `model:`: Sonnet by default, and Opus (with a `model_rationale:`) only where judgment quality needs it.
- Subagents read and run; they never write. Every Claude subagent declares an explicit `tools:` list without Edit, Write, MultiEdit, NotebookEdit or `*`. The main loop makes every change and verifies what subagents return.
- Antigravity uses native `Orchestrator (Carbon)` (`gemini-pro-orchestrator`), which plans on Carbon (`<plan_execute_protocol>`), hands execution to Hydrogen via `exit_plan_mode`, manages its own effort (rejecting `--effort`), and provides built-in subagents (`self`, `research`, `image-generator`) without custom `.agents/agents/*.md` files or wrapper scripts. Codex has no subagent definitions: it runs mechanical subtasks in the main session.
- Haiku is only for near-mechanical work, at least 90% mechanical (read-only lookups, inventories, structural checks), whose output a script or the main loop verifies. Pin `claude-haiku-5-5` or later, declare `mechanical_share:` (90 to 100), point `haiku_replay:` at a record of a known-answer replay that showed no loss against Sonnet, and give it no edit tools. Never use Haiku for review, audit, research, security, debugging, diagnosis, planning or design.
- Run `node scripts/verify-agent-tiers.mjs` after adding or changing a Claude agent definition in `.claude/agents/`; it enforces these rules.

## TODO workflow

Plan and build through the TODO system: [docs/todo-workflow.md](./docs/todo-workflow.md).
