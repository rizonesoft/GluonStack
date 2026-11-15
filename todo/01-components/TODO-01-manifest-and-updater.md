---
schema_version: 1
id: component-manifest
domain: 01-components
status: active
title: "TODO-01 -- Component manifest and updater"
depends_on: ["quality-gates"]
---

# TODO-01 -- Component manifest and updater

> **Goal:** One manifest records every bundled component's version, source and checksum, and one script checks, updates one or updates all of them with a rollback, so a version is never written by hand again.

> **Current state:** Measured 2026-11-15. Component binaries are ignored by git and exist only as folders on the developer machine (`apache24`, `php`, `mariadb`, `mailpit`, `phpmyadmin`, `adminer`, `phpliteadmin`, `pwsh`, `bin`). `README.md` lists versions by hand (Apache 2.4.65, PHP 8.4.11, MariaDB 12.0.2, phpMyAdmin 5.2.2, Adminer 5.3.0, Mailpit 1.27.7, NSSM 2.24). `scripts/Switch-PHPVersion.ps1` and `scripts/Switch-MariaDBVersion.ps1` discover versioned folders. Nothing downloads, verifies or updates a component.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: the update mechanism and the components decisions.
- `scripts/_Template.ps1` and `docs/script-conventions.md`: the shape every product script follows.
- `scripts/GluonStack.Common.psm1` (D00 T01 §2): root, service names and logging.

## Outcome

- `scripts/Update-Components.ps1 -Check` lists each component with its installed and latest version, and `-All` brings every one to latest or puts the previous version back.
- `python scripts/component-drift.py` appends one finding per stale component to `todo/findings.md`.

**Adjacency:** list=applicable @ D01 T01 §4; document=not-applicable (the updater has no such surface of its own); settings=applicable @ D01 T01 §1; reporting=not-applicable (the updater has no such surface of its own); notifications=applicable @ D01 T01 §8; permissions=not-applicable (the updater has no such surface of its own); audit=applicable @ D01 T01 §7; exchange=not-applicable (the updater has no such surface of its own); reverse=applicable @ D01 T01 §5

**Adjacency rationale:** The list is `-Check`; the settings are the manifest's own keys; the audit trail is the update log §7 writes; the reverse of an update is §5's rollback; the notice that a component fell behind is §8's finding. The control panel's Updates pane is D03 T05's and reads the same script.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Manifest schema and the components installed today | -- | [ ] |
| 2 | §2 | Manifest reader with validation | §1 | [ ] |
| 3 | §3 | Upstream version resolvers | §2 | [ ] |
| 4 | §4 | Update-Components -Check | §3 | [ ] |
| 5 | §5 | Staged update of one component with rollback | §4 | [ ] |
| 6 | §6 | Database dump before a database server update | §5 | [ ] |
| 7 | §7 | Update all with a summary and a log | §6 | [ ] |
| 8 | §8 | Drift filed to the TODO findings | §4 | [ ] |
| 9 | §9 | Component list in the README generated from the manifest | §7 | [ ] |

## 1. Manifest schema and the components installed today

The manifest is the single place a version, source and checksum live. It starts as a true record of what is installed now.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Write `config/components.schema.json`: per component `id`, `name`, `version`, `folder`, `kind` (`service`, `runtime`, `tool`, `webapp`), `feed`, `url`, `sha256`, `service` and `versioned`. Done when: the schema validates with `python -c "import json; json.load(open('config/components.schema.json'))"`.
2. Write `config/components.json` with one entry per installed component, each version read from the binary itself (`httpd -v`, `php -v`, `mariadbd --version`, `mailpit version`). Done when: every entry's version equals what its binary prints.
3. Record each entry's upstream download URL pattern and the feed that lists its releases. Done when: each `url` with the current version substituted answers HTTP 200 to a HEAD request.
4. Record the SHA-256 of each archive as published upstream, or computed from the download when upstream publishes none, with `sha256_source` saying which. Done when: no entry has an empty `sha256`.

- [ ] Write `config/components.schema.json`: per component `id`, `name`, `version`, `folder`, `kind` (`service`, `runtime`, `tool`, `webapp`), `feed`, `url`, `sha256`, `service` and `versioned`. Done when: the schema validates with `python -c "import json; json.load(open('config/components.schema.json'))"`.
- [ ] Write `config/components.json` with one entry per installed component, each version read from the binary itself (`httpd -v`, `php -v`, `mariadbd --version`, `mailpit version`). Done when: every entry's version equals what its binary prints. Cheaper substitute: copying versions from `README.md`.
- [ ] Record each entry's upstream download URL pattern and the feed that lists its releases. Done when: each `url` with the current version substituted answers HTTP 200 to a HEAD request.
- [ ] Record the SHA-256 of each archive as published upstream, or computed from the download when upstream publishes none, with `sha256_source` saying which. Done when: no entry has an empty `sha256`.
- [ ] Commit: `components: manifest schema and current components`

