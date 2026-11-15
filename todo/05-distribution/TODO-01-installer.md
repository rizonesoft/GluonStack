---
schema_version: 1
id: installer
domain: 05-distribution
status: active
title: "TODO-01 -- Installer"
depends_on: ["webapp-installer", "control-settings-backup-updates", "control-settings-reliability", "web-dashboard-design", "design-contract", "mariadb-multi-version"]
---

# TODO-01 -- Installer

> **Goal:** One command builds a signed-ready installer from the tracked script and the manifest: it checks the machine, installs the chosen components, registers the services and uninstalls without taking the user's data.

> **Current state:** Measured 2026-11-15. `distribution/IsotoneStack.iss`, `distribution/Build-Installer.bat` and `distribution/InnoDependencyInstaller/` exist on disk but `.gitignore` ignores `/distribution`, so none is under version control. The script hardcodes component versions and the old names, references `iso-control\assets\isotone.ico` (deleted 2026-11-15), and offers a selectable component page.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: installer source, default folder and the explicit script list.
- `docs/design/SPEC.md` section 9 and `assets/brand/installer/`.
- D01 T01: the manifest every version comes from.

## Outcome

- `pwsh installer/Build-Installer.ps1` writes `GluonStack-<version>-Setup.exe` and its `.sha256`; installing it on a clean Windows machine ends with the control panel running and every chosen service started.

**Adjacency:** list=not-applicable (an installer has no such surface); document=not-applicable (an installer has no such surface); settings=applicable @ D05 T01 §3; reporting=not-applicable (an installer has no such surface); notifications=not-applicable (an installer has no such surface); permissions=applicable @ D05 T01 §2; audit=not-applicable (an installer has no such surface); exchange=not-applicable (an installer has no such surface); reverse=applicable @ D05 T01 §5

**Adjacency rationale:** Its settings are the wizard's pages; the reverse of install is uninstall with data kept; the permission is the administrator requirement and the refusal on a busy port.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Installer source tracked under installer/ | -- | [ ] |
| 2 | §2 | Versions from the manifest and pre-install checks | §1 | [ ] |
| 3 | §3 | Wizard pages: location, components, ports | §2 | [ ] |
| 4 | §4 | Post-install: configure, register, verify, open | §3 | [ ] |
| 5 | §5 | Uninstall that keeps the user's data | §4 | [ ] |
| 6 | §6 | Build script with checksum | §5 | [ ] |

## 1. Installer source tracked under installer/

The installer's source must be in the repository before anything else about it can be reviewed.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Copy `distribution/IsotoneStack.iss` to `installer/GluonStack.iss` and `distribution/InnoDependencyInstaller/CodeDependencies.iss` with its licence to `installer/deps/`, and add them to git. Done when: `git ls-files installer` lists them.
2. Rename every product name, path, service and icon reference in the script to the GluonStack names and `assets\brand\gluonstack.ico`. Done when: `git grep -n -i isotone -- installer` prints nothing.
3. Replace `[Files]` entries that take `scripts\*` with an explicit list of product scripts and modules. Done when: no `.py` file and no `scripts\tests` path is in the built installer.
4. Set the wizard images to `assets\brand\installer\wizard-banner.bmp` and `wizard-small.bmp` with their `@2x` forms. Done when: the wizard shows the mark.

- [ ] Copy `distribution/IsotoneStack.iss` to `installer/GluonStack.iss` and `distribution/InnoDependencyInstaller/CodeDependencies.iss` with its licence to `installer/deps/`, and add them to git. Done when: `git ls-files installer` lists them.
- [ ] Rename every product name, path, service and icon reference in the script to the GluonStack names and `assets\brand\gluonstack.ico`. Done when: `git grep -n -i isotone -- installer` prints nothing.
- [ ] Replace `[Files]` entries that take `scripts\*` with an explicit list of product scripts and modules. Done when: no `.py` file and no `scripts\tests` path is in the built installer. Cheaper substitute: an exclusion list that the next new tool file slips past.
- [ ] Set the wizard images to `assets\brand\installer\wizard-banner.bmp` and `wizard-small.bmp` with their `@2x` forms. Done when: the wizard shows the mark.
- [ ] Commit: `installer: tracked GluonStack.iss`

