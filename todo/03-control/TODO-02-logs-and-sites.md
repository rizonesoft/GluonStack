---
schema_version: 1
id: control-logs-sites
domain: 03-control
status: active
title: "TODO-02 -- Logs and Sites panes"
depends_on: ["control-panel-shell"]
---

# TODO-02 -- Logs and Sites panes

> **Goal:** The Logs pane reads any log under `logs\` live, and the Sites pane creates, edits and removes virtual hosts including their hosts file entry and certificate.

> **Current state:** Measured 2026-11-15. `gluon-control/Views/LogsView.xaml` (62 lines) and `LogsViewModel.cs` load placeholder text. No virtual host management exists in the application; `config/apache/extra/` holds the default host's file and the scripts write nothing per site.

## Inputs

- `docs/design/SPEC.md` section 6.6, Logs and Sites.
- D02 T01 §3: the log well. D02 T02: pane host, commands, dialog.

## Outcome

- A site created in the pane answers in a browser at its name, over HTTPS when TLS was ticked, and removing it removes its host entry and configuration but not its files.

**Adjacency:** list=applicable @ D03 T02 §4; document=not-applicable (no such surface for logs or local sites); settings=applicable @ D03 T02 §5; reporting=not-applicable (no such surface for logs or local sites); notifications=not-applicable (no such surface for logs or local sites); permissions=applicable @ D03 T02 §3; audit=applicable @ D03 T02 §5; exchange=not-applicable (no such surface for logs or local sites); reverse=applicable @ D03 T02 §5

**Adjacency rationale:** The list is the sites table; the reverse of adding a site is removing it; the permission is the single elevation the hosts file needs and its refusal; a site's settings are its dialog's fields; each change is on the status line and in the control log.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Logs pane: file select, level filter and live tail | -- | [ ] |
| 2 | §2 | Log search | §1 | [ ] |
| 3 | §3 | Virtual host files and the hosts file | -- | [ ] |
| 4 | §4 | Sites pane and table | §3 | [ ] |
| 5 | §5 | New site, edit and remove, with TLS | §4 | [ ] |

## 1. Logs pane: file select, level filter and live tail

Every log the stack writes, in one place, without loading whole files.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Logs) and `docs/design/reference/control-panel.dc.html`.
**Job:** Find out what a service just did or why it failed.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Rebuild `gluon-control/Views/LogsView.xaml` as section 6.6: file select over every file under `logs\`, level filter, `live`, `open folder`, the log well. Done when: selecting a file shows its tail.
2. Classify lines as warning or error per log format (Apache, PHP, MariaDB, PostgreSQL, Mailpit, the product's own) in `gluon-control/Services/LogLevels.cs`. Done when: the filter `errors` shows only error lines of each format.
3. Follow the file with a `FileSystemWatcher` plus a size poll, surviving rotation and truncation. Done when: a rotated log keeps tailing the new file.
4. Register `log <service>` and `go logs`. Done when: `log apache` opens Apache's error log.

- [ ] Rebuild `gluon-control/Views/LogsView.xaml` as section 6.6: file select over every file under `logs\`, level filter, `live`, `open folder`, the log well. Done when: selecting a file shows its tail.
- [ ] Classify lines as warning or error per log format (Apache, PHP, MariaDB, PostgreSQL, Mailpit, the product's own) in `gluon-control/Services/LogLevels.cs`. Done when: the filter `errors` shows only error lines of each format.
- [ ] Follow the file with a `FileSystemWatcher` plus a size poll, surviving rotation and truncation. Done when: a rotated log keeps tailing the new file. Cheaper substitute: re-reading the whole file on each change.
- [ ] Register `log <service>` and `go logs`. Done when: `log apache` opens Apache's error log.
- [ ] Commit: `logs: pane with live tail and filter`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~LogLevels` reports all passed. A rotation test passes.

## 2. Log search

Find a string in a large log.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Logs) and `docs/design/reference/control-panel.dc.html`.
**Job:** Jump to the line that matters.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Add the search input: matches underlined in `phosphor`, Enter to the next, Shift Enter to the previous, a count on the status line. Done when: searching a 50 MB log returns the first match in under two seconds.
2. Search backwards from the tail in chunks without loading the file. Done when: memory stays flat while searching.
3. Treat the text as literal unless it is wrapped in slashes, then as a regular expression with a timeout. Done when: a catastrophic pattern is cancelled and reported.

