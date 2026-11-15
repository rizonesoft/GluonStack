# GluonStack design contract

Set 2026-11-15 from the owner's choice in [direction.md](./direction.md): the G mark from direction B, the colours and layout of direction C. Every user-facing surface is built against this file. A TODO section with `**Surface:** yes` names the part of this file it implements in its `**Fidelity:**` line.

## 1. How the contract binds

1. **Tokens only.** Every colour, font, size, spacing, radius and layout dimension on a surface comes from `docs/design/tokens.json` through its generated file: `Themes/Tokens.xaml` in the control panel, `default/assets/tokens.css` on the web dashboard. A literal hex value, font name or pixel size on a control is a defect. A value the tokens lack is added to `tokens.json` and regenerated.
2. **One source per asset.** Icons are rendered from `assets/brand/svg/` by `scripts/build-brand-assets.py`; fonts live in `assets/fonts/`. Nothing is redrawn, recoloured or resized by hand.
3. **Everything shown works.** Every control this file lists for a surface is either working with real data or absent. A disabled control, a placeholder pane or a "coming soon" label is not a state this contract has.
4. **State is never colour alone.** A state is always shape plus word: `●` running, `○` stopped, `◐` starting or stopping, `✕` failed, each followed by the word.
5. **Keyboard first.** Every action has a typed command (section 6.3) and every control is reachable by Tab in reading order with a visible focus ring. Nothing needs a pointer.
6. **Contrast.** Text is at least 4.5:1 on its background, and 3:1 at 24 pixels and above. The token pairs in section 2 meet this; a new pair is checked before it is added.
7. **A change to the design is a change to this file first**, then to the tokens, then to the surface. The reference boards are a picture of the target; where a board and this file disagree, this file is right and the board is corrected.

Checks that hold the contract: `python scripts/generate-ui-tokens.py --check` and `python scripts/build-brand-assets.py --check` (generated files match their sources), and `python scripts/design-lint.py` (no literal colour, font or size on a surface; D02 T01 §2 builds it and adds all three to `scripts/check-all.ps1`).

## 2. Tokens

The values are in `docs/design/tokens.json`; this table gives their meaning. Names are written here as in the JSON; XAML keys are the same name in Pascal case with a `Brush`, `Color`, `Size` or `Font` suffix, and CSS variables are the name with a leading `--`.

| Token | Value | Use | On |
| ----- | ----- | --- | -- |
| `void` | `#07090A` | Window and page background | |
| `panel` | `#0F1312` | Inputs, secondary buttons, menus, dialogs | |
| `log` | `#0A0D0C` | Log and code wells | |
| `rule` | `#1F2724` | Every border and divider | |
| `text` | `#D7E3DC` | Primary text | `void`, `panel` |
| `text-dim` | `#AFC0B7` | Log lines, secondary values | `void`, `log` |
| `muted` | `#8FA39A` | Captions, labels, hints | `void`, `panel` |
| `phosphor` | `#B6F36A` | Primary action, selection, running, links | `void`, `panel` |
| `phosphor-hover` | `#D3F9A4` | Hover on a phosphor fill or link | |
| `on-phosphor` | `#07090A` | Text and marks on phosphor, caution or fault fills | |
| `signal` | `#5EEAD4` | Information: update available, starting | `void`, `panel` |
| `caution` | `#FBBF24` | Stopped, warnings | `void`, `panel` |
| `fault` | `#FF6B6B` | Failed, errors, destructive confirmation | `void`, `panel` |

Type sizes: `caption` 12, `body` 13, `value` 15, `wordmark` 16, `title` 20, `heading` 28. Spacing steps 1 to 7 are 4, 8, 12, 16, 20, 24 and 28 pixels. Corners are `radius.control` (4). Borders are `border.rule` (1). There are no shadows, gradients, blurs or transparency effects.

There is one theme. Windows high-contrast mode is honoured by falling back to system colours; no light theme exists.

## 3. Mark and icons

The mark is a capital G drawn as a bond: an open ring ending in one node, and a bar ending in a second node at the centre.

| Source in `assets/brand/svg/` | Rendered at | Form |
| ----------------------------- | ----------- | ---- |
| `gluonstack-mark.svg` | 48 and up | Panel tile with a rule border, `text` G, two `phosphor` nodes |
| `gluonstack-mark-32.svg` | 24 to 40 | Panel tile, heavier G, larger nodes, no border |
| `gluonstack-mark-16.svg` | 16 and 20 | `phosphor` tile, `on-phosphor` G, no nodes |
| `gluonstack-mark-solid.svg` | Installer small image | `phosphor` tile, `on-phosphor` G and nodes |
| `gluonstack-tray-running.svg` | Tray, 16 to 32 | `phosphor` tile, whole G |
| `gluonstack-tray-partial.svg` | Tray, 16 to 32 | `caution` tile, dashed G |
| `gluonstack-tray-stopped.svg` | Tray, 16 to 32 | Outline tile, `muted` G |
| `gluonstack-tray-fault.svg` | Tray, 16 to 32 | `fault` tile, a cross |
| `gluonstack-installer-banner.svg` | Installer wizard image | `void` field, the mark, a `phosphor` rule |

