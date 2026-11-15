# GluonStack design direction

Decided by the owner on 2026-11-15, from three directions shown side by side (A Charge, B Bond, C Field): **the G mark from B, with the colours and layout of C.** This file is the design source every surface section builds against together with `docs/design/SPEC.md`, the contract that expands it screen by screen.

## Reference boards

The boards are static HTML with inline styles, so every colour, size and spacing value can be read from the markup. They are a picture of the target, not code to ship.

| Board | File | Shows |
| ----- | ---- | ----- |
| Brand | `docs/design/reference/brand.dc.html` | The mark at 256, 64, 32 and 16, the solid variant, tray states, palette |
| Control panel | `docs/design/reference/control-panel.dc.html` | Command bar, service list, service detail, live log |
| Other surfaces | `docs/design/reference/other-surfaces.dc.html` | Splash, tray menu, installer page, web dashboard |

All three boards carry the chosen mark. The originals of every direction are on the design canvas the owner chose from.

## The mark

A capital G drawn as a bond: an open ring that ends in one node, and a bar that ends in a second node at the centre. Sources are in `assets/brand/svg/`, and `python scripts/build-brand-assets.py` renders every icon from them.

| File | Use |
| ---- | --- |
| `gluonstack-mark.svg` | 48 pixels and up: panel tile, light G, two phosphor nodes |
| `gluonstack-mark-32.svg` | 24 to 40 pixels: heavier stroke, larger nodes, no tile border |
| `gluonstack-mark-16.svg` | 16 and 20 pixels: phosphor tile, dark G, no nodes |
| `gluonstack-mark-solid.svg` | On dark photographs or the installer banner: phosphor tile, dark G and nodes |

Tray states use the 16 pixel form and differ in shape as well as colour: all running is the phosphor tile with a whole G; some stopped is a caution tile with a dashed G; all stopped is an outline tile with a grey G.

## Colour tokens

| Token | Value | Use |
| ----- | ----- | --- |
| `void` | `#07090A` | Window background |
| `panel` | `#0F1312` | Inputs, buttons, menus, raised panels |
| `log` | `#0A0D0C` | Log and code wells |
| `rule` | `#1F2724` | Every border and divider, 1 pixel |
| `text` | `#D7E3DC` | Primary text |
| `text-dim` | `#AFC0B7` | Log lines and secondary values |
| `muted` | `#8FA39A` | Labels and captions |
| `phosphor` | `#B6F36A` | The one accent: primary action, selection, running |
| `on-phosphor` | `#07090A` | Text and marks on a phosphor fill |
| `signal` | `#5EEAD4` | Information: an update is available, a service is starting |
| `caution` | `#FBBF24` | Stopped, warnings |
| `fault` | `#FF6B6B` | Errors and failed services (not on the boards; chosen to pass 4.5:1 on `void`) |

There is one theme, dark. A light theme is not part of this direction.

## Type

- Headings and the wordmark: Space Grotesk, 600 and 700.
- Everything else, including body text, buttons, tables and logs: JetBrains Mono, 400 and 500, 13 pixels in the control panel.
- Both fonts are bundled with the application under the SIL Open Font License; nothing is loaded from the network.
- Labels in the control panel and the web dashboard are lower case (`start all`, `backup now`); headings and the installer's page titles are sentence case.

## Layout

- Corners are 4 pixels. Borders are 1 pixel `rule`. No shadows and no gradients.
- The control panel is three regions: a 56 pixel header (mark, wordmark, command bar, `stop all`, `start all`), a 340 pixel left list (services with state, version and port, then the workspace entries: sites, databases, updates, logs, with settings pinned to the bottom), and a detail pane for the selected entry.
- The selected list row is a full-width phosphor fill with `on-phosphor` text.
- A service's detail pane is a heading with its state line and actions, a row of three fact cards (version, installed versions, connection), and its live log.
- Every action in the interface also has a typed command in the command bar (`start postgres`, `switch php 8.4`), opened with Ctrl K.
- State is never colour alone: running is a filled dot, stopped is a hollow ring, and the word is always shown.
- Controls are at least 44 pixels tall where they are the target of a click.

## What the other directions were

Kept for the record; neither is built. A Charge: a dark interface with a sidebar and service cards, and a mark of three colour-charge dots (red, green, blue) bound in a triangle. B Bond: a light, table-first interface on warm paper with one ember accent and IBM Plex type; only its G mark was taken.
