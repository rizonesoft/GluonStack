---
schema_version: 1
id: control-settings-backup-updates
domain: 03-control
status: active
title: "TODO-03 -- Service settings, backup and updates"
depends_on: ["control-databases"]
---

# TODO-03 -- Service settings, backup and updates

> **Goal:** Each service's settings are edited in its pane with validation and a kept previous file, every database can be backed up and restored, and the Updates pane runs the component updater.

> **Current state:** Measured 2026-11-15. Service configuration is edited by hand in `config/`. `scripts/Restore-MariaDB.ps1` exists; there is no backup script for MariaDB in `scripts/` beyond it, and D01 T02 §6 adds PostgreSQL's. `scripts/Update-Components.ps1` (D01 T01) has no interface in the application.

## Inputs

- `docs/design/SPEC.md` sections 6.5 (settings) and 6.6 (Updates).
- D01 T01 §4 to §7: the updater and its JSON output. D01 T02 §6: PostgreSQL backup.

## Outcome

- A port changed in a service's settings is in its configuration file and in effect after `restart now`; `backup now` writes a dump of every database; `update all` updates every stale component and shows each step.

**Adjacency:** list=applicable @ D03 T03 §5; document=not-applicable (no such surface here); settings=applicable @ D03 T03 §1; reporting=applicable @ D03 T03 §4; notifications=not-applicable (no such surface here); permissions=not-applicable (no such surface here); audit=applicable @ D03 T03 §5; exchange=applicable @ D03 T03 §3; reverse=applicable @ D03 T03 §1

**Adjacency rationale:** Settings are the forms; their reverse is the kept `.bak` and `restore previous`; exchange is backup and restore; the Updates table is the list and the update log its trail; the backup history is the one report.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Settings form for Apache with validated save | -- | [ ] |
| 2 | §2 | Settings forms for PHP, MariaDB, PostgreSQL and Mailpit | §1 | [ ] |
| 3 | §3 | Backup service and the backup now command | §1 | [ ] |
| 4 | §4 | Backup history and restore | §3 | [ ] |
| 5 | §5 | Updates pane over the component updater | §1 | [ ] |

## 1. Settings form for Apache with validated save

The first settings form and the save path the others reuse.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.5, settings) and `docs/design/reference/control-panel.dc.html`.
**Job:** Change how a service is configured without editing a file by hand.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Create `gluon-control/Services/Config/ConfigFile.cs`: read named directives from a configuration file and write them back preserving every other line and comment. Done when: a round-trip of `httpd.conf` with no change is byte-identical.
2. Add `SaveValidatedAsync`: write to a temporary file, run the service's validator, keep the live file as `.bak`, replace it. Done when: an invalid value leaves the live file untouched and reports the validator's message.
3. Build Apache's form in the service pane: http port, https port, document root, server name, with `save`, `cancel` and `restore previous`. Done when: a changed port is in `httpd.conf` and `restart now` appears on the status line.
4. Check a new port against listening sockets and name the process that holds a busy one. Done when: a busy port is refused with the process name.

- [ ] Create `gluon-control/Services/Config/ConfigFile.cs`: read named directives from a configuration file and write them back preserving every other line and comment. Done when: a round-trip of `httpd.conf` with no change is byte-identical.
- [ ] Add `SaveValidatedAsync`: write to a temporary file, run the service's validator, keep the live file as `.bak`, replace it. Done when: an invalid value leaves the live file untouched and reports the validator's message. Cheaper substitute: writing the live file and validating afterwards.
- [ ] Build Apache's form in the service pane: http port, https port, document root, server name, with `save`, `cancel` and `restore previous`. Done when: a changed port is in `httpd.conf` and `restart now` appears on the status line.
- [ ] Check a new port against listening sockets and name the process that holds a busy one. Done when: a busy port is refused with the process name.
- [ ] Commit: `settings: Apache form and validated save`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ConfigFile` reports all passed.

## 2. Settings forms for PHP, MariaDB, PostgreSQL and Mailpit

The same pattern for the other four.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.5, settings) and `docs/design/reference/control-panel.dc.html`.
**Job:** Tune each service from its pane.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. PHP: `memory_limit`, `upload_max_filesize`, `post_max_size`, `max_execution_time`, `display_errors`, the Xdebug switch, written to the active version's `php.ini`. Done when: `php -i` shows the saved values.
2. MariaDB: port, `innodb_buffer_pool_size`, `max_connections`, character set and collation in `my.ini`, validated with `mariadbd --validate-config`. Done when: an invalid buffer size is refused.
3. PostgreSQL: port, `shared_buffers`, `max_connections` in `postgresql.conf`, validated with `postgres -C`. Done when: the saved port is in effect after restart.
4. Mailpit: SMTP port, web port and maximum stored messages in the service's arguments. Done when: the inbox opens on the new web port.

- [ ] PHP: `memory_limit`, `upload_max_filesize`, `post_max_size`, `max_execution_time`, `display_errors`, the Xdebug switch, written to the active version's `php.ini`. Done when: `php -i` shows the saved values.
- [ ] MariaDB: port, `innodb_buffer_pool_size`, `max_connections`, character set and collation in `my.ini`, validated with `mariadbd --validate-config`. Done when: an invalid buffer size is refused.
- [ ] PostgreSQL: port, `shared_buffers`, `max_connections` in `postgresql.conf`, validated with `postgres -C`. Done when: the saved port is in effect after restart.
- [ ] Mailpit: SMTP port, web port and maximum stored messages in the service's arguments. Done when: the inbox opens on the new web port.
- [ ] Commit: `settings: PHP, MariaDB, PostgreSQL and Mailpit forms`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ConfigFile` reports all passed. Each validator's refusal has a test.