**Test checkpoint:** `pwsh -NoProfile -Command "(Get-Content config/components.json -Raw | ConvertFrom-Json).components.Count"` prints the number of installed components, at least 9.

## 2. Manifest reader with validation

Every consumer reads the manifest through one function that refuses a malformed file with the key named.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add `Get-GluonComponent` and `Set-GluonComponentVersion` to `scripts/GluonStack.Components.psm1`. Done when: `Get-GluonComponent -Id php` returns the entry as an object.
2. Validate required keys, a known `kind`, a 64 character hexadecimal `sha256` and unique ids on every read. Done when: a manifest with a duplicate id is refused naming the id.
3. Write the manifest atomically: a temporary file in the same folder, then a rename. Done when: killing the process mid-write leaves the previous manifest intact.
4. Add `scripts/tests/Components.Tests.ps1` for a valid file, each refusal and the atomic write. Done when: the tests pass and fail when a validation is removed.

- [ ] Add `Get-GluonComponent` and `Set-GluonComponentVersion` to `scripts/GluonStack.Components.psm1`. Done when: `Get-GluonComponent -Id php` returns the entry as an object.
- [ ] Validate required keys, a known `kind`, a 64 character hexadecimal `sha256` and unique ids on every read. Done when: a manifest with a duplicate id is refused naming the id. Cheaper substitute: returning the first match and ignoring the rest.
- [ ] Write the manifest atomically: a temporary file in the same folder, then a rename. Done when: killing the process mid-write leaves the previous manifest intact.
- [ ] Add `scripts/tests/Components.Tests.ps1` for a valid file, each refusal and the atomic write. Done when: the tests pass and fail when a validation is removed.
- [ ] Commit: `components: manifest reader with validation`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Components.Tests.ps1 -CI"` reports 0 failed.

## 3. Upstream version resolvers

Latest is a fact read from upstream on the day, by one resolver per feed type.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add `Resolve-GluonLatestVersion` with resolvers for a GitHub releases feed, the `windows.php.net` releases JSON, the MariaDB REST API, the PostgreSQL versions feed and an Apache Lounge page. Done when: each resolver returns a version and a download URL for its component.
2. Restrict each resolver to stable releases and, for a `versioned` component, to the component's own series. Done when: PHP 8.3 resolves to the newest 8.3 release, never to 8.4.
3. Cache answers for one hour under `tmp\component-feeds` and time out a request after 20 seconds. Done when: a second `-Check` within the hour makes no request.
4. Return a named failure, not an exception, when a feed cannot be reached. Done when: with the network off, `-Check` lists the component as `unknown (feed unreachable)` and exits 0.
5. Add tests that feed each resolver a saved response from `scripts/tests/fixtures/feeds/`. Done when: the tests pass offline.

- [ ] Add `Resolve-GluonLatestVersion` with resolvers for a GitHub releases feed, the `windows.php.net` releases JSON, the MariaDB REST API, the PostgreSQL versions feed and an Apache Lounge page. Done when: each resolver returns a version and a download URL for its component.
- [ ] Restrict each resolver to stable releases and, for a `versioned` component, to the component's own series. Done when: PHP 8.3 resolves to the newest 8.3 release, never to 8.4. Cheaper substitute: taking the first tag, which may be a release candidate.
- [ ] Cache answers for one hour under `tmp\component-feeds` and time out a request after 20 seconds. Done when: a second `-Check` within the hour makes no request.
- [ ] Return a named failure, not an exception, when a feed cannot be reached. Done when: with the network off, `-Check` lists the component as `unknown (feed unreachable)` and exits 0.
- [ ] Add tests that feed each resolver a saved response from `scripts/tests/fixtures/feeds/`. Done when: the tests pass offline.
- [ ] Commit: `components: upstream version resolvers`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Resolvers.Tests.ps1 -CI"` reports 0 failed.

## 4. Update-Components -Check