Generated files: `assets/brand/gluonstack.ico` (16, 20, 24, 32, 40, 48, 64, 128, 256), `assets/brand/png/gluonstack-<size>.png`, `assets/brand/tray/gluonstack-tray-<state>.ico`, `assets/brand/installer/wizard-banner.bmp` and `wizard-small.bmp` with their `@2x` forms, `default/favicon.ico` and `default/assets/gluonstack-mark.svg`. Each size is rendered from its SVG at its own pixel size.

Rules: the mark is never stretched, rotated, recoloured outside these forms or placed on a background other than `void`, `panel` or a photograph under the solid form. Clear space around it is at least one node diameter. The wordmark is `GluonStack` in Space Grotesk 700, one word, capital G and S, set to the right of the mark with a gap of `space.3`.

## 4. Type

- Space Grotesk (600, 700): the wordmark, pane headings (`heading`), dialog and installer page titles (`title`).
- JetBrains Mono (400, 500): everything else.
- Files: `assets/fonts/SpaceGrotesk-SemiBold.ttf`, `SpaceGrotesk-Bold.ttf`, `JetBrainsMono-Regular.ttf`, `JetBrainsMono-Medium.ttf`, static instances cut from the upstream variable fonts because WPF renders only a variable font's default instance. Both families are under the SIL Open Font License 1.1; the licence texts sit beside them and ship with the product.
- Line height is 1.8 in log wells and 1.5 in prose. Numbers that change in place (ports, versions, counts) are always in JetBrains Mono, which is fixed width.

## 5. Voice

- Control labels, list entries, commands and state words are lower case: `start all`, `backup now`, `running`.
- Headings, dialog titles, installer page titles and sentences are sentence case: `Choose components`.
- Service names are written as their command name in lists and commands (`apache`, `php`, `mariadb`, `postgres`, `mailpit`) and as their product name in a pane heading (`MariaDB`, `PostgreSQL`).
- A message says what happened and what to do next, in that order, with the real value: `port 3306 is in use by mysqld.exe (PID 4120). stop it, or change the port in settings.` Never "an error occurred".
- No exclamation marks, no emoji, no "please", no "successfully".

## 6. Control panel

One window. Minimum size `window-min-width` by `window-min-height`; it remembers its size, position and selected entry.

### 6.1 Regions

| Region | Size | Holds |
| ------ | ---- | ----- |
| Header | `header-height`, full width, rule below | Mark (28), wordmark, command bar, `stop all`, `start all` |
| List | `list-width`, rule to its right | `SERVICES n/m` caption, one row per service, `WORKSPACE` caption, workspace entries, `settings` pinned to the bottom above a rule |
| Detail pane | The rest, padding `space.6` by `space.7` | The pane for the selected list entry |
| Status line | 28 high, rule above | Last action and its result, left; the install root, right |

### 6.2 List

- A service row is `service-row-height`: state glyph and name on the left, version and port in `muted` on the right. Rows, in order: `apache`, `php`, `mariadb`, `postgres`, `mailpit`. A component that is not installed has no row.
- A workspace entry is `entry-row-height`: name on the left, a count or note in `muted` on the right (`sites` with the number of sites, `databases` with the servers that are running, `updates` with `n available` in `signal` or `current`, `logs`).
- The selected row is a full-width `phosphor` fill with `on-phosphor` text at weight 500. Hover is a `panel` fill. Focus is a 2 pixel `phosphor` outline inset by 2.
- Up and Down move the selection; Enter moves focus into the pane.

### 6.3 Command bar

A single-line input, `control-height` high, `panel` fill, rule border, a `phosphor` `>` prompt on the left and `Ctrl K` in `muted` on the right. Ctrl K focuses it from anywhere; Escape clears it and returns focus.

Typing shows a list of matching commands below it (a `panel` menu, at most 8 rows, the first one selected). Enter runs the selected command. The grammar is `verb [target] [value]`:

| Command | Does |
| ------- | ---- |
| `start <service\|all>`, `stop <service\|all>`, `restart <service>` | Controls services |
| `open <localhost\|inbox\|phpmyadmin\|adminer\|folder>` | Opens the address or folder |
| `go <entry>` | Selects a list entry |
| `switch php <version>`, `switch mariadb <version>` | Switches the active version |
| `new site <name>`, `new database <name> [on mariadb\|postgres]` | Opens the dialog with the name filled in |
| `backup now` | Dumps every database |
| `update <component\|all>`, `check updates` | Runs the updater |
| `log <service>` | Selects the service and focuses its log |

