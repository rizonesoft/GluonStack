---
schema_version: 1
id: rename-gluonstack
domain: 00-foundation
status: active
title: "TODO-01 -- Rename to GluonStack"
---

# TODO-01 -- Rename to GluonStack

> **Goal:** Every tracked file, project, service, script and setting carries the GluonStack names in the plan's decisions table, and an existing Isotone install can be moved over without touching its data.

> **Current state:** Measured 2026-11-15. The product is named IsotoneStack throughout: `iso-control/Isotone.csproj` (namespace `Isotone`, 50 tracked files), the services `IsotoneApache`, `IsotoneMariaDB` and `IsotoneMailpit` in `scripts/Register-Services.ps1`, `config/isotone-settings.json`, `scripts/Configure-IsotoneStack.ps1`, `scripts/Set-IsotoneSettings.ps1`, the log folder `logs\isotone`, and the text of `README.md`, `INSTALL.bat`, `default/` and `config/`. A count on 2026-11-15 found the name in 60 tracked files.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: the decisions table gives every new name.
- `git grep -il isotone` and `git ls-files | grep -i -E 'isotone|iso-control'`: the full list of files and paths to change.

## Outcome

- `git grep -i isotone` returns only `docs/legacy-todo.md`, the plan, `scripts/Migrate-FromIsotone.ps1` and its documentation.
- The control panel builds as `GluonStack.exe` and the scripts register `Gluon*` services.

**Adjacency:** all=not-applicable (a rename: no record a user lists, exports or is notified of; the one reversible act, the service migration, is covered by its own section)

**Adjacency rationale:** The migration script is the only part with a user-visible effect, and its refusal and rollback paths are §5's own steps.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Control panel project, folder and namespace rename | -- | [ ] |
| 2 | §2 | Service names, settings file and log folder in scripts | §1 | [ ] |
| 3 | §3 | Renamed product scripts and their launchers | §2 | [ ] |
| 4 | §4 | Web dashboard, configuration templates and documentation text | §3 | [ ] |
| 5 | §5 | Migration script for existing Isotone installs | §2 | [ ] |
| 6 | §6 | Agent documents describing GluonStack | §4 | [ ] |

## 1. Control panel project, folder and namespace rename

The control panel is the largest block of the old name. It moves as one commit so the tree never holds a half-renamed project.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Move the folder with `git mv iso-control gluon-control` and the project with `git mv gluon-control/Isotone.csproj gluon-control/GluonStack.Control.csproj`. Done when: `git status --short` shows only renames under `gluon-control/`.
2. Set `AssemblyName` and `RootNamespace` to `GluonStack` and `StartupObject` to `GluonStack.App` in `gluon-control/GluonStack.Control.csproj`. Done when: `dotnet build gluon-control` writes `GluonStack.exe`.
3. Replace the namespace `Isotone` with `GluonStack` in every `.cs` and `.xaml` file under `gluon-control/`, including `x:Class` and `clr-namespace` values. Done when: `git grep -n 'Isotone' -- gluon-control` returns nothing and the build has 0 errors.
4. Delete `gluon-control/Isotone.sln`; the root solution is D00 T02 §1's. Done when: the file is gone and `dotnet build gluon-control/GluonStack.Control.csproj` still succeeds.
5. Update `/iso-control/` patterns in `.gitignore` to `/gluon-control/`. Done when: `git status --short` lists no `bin` or `obj` path after a build.

- [ ] Move the folder with `git mv iso-control gluon-control` and the project with `git mv gluon-control/Isotone.csproj gluon-control/GluonStack.Control.csproj`. Done when: `git status --short` shows only renames under `gluon-control/`. Cheaper substitute: copying the folder, which loses file history.
- [ ] Set `AssemblyName` and `RootNamespace` to `GluonStack` and `StartupObject` to `GluonStack.App` in `gluon-control/GluonStack.Control.csproj`. Done when: `dotnet build gluon-control` writes `GluonStack.exe`.
- [ ] Replace the namespace `Isotone` with `GluonStack` in every `.cs` and `.xaml` file under `gluon-control/`, including `x:Class` and `clr-namespace` values. Done when: `git grep -n 'Isotone' -- gluon-control` returns nothing and the build has 0 errors. Cheaper substitute: a `using` alias that leaves the old namespace in place.
- [ ] Delete `gluon-control/Isotone.sln`; the root solution is D00 T02 §1's. Done when: the file is gone and `dotnet build gluon-control/GluonStack.Control.csproj` still succeeds.
- [ ] Update `/iso-control/` patterns in `.gitignore` to `/gluon-control/`. Done when: `git status --short` lists no `bin` or `obj` path after a build.
- [ ] Commit: `rename: control panel project to GluonStack.Control`

