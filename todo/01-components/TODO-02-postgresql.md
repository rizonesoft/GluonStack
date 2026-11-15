---
schema_version: 1
id: postgresql
domain: 01-components
status: active
title: "TODO-02 -- PostgreSQL in the stack"
depends_on: ["component-manifest"]
---

# TODO-02 -- PostgreSQL in the stack

> **Goal:** PostgreSQL is a first-class component: installed from the manifest, initialised, registered as `GluonPostgreSQL`, reachable from PHP and Adminer, backed up and shown in the control panel.

> **Current state:** Measured 2026-11-15. The stack has MariaDB and SQLite only. `adminer/` already supports PostgreSQL. `config/php/php.ini` does not enable `pdo_pgsql` or `pgsql`. No script or control panel code knows PostgreSQL.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: PostgreSQL is added at its latest stable major; Adminer is its web client.
- D01 T01: the manifest and the updater the component is installed through.

## Outcome

- `scripts/Start-Services.ps1` starts `GluonPostgreSQL` and `psql -c "select version()"` answers.
- A PHP page connects with `pdo_pgsql`, and the control panel lists the service.

**Adjacency:** list=not-applicable (a database server with no document or report of its own); document=not-applicable (a database server with no document or report of its own); settings=applicable @ D01 T02 §2; reporting=not-applicable (a database server with no document or report of its own); notifications=not-applicable (a database server with no document or report of its own); permissions=applicable @ D01 T02 §2; audit=not-applicable (a database server with no document or report of its own); exchange=applicable @ D01 T02 §6; reverse=applicable @ D01 T02 §3

**Adjacency rationale:** Settings are the cluster's `postgresql.conf` template; exchange is dump and restore; the reverse of registering the service is unregistering it; permissions are the local-only `pg_hba.conf` and its refusal of a remote address.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | PostgreSQL in the manifest, fetched by the updater | -- | [ ] |
| 2 | §2 | Cluster initialisation and configuration | §1 | [ ] |
| 3 | §3 | Service registration and control | §2 | [ ] |
| 4 | §4 | PHP drivers for PostgreSQL | §3 | [ ] |
| 5 | §5 | Adminer preset for PostgreSQL | §4 | [ ] |
| 6 | §6 | PostgreSQL backup and restore scripts | §3 | [ ] |
| 7 | §7 | PostgreSQL in the control panel's service model | §3 | [ ] |

## 1. PostgreSQL in the manifest, fetched by the updater

The component arrives the same way every other one does.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add a `postgresql` entry to `config/components.json` with the EDB binaries zip as its source and its resolver feed. Done when: `Update-Components.ps1 -Check` lists `postgresql` as not installed.
2. Teach the updater to install a component whose folder is absent. Done when: `-Component postgresql` creates `postgresql\` with `bin\postgres.exe`.
3. Ignore `/postgresql` and its data folder in `.gitignore`. Done when: `git status --short` is clean after the install.

- [ ] Add a `postgresql` entry to `config/components.json` with the EDB binaries zip as its source and its resolver feed. Done when: `Update-Components.ps1 -Check` lists `postgresql` as not installed.
- [ ] Teach the updater to install a component whose folder is absent. Done when: `-Component postgresql` creates `postgresql\` with `bin\postgres.exe`.
- [ ] Ignore `/postgresql` and its data folder in `.gitignore`. Done when: `git status --short` is clean after the install.
- [ ] Commit: `postgresql: manifest entry and install`

**Test checkpoint:** `postgresql\bin\postgres.exe --version` prints the version the manifest records.

## 2. Cluster initialisation and configuration

A fresh cluster with safe defaults: local connections only, UTF-8, a password for the superuser.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Initialize-PostgreSQL.ps1` and its launcher: run `initdb` into `postgresql\data` with UTF-8, the `postgres` superuser and `scram-sha-256`. Done when: the data folder exists and `pg_controldata` reports the cluster.
2. Write `config/postgresql/postgresql.conf` and `pg_hba.conf` templates (port 5432, `listen_addresses = 'localhost'`, logs to `logs\postgresql`) and apply them at initialisation. Done when: a connection from another machine's address is refused.
3. Refuse to initialise over an existing cluster unless `-Force` is given, and then move the old data folder aside instead of deleting it. Done when: a second run without `-Force` exits 1 and the data is untouched.
4. Generate the superuser password, store it with the other credentials in `config/gluonstack-settings.json`, and never print it. Done when: the script's output and log contain no password.

