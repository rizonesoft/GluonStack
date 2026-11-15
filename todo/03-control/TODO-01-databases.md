---
schema_version: 1
id: control-databases
domain: 03-control
status: active
title: "TODO-01 -- Databases pane"
depends_on: ["control-panel-shell"]
---

# TODO-01 -- Databases pane

> **Goal:** The Databases pane lists the databases of the running MariaDB and PostgreSQL servers and creates, drops, exports and imports them.

> **Current state:** Measured 2026-11-15. `gluon-control/Views/DatabaseView.xaml` (50 lines) and `ViewModels/DatabaseViewModel.cs` are stubs with no behaviour. The command-line clients ship with each server (`mariadb.exe`, `mariadb-dump.exe`, `psql.exe`, `pg_dump.exe`, `pg_restore.exe`).

## Inputs

- `docs/design/SPEC.md` section 6.6, Databases, and section 6.4 for the dialog and destructive confirmation.
- D02 T02: the pane host, command registry, status line and pane states.
- D01 T02: PostgreSQL's service, credentials and backup scripts.

## Outcome

- A database created in the pane exists on the server, an export can be imported back, and a dropped database is gone only after its name is typed.

**Adjacency:** list=applicable @ D03 T01 §3; document=not-applicable (no such surface for databases in a local development stack); settings=not-applicable (no such surface for databases in a local development stack); reporting=not-applicable (no such surface for databases in a local development stack); notifications=not-applicable (no such surface for databases in a local development stack); permissions=applicable @ D03 T01 §1; audit=applicable @ D03 T01 §4; exchange=applicable @ D03 T01 §5; reverse=applicable @ D03 T01 §4

**Adjacency rationale:** The list is the table; exchange is export and import; the reverse of create is drop, guarded by the typed name; permissions are the refusal to act on the servers' system databases; create and drop are written to the control log through the status line.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Database service for MariaDB | -- | [ ] |
| 2 | §2 | Database service for PostgreSQL | §1 | [ ] |
| 3 | §3 | Databases pane with the server switch and table | §2 | [ ] |
| 4 | §4 | New database dialog and drop confirmation | §3 | [ ] |
| 5 | §5 | Export and import with progress and cancel | §4 | [ ] |

## 1. Database service for MariaDB

The operations behind the pane, over the server's own command-line client, with credentials passed without appearing in a process list.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Create `gluon-control/Services/Databases/IDatabaseServer.cs` (`ListAsync`, `CreateAsync`, `DropAsync`, `ExportAsync`, `ImportAsync`) and `MariaDbServer.cs` over `mariadb.exe`. Done when: `ListAsync` returns each database's name, size and table count.
2. Pass the password through a temporary defaults file readable only by the user, deleted after the call. Done when: no password appears in any process's command line.
3. Refuse create, drop and import on `mysql`, `information_schema`, `performance_schema` and `sys`, and validate names against `[A-Za-z0-9_]{1,64}`. Done when: `DropAsync("mysql")` returns a refusal and runs nothing.
4. Add `MariaDbServerTests` against a fake client executable that records its arguments. Done when: the tests pass without a server and fail when the name check is removed.

- [ ] Create `gluon-control/Services/Databases/IDatabaseServer.cs` (`ListAsync`, `CreateAsync`, `DropAsync`, `ExportAsync`, `ImportAsync`) and `MariaDbServer.cs` over `mariadb.exe`. Done when: `ListAsync` returns each database's name, size and table count.
- [ ] Pass the password through a temporary defaults file readable only by the user, deleted after the call. Done when: no password appears in any process's command line. Cheaper substitute: `--password=` on the command line.
- [ ] Refuse create, drop and import on `mysql`, `information_schema`, `performance_schema` and `sys`, and validate names against `[A-Za-z0-9_]{1,64}`. Done when: `DropAsync("mysql")` returns a refusal and runs nothing.
- [ ] Add `MariaDbServerTests` against a fake client executable that records its arguments. Done when: the tests pass without a server and fail when the name check is removed.
- [ ] Commit: `databases: MariaDB service`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~MariaDbServer` reports all passed.

## 2. Database service for PostgreSQL

The same interface over `psql`, `pg_dump` and `pg_restore`.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Create `gluon-control/Services/Databases/PostgresServer.cs` implementing `IDatabaseServer`. Done when: `ListAsync` returns each database's name, size and table count.
2. Pass the password through a `PGPASSFILE` readable only by the user, deleted after the call. Done when: no password appears in a command line or the environment of a child that outlives the call.
3. Refuse operations on `postgres`, `template0` and `template1`. Done when: `DropAsync("template1")` returns a refusal.
4. Add `PostgresServerTests` against the fake client. Done when: the tests pass without a server.

- [ ] Create `gluon-control/Services/Databases/PostgresServer.cs` implementing `IDatabaseServer`. Done when: `ListAsync` returns each database's name, size and table count.
- [ ] Pass the password through a `PGPASSFILE` readable only by the user, deleted after the call. Done when: no password appears in a command line or the environment of a child that outlives the call.
- [ ] Refuse operations on `postgres`, `template0` and `template1`. Done when: `DropAsync("template1")` returns a refusal.
- [ ] Add `PostgresServerTests` against the fake client. Done when: the tests pass without a server.
- [ ] Commit: `databases: PostgreSQL service`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~PostgresServer` reports all passed.