**Test checkpoint:** `git ls-files installer/GluonStack.iss` prints the path and `git grep -c -i isotone -- installer` prints nothing.

## 2. Versions from the manifest and pre-install checks

No version is typed into the installer, and a machine that cannot run the stack is told why before anything is copied.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Generate `installer/version.iss` from `config/components.json` and the control panel's assembly version in the build script, and include it. Done when: component descriptions show the manifest's versions.
2. In `InitializeSetup`, check ports 80, 443, 3306, 5432, 1025 and 8025 and name the process holding a busy one, offering to continue. Done when: with port 80 taken the wizard names the process.
3. Detect XAMPP, WampServer and Laragon services and warn that they use the same ports. Done when: a machine with XAMPP's Apache service gets the warning.
4. Require administrator rights and 64-bit Windows 10 or later; state the real disk space needed. Done when: a 32-bit or older system is refused with the reason.

- [ ] Generate `installer/version.iss` from `config/components.json` and the control panel's assembly version in the build script, and include it. Done when: component descriptions show the manifest's versions.
- [ ] In `InitializeSetup`, check ports 80, 443, 3306, 5432, 1025 and 8025 and name the process holding a busy one, offering to continue. Done when: with port 80 taken the wizard names the process.
- [ ] Detect XAMPP, WampServer and Laragon services and warn that they use the same ports. Done when: a machine with XAMPP's Apache service gets the warning.
- [ ] Require administrator rights and 64-bit Windows 10 or later; state the real disk space needed. Done when: a 32-bit or older system is refused with the reason.
- [ ] Commit: `installer: manifest versions and pre-install checks`

**Test checkpoint:** `pwsh installer/Build-Installer.ps1 -VersionOnly` writes `installer/version.iss` whose versions equal the manifest's.

## 3. Wizard pages: location, components, ports

The pages of the design contract.