**Test checkpoint:** `dotnet build gluon-control/GluonStack.Control.csproj -c Debug` ends with `0 Error(s)` and `git grep -c Isotone -- gluon-control` prints nothing.

## 2. Service names, settings file and log folder in scripts

The scripts name the Windows services, the settings file and the log folder in many places. One shared definition replaces the repeats so the next rename is one line.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Add `scripts/GluonStack.Common.psm1` exporting `Get-GluonServiceNames`, `Get-GluonRoot`, `Get-GluonSettingsPath` and `Write-Log`, with the names from the plan's decisions table. Done when: `Import-Module scripts/GluonStack.Common.psm1; (Get-GluonServiceNames).Apache` prints `GluonApache`.
2. Replace each literal `Isotone*` service name in `scripts/*.ps1` and `scripts/**/*.ps1` with a call to `Get-GluonServiceNames`. Done when: `git grep -n -E 'Isotone(Apache|MariaDB|Mailpit)' -- scripts` returns only `Migrate-FromIsotone.ps1`.
3. Rename `config/isotone-settings.json` to `config/gluonstack-settings.json` with `git mv` and point every reader at `Get-GluonSettingsPath`. Done when: `git grep -n isotone-settings` returns nothing outside the migration script.
4. Change the script log folder from `logs\isotone` to `logs\gluonstack` in `Write-Log` and in `scripts/_Template.ps1`. Done when: running `scripts/Start-Services.ps1 -WhatIf` writes its log under `logs\gluonstack`.
5. Update `gluon-control/Services/ServiceManager.cs` and `gluon-control/Utilities/ConfigurationManager.cs` to the new service names and settings path. Done when: `git grep -n -i isotone -- gluon-control` returns nothing.

- [ ] Add `scripts/GluonStack.Common.psm1` exporting `Get-GluonServiceNames`, `Get-GluonRoot`, `Get-GluonSettingsPath` and `Write-Log`, with the names from the plan's decisions table. Done when: `Import-Module scripts/GluonStack.Common.psm1; (Get-GluonServiceNames).Apache` prints `GluonApache`.
- [ ] Replace each literal `Isotone*` service name in `scripts/*.ps1` and `scripts/**/*.ps1` with a call to `Get-GluonServiceNames`. Done when: `git grep -n -E 'Isotone(Apache|MariaDB|Mailpit)' -- scripts` returns only `Migrate-FromIsotone.ps1`. Cheaper substitute: a search and replace that leaves each script with its own copy of the names.
- [ ] Rename `config/isotone-settings.json` to `config/gluonstack-settings.json` with `git mv` and point every reader at `Get-GluonSettingsPath`. Done when: `git grep -n isotone-settings` returns nothing outside the migration script.
- [ ] Change the script log folder from `logs\isotone` to `logs\gluonstack` in `Write-Log` and in `scripts/_Template.ps1`. Done when: running `scripts/Start-Services.ps1 -WhatIf` writes its log under `logs\gluonstack`.
- [ ] Update `gluon-control/Services/ServiceManager.cs` and `gluon-control/Utilities/ConfigurationManager.cs` to the new service names and settings path. Done when: `git grep -n -i isotone -- gluon-control` returns nothing.
- [ ] Commit: `rename: Gluon service names, settings file and log folder`

**Test checkpoint:** `pwsh -NoProfile -Command "Import-Module ./scripts/GluonStack.Common.psm1; (Get-GluonServiceNames).Values -join ','"` prints `GluonApache,GluonMariaDB,GluonPostgreSQL,GluonMailpit` in that order.

## 3. Renamed product scripts and their launchers

