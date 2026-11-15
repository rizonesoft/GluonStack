---
schema_version: 1
id: quality-gates
domain: 00-foundation
status: active
title: "TODO-03 -- One gate command and CI"
depends_on: ["dotnet-11"]
---

# TODO-03 -- One gate command and CI

> **Goal:** One command runs every check a section must pass, and CI runs the same command on each push.

> **Current state:** Measured 2026-11-15. No gate exists. The 39 product scripts under `scripts/` have never been linted. There is no `.github/` folder. The Conclave kit's own tests are in `scripts/tests/` (Python).

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: the gate section.
- `scripts/todo-graph.py` and `scripts/tests/`: the kit's checks the gate also runs.

## Outcome

- `pwsh scripts/check-all.ps1` exits 0 on a clean tree and non-zero when any one check fails, naming it.
- A push to `main` runs the same command on `windows-latest`.

**Adjacency:** all=not-applicable (developer tooling with no user-facing record)

**Adjacency rationale:** The gate's only setting is its list of checks, which lives in the script.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | The check-all command | -- | [ ] |
| 2 | §2 | PSScriptAnalyzer and Pester over the product scripts | §1 | [ ] |
| 3 | §3 | CI workflow | §2 | [ ] |

## 1. The check-all command

Sections cite one command instead of five. It runs each check, keeps going after a failure so every fault shows at once, and exits non-zero if any failed.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/check-all.ps1` running `dotnet build GluonStack.slnx -warnaserror`, `dotnet test GluonStack.slnx`, `dotnet format --verify-no-changes`, `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check`. Done when: it prints one PASS or FAIL line per check and a final count.
2. Run the build and test steps through `bosun run --` when `bosun` is on PATH. Done when: with Bosun installed the two steps appear in `bosun` output; without it they run directly.
3. Add `-Only <name>` and `-Skip <name>` switches. Done when: `pwsh scripts/check-all.ps1 -Only todo` runs the two todo checks alone.
4. Document the command in `AGENTS.md` under the verify commands. Done when: `AGENTS.md` names `pwsh scripts/check-all.ps1`.

- [ ] Create `scripts/check-all.ps1` running `dotnet build GluonStack.slnx -warnaserror`, `dotnet test GluonStack.slnx`, `dotnet format --verify-no-changes`, `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check`. Done when: it prints one PASS or FAIL line per check and a final count.
- [ ] Run the build and test steps through `bosun run --` when `bosun` is on PATH. Done when: with Bosun installed the two steps appear in `bosun` output; without it they run directly.
- [ ] Add `-Only <name>` and `-Skip <name>` switches. Done when: `pwsh scripts/check-all.ps1 -Only todo` runs the two todo checks alone.
- [ ] Document the command in `AGENTS.md` under the verify commands. Done when: `AGENTS.md` names `pwsh scripts/check-all.ps1`.
- [ ] Commit: `build: check-all.ps1 gate`

**Test checkpoint:** `pwsh scripts/check-all.ps1` exits 0, and exits 1 naming `build` after a syntax error is added to any `.cs` file.

## 2. PSScriptAnalyzer and Pester over the product scripts

The product is mostly PowerShell and none of it is checked. Real defects are fixed; a rule that does not fit the project is turned off in the settings file with its reason.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Add `scripts/PSScriptAnalyzerSettings.psd1` with the default rules and the exclusions the script conventions require (for example `PSAvoidUsingWriteHost`), each with a comment. Done when: `Invoke-ScriptAnalyzer -Path scripts -Recurse -Settings scripts/PSScriptAnalyzerSettings.psd1` runs.
2. Fix every Error and Warning it reports in `scripts/**/*.ps1` at the line that causes it. Done when: the same command returns no Error or Warning.
3. Add an `analyze` check to `scripts/check-all.ps1`, installing PSScriptAnalyzer for the current user when it is missing. Done when: the gate fails when an unused variable is added to a script.
4. Add a `pester` check that runs `scripts/tests/*.Tests.ps1`. Done when: the gate runs `Migrate-FromIsotone.Tests.ps1` and fails when a test fails.

- [ ] Add `scripts/PSScriptAnalyzerSettings.psd1` with the default rules and the exclusions the script conventions require (for example `PSAvoidUsingWriteHost`), each with a comment. Done when: `Invoke-ScriptAnalyzer -Path scripts -Recurse -Settings scripts/PSScriptAnalyzerSettings.psd1` runs.
- [ ] Fix every Error and Warning it reports in `scripts/**/*.ps1` at the line that causes it. Done when: the same command returns no Error or Warning. Cheaper substitute: `SuppressMessageAttribute` on a script instead of a fix.
- [ ] Add an `analyze` check to `scripts/check-all.ps1`, installing PSScriptAnalyzer for the current user when it is missing. Done when: the gate fails when an unused variable is added to a script.
- [ ] Add a `pester` check that runs `scripts/tests/*.Tests.ps1`. Done when: the gate runs `Migrate-FromIsotone.Tests.ps1` and fails when a test fails.
- [ ] Commit: `build: PSScriptAnalyzer and Pester in the gate`

**Test checkpoint:** `pwsh scripts/check-all.ps1 -Only analyze,pester` exits 0.

## 3. CI workflow

The same gate runs on every push and pull request so a red tree is seen without a local run.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `.github/workflows/ci.yml` on `windows-latest`: checkout, `actions/setup-dotnet` from `global.json`, `actions/setup-python`, then `pwsh scripts/check-all.ps1`. Done when: the workflow file passes `actionlint` or GitHub's own parse on push.
2. Cache NuGet packages keyed on `Directory.Packages.props`. Done when: a second run restores from cache.
3. Pin each action to a full commit SHA with its version in a comment. Done when: no `uses:` line ends in a tag or branch.

- [ ] Create `.github/workflows/ci.yml` on `windows-latest`: checkout, `actions/setup-dotnet` from `global.json`, `actions/setup-python`, then `pwsh scripts/check-all.ps1`. Done when: the workflow file passes `actionlint` or GitHub's own parse on push.
- [ ] Cache NuGet packages keyed on `Directory.Packages.props`. Done when: a second run restores from cache.
- [ ] Pin each action to a full commit SHA with its version in a comment. Done when: no `uses:` line ends in a tag or branch.
- [ ] Commit: `ci: run check-all on push and pull request`

**Test checkpoint:** `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))"` exits 0 and `git grep -n -E 'uses: .*@v[0-9]' -- .github` prints nothing.
## Verification

- `pwsh scripts/check-all.ps1` exits 0 on a clean clone with the .NET 11 SDK, Python 3 and PowerShell 7.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