**Phase:** 5
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` section 9 and `docs/design/reference/other-surfaces.dc.html` (Installer).
**Job:** Choose where the stack goes, which servers it includes and which ports it uses.
**Treatment:** The wizard keeps the system look; the images are from `assets/brand/installer/` and the wording from the contract.
**Chrome:** The Inno Setup wizard window.

**Build order:**

1. Default the folder to `C:\GluonStack` and refuse a path with spaces or non-ASCII characters, which Apache and MariaDB mishandle, saying why. Done when: such a path cannot be accepted.
2. Make Apache, PHP and the control panel fixed and MariaDB, PostgreSQL and Mailpit selectable, on by default. Done when: an install without PostgreSQL has no `postgresql` folder and no service.
3. Add the Ports page: each port editable, checked as typed, written to the configuration the configure script reads. Done when: an install on port 8080 serves on 8080.
4. Word every page as section 9 and section 5 give it. Done when: page titles are sentence case and match the contract.

- [ ] Default the folder to `C:\GluonStack` and refuse a path with spaces or non-ASCII characters, which Apache and MariaDB mishandle, saying why. Done when: such a path cannot be accepted.
- [ ] Make Apache, PHP and the control panel fixed and MariaDB, PostgreSQL and Mailpit selectable, on by default. Done when: an install without PostgreSQL has no `postgresql` folder and no service.
- [ ] Add the Ports page: each port editable, checked as typed, written to the configuration the configure script reads. Done when: an install on port 8080 serves on 8080.
- [ ] Word every page as section 9 and section 5 give it. Done when: page titles are sentence case and match the contract.
- [ ] Commit: `installer: location, components and ports pages`

**Test checkpoint:** A silent install with `/COMPONENTS="core,mariadb" /DIR=C:\GluonStackTest` creates no `postgresql` folder and registers no `GluonPostgreSQL` service.

## 4. Post-install: configure, register, verify, open

The install is done when the stack runs, not when the files are copied.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Run `Configure-GluonStack.ps1`, the database initialisations and `Register-Services.ps1` from `[Run]`, with each step named on the progress page. Done when: the services exist after install.
2. Verify the critical files and that each chosen service starts; on failure show the step and the log path instead of finishing as if all was well. Done when: a failed MariaDB initialisation is reported on the last page.
3. Offer `open the control panel` on the Done page, checked. Done when: finishing opens the control panel.
4. Run `Migrate-FromIsotone.ps1` when an Isotone install is detected in the chosen folder. Done when: an upgrade over the old name keeps its databases and sites.

- [ ] Run `Configure-GluonStack.ps1`, the database initialisations and `Register-Services.ps1` from `[Run]`, with each step named on the progress page. Done when: the services exist after install.
- [ ] Verify the critical files and that each chosen service starts; on failure show the step and the log path instead of finishing as if all was well. Done when: a failed MariaDB initialisation is reported on the last page. Cheaper substitute: ignoring the exit codes of `[Run]` entries.
- [ ] Offer `open the control panel` on the Done page, checked. Done when: finishing opens the control panel.
- [ ] Run `Migrate-FromIsotone.ps1` when an Isotone install is detected in the chosen folder. Done when: an upgrade over the old name keeps its databases and sites.
- [ ] Commit: `installer: post-install steps`

**Test checkpoint:** After a silent install, `Get-Service Gluon*` lists a running service per chosen component.

## 5. Uninstall that keeps the user's data

Removing the product must not remove someone's databases and sites by surprise.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Stop and unregister every `Gluon*` service before files are removed, with a timeout and a forced stop. Done when: uninstall never fails on a file in use.
2. Ask what to keep: `www`, database data folders, `backups`, `config`, each kept by default. Done when: an uninstall with the defaults leaves those four.
3. Remove the hosts file block the application owns and the current user's Run key. Done when: no trace is left in either.
4. Remove the trusted self-signed certificates the application added. Done when: the user's certificate store holds none of them.

- [ ] Stop and unregister every `Gluon*` service before files are removed, with a timeout and a forced stop. Done when: uninstall never fails on a file in use.
- [ ] Ask what to keep: `www`, database data folders, `backups`, `config`, each kept by default. Done when: an uninstall with the defaults leaves those four.
- [ ] Remove the hosts file block the application owns and the current user's Run key. Done when: no trace is left in either.
- [ ] Remove the trusted self-signed certificates the application added. Done when: the user's certificate store holds none of them.
- [ ] Commit: `installer: uninstall keeps data`

**Test checkpoint:** After a silent uninstall, `C:\GluonStackTest\www` still exists and `Get-Service Gluon*` lists nothing.

## 6. Build script with checksum

One command, the same on a developer machine and in CI.

**Phase:** 5
**Needs:** none
**Surface:** no

**Build order:**

1. Create `installer/Build-Installer.ps1`: publish the control panel (`dotnet publish -c Release -r win-x64`), fetch any missing component through the updater, generate `version.iss`, run `ISCC.exe`. Done when: it writes `installer/output/GluonStack-<version>-Setup.exe`.
2. Write `<file>.sha256` beside the installer. Done when: the hash matches `Get-FileHash`.
3. Fail with the fix when Inno Setup is not installed. Done when: without `ISCC.exe` it names the download.
4. Delete `distribution/Build-Installer.bat`'s role from the documentation; the ignored `distribution/` folder is no longer a source of anything. Done when: no tracked file refers to `distribution/`.

- [ ] Create `installer/Build-Installer.ps1`: publish the control panel (`dotnet publish -c Release -r win-x64`), fetch any missing component through the updater, generate `version.iss`, run `ISCC.exe`. Done when: it writes `installer/output/GluonStack-<version>-Setup.exe`.
- [ ] Write `<file>.sha256` beside the installer. Done when: the hash matches `Get-FileHash`.
- [ ] Fail with the fix when Inno Setup is not installed. Done when: without `ISCC.exe` it names the download.
- [ ] Delete `distribution/Build-Installer.bat`'s role from the documentation; the ignored `distribution/` folder is no longer a source of anything. Done when: no tracked file refers to `distribution/`.
- [ ] Commit: `installer: build script and checksum`

**Test checkpoint:** `pwsh installer/Build-Installer.ps1` exits 0 and `installer/output/*.sha256` matches the built file.
## Verification

- On a clean Windows virtual machine the installer installs, the control panel starts every chosen service, and uninstall leaves `www`, data, backups and config.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