- [ ] Add the search input: matches underlined in `phosphor`, Enter to the next, Shift Enter to the previous, a count on the status line. Done when: searching a 50 MB log returns the first match in under two seconds.
- [ ] Search backwards from the tail in chunks without loading the file. Done when: memory stays flat while searching.
- [ ] Treat the text as literal unless it is wrapped in slashes, then as a regular expression with a timeout. Done when: a catastrophic pattern is cancelled and reported.
- [ ] Commit: `logs: search`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~LogSearch` reports all passed.

## 3. Virtual host files and the hosts file

The service behind Sites. One file per site, a tested configuration before any reload, and one elevation for the hosts file.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Create `gluon-control/Services/Sites/SiteStore.cs`: read and write one `config/apache/extra/sites/<name>.conf` per site from a template, and list them. Done when: a written site reads back with the same fields.
2. Include `extra/sites/*.conf` from `config/apache/httpd.conf`. Done when: `httpd -t` passes with zero and with several sites.
3. Run `httpd -t` on the new configuration before reloading, and put the previous file back when it fails. Done when: a site with a bad document root is refused and Apache keeps serving.
4. Add and remove the site's `127.0.0.1` line in the hosts file through one elevated helper call, inside a marked block the application owns. Done when: lines outside the block are never touched and a declined elevation is reported, with the site left unsaved.
5. Add `SiteStoreTests` for the round-trip, the failed test rollback and the hosts block. Done when: the tests pass against a temporary folder and a fake hosts file.

- [ ] Create `gluon-control/Services/Sites/SiteStore.cs`: read and write one `config/apache/extra/sites/<name>.conf` per site from a template, and list them. Done when: a written site reads back with the same fields.
- [ ] Include `extra/sites/*.conf` from `config/apache/httpd.conf`. Done when: `httpd -t` passes with zero and with several sites.
- [ ] Run `httpd -t` on the new configuration before reloading, and put the previous file back when it fails. Done when: a site with a bad document root is refused and Apache keeps serving. Cheaper substitute: reloading and hoping.
- [ ] Add and remove the site's `127.0.0.1` line in the hosts file through one elevated helper call, inside a marked block the application owns. Done when: lines outside the block are never touched and a declined elevation is reported, with the site left unsaved.
- [ ] Add `SiteStoreTests` for the round-trip, the failed test rollback and the hosts block. Done when: the tests pass against a temporary folder and a fake hosts file.
- [ ] Commit: `sites: virtual host store and hosts file`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~SiteStore` reports all passed.

## 4. Sites pane and table

The list of sites.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Sites) and `docs/design/reference/control-panel.dc.html`.
**Job:** See every local site and open one.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Create `gluon-control/Views/SitesView.xaml` as section 6.6: heading, `new site`, the table with name, document root, PHP version, `tls`, `edit`, `remove`. Done when: the default site and every created site are listed.
2. Make the name a link that opens the site in the browser. Done when: the link opens `http://<name>` or `https://<name>`.
3. Bind the `sites` list entry's note to the count and register `go sites`. Done when: the note shows the number of sites.
4. Show the empty state when only the default site exists. Done when: the sentence and `new site` appear.

- [ ] Create `gluon-control/Views/SitesView.xaml` as section 6.6: heading, `new site`, the table with name, document root, PHP version, `tls`, `edit`, `remove`. Done when: the default site and every created site are listed.
- [ ] Make the name a link that opens the site in the browser. Done when: the link opens `http://<name>` or `https://<name>`.
- [ ] Bind the `sites` list entry's note to the count and register `go sites`. Done when: the note shows the number of sites.
- [ ] Show the empty state when only the default site exists. Done when: the sentence and `new site` appear.
- [ ] Commit: `sites: pane and table`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~SitesViewModel` reports all passed.

## 5. New site, edit and remove, with TLS

Create, change and reverse.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (sections 6.4 (dialog) and 6.6, Sites) and `docs/design/reference/control-panel.dc.html`.
**Job:** Add a local site with its own name, PHP version and certificate.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** A dialog over the main window.

**Build order:**

1. Add the site dialog: server name, document root with a folder picker, PHP version, `tls`. Done when: saving creates the site and it answers in a browser.
2. Create a self-signed certificate for a `tls` site with the bundled OpenSSL into `ssl\<name>`, and offer to trust it for the current user. Done when: the site answers over HTTPS and, once trusted, without a browser warning.
3. Serve a per-site PHP version through that version's handler. Done when: two sites on different PHP versions report their own version.
4. Add `remove` with a confirmation that states the document root is kept. Done when: the configuration, hosts line and certificate are gone and the folder remains.
5. Register `new site <name>`. Done when: the command opens the dialog with the name filled in.

- [ ] Add the site dialog: server name, document root with a folder picker, PHP version, `tls`. Done when: saving creates the site and it answers in a browser.
- [ ] Create a self-signed certificate for a `tls` site with the bundled OpenSSL into `ssl\<name>`, and offer to trust it for the current user. Done when: the site answers over HTTPS and, once trusted, without a browser warning.
- [ ] Serve a per-site PHP version through that version's handler. Done when: two sites on different PHP versions report their own version.
- [ ] Add `remove` with a confirmation that states the document root is kept. Done when: the configuration, hosts line and certificate are gone and the folder remains. Cheaper substitute: deleting the document root.
- [ ] Register `new site <name>`. Done when: the command opens the dialog with the name filled in.
- [ ] Commit: `sites: new, edit, remove and TLS`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~SitesViewModel` reports all passed. A manual create with `tls` answers over HTTPS.
## Verification

- A site is created with TLS, opened, edited to another PHP version and removed from the pane alone, and `httpd -t` passes after each step.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