- [ ] Create `scripts/Initialize-PostgreSQL.ps1` and its launcher: run `initdb` into `postgresql\data` with UTF-8, the `postgres` superuser and `scram-sha-256`. Done when: the data folder exists and `pg_controldata` reports the cluster.
- [ ] Write `config/postgresql/postgresql.conf` and `pg_hba.conf` templates (port 5432, `listen_addresses = 'localhost'`, logs to `logs\postgresql`) and apply them at initialisation. Done when: a connection from another machine's address is refused.
- [ ] Refuse to initialise over an existing cluster unless `-Force` is given, and then move the old data folder aside instead of deleting it. Done when: a second run without `-Force` exits 1 and the data is untouched. Cheaper substitute: `Remove-Item -Recurse` on the data folder.
- [ ] Generate the superuser password, store it with the other credentials in `config/gluonstack-settings.json`, and never print it. Done when: the script's output and log contain no password.
- [ ] Commit: `postgresql: cluster initialisation`

**Test checkpoint:** `pwsh scripts/Initialize-PostgreSQL.ps1` followed by `postgresql\bin\pg_ctl status -D postgresql\data` reports a cluster, and a second run exits 1.

## 3. Service registration and control

The service joins the same four scripts that register, unregister, start and stop the others.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Register `GluonPostgreSQL` with `pg_ctl register` in `scripts/Register-Services.ps1`. Done when: `Get-Service GluonPostgreSQL` exists after registration.
2. Unregister it in `scripts/Unregister-Services.ps1`. Done when: the service is gone and the data folder is untouched.
3. Start and stop it in `scripts/Start-Services.ps1` and `scripts/Stop-Services.ps1`, skipping it when the component is not installed. Done when: both scripts succeed on a machine without PostgreSQL.
4. Report a busy port 5432 with the process that holds it. Done when: with the port taken, the start fails naming the process.

- [ ] Register `GluonPostgreSQL` with `pg_ctl register` in `scripts/Register-Services.ps1`. Done when: `Get-Service GluonPostgreSQL` exists after registration.
- [ ] Unregister it in `scripts/Unregister-Services.ps1`. Done when: the service is gone and the data folder is untouched.
- [ ] Start and stop it in `scripts/Start-Services.ps1` and `scripts/Stop-Services.ps1`, skipping it when the component is not installed. Done when: both scripts succeed on a machine without PostgreSQL.
- [ ] Report a busy port 5432 with the process that holds it. Done when: with the port taken, the start fails naming the process.
- [ ] Commit: `postgresql: GluonPostgreSQL service`

**Test checkpoint:** `pwsh scripts/Start-Services.ps1` then `postgresql\bin\pg_isready -p 5432` prints `accepting connections`.

## 4. PHP drivers for PostgreSQL

PHP ships the drivers; they only need enabling, in the template every PHP version's `php.ini` is made from.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Enable `extension=pdo_pgsql` and `extension=pgsql` in `config/php/php.ini`. Done when: `php -m` lists both.
2. Apply the same in `scripts/Switch-PHPVersion.ps1`'s per-version configuration. Done when: both extensions load after a version switch.
3. Add `default/tests/pgsql.php`, which connects with `pdo_pgsql` and prints the server version. Done when: the page shows the version with the service running and a plain message with it stopped.

- [ ] Enable `extension=pdo_pgsql` and `extension=pgsql` in `config/php/php.ini`. Done when: `php -m` lists both.
- [ ] Apply the same in `scripts/Switch-PHPVersion.ps1`'s per-version configuration. Done when: both extensions load after a version switch.
- [ ] Add `default/tests/pgsql.php`, which connects with `pdo_pgsql` and prints the server version. Done when: the page shows the version with the service running and a plain message with it stopped.
- [ ] Commit: `postgresql: PHP pdo_pgsql and pgsql enabled`