The read-only half: what is installed, what is latest, what is behind.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Update-Components.ps1` from the template with `-Check`, `-Component <id>`, `-All` and `-Json`. Done when: `-Check` prints one row per component: id, installed, latest, state.
2. Exit 0 when everything is current and 3 when anything is behind. Done when: the exit code is 3 when the manifest's PHP version is lowered by hand.
3. Emit the same rows as JSON with `-Json` for the control panel and the drift script. Done when: `-Check -Json | ConvertFrom-Json` yields objects with the four fields.
4. Add `scripts/Update-Components.bat` from the launcher template with self-elevation. Done when: the launcher starts the script elevated.

- [ ] Create `scripts/Update-Components.ps1` from the template with `-Check`, `-Component <id>`, `-All` and `-Json`. Done when: `-Check` prints one row per component: id, installed, latest, state.
- [ ] Exit 0 when everything is current and 3 when anything is behind. Done when: the exit code is 3 when the manifest's PHP version is lowered by hand.
- [ ] Emit the same rows as JSON with `-Json` for the control panel and the drift script. Done when: `-Check -Json | ConvertFrom-Json` yields objects with the four fields.
- [ ] Add `scripts/Update-Components.bat` from the launcher template with self-elevation. Done when: the launcher starts the script elevated.
- [ ] Commit: `components: Update-Components -Check`

**Test checkpoint:** `pwsh scripts/Update-Components.ps1 -Check -Json` prints valid JSON with one object per manifest entry.

## 5. Staged update of one component with rollback

An update must never leave a component half replaced. It is staged beside the live folder and swapped by rename, and any failure puts the old folder back.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Download the archive to `tmp\component-staging\<id>` and verify its SHA-256 against the resolver's or upstream's published value. Done when: a corrupted download is refused and nothing is changed.
2. Extract to `<folder>.new`, carrying over the configuration files the manifest lists under `preserve`. Done when: the staged folder holds the new binaries and the old configuration.
3. Stop the component's service, rename `<folder>` to `<folder>.previous` and `<folder>.new` to `<folder>`, then start the service. Done when: the service runs the new version.
4. Prove the component answers (`httpd -t` and an HTTP 200, a `SELECT 1`, a version probe) and write the new version and checksum to the manifest. Done when: the manifest shows the new version only after the probe passes.
5. On a failed stop, swap, start or probe, rename the folders back, start the service and exit 1 naming the step. Done when: a test that fails the probe ends with the old version running and the manifest unchanged.
6. Keep one `.previous` per component and delete it only at the next successful update. Done when: `-Rollback <id>` swaps back to `.previous` after a successful update.

- [ ] Download the archive to `tmp\component-staging\<id>` and verify its SHA-256 against the resolver's or upstream's published value. Done when: a corrupted download is refused and nothing is changed. Cheaper substitute: skipping the check when upstream publishes no checksum.
- [ ] Extract to `<folder>.new`, carrying over the configuration files the manifest lists under `preserve`. Done when: the staged folder holds the new binaries and the old configuration.
- [ ] Stop the component's service, rename `<folder>` to `<folder>.previous` and `<folder>.new` to `<folder>`, then start the service. Done when: the service runs the new version.
- [ ] Prove the component answers (`httpd -t` and an HTTP 200, a `SELECT 1`, a version probe) and write the new version and checksum to the manifest. Done when: the manifest shows the new version only after the probe passes.
- [ ] On a failed stop, swap, start or probe, rename the folders back, start the service and exit 1 naming the step. Done when: a test that fails the probe ends with the old version running and the manifest unchanged.
- [ ] Keep one `.previous` per component and delete it only at the next successful update. Done when: `-Rollback <id>` swaps back to `.previous` after a successful update.
- [ ] Commit: `components: staged update with rollback`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Update.Tests.ps1 -CI"` reports 0 failed, including the failed-probe rollback test.

## 6. Database dump before a database server update

A database server update is the one that can lose data. Every database is dumped before the server is stopped, and the update refuses to go on without the dump.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Before updating a component whose `kind` is `service` and that has a `dump` command in the manifest, dump every database to `backups\pre-update\<id>-<version>-<timestamp>`. Done when: the folder holds one dump per database after an update.
2. Refuse the update when the dump fails or the server is not running to be dumped, unless `-SkipDump` is given. Done when: with the server stopped, the update exits 1 saying to start it or pass `-SkipDump`.
3. Refuse a MariaDB or PostgreSQL update that changes the major version, pointing to the version switch and migration scripts. Done when: an update from one major series to the next is refused with that message.

- [ ] Before updating a component whose `kind` is `service` and that has a `dump` command in the manifest, dump every database to `backups\pre-update\<id>-<version>-<timestamp>`. Done when: the folder holds one dump per database after an update.
- [ ] Refuse the update when the dump fails or the server is not running to be dumped, unless `-SkipDump` is given. Done when: with the server stopped, the update exits 1 saying to start it or pass `-SkipDump`. Cheaper substitute: logging a warning and continuing.
- [ ] Refuse a MariaDB or PostgreSQL update that changes the major version, pointing to the version switch and migration scripts. Done when: an update from one major series to the next is refused with that message.
- [ ] Commit: `components: dump databases before a server update`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Update.Tests.ps1 -CI -FullNameFilter '*dump*'"` reports 0 failed.

