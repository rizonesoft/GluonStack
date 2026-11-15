---
schema_version: 1
id: mariadb-multi-version
domain: 01-components
status: active
title: "TODO-04 -- MariaDB version switching"
depends_on: ["component-refresh"]
---

# TODO-04 -- MariaDB version switching

> **Goal:** Switching between installed MariaDB series is one command with the data of each series kept apart, and data can be moved from one series to another.

> **Current state:** Measured 2026-11-15. `scripts/Switch-MariaDBVersion.ps1` and its launcher exist (commit 32de5e8) and have not been tested against the legacy backlog's list: `-Version`, `-NoRestart`, `-ListVersions`, discovery, validation, data folder mapping, service reconfigure. `Migrate-MariaDBData.ps1` does not exist.

## Inputs

- `docs/legacy-todo.md`, MariaDB Multi-Version, Phase 8: the behaviours the script must have.
- D01 T03 §3 and §8: the series installed and the native service registration the switch must redo.

## Outcome

- `Switch-MariaDBVersion.ps1 -Version <series>` leaves the service running that series on its own data folder.
- `Migrate-MariaDBData.ps1` copies every database from one series to another.

**Adjacency:** list=applicable @ D01 T04 §1; document=not-applicable (a version switch with no document, report or notification); settings=not-applicable (a version switch with no document, report or notification); reporting=not-applicable (a version switch with no document, report or notification); notifications=not-applicable (a version switch with no document, report or notification); permissions=not-applicable (a version switch with no document, report or notification); audit=not-applicable (a version switch with no document, report or notification); exchange=applicable @ D01 T04 §2; reverse=applicable @ D01 T04 §1

**Adjacency rationale:** The list is `-ListVersions`; the reverse of a switch is a switch back, proven by the round-trip test; exchange is the migration helper.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Version switch verified against its contract | -- | [ ] |
| 2 | §2 | Data migration helper between series | §1 | [ ] |

## 1. Version switch verified against its contract

The script exists. Each behaviour the backlog lists is proven by a test, and what is missing is added.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Add `scripts/tests/Switch-MariaDBVersion.Tests.ps1` covering discovery, a missing `mariadbd.exe`, the series to data folder mapping and `-NoRestart`, against fake version folders. Done when: the tests run without a real server.
2. Fix each behaviour the tests show missing in `scripts/Switch-MariaDBVersion.ps1`. Done when: every test passes.
3. Print the current and target version and the data-not-shared warning before switching, and require `-Force` or a typed confirmation. Done when: a run without either changes nothing.
4. Verify the running version after the restart and switch back when it is not the target. Done when: a test with a broken target ends on the original version.

- [ ] Add `scripts/tests/Switch-MariaDBVersion.Tests.ps1` covering discovery, a missing `mariadbd.exe`, the series to data folder mapping and `-NoRestart`, against fake version folders. Done when: the tests run without a real server.
- [ ] Fix each behaviour the tests show missing in `scripts/Switch-MariaDBVersion.ps1`. Done when: every test passes.
- [ ] Print the current and target version and the data-not-shared warning before switching, and require `-Force` or a typed confirmation. Done when: a run without either changes nothing.
- [ ] Verify the running version after the restart and switch back when it is not the target. Done when: a test with a broken target ends on the original version.
- [ ] Commit: `mariadb: version switch tests and fixes`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Switch-MariaDBVersion.Tests.ps1 -CI"` reports 0 failed.

## 2. Data migration helper between series

Data is not shared between series, so moving up or down needs an export and an import that handles collation differences.

**Phase:** 1
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Migrate-MariaDBData.ps1` and its launcher with `-From`, `-To` and `-Database`. Done when: the help lists the three parameters with examples.
2. Dump from the source series with `mariadb-dump --routines --triggers --events`, then switch and import into the target. Done when: the target lists the migrated databases.
3. Rewrite collations the target does not know, listed in a table in the script, and report each rewrite. Done when: a dump using a newer default collation imports into the long-term series.
4. Leave the source data folder untouched and stop on the first import error, naming the statement. Done when: a failed import leaves the source series runnable.

- [ ] Create `scripts/Migrate-MariaDBData.ps1` and its launcher with `-From`, `-To` and `-Database`. Done when: the help lists the three parameters with examples.
- [ ] Dump from the source series with `mariadb-dump --routines --triggers --events`, then switch and import into the target. Done when: the target lists the migrated databases.
- [ ] Rewrite collations the target does not know, listed in a table in the script, and report each rewrite. Done when: a dump using a newer default collation imports into the long-term series.
- [ ] Leave the source data folder untouched and stop on the first import error, naming the statement. Done when: a failed import leaves the source series runnable.
- [ ] Commit: `mariadb: data migration helper`

**Test checkpoint:** `pwsh scripts/Migrate-MariaDBData.ps1 -From <a> -To <b> -WhatIf` lists the databases it would move and changes nothing.
## Verification

- Switching from one installed series to another and back leaves both data folders intact and the service running.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
