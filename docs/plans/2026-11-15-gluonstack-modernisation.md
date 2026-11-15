# GluonStack modernisation plan

Written 2026-11-15. This is the governing document for `todo/`: the TODO files execute it and do not restate it. The earlier backlog is kept as `docs/legacy-todo.md`; every open item in it is owned by a section in `todo/` or dropped here with a reason.

## What the owner asked for

1. Bring the project to the point where an unattended campaign can run it to completion.
2. Modernise the tech stack: .NET 11 and the latest C#.
3. Import the relevant Conclave-SDK kits.
4. Add the latest components to the stack (MariaDB, PostgreSQL, PHP and the rest), with a way to update all of them.
5. Put all of it in the TODO system and the plan file.
6. Rename the project to GluonStack.
7. Redesign the resources: icons, interface and everything else.

## Where the repository stood (measured 2026-11-15)

- `iso-control/Isotone.csproj` targets `net9.0-windows` (WPF, MaterialDesignThemes 5.2.1, CommunityToolkit.Mvvm 8.4.0, Newtonsoft.Json) and builds with 0 errors and 20 nullable warnings on the .NET SDK 11.0.100. There is no test project.
- `DatabaseView` and `LogsView` are stubs; several navigation entries open `ComingSoonView`.
- 39 PowerShell and batch scripts in `scripts/` register and control the services `IsotoneApache`, `IsotoneMariaDB` and `IsotoneMailpit` through NSSM. They assume the install root from the script location.
- Component binaries (`apache24`, `php`, `mariadb`, `mailpit`, `phpmyadmin`, `pwsh`, `bin`) are ignored by git and live only on the developer machine. Their versions are written by hand in `README.md`. Nothing records where a binary came from or its checksum.
- `distribution/` is ignored as a whole, so the installer script `distribution/IsotoneStack.iss` and `distribution/Build-Installer.bat` are not under version control.
- There is no CI, no changelog and no release.

## Decisions

Each is the owner's, or taken here as the conventional option. Reversing any of them is a rename or a setting, except where noted.

| Subject | Decision |
| ------- | -------- |
| Product name | GluonStack |
| Control panel folder and project | `gluon-control/`, `GluonStack.Control.csproj`, assembly and exe `GluonStack`, root namespace `GluonStack` |
| Test project | `gluon-control.tests/GluonStack.Control.Tests.csproj`, xUnit |
| Solution | `GluonStack.slnx` at the repository root |
| Windows services | `GluonApache`, `GluonMariaDB`, `GluonPostgreSQL`, `GluonMailpit` |
| Default install folder | `C:\GluonStack` (scripts still derive the root from their own location) |
| Settings file | `config/gluonstack-settings.json` |
| Script log folder | `logs\gluonstack` |
| Renamed scripts | `Configure-GluonStack`, `Set-GluonStackSettings` |
| Existing installs | `scripts/Migrate-FromIsotone.ps1` unregisters the `Isotone*` services, registers the `Gluon*` ones on the same data, and moves the settings file. Data folders are never moved or deleted. |
| Framework | `net11.0-windows`, `LangVersion` latest, nullable and warnings as errors |
| JSON | `System.Text.Json` with source generation; Newtonsoft.Json removed |
| UI toolkit | WPF stays. MaterialDesignThemes is removed in Phase 2: the chosen design is flat, square and monospace, and is built from the project's own resource dictionaries and tokens. |
| Design | `docs/design/direction.md`: the G mark from direction B, the colours and layout of direction C |
| Components | One manifest, `config/components.json`, is the only place a version, a download source and a checksum are written |
| New components | PostgreSQL (latest stable major), Composer, Node.js (current LTS). Adminer is the PostgreSQL web client. |
| Not added | pgAdmin (a second Python runtime for what Adminer already does), Redis or Valkey (no upstream Windows build to pin) |
| Versions | Never written into a TODO. "Latest" means what `scripts/Update-Components.ps1 -Check` resolves from the upstream feed on the day a section runs, recorded in the manifest with its checksum. |
| Service wrapper | NSSM stays for Mailpit only. Apache, MariaDB and PostgreSQL register through their own service support. |
| Installer source | Moved out of the ignored `distribution/` folder to a tracked `installer/` folder |
| Agent tooling in `scripts/` | The Conclave kit's Python files share `scripts/` with the product's PowerShell. The installer ships an explicit list of product scripts, never the folder. |
| Repository folder and GitHub repository name | Left as they are (`D:\IsotoneStack`, the existing remote). Renaming either is the operator's, in phase 99. |