## 7. Update all with a summary and a log

The owner's request: one way to update everything. Components update one at a time in dependency order, and one failure does not stop the rest.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Implement `-All`: update every component that is behind, runtimes and tools first, then services, then web applications. Done when: a run with two stale components updates both.
2. Continue after a component fails and exit 1 at the end if any failed. Done when: the summary lists each component as `updated`, `current`, `failed (step)` or `skipped`.
3. Write `logs\gluonstack\updates.log` with one line per step: time, component, from, to, step, result. Done when: the log shows the full sequence of an update and a rollback.
4. Refuse to start when another update holds `tmp\component-staging\update.lock`, naming its process. Done when: a second `-All` started during the first exits 1 at once.

- [ ] Implement `-All`: update every component that is behind, runtimes and tools first, then services, then web applications. Done when: a run with two stale components updates both.
- [ ] Continue after a component fails and exit 1 at the end if any failed. Done when: the summary lists each component as `updated`, `current`, `failed (step)` or `skipped`.
- [ ] Write `logs\gluonstack\updates.log` with one line per step: time, component, from, to, step, result. Done when: the log shows the full sequence of an update and a rollback.
- [ ] Refuse to start when another update holds `tmp\component-staging\update.lock`, naming its process. Done when: a second `-All` started during the first exits 1 at once.
- [ ] Commit: `components: update all with summary and log`

**Test checkpoint:** `pwsh scripts/Update-Components.ps1 -All -WhatIf` lists every stale component with the steps it would run and changes nothing.

## 8. Drift filed to the TODO findings

A component that fell behind upstream should become planned work without anyone remembering to look.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/component-drift.py`: run the updater's `-Check -Json` and compare with the manifest. Done when: it prints one line per stale component.
2. Append one line per stale component to `todo/findings.md` as `config/components.json:<line>` with the installed and latest version, skipping a finding already present. Done when: running it twice adds each finding once.
3. Add `--check` that exits 3 when anything is stale and writes nothing. Done when: the exit code is 3 with a stale manifest and 0 otherwise.
4. Document it in `docs/todo-workflow.md` under Validation. Done when: the document names the command.

- [ ] Create `scripts/component-drift.py`: run the updater's `-Check -Json` and compare with the manifest. Done when: it prints one line per stale component.
- [ ] Append one line per stale component to `todo/findings.md` as `config/components.json:<line>` with the installed and latest version, skipping a finding already present. Done when: running it twice adds each finding once.
- [ ] Add `--check` that exits 3 when anything is stale and writes nothing. Done when: the exit code is 3 with a stale manifest and 0 otherwise.
- [ ] Document it in `docs/todo-workflow.md` under Validation. Done when: the document names the command.
- [ ] Commit: `components: file stale components as findings`

**Test checkpoint:** `python scripts/component-drift.py --check` exits 0 on a current manifest and 3 after a version in the manifest is lowered.

## 9. Component list in the README generated from the manifest

The README's hand-written version list is the thing that went stale. It is generated.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add `scripts/Update-Components.ps1 -WriteDocs`, which rewrites the block between `<!-- components:start -->` and `<!-- components:end -->` in `README.md`. Done when: the block lists every component with its manifest version.
2. Delete the hand-written versions elsewhere in `README.md`. Done when: `git grep -n -E '[0-9]+\.[0-9]+\.[0-9]+' README.md` shows versions only inside the block.
3. Run `-WriteDocs` at the end of every successful update. Done when: the README changes in the same working tree as the manifest.

- [ ] Add `scripts/Update-Components.ps1 -WriteDocs`, which rewrites the block between `<!-- components:start -->` and `<!-- components:end -->` in `README.md`. Done when: the block lists every component with its manifest version.
- [ ] Delete the hand-written versions elsewhere in `README.md`. Done when: `git grep -n -E '[0-9]+\.[0-9]+\.[0-9]+' README.md` shows versions only inside the block.
- [ ] Run `-WriteDocs` at the end of every successful update. Done when: the README changes in the same working tree as the manifest.
- [ ] Commit: `docs: README component list from the manifest`

**Test checkpoint:** `pwsh scripts/Update-Components.ps1 -WriteDocs` leaves `git diff --stat README.md` empty on a current tree.
## Verification

- On a machine with the components installed, `pwsh scripts/Update-Components.ps1 -Check` exits 0 or 3 and `-All` ends with every component `updated` or `current`.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