**Test checkpoint:** `php\php.exe -m` prints both `pdo_pgsql` and `pgsql`.

## 5. Adminer preset for PostgreSQL

Adminer is the PostgreSQL web client. A link that opens it on the PostgreSQL driver saves the user the dropdown.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add a `?pgsql=127.0.0.1` entry point for Adminer in `config/apache/extra/httpd-gluonstack-default.conf` or `adminer/index.php`. Done when: `http://localhost/adminer/?pgsql=127.0.0.1` opens the PostgreSQL login.
2. Keep the MariaDB and SQLite entry points working. Done when: each driver's login still opens.

- [ ] Add a `?pgsql=127.0.0.1` entry point for Adminer in `config/apache/extra/httpd-gluonstack-default.conf` or `adminer/index.php`. Done when: `http://localhost/adminer/?pgsql=127.0.0.1` opens the PostgreSQL login.
- [ ] Keep the MariaDB and SQLite entry points working. Done when: each driver's login still opens.
- [ ] Commit: `postgresql: Adminer entry point`

**Test checkpoint:** `curl -s -o NUL -w "%{http_code}" "http://localhost/adminer/?pgsql=127.0.0.1"` prints `200` with Apache running.

## 6. PostgreSQL backup and restore scripts

The stack backs up MariaDB; PostgreSQL gets the same two operations.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Backup-PostgreSQL.ps1` and its launcher: `pg_dumpall` roles and one `pg_dump -Fc` per database into `backups\postgresql\<timestamp>`. Done when: the folder holds one file per database and a roles file.
2. Create `scripts/Restore-PostgreSQL.ps1`: restore one database from a named backup, refusing to overwrite an existing database unless `-Force`. Done when: a restore into an existing name without `-Force` exits 1 and changes nothing.
3. Register the dump command in the manifest so the updater's pre-update dump (D01 T01 §6) uses it. Done when: an update of `postgresql` writes a pre-update dump.

- [ ] Create `scripts/Backup-PostgreSQL.ps1` and its launcher: `pg_dumpall` roles and one `pg_dump -Fc` per database into `backups\postgresql\<timestamp>`. Done when: the folder holds one file per database and a roles file.
- [ ] Create `scripts/Restore-PostgreSQL.ps1`: restore one database from a named backup, refusing to overwrite an existing database unless `-Force`. Done when: a restore into an existing name without `-Force` exits 1 and changes nothing.
- [ ] Register the dump command in the manifest so the updater's pre-update dump (D01 T01 §6) uses it. Done when: an update of `postgresql` writes a pre-update dump.
- [ ] Commit: `postgresql: backup and restore scripts`

**Test checkpoint:** `pwsh scripts/Backup-PostgreSQL.ps1` creates a timestamped folder under `backups\postgresql` containing `roles.sql`.

## 7. PostgreSQL in the control panel's service model

The control panel's service list is hard-coded to three services. It reads the installed services instead, so PostgreSQL appears and a missing component does not.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Make `gluon-control/Services/ServiceManager.cs` build its list from the manifest entries whose `kind` is `service`. Done when: the dashboard shows PostgreSQL when installed and omits it when not.
2. Add version and port lookup for PostgreSQL. Done when: the service shows its version and 5432.
3. Add tests for the list with and without the component. Done when: `dotnet test` passes and fails when the list is hard-coded again.

- [ ] Make `gluon-control/Services/ServiceManager.cs` build its list from the manifest entries whose `kind` is `service`. Done when: the dashboard shows PostgreSQL when installed and omits it when not. Cheaper substitute: adding a fourth hard-coded entry.
- [ ] Add version and port lookup for PostgreSQL. Done when: the service shows its version and 5432.
- [ ] Add tests for the list with and without the component. Done when: `dotnet test` passes and fails when the list is hard-coded again.
- [ ] Commit: `control: services read from the manifest, PostgreSQL included`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ServiceManager` reports all passed.
## Verification

- With the stack started, `psql`, a PHP page and Adminer each reach PostgreSQL, and `Stop-Services.ps1` stops it cleanly.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