Every button in the interface runs one of these commands through the same code path. A command that fails writes its message to the status line in `fault` and keeps the typed text.

### 6.4 Buttons, inputs and other controls

| Control | Rest | Hover | Pressed | Disabled |
| ------- | ---- | ----- | ------- | -------- |
| Primary button | `phosphor` fill, `on-phosphor` text, weight 500, no border | `phosphor-hover` fill | `phosphor` fill, text offset 1 down | Not used: an action that cannot run is not shown |
| Secondary button | `panel` fill, rule border, `text` | Border `muted` | `rule` fill | Same |
| Destructive button | `panel` fill, `fault` border and text | `fault` fill, `on-phosphor` text | Same as hover | Same |
| Text input, select | `panel` fill, rule border, `text` | Border `muted` | Focus: border `phosphor` | `muted` text, read only |
| Checkbox | 18 square, rule border; checked: `phosphor` fill with an `on-phosphor` tick | Border `muted` | | |
| Link | `phosphor`, no underline | `phosphor-hover`, underlined | | |

All are `control-height` (44) high where they are click targets, with horizontal padding `space.4` and `radius.control` corners. There is at most one primary button in a pane and one in the header (`start all`). Scrollbars are 8 pixels, a `rule` thumb on `void`, `muted` on hover.

A **fact card** is a rule-bordered box with padding `space.3` by `space.4`: an upper-case `caption` label in `muted`, a `value` line, and at most one link or note. A **log well** is a rule-bordered box with a 44 high caption row (`LOG, LIVE` on the left, the file path in `muted` on the right, rule below) over a `log` fill showing lines in `text-dim`; warning lines are `caution`, error lines are `fault`; a `phosphor` block cursor ends a live log; it follows the tail unless the user has scrolled up.

A **dialog** is a `panel` box with a rule border, centred over the window on a `void` scrim at 70% opacity, padding `space.6`: a `title` heading, its fields, and a right-aligned button row with the secondary `cancel` first and the primary action last. Escape cancels; Enter runs the primary action. A destructive confirmation names the thing destroyed and requires its name to be typed when data is lost.

### 6.5 Service panes

Each service pane has, top to bottom: the heading row (product name in `heading`; under it a `muted` line with state, service name and data folder; on the right the secondary buttons), a row of three fact cards, and the service's log well filling the rest.

| Service | Buttons | Fact cards |
| ------- | ------- | ---------- |
| Apache | `restart`, `stop` or `start`, `open localhost`, `settings` | VERSION (with `update to <version>` when behind); PORTS (http and https); CONFIG (`open httpd.conf`, last `httpd -t` result) |
| PHP | `switch version`, `open php.ini`, `settings` | VERSION (active); INSTALLED VERSIONS (`switch version`); EXTENSIONS (count enabled, `manage`) |
| MariaDB | `restart`, `stop` or `start`, `backup now`, `settings` | VERSION; INSTALLED VERSIONS (`switch version`); CONNECTION (`copy connection string`) |
| PostgreSQL | `restart`, `stop` or `start`, `backup now`, `settings` | VERSION; DATA (cluster folder and size); CONNECTION (`copy connection string`) |
| Mailpit | `restart`, `stop` or `start`, `open inbox`, `settings` | VERSION; PORTS (smtp and web); MESSAGES (count held, `clear`) |

`settings` swaps the fact cards and log for that service's settings form (ports, paths and the tunables the configuration file exposes), with `save` as the pane's primary button and `cancel` beside it. Saving validates the configuration (`httpd -t`, a dry start) before it replaces the file, keeps the previous file as `.bak`, and offers `restart now` on the status line.

### 6.6 Workspace panes