## 3. Databases pane with the server switch and table

The pane itself.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Databases) and `docs/design/reference/control-panel.dc.html`.
**Job:** See the databases on a server and act on one.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Rebuild `gluon-control/Views/DatabaseView.xaml` as section 6.6: heading, server switch offering only running servers, the table, `new database`. Done when: the pane lists the real databases of the selected server.
2. Show the not-running state with `start <server>` when no server runs. Done when: with both stopped the pane offers to start one.
3. Register `go databases` and bind the `databases` list entry's note to the running servers. Done when: the note reads `mariadb, postgres` when both run.
4. Refresh the table after every operation and on entry. Done when: a database created outside the application appears on re-entry.

- [ ] Rebuild `gluon-control/Views/DatabaseView.xaml` as section 6.6: heading, server switch offering only running servers, the table, `new database`. Done when: the pane lists the real databases of the selected server.
- [ ] Show the not-running state with `start <server>` when no server runs. Done when: with both stopped the pane offers to start one.
- [ ] Register `go databases` and bind the `databases` list entry's note to the running servers. Done when: the note reads `mariadb, postgres` when both run.
- [ ] Refresh the table after every operation and on entry. Done when: a database created outside the application appears on re-entry.
- [ ] Commit: `databases: pane and table`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~DatabaseViewModel` reports all passed.

## 4. New database dialog and drop confirmation

Create, and its reverse.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (sections 6.4 (dialog) and 6.6, Databases) and `docs/design/reference/control-panel.dc.html`.
**Job:** Create a database with the right encoding, and remove one deliberately.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** A dialog over the main window.

**Build order:**

1. Add the `new database` dialog: name, character set and collation for MariaDB, encoding for PostgreSQL, with the server's own defaults preselected. Done when: the created database has the chosen settings.
2. Register `new database <name> [on mariadb|postgres]`, opening the dialog with the name filled in. Done when: the command opens the dialog.
3. Add `drop` per row with the destructive dialog that requires the database name to be typed. Done when: the confirm button does nothing until the name matches.
4. Report each create and drop on the status line. Done when: the control log holds a line for each.

- [ ] Add the `new database` dialog: name, character set and collation for MariaDB, encoding for PostgreSQL, with the server's own defaults preselected. Done when: the created database has the chosen settings.
- [ ] Register `new database <name> [on mariadb|postgres]`, opening the dialog with the name filled in. Done when: the command opens the dialog.
- [ ] Add `drop` per row with the destructive dialog that requires the database name to be typed. Done when: the confirm button does nothing until the name matches. Cheaper substitute: a yes or no message box.
- [ ] Report each create and drop on the status line. Done when: the control log holds a line for each.
- [ ] Commit: `databases: create dialog and drop confirmation`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~DatabaseViewModel` reports all passed. A manual create then drop round-trips on both servers.

## 5. Export and import with progress and cancel

Moving a database in and out as a file.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Databases) and `docs/design/reference/control-panel.dc.html`.
**Job:** Take a database out as a file and bring one in.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Add `export` per row: a save dialog, then `mariadb-dump` or `pg_dump` streamed to the file, with bytes written shown on the status line. Done when: the file restores into an empty database.
2. Add `import` per row: an open dialog, then the client reading the file, with progress by bytes read. Done when: an exported file imports back with the same tables.
3. Make both cancellable: cancel kills the client's whole process tree and deletes a partial export. Done when: cancelling leaves no client process and no partial file.
4. Report a failed import with the client's own error and the line it names. Done when: a broken dump reports the statement that failed.
5. Add `copy connection string` to the MariaDB and PostgreSQL service panes' CONNECTION cards if not already bound. Done when: the clipboard holds a working connection string without the password.

- [ ] Add `export` per row: a save dialog, then `mariadb-dump` or `pg_dump` streamed to the file, with bytes written shown on the status line. Done when: the file restores into an empty database.
- [ ] Add `import` per row: an open dialog, then the client reading the file, with progress by bytes read. Done when: an exported file imports back with the same tables.
- [ ] Make both cancellable: cancel kills the client's whole process tree and deletes a partial export. Done when: cancelling leaves no client process and no partial file. Cheaper substitute: killing only the direct child.
- [ ] Report a failed import with the client's own error and the line it names. Done when: a broken dump reports the statement that failed.
- [ ] Add `copy connection string` to the MariaDB and PostgreSQL service panes' CONNECTION cards if not already bound. Done when: the clipboard holds a working connection string without the password.
- [ ] Commit: `databases: export and import`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~DatabaseTransfer` reports all passed. The cancel test asserts no child process remains.
## Verification

- On a machine with both servers running, a database is created, exported, dropped and imported back on each from the pane alone.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
