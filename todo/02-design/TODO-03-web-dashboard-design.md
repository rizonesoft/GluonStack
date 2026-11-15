---
schema_version: 1
id: web-dashboard-design
domain: 02-design
status: active
title: "TODO-03 -- Web dashboard in the chosen design"
depends_on: ["quality-gates"]
---

# TODO-03 -- Web dashboard in the chosen design

> **Goal:** The pages the stack serves at `http://localhost` follow the design contract and show real state.

> **Current state:** Measured 2026-11-15. `default/index.php` (228 lines) and `default/control/` (an index and pages for dashboard, services, databases, logs, security, scripts, mailtest and a stub `files.php`) use their own inline styles and colours. `default/assets/tokens.css`, the fonts under `default/assets/fonts/`, `default/assets/gluonstack-mark.svg` and `default/favicon.ico` were generated on 2026-11-15 and are linked by no page yet.

## Inputs

- `docs/design/SPEC.md` section 10.
- `default/assets/tokens.css`: generated, the only source of values.

## Outcome

- `http://localhost` shows the landing page of section 10 with live versions.
- `python scripts/design-lint.py` reports no violation under `default/`.

**Adjacency:** list=applicable @ D02 T03 §2; document=not-applicable (read-only pages over state owned by the services); settings=not-applicable (read-only pages over state owned by the services); reporting=not-applicable (read-only pages over state owned by the services); notifications=not-applicable (read-only pages over state owned by the services); permissions=not-applicable (read-only pages over state owned by the services); audit=not-applicable (read-only pages over state owned by the services); exchange=not-applicable (read-only pages over state owned by the services); reverse=not-applicable (read-only pages over state owned by the services)

**Adjacency rationale:** The pages list services, sites, databases and logs and change nothing; every write belongs to the control panel application.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Landing page | T01 §1 | [ ] |
| 2 | §2 | Read-only web control panel | §1 | [ ] |
| 3 | §3 | Narrow widths | §2 | [ ] |

## 1. Landing page

The first thing a new install shows.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 10, Landing) and `docs/design/reference/other-surfaces.dc.html`.
**Job:** Confirm the stack works and reach its tools.
**Treatment:** Tokens from `default/assets/tokens.css` only; no raw hex value in a page.
**Chrome:** A browser page served by the stack's own Apache; no application chrome.

**Build order:**

1. Rewrite `default/index.php` as section 10's landing: mark, wordmark, heading, the link list, the versions block. Done when: the page matches the reference board's web dashboard.
2. Link `assets/tokens.css` and a new `assets/site.css` that uses only its variables. Done when: the lint reports no literal in either.
3. Read each link's service state at request time and show a stopped one as `muted` text, not a link. Done when: with Mailpit stopped its row reads `stopped` and has no anchor.
4. Read the PHP and Apache versions and the document root at request time. Done when: the block changes after a PHP version switch.

- [ ] Rewrite `default/index.php` as section 10's landing: mark, wordmark, heading, the link list, the versions block. Done when: the page matches the reference board's web dashboard.
- [ ] Link `assets/tokens.css` and a new `assets/site.css` that uses only its variables. Done when: the lint reports no literal in either.
- [ ] Read each link's service state at request time and show a stopped one as `muted` text, not a link. Done when: with Mailpit stopped its row reads `stopped` and has no anchor. Cheaper substitute: always rendering the link.
- [ ] Read the PHP and Apache versions and the document root at request time. Done when: the block changes after a PHP version switch.
- [ ] Commit: `web: landing page`

**Test checkpoint:** `curl -s http://localhost/ | findstr /C:"It works."` finds the heading and `python scripts/design-lint.py` reports nothing under `default/index.php`.

## 2. Read-only web control panel

The same shape as the application, in the browser, showing state without changing it.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 10, Web control panel) and `docs/design/reference/other-surfaces.dc.html`.
**Job:** Look at the stack's state from a browser.
**Treatment:** Tokens from `default/assets/tokens.css` only; no raw hex value in a page.
**Chrome:** A browser page served by the stack's own Apache; no application chrome.

**Build order:**

1. Rebuild `default/control/index.php` with the header and left list of sections 6.1 and 6.2 as links. Done when: each entry opens its pane.
2. Restyle the panes under `default/control/pages/` on `site.css`: services, sites, databases, logs, PHP information. Done when: no page carries an inline colour or font.
3. Remove the pages that write (`scripts.php`, `mailtest.php`, `security.php`) or reduce them to read-only views, and say on each pane that changes are made in the application. Done when: no form on the web control panel changes the stack.
4. Replace the stub `files.php` with a list of the folders under `www\` and their sizes. Done when: the page lists the real folders.

- [ ] Rebuild `default/control/index.php` with the header and left list of sections 6.1 and 6.2 as links. Done when: each entry opens its pane.
- [ ] Restyle the panes under `default/control/pages/` on `site.css`: services, sites, databases, logs, PHP information. Done when: no page carries an inline colour or font.
- [ ] Remove the pages that write (`scripts.php`, `mailtest.php`, `security.php`) or reduce them to read-only views, and say on each pane that changes are made in the application. Done when: no form on the web control panel changes the stack. Cheaper substitute: leaving a script runner reachable from any page that can reach localhost.
- [ ] Replace the stub `files.php` with a list of the folders under `www\` and their sizes. Done when: the page lists the real folders.
- [ ] Commit: `web: read-only control panel`

**Test checkpoint:** `git grep -n -E 'shell_exec|exec\(|proc_open' -- default/control` prints nothing and each pane returns HTTP 200.

## 3. Narrow widths

The pages are opened from phones on the same network when testing sites.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 10, last item) and `docs/design/reference/other-surfaces.dc.html`.
**Job:** Use the dashboard on a phone.
**Treatment:** Tokens from `default/assets/tokens.css` only; no raw hex value in a page.
**Chrome:** A browser page served by the stack's own Apache; no application chrome.

**Build order:**

1. Stack the list above the pane under 720 pixels in `default/assets/site.css`. Done when: at 390 pixels wide nothing scrolls sideways.
2. Put each table in its own horizontally scrolling box. Done when: a wide table scrolls inside its box.
3. Keep link rows at least 44 pixels tall. Done when: every row meets the size at every width.

- [ ] Stack the list above the pane under 720 pixels in `default/assets/site.css`. Done when: at 390 pixels wide nothing scrolls sideways.
- [ ] Put each table in its own horizontally scrolling box. Done when: a wide table scrolls inside its box.
- [ ] Keep link rows at least 44 pixels tall. Done when: every row meets the size at every width.
- [ ] Commit: `web: narrow widths`

**Test checkpoint:** A page load at 390 pixels wide in a headless browser reports `document.documentElement.scrollWidth <= 390` for `/` and `/control/`.
## Verification

- `python scripts/design-lint.py` exits 0 for `default/` and every page under it returns HTTP 200.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