## The update mechanism

`config/components.json` lists each component with its id, installed version, folder, upstream feed, download URL pattern and SHA-256. Three things read it:

- `scripts/Update-Components.ps1` (the product, shipped): `-Check` lists what is behind, `-Component <id>` updates one, `-All` updates every component. An update downloads to a staging folder, verifies the checksum, stops the service, keeps the previous folder as a rollback, swaps, starts the service and proves it answers. A database server is dumped before it is touched. A failed step puts the previous folder back.
- The control panel's Updates entry and its `update all` command call the same script and show its progress.
- `scripts/component-drift.py` (the repository, never shipped): compares the manifest with upstream and appends one line per stale component to `todo/findings.md`, so a version that fell behind becomes scheduled work through `add-todo`.

## Phases

| Phase | Name | Delivers |
| ----- | ---- | -------- |
| 0 | Repository and tooling | The rename, .NET 11, a test project, one gate command, CI |
| 1 | Component platform | The manifest, the updater, PostgreSQL, Composer, Node.js, every component at its latest, MariaDB multi-version |
| 2 | Design system | The design spec and tokens, the icon set, the control panel shell, splash, tray, web dashboard |
| 3 | Control panel features | Databases, logs, sites, service settings, backup, updates, settings, reliability |
| 4 | Web application installer | Recipes, the script, WordPress and Laravel, the new-project flows |
| 5 | Installer and distribution | The tracked installer, pre-install checks, uninstall, checksums |
| 6 | Documentation and release | README, community files, user guides, the release workflow |
| 99 | Manual, operator only | Renaming the folder and the GitHub repository, publishing the first release, code signing |

## The gate

`pwsh scripts/check-all.ps1` is the one command a section runs before review (built in D00 T03 §1): `dotnet build` with warnings as errors, `dotnet test`, PSScriptAnalyzer over the product scripts, `python scripts/todo-graph.py validate` and `plan --check`. Full builds and test runs go through `bosun run --` where Bosun is installed.

## Dropped from the legacy backlog

- "Import each database from migration-ready backups to 10.11" and its two neighbours: a one-off migration of the owner's own data, not product work.
- `.github/FUNDING.yml` and `CODE_OF_CONDUCT.md`: not wanted until the project takes outside contributions.
- "Add LICENSE headers to all scripts": the repository's `LICENSE` covers them.
- Light theme and accent colour customisation: the chosen direction has one theme and one accent.
- Function-key shortcuts, breadcrumb navigation, the quick action bar and statistics cards: replaced by the chosen design's command bar, list and fact cards (`docs/design/SPEC.md` section 6).
- "Make all components mandatory" in the installer: reversed. Apache, PHP and the control panel are fixed; the database servers and Mailpit are selectable (`docs/design/SPEC.md` section 9).

## Running the campaign

`pwsh scripts/start-campaign.ps1` starts an interactive Claude Code session in this checkout with its goal set to finishing `todo/implementation-plan.md` through the `process-plan` skill; `-Runner agy` starts it in Antigravity. `-InstallShortcut` puts "GluonStack Claude campaign" and "GluonStack Carbon campaign" on the desktop, and `-DryRun` prints what would run. A run starts only when the operator starts it: closing its window, a crash or a reboot ends it, and nothing restarts it.