## 3. Backup service and the backup now command

One command dumps every database on every running server.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Backup-MariaDB.ps1` and its launcher beside the existing restore script: one `mariadb-dump` per database into `backups\mariadb\<timestamp>`. Done when: the folder holds one file per database.
2. Create `gluon-control/Services/BackupService.cs` running the MariaDB and PostgreSQL backup scripts and reporting progress per database. Done when: `backup now` writes both servers' dumps.
3. Register `backup now` and bind the service panes' buttons to it. Done when: the button and the command do the same.
4. Skip a stopped server and say so; fail the command if a running server's dump fails. Done when: the status line names what was backed up and what was skipped.

- [ ] Create `scripts/Backup-MariaDB.ps1` and its launcher beside the existing restore script: one `mariadb-dump` per database into `backups\mariadb\<timestamp>`. Done when: the folder holds one file per database.
- [ ] Create `gluon-control/Services/BackupService.cs` running the MariaDB and PostgreSQL backup scripts and reporting progress per database. Done when: `backup now` writes both servers' dumps.
- [ ] Register `backup now` and bind the service panes' buttons to it. Done when: the button and the command do the same.
- [ ] Skip a stopped server and say so; fail the command if a running server's dump fails. Done when: the status line names what was backed up and what was skipped.
- [ ] Commit: `backup: backup now`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~BackupService` reports all passed.

## 4. Backup history and restore

The backups that exist, and putting one back.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.4 (dialog)) and `docs/design/reference/control-panel.dc.html`.
**Job:** Find a backup and restore a database from it.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** A dialog over the main window.

**Build order:**

1. Add a backups dialog reached from the database server panes: a table of backups with time, server, databases and size, read from `backups\`. Done when: the table lists the real folders, newest first.
2. Add `restore` per database from a backup, with the destructive confirmation when the database exists. Done when: a restored database matches its dump.
3. Add `delete` per backup with a confirmation, and `open folder`. Done when: a deleted backup's folder is gone.
4. Keep the newest 10 backups per server by default, set in Settings. Done when: the eleventh backup removes the oldest and says so.

- [ ] Add a backups dialog reached from the database server panes: a table of backups with time, server, databases and size, read from `backups\`. Done when: the table lists the real folders, newest first.
- [ ] Add `restore` per database from a backup, with the destructive confirmation when the database exists. Done when: a restored database matches its dump.
- [ ] Add `delete` per backup with a confirmation, and `open folder`. Done when: a deleted backup's folder is gone.
- [ ] Keep the newest 10 backups per server by default, set in Settings. Done when: the eleventh backup removes the oldest and says so.
- [ ] Commit: `backup: history and restore`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~BackupService` reports all passed. A manual restore round-trips a database.

## 5. Updates pane over the component updater

The interface to `scripts/Update-Components.ps1`.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Updates) and `docs/design/reference/control-panel.dc.html`.
**Job:** See what is out of date and update one component or all of them.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Create `gluon-control/Services/UpdateService.cs`: run the script with `-Check -Json` and parse the rows; run `-Component <id>` and `-All`, reading step lines as they arrive. Done when: the service returns typed rows and step events.
2. Create `gluon-control/Views/UpdatesView.xaml` as section 6.6: table, `check now`, `update all`, per-row `update`, the dump note. Done when: the table shows the real installed and latest versions.
3. Show each row's step while it updates and the failed step with the put-back note on failure. Done when: a failed probe shows `failed (checking)` and that the previous version was restored.
4. Register `check updates` and `update <component|all>`, and bind the `updates` entry's note. Done when: the note reads `2 available` in `signal` when two are behind.
5. Stop the script's whole process tree when the application exits mid-update, after the current step's rollback point. Done when: closing the window during a download leaves no script process.

- [ ] Create `gluon-control/Services/UpdateService.cs`: run the script with `-Check -Json` and parse the rows; run `-Component <id>` and `-All`, reading step lines as they arrive. Done when: the service returns typed rows and step events.
- [ ] Create `gluon-control/Views/UpdatesView.xaml` as section 6.6: table, `check now`, `update all`, per-row `update`, the dump note. Done when: the table shows the real installed and latest versions.
- [ ] Show each row's step while it updates and the failed step with the put-back note on failure. Done when: a failed probe shows `failed (checking)` and that the previous version was restored.
- [ ] Register `check updates` and `update <component|all>`, and bind the `updates` entry's note. Done when: the note reads `2 available` in `signal` when two are behind.
- [ ] Stop the script's whole process tree when the application exits mid-update, after the current step's rollback point. Done when: closing the window during a download leaves no script process. Cheaper substitute: leaving the script running detached.
- [ ] Commit: `updates: Updates pane`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~UpdateService` reports all passed.
## Verification

- From the application alone: a port is changed and restored, every database is backed up and one restored, and `update all` completes with each step shown.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