Two scripts carry the old product name in their file names, and every batch launcher prints it.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Rename `scripts/Configure-IsotoneStack.ps1` and `.bat` to `Configure-GluonStack` with `git mv`. Done when: `git ls-files scripts | grep -i isotone` lists only the migration script.
2. Rename `scripts/Set-IsotoneSettings.ps1` and `.bat` to `Set-GluonStackSettings` with `git mv`. Done when: both new files exist and the old names are gone.
3. Update every caller of the two scripts in `scripts/`, `INSTALL.bat` and `gluon-control/`. Done when: `git grep -n -E 'Configure-IsotoneStack|Set-IsotoneSettings'` returns nothing.
4. Replace the product name in the banner and message text of every `scripts/*.bat` and `INSTALL.bat`. Done when: `git grep -n -i isotone -- '*.bat'` returns nothing.

- [ ] Rename `scripts/Configure-IsotoneStack.ps1` and `.bat` to `Configure-GluonStack` with `git mv`. Done when: `git ls-files scripts | grep -i isotone` lists only the migration script.
- [ ] Rename `scripts/Set-IsotoneSettings.ps1` and `.bat` to `Set-GluonStackSettings` with `git mv`. Done when: both new files exist and the old names are gone.
- [ ] Update every caller of the two scripts in `scripts/`, `INSTALL.bat` and `gluon-control/`. Done when: `git grep -n -E 'Configure-IsotoneStack|Set-IsotoneSettings'` returns nothing.
- [ ] Replace the product name in the banner and message text of every `scripts/*.bat` and `INSTALL.bat`. Done when: `git grep -n -i isotone -- '*.bat'` returns nothing.
- [ ] Commit: `rename: Configure-GluonStack and Set-GluonStackSettings`

**Test checkpoint:** `git grep -l -i isotone -- scripts INSTALL.bat` prints only `scripts/Migrate-FromIsotone.ps1` once §5 exists, and nothing before it.

## 4. Web dashboard, configuration templates and documentation text

The remaining uses of the old name are text: the PHP dashboard under `default/`, configuration templates and Markdown.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Replace the product name in `default/index.php` and every file under `default/control/`. Done when: `git grep -n -i isotone -- default` returns nothing.
2. Rename `config/apache/extra/httpd-isotone-default.conf` to `httpd-gluonstack-default.conf` and update its `Include` line in `config/apache/httpd.conf`. Done when: `httpd -t` against the configured tree reports `Syntax OK`.
3. Replace the name and the default path `C:\isotone` with `C:\GluonStack` in `config/**` comments and templates. Done when: `git grep -n -i isotone -- config` returns nothing.
4. Replace the name in `README.md`, `gluon-control/ERROR_HANDLING.md` and `.agent/`. Done when: `git grep -l -i isotone` prints only `docs/legacy-todo.md`, the plan and the migration script.

- [ ] Replace the product name in `default/index.php` and every file under `default/control/`. Done when: `git grep -n -i isotone -- default` returns nothing.
- [ ] Rename `config/apache/extra/httpd-isotone-default.conf` to `httpd-gluonstack-default.conf` and update its `Include` line in `config/apache/httpd.conf`. Done when: `httpd -t` against the configured tree reports `Syntax OK`. Cheaper substitute: leaving the old file name behind an extra `Include`.
- [ ] Replace the name and the default path `C:\isotone` with `C:\GluonStack` in `config/**` comments and templates. Done when: `git grep -n -i isotone -- config` returns nothing.
- [ ] Replace the name in `README.md`, `gluon-control/ERROR_HANDLING.md` and `.agent/`. Done when: `git grep -l -i isotone` prints only `docs/legacy-todo.md`, the plan and the migration script.
- [ ] Commit: `rename: dashboard, config templates and docs text`

**Test checkpoint:** `git grep -l -i isotone -- . ':!docs' ':!scripts/Migrate-FromIsotone.ps1'` prints nothing.

## 5. Migration script for existing Isotone installs

