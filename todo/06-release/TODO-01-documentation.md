---
schema_version: 1
id: documentation
domain: 06-release
status: active
title: "TODO-01 -- Documentation"
depends_on: ["installer"]
---

# TODO-01 -- Documentation

> **Goal:** Someone new can install GluonStack, start a project and fix the common problems from the documentation alone, and a contributor can build and test it.

> **Current state:** Measured 2026-11-15. `README.md` describes a Python control panel that no longer exists, hard-coded `C:\isotone` paths and script names that changed. There is no changelog, contributing guide, security policy or user guide. `gluon-control/ERROR_HANDLING.md` and `config/README.md` exist.

## Inputs

- `docs/legacy-todo.md`, GitHub and Repository, and Documentation.
- The global writing rules: answer first, question-shaped headings, short active sentences, every figure sourced, no em dashes.

## Outcome

- Every command and path the documentation names exists and runs.
- The README's component list is the generated block from the manifest.

**Adjacency:** all=not-applicable (documentation: no record, setting or reversal of its own)

**Adjacency rationale:** The only generated part is the README's component block, owned by D01 T01 §9.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | README rewritten for GluonStack | -- | [ ] |
| 2 | §2 | Changelog, contributing, security and templates | §1 | [ ] |
| 3 | §3 | User guides | §1 | [ ] |
| 4 | §4 | Architecture and conventions for contributors | §3 | [ ] |

## 1. README rewritten for GluonStack

The front page.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Rewrite `README.md`: what GluonStack is in two sentences, a screenshot of the control panel, a quick start, what is in the stack (the generated block), switching versions, updating, building from source, licence. Done when: a reader can install and open `http://localhost` from the quick start alone.
2. Capture the control panel and the web dashboard to `docs/images/` from the built application. Done when: the images show the real application in the chosen design.
3. Add build and licence badges that resolve. Done when: each badge loads.

- [ ] Rewrite `README.md`: what GluonStack is in two sentences, a screenshot of the control panel, a quick start, what is in the stack (the generated block), switching versions, updating, building from source, licence. Done when: a reader can install and open `http://localhost` from the quick start alone.
- [ ] Capture the control panel and the web dashboard to `docs/images/` from the built application. Done when: the images show the real application in the chosen design. Cheaper substitute: a mock-up.
- [ ] Add build and licence badges that resolve. Done when: each badge loads.
- [ ] Commit: `docs: README`

**Test checkpoint:** Every relative link and image path in `README.md` resolves: `python scripts/check-doc-links.py README.md` exits 0.

## 2. Changelog, contributing, security and templates

What a public repository is expected to have.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Create `CHANGELOG.md` in Keep a Changelog form, with the rename and the modernisation as the first entry. Done when: the file lists the changes since the last Isotone release.
2. Create `CONTRIBUTING.md`: prerequisites, `pwsh scripts/check-all.ps1`, the TODO workflow, the script conventions, the design contract. Done when: a fresh clone passes the gate by following it.
3. Create `SECURITY.md` with a private reporting route. Done when: it names how to report and what to expect.
4. Create `.github/ISSUE_TEMPLATE/bug_report.md`, `feature_request.md` and `.github/PULL_REQUEST_TEMPLATE.md`. Done when: GitHub offers the templates.

- [ ] Create `CHANGELOG.md` in Keep a Changelog form, with the rename and the modernisation as the first entry. Done when: the file lists the changes since the last Isotone release.
- [ ] Create `CONTRIBUTING.md`: prerequisites, `pwsh scripts/check-all.ps1`, the TODO workflow, the script conventions, the design contract. Done when: a fresh clone passes the gate by following it.
- [ ] Create `SECURITY.md` with a private reporting route. Done when: it names how to report and what to expect.
- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.md`, `feature_request.md` and `.github/PULL_REQUEST_TEMPLATE.md`. Done when: GitHub offers the templates.
- [ ] Commit: `docs: changelog, contributing, security, templates`

**Test checkpoint:** `python scripts/check-doc-links.py CONTRIBUTING.md SECURITY.md CHANGELOG.md` exits 0.

## 3. User guides

The questions people actually ask, one page each, answer first.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Write `docs/guide/getting-started.md`: install, first start, first site. Done when: following it on a clean machine works.
2. Write `docs/guide/switching-versions.md` (PHP and MariaDB) and `docs/guide/updating.md` (the Updates pane and `Update-Components.ps1`). Done when: each command shown runs as written.
3. Write `docs/guide/sites-and-https.md`, `docs/guide/databases.md` (MariaDB, PostgreSQL, backup, restore) and `docs/guide/mail.md`. Done when: each page's steps were run against the built application.
4. Write `docs/guide/troubleshooting.md` from the mapped failure messages of D03 T04 §3: busy ports, a service that will not start, hosts file, certificates. Done when: every message the application can show has an entry.
5. Add `scripts/check-doc-links.py` to the gate. Done when: a broken relative link fails `check-all.ps1`.

- [ ] Write `docs/guide/getting-started.md`: install, first start, first site. Done when: following it on a clean machine works.
- [ ] Write `docs/guide/switching-versions.md` (PHP and MariaDB) and `docs/guide/updating.md` (the Updates pane and `Update-Components.ps1`). Done when: each command shown runs as written.
- [ ] Write `docs/guide/sites-and-https.md`, `docs/guide/databases.md` (MariaDB, PostgreSQL, backup, restore) and `docs/guide/mail.md`. Done when: each page's steps were run against the built application.
- [ ] Write `docs/guide/troubleshooting.md` from the mapped failure messages of D03 T04 §3: busy ports, a service that will not start, hosts file, certificates. Done when: every message the application can show has an entry.
- [ ] Add `scripts/check-doc-links.py` to the gate. Done when: a broken relative link fails `check-all.ps1`.
- [ ] Commit: `docs: user guides`

**Test checkpoint:** `python scripts/check-doc-links.py docs/guide` exits 0.

## 4. Architecture and conventions for contributors

How the pieces fit, for the next person to change them.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Write `docs/architecture.md`: the control panel's regions, command registry, services and how it calls the scripts; the manifest and updater; the installer. Done when: each named type and file exists.
2. Bring `docs/script-conventions.md` up to date with the common module, Pester and the analyzer settings. Done when: a new script written from it passes the gate.
3. Fold `gluon-control/ERROR_HANDLING.md` into `docs/architecture.md` and delete it. Done when: one document describes error handling.

- [ ] Write `docs/architecture.md`: the control panel's regions, command registry, services and how it calls the scripts; the manifest and updater; the installer. Done when: each named type and file exists.
- [ ] Bring `docs/script-conventions.md` up to date with the common module, Pester and the analyzer settings. Done when: a new script written from it passes the gate.
- [ ] Fold `gluon-control/ERROR_HANDLING.md` into `docs/architecture.md` and delete it. Done when: one document describes error handling.
- [ ] Commit: `docs: architecture and conventions`

**Test checkpoint:** `python scripts/check-doc-links.py docs` exits 0.
## Verification

- `pwsh scripts/check-all.ps1` exits 0 with the link check in it.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
