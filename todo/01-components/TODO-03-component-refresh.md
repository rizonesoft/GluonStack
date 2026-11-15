---
schema_version: 1
id: component-refresh
domain: 01-components
status: active
title: "TODO-03 -- Every component at its latest"
depends_on: ["postgresql"]
---

# TODO-03 -- Every component at its latest

> **Goal:** Every bundled component is at the latest stable release its series has, Composer and Node.js are part of the stack, and Apache and MariaDB register as services without NSSM.

> **Current state:** Measured 2026-11-15. Versions as installed are recorded by D01 T01 §1. Composer has an empty `composer/` folder. Node.js is absent. Apache, MariaDB and Mailpit are all registered through NSSM 2.24, which has had no release since 2017.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: components, versions and service wrapper decisions.
- D01 T01: every update here is `scripts/Update-Components.ps1 -Component <id>`, never a manual copy.

## Outcome

- `scripts/Update-Components.ps1 -Check` exits 0.
- `composer --version` and `node --version` answer from the stack's own folders.

**Adjacency:** all=not-applicable (updates through an existing mechanism; the records and reversals are the updater's)

**Adjacency rationale:** Each update's rollback and log are D01 T01's. This file only runs them and fixes what a new version breaks.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Apache at its latest 2.4 release | -- | [ ] |
| 2 | §2 | Every supported PHP series at its latest release | §1 | [ ] |
| 3 | §3 | MariaDB series at their latest releases | §1 | [ ] |
| 4 | §4 | Mailpit, phpMyAdmin, Adminer and phpLiteAdmin at latest | §2 | [ ] |
| 5 | §5 | Composer in the stack | §2 | [ ] |
| 6 | §6 | Node.js LTS in the stack | §1 | [ ] |
| 7 | §7 | Portable PowerShell and the Visual C++ runtime at latest | §1 | [ ] |
| 8 | §8 | Apache and MariaDB as services without NSSM | §3 | [ ] |

## 1. Apache at its latest 2.4 release

Apache first: every other web component is tested through it.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Run `scripts/Update-Components.ps1 -Component apache`. Done when: `apache24\bin\httpd.exe -v` prints the latest release the resolver reports.
2. Fix any directive `httpd -t` now rejects in `config/apache/httpd.conf` and `config/apache/extra/*.conf`. Done when: `httpd -t` prints `Syntax OK`.
3. Load `http2` and enable TLS 1.3 only defaults in the SSL template. Done when: `curl -sI --http2 https://localhost -k` answers over HTTP/2.

- [ ] Run `scripts/Update-Components.ps1 -Component apache`. Done when: `apache24\bin\httpd.exe -v` prints the latest release the resolver reports.
- [ ] Fix any directive `httpd -t` now rejects in `config/apache/httpd.conf` and `config/apache/extra/*.conf`. Done when: `httpd -t` prints `Syntax OK`. Cheaper substitute: commenting out the module that fails to load.
- [ ] Load `http2` and enable TLS 1.3 only defaults in the SSL template. Done when: `curl -sI --http2 https://localhost -k` answers over HTTP/2.
- [ ] Commit: `components: Apache at latest 2.4`

**Test checkpoint:** `apache24\bin\httpd.exe -t` prints `Syntax OK` and `Update-Components.ps1 -Check` shows `apache` as `current`.

## 2. Every supported PHP series at its latest release

The stack carries several PHP series side by side. Each supported series is brought to its newest release, and a series upstream no longer supports is removed from the default set.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. List the series `windows.php.net` marks as supported and record them as `versioned` entries in the manifest. Done when: the manifest holds one entry per supported series.
2. Update each with `-Component php-<series>` (thread safe, x64). Done when: each `php\<series>\php.exe -v` prints its latest release.
3. Make the newest stable series the default in `scripts/Switch-PHPVersion.ps1` and `config/php/php.ini`. Done when: a fresh configure serves the newest series.
4. Run `php -m` on each series against the extension list the stack enables. Done when: every enabled extension loads on every series, or is recorded per series in the manifest.

- [ ] List the series `windows.php.net` marks as supported and record them as `versioned` entries in the manifest. Done when: the manifest holds one entry per supported series.
- [ ] Update each with `-Component php-<series>` (thread safe, x64). Done when: each `php\<series>\php.exe -v` prints its latest release.
- [ ] Make the newest stable series the default in `scripts/Switch-PHPVersion.ps1` and `config/php/php.ini`. Done when: a fresh configure serves the newest series.
- [ ] Run `php -m` on each series against the extension list the stack enables. Done when: every enabled extension loads on every series, or is recorded per series in the manifest.
- [ ] Commit: `components: supported PHP series at latest`

**Test checkpoint:** `pwsh scripts/Switch-PHPVersion.ps1 -ListVersions` lists each supported series at the version the manifest records.

## 3. MariaDB series at their latest releases

MariaDB's long-term series and its current stable series are both carried, each at its newest release.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Record the long-term and current stable series the MariaDB REST API reports as `versioned` manifest entries. Done when: the manifest holds one entry per series.
2. Update each within its own series through the updater. Done when: each `mariadbd.exe --version` prints its latest release and the pre-update dump exists.
3. Run `mariadb-upgrade` after each minor update where upstream requires it. Done when: the server log shows no upgrade warning on start.

- [ ] Record the long-term and current stable series the MariaDB REST API reports as `versioned` manifest entries. Done when: the manifest holds one entry per series.
- [ ] Update each within its own series through the updater. Done when: each `mariadbd.exe --version` prints its latest release and the pre-update dump exists.
- [ ] Run `mariadb-upgrade` after each minor update where upstream requires it. Done when: the server log shows no upgrade warning on start.
- [ ] Commit: `components: MariaDB series at latest`

**Test checkpoint:** `pwsh scripts/Switch-MariaDBVersion.ps1 -ListVersions` lists each series at the version the manifest records.

## 4. Mailpit, phpMyAdmin, Adminer and phpLiteAdmin at latest

The tools and web applications, each through the updater with its configuration preserved.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Update `mailpit`. Done when: `mailpit\mailpit.exe version` prints the latest release.
2. Update `phpmyadmin`, preserving `config.inc.php`. Done when: the login page loads and shows the new version.
3. Update `adminer` to the latest single-file release, keeping the wrapper `adminer/index.php`. Done when: the page footer shows the new version.
4. Check `phpliteadmin` against the newest PHP series; replace it with Adminer's SQLite driver if it no longer runs. Done when: a SQLite database opens in the tool the dashboard links to.

- [ ] Update `mailpit`. Done when: `mailpit\mailpit.exe version` prints the latest release.
- [ ] Update `phpmyadmin`, preserving `config.inc.php`. Done when: the login page loads and shows the new version.
- [ ] Update `adminer` to the latest single-file release, keeping the wrapper `adminer/index.php`. Done when: the page footer shows the new version.
- [ ] Check `phpliteadmin` against the newest PHP series; replace it with Adminer's SQLite driver if it no longer runs. Done when: a SQLite database opens in the tool the dashboard links to.
- [ ] Commit: `components: Mailpit and database web tools at latest`

**Test checkpoint:** `pwsh scripts/Update-Components.ps1 -Check -Json` shows `mailpit`, `phpmyadmin` and `adminer` as `current`.

## 5. Composer in the stack

`composer/` is empty. Composer is added as a manifest component with a launcher that uses the active PHP.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add a `composer` manifest entry for `composer.phar` with its published SHA-256. Done when: the updater installs `composer\composer.phar`.
2. Add `bin\composer.bat` that runs the phar with the active PHP. Done when: `composer --version` works from a shell opened by `scripts/Set-Environment.ps1`.
3. Track `composer/` in git as a folder with only a `.gitkeep`, and ignore the phar. Done when: `git status --short` is clean after the install.

- [ ] Add a `composer` manifest entry for `composer.phar` with its published SHA-256. Done when: the updater installs `composer\composer.phar`.
- [ ] Add `bin\composer.bat` that runs the phar with the active PHP. Done when: `composer --version` works from a shell opened by `scripts/Set-Environment.ps1`.
- [ ] Track `composer/` in git as a folder with only a `.gitkeep`, and ignore the phar. Done when: `git status --short` is clean after the install.
- [ ] Commit: `components: Composer`

**Test checkpoint:** `bin\composer.bat --version` prints the version the manifest records.

## 6. Node.js LTS in the stack

Front-end tooling for the sites people build on the stack.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add a `nodejs` manifest entry for the current LTS Windows x64 zip, resolved from `nodejs.org/dist/index.json`. Done when: the updater installs `nodejs\node.exe`.
2. Add `nodejs` to the PATH that `scripts/Set-Environment.ps1` sets. Done when: `node --version` and `npm --version` answer in that shell.
3. Ignore `/nodejs` in `.gitignore`. Done when: `git status --short` is clean after the install.

- [ ] Add a `nodejs` manifest entry for the current LTS Windows x64 zip, resolved from `nodejs.org/dist/index.json`. Done when: the updater installs `nodejs\node.exe`.
- [ ] Add `nodejs` to the PATH that `scripts/Set-Environment.ps1` sets. Done when: `node --version` and `npm --version` answer in that shell.
- [ ] Ignore `/nodejs` in `.gitignore`. Done when: `git status --short` is clean after the install.
- [ ] Commit: `components: Node.js LTS`

**Test checkpoint:** `nodejs\node.exe --version` prints the LTS version the manifest records.

## 7. Portable PowerShell and the Visual C++ runtime at latest

The two things everything else stands on.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Update the `pwsh` component to the latest stable PowerShell 7 release. Done when: `pwsh\pwsh.exe -v` prints it.
2. Record the Visual C++ redistributable as a manifest component with Microsoft's permanent link, and make `scripts/Install-VCRedist.ps1` read it. Done when: the script installs or confirms the current runtime.
3. Run every product script's `-WhatIf` or help under the new PowerShell. Done when: no script fails to parse.

- [ ] Update the `pwsh` component to the latest stable PowerShell 7 release. Done when: `pwsh\pwsh.exe -v` prints it.
- [ ] Record the Visual C++ redistributable as a manifest component with Microsoft's permanent link, and make `scripts/Install-VCRedist.ps1` read it. Done when: the script installs or confirms the current runtime.
- [ ] Run every product script's `-WhatIf` or help under the new PowerShell. Done when: no script fails to parse.
- [ ] Commit: `components: PowerShell and VC++ runtime at latest`

**Test checkpoint:** `pwsh\pwsh.exe -NoProfile -File scripts/check-all.ps1 -Only analyze` exits 0.

## 8. Apache and MariaDB as services without NSSM

NSSM is unmaintained. Apache and MariaDB install as Windows services themselves; only Mailpit, which cannot, keeps the wrapper.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Register Apache with `httpd.exe -k install -n GluonApache` in `scripts/Register-Services.ps1`. Done when: `sc qc GluonApache` shows `httpd.exe` as the binary.
2. Register MariaDB with `mariadbd.exe --install GluonMariaDB --defaults-file=...`. Done when: `sc qc GluonMariaDB` shows `mariadbd.exe`.
3. Update `scripts/Unregister-Services.ps1` and both version-switch scripts for the native registrations. Done when: a version switch re-registers the service on the new binary.
4. Keep NSSM for `GluonMailpit` only and record why in a comment at the call. Done when: `git grep -n nssm -- scripts` shows only Mailpit's registration.

- [ ] Register Apache with `httpd.exe -k install -n GluonApache` in `scripts/Register-Services.ps1`. Done when: `sc qc GluonApache` shows `httpd.exe` as the binary.
- [ ] Register MariaDB with `mariadbd.exe --install GluonMariaDB --defaults-file=...`. Done when: `sc qc GluonMariaDB` shows `mariadbd.exe`.
- [ ] Update `scripts/Unregister-Services.ps1` and both version-switch scripts for the native registrations. Done when: a version switch re-registers the service on the new binary.
- [ ] Keep NSSM for `GluonMailpit` only and record why in a comment at the call. Done when: `git grep -n nssm -- scripts` shows only Mailpit's registration.
- [ ] Commit: `services: native registration for Apache and MariaDB`

**Test checkpoint:** `sc.exe qc GluonApache` and `sc.exe qc GluonMariaDB` each print a `BINARY_PATH_NAME` that does not contain `nssm`.
## Verification

- `pwsh scripts/Update-Components.ps1 -Check` exits 0 and `pwsh scripts/Start-Services.ps1` starts every installed service.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