A machine that ran the old name has `Isotone*` services registered and a settings file under the old name. The move must keep its databases and sites exactly where they are.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Migrate-FromIsotone.ps1` from `scripts/_Template.ps1`: detect the `Isotone*` services and `config/isotone-settings.json`. Done when: run on a machine with neither, it prints `[OK] Nothing to migrate` and exits 0.
2. Stop and unregister each `Isotone*` service, then call `scripts/Register-Services.ps1` for the `Gluon*` ones on the same data folders. Done when: `Get-Service Gluon*` lists the services and `Get-Service Isotone*` lists none.
3. Copy the old settings file to `config/gluonstack-settings.json` when the new one is absent, and keep the old file as `.migrated`. Done when: the new file holds the old values and the old file still exists under its new suffix.
4. On any failed step, register the `Isotone*` services again and exit 1 with the step named. Done when: a run with `-FailAfter Unregister` (a test switch) leaves the old services registered and running.
5. Add `scripts/Migrate-FromIsotone.bat` with the self-elevation pattern, and `scripts/tests/Migrate-FromIsotone.Tests.ps1` covering nothing-to-migrate and the rollback. Done when: `Invoke-Pester scripts/tests/Migrate-FromIsotone.Tests.ps1` passes and fails when the rollback block is removed.

- [ ] Create `scripts/Migrate-FromIsotone.ps1` from `scripts/_Template.ps1`: detect the `Isotone*` services and `config/isotone-settings.json`. Done when: run on a machine with neither, it prints `[OK] Nothing to migrate` and exits 0.
- [ ] Stop and unregister each `Isotone*` service, then call `scripts/Register-Services.ps1` for the `Gluon*` ones on the same data folders. Done when: `Get-Service Gluon*` lists the services and `Get-Service Isotone*` lists none. Cheaper substitute: renaming the registry key of the service, which leaves its image path wrong.
- [ ] Copy the old settings file to `config/gluonstack-settings.json` when the new one is absent, and keep the old file as `.migrated`. Done when: the new file holds the old values and the old file still exists under its new suffix.
- [ ] On any failed step, register the `Isotone*` services again and exit 1 with the step named. Done when: a run with `-FailAfter Unregister` (a test switch) leaves the old services registered and running.
- [ ] Add `scripts/Migrate-FromIsotone.bat` with the self-elevation pattern, and `scripts/tests/Migrate-FromIsotone.Tests.ps1` covering nothing-to-migrate and the rollback. Done when: `Invoke-Pester scripts/tests/Migrate-FromIsotone.Tests.ps1` passes and fails when the rollback block is removed.
- [ ] Commit: `rename: migration script from Isotone installs`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Migrate-FromIsotone.Tests.ps1 -CI"` reports 0 failed.

## 6. Agent documents describing GluonStack

`AGENTS.md` was installed from the Conclave kit and still asks to be adapted. The older `.agent/` folder holds the script rules every product script must follow.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Move `.agent/rules/core-rules.md` to `docs/script-conventions.md` with `git mv` and link it from `AGENTS.md`. Done when: `AGENTS.md` names the file and the file exists.
2. Delete `.agent/workflows/`, whose four workflows are replaced by the TODO skills. Done when: `git ls-files .agent` prints nothing.
3. Rewrite the project paragraph and the verify commands in `AGENTS.md` for the renamed tree. Done when: every path and command `AGENTS.md` names exists and runs.

- [ ] Move `.agent/rules/core-rules.md` to `docs/script-conventions.md` with `git mv` and link it from `AGENTS.md`. Done when: `AGENTS.md` names the file and the file exists.
- [ ] Delete `.agent/workflows/`, whose four workflows are replaced by the TODO skills. Done when: `git ls-files .agent` prints nothing. Cheaper substitute: leaving two sets of instructions that disagree.
- [ ] Rewrite the project paragraph and the verify commands in `AGENTS.md` for the renamed tree. Done when: every path and command `AGENTS.md` names exists and runs.
- [ ] Commit: `docs: AGENTS.md for the renamed tree`

**Test checkpoint:** `git ls-files .agent` prints nothing and `python scripts/todo-graph.py validate` exits 0.
## Verification

- `git grep -l -i isotone` prints only `docs/legacy-todo.md`, `docs/plans/2026-11-15-gluonstack-modernisation.md`, `scripts/Migrate-FromIsotone.ps1`, its launcher and its test.
- `dotnet build gluon-control/GluonStack.Control.csproj` ends with `0 Error(s)`.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