- **Sites.** Heading `Sites` with the primary `new site`. A table: name (a link that opens it), document root, PHP version, `tls` when it has a certificate, and per-row `edit` and `remove`. `new site` and `edit` open a dialog: server name, document root (with a folder picker), PHP version, a `tls` checkbox that makes a self-signed certificate. Saving writes the virtual host, adds the hosts file entry (asking for elevation once, and saying so first), tests the configuration and reloads Apache. `remove` asks to confirm and never deletes the document root.
- **Databases.** Heading `Databases`, a server switch (`mariadb`, `postgres`; only running servers are offered) and the primary `new database`. A table: name, size, tables, and per-row `export`, `import`, `drop`. `new database` asks for name, character set and collation (MariaDB) or encoding (PostgreSQL). `export` and `import` show a progress line on the status line and can be cancelled. `drop` requires the database name to be typed.
- **Updates.** Heading `Updates` with the primary `update all` when anything is behind, and `check now`. A table: component, installed version, latest version, state (`current`, `update available`, `updating`, `failed`), and per-row `update`. A note states that every database is dumped before a database server is updated. While an update runs the row shows its step (`downloading`, `verifying`, `stopping`, `swapping`, `starting`, `checking`), and a failure shows the step that failed and that the previous version was put back.
- **Logs.** Heading `Logs`, a file select listing every log under `logs\`, a search input, a level filter (`all`, `warnings`, `errors`), a `live` checkbox and `open folder`. The log well fills the rest. Search highlights matches with a `phosphor` underline and Enter moves to the next.
- **Settings.** Sections with `title` headings: General (`start with windows`, `minimise to tray on close`, `start services on launch`), Paths (install root, read only, with `open folder`; web root), Updates (`check on launch`), Advanced (log level; `export settings`, `import settings`), About (version, licence, the fonts' licences, `open repository`). Each setting saves when it changes and says so on the status line; there is no save button.

### 6.7 States every pane has

- **Loading**: the pane's heading and a `muted` line saying what is being read. No spinner, no skeleton blocks.
- **Empty**: one `muted` sentence saying what would be here and the command that makes it, with the primary button: `no sites yet. new site adds one.`
- **Failed**: the message in `fault` with what to do next, and a `details` link opening the error dialog (the full text, `copy`, `open log`).
- **Not running** (a pane that needs a stopped service): `mariadb is stopped.` with the primary `start mariadb`.

## 7. Splash

A borderless 520 by 300 window, `void` fill, rule border, padding `space.7`. The mark (44) and wordmark (`heading`) on the first row; below, one line per service in JetBrains Mono: a two-character state (`ok` in `phosphor`, `..` in `signal`, `--` in `muted`, `!!` in `fault`), the service name, and its ports or state word. It closes when the main window is ready, and it is skipped when the application starts minimised to the tray.

## 8. Tray

The tray icon is one of the four tray forms in section 3, and its tooltip is `GluonStack: 4 of 5 running`. Left click opens the control panel. The menu is a `panel` box with a rule border, 280 wide, rows `control-height` high: a header row (wordmark in Space Grotesk 600, `n/m up` in `muted`), then `open control panel` (a `phosphor` fill row), `start all`, `stop all`, `open localhost`, `open mail inbox`, a rule, and `exit`. `exit` leaves the services running and says so the first time. A service that fails while the window is hidden raises one Windows notification naming it.

## 9. Installer

An Inno Setup wizard with the modern style. `assets/brand/installer/wizard-banner.bmp` is the left image and `wizard-small.bmp` the top-right image; the setup icon is `assets/brand/gluonstack.ico`. Pages, in order: Location (default `C:\GluonStack`, with the free space needed), Components (Apache, PHP and the control panel fixed; MariaDB, PostgreSQL and Mailpit selectable and on by default), Ports (each port with its default, checked as it is typed, naming the process that holds a busy one), Install (progress with the step named), Done (`open the control panel` checked). Page titles are sentence case. The wizard's own controls keep the system look; the contract covers the images, the page order, the wording and the checks.

## 10. Web dashboard

Served from `default/` at `http://localhost`. Every page links `assets/tokens.css` and uses only its variables.

- **Landing** (`default/index.php`): `void` page, a centred column of at most 720 pixels with padding `space.6`. The mark (44) and wordmark; the heading `It works.` with `localhost, served by GluonStack` in `muted`; a rule-bordered list of links, each row 48 high with the path on the left and what it is on the right (`/phpmyadmin` mariadb, `/adminer` postgres and sqlite, `:8025` mail inbox, `/control` web control panel, `/phpinfo.php` php info); a last block with the PHP and Apache versions and the document root, read at request time. A link whose service is stopped is shown in `muted` with `stopped` and is not a link.
- **Web control panel** (`default/control/`): the same header and left list as the control panel at 6.1 and 6.2, as links, with read-only panes: services and their state, sites, databases, logs, PHP information. It changes nothing; a note on each pane says the control panel application does.
- At widths under 720 pixels the list stacks above the pane and tables scroll inside their own box.

## 11. Accessibility

- Every control has an automation name equal to its label; icon-only controls do not exist.
- Focus order is header, list, pane, status line. Focus is always visible (2 pixel `phosphor` outline).
- Text scales with the Windows text size setting up to 200% without clipping; the list and panes scroll instead.
- The status line is a live region: screen readers announce each new result.
- Motion: none. Nothing animates except the log's text arriving and the block cursor, which stops blinking when the system setting for reduced motion is on.
