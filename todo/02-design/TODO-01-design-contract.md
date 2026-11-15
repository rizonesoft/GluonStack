---
schema_version: 1
id: design-contract
domain: 02-design
status: active
title: "TODO-01 -- Design contract enforced in the control panel"
depends_on: ["quality-gates"]
---

# TODO-01 -- Design contract enforced in the control panel

> **Goal:** The control panel draws every control from the design tokens through its own styles, a lint refuses a literal colour, font or size, and the MaterialDesign dependency is gone.

> **Current state:** Measured 2026-11-15. Done on 2026-11-15: `docs/design/SPEC.md` (the contract), `docs/design/direction.md`, `docs/design/tokens.json`, `scripts/generate-ui-tokens.py` (writes `Themes/Tokens.xaml` and `default/assets/tokens.css`), `scripts/build-brand-assets.py` (writes `assets/brand/**` and `default/favicon.ico`), the fonts in `assets/fonts/`, and the project file's links to the icon, tray icons and fonts. Not done: `App.xaml` still merges `MaterialDesignThemes` (`BundledTheme BaseTheme="Dark"`) and defines its own brushes with literal colours (`#0F0F0F`, `#22D3EE` and others); `Tokens.xaml` is compiled but merged nowhere; every view uses MaterialDesign controls.

## Inputs

- `docs/design/SPEC.md` sections 1, 2, 4 and 6.4: the rules, tokens, type and controls.
- `gluon-control/Themes/Tokens.xaml`: generated, never edited.

## Outcome

- `python scripts/design-lint.py` exits 0 over `gluon-control/` and `default/`.
- `git grep -n MaterialDesign -- gluon-control Directory.Packages.props` returns nothing.

**Adjacency:** all=not-applicable (styles and a lint: no record a user lists, exports or reverses)

**Adjacency rationale:** The only tunables are the tokens, owned by `docs/design/tokens.json` and read by the generator.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Design lint and generated-file checks in the gate | -- | [ ] |
| 2 | §2 | Base control styles from the tokens | §1 | [ ] |
| 3 | §3 | Composite styles: fact card, log well, table, dialog | §2 | [ ] |
| 4 | §4 | Tokens and styles merged; MaterialDesign removed | T02 §9 | [ ] |

## 1. Design lint and generated-file checks in the gate

The contract holds only if a machine refuses a break. The lint starts by listing today's violations so later sections burn the list down to zero.

**Phase:** 2
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/design-lint.py`: scan `gluon-control/**/*.xaml` and `default/**/*.{php,css}` for literal colours (`#RGB`, `#RRGGBB`, `#AARRGGBB`, named colours on a brush property), `FontFamily` and `font-family` literals, and `FontSize` or `font-size` literals. Done when: it prints `file:line: rule: value` per violation and exits 1 when there are any.
2. Exempt the generated `Themes/Tokens.xaml`, `default/assets/tokens.css` and the third-party folders (`phpmyadmin`, `adminer`, `phpliteadmin`). Done when: none of those paths appears in the output.
3. Add `--baseline docs/design/lint-baseline.txt`: violations listed there are reported as known and do not fail; a new one does; a baseline line that no longer matches fails as stale. Done when: the lint exits 0 with the baseline, 1 after a new literal is added, and 1 after a baselined line is fixed without removing it from the file.
4. Add `tokens`, `assets` and `design` checks to `scripts/check-all.ps1` running the two `--check` commands and the lint. Done when: the gate fails when `tokens.json` is edited without regenerating.
5. Add `scripts/tests/test_design_lint.py` with a violating and a clean fixture. Done when: `python -m unittest scripts.tests.test_design_lint` passes and fails when a rule is removed.

- [ ] Create `scripts/design-lint.py`: scan `gluon-control/**/*.xaml` and `default/**/*.{php,css}` for literal colours (`#RGB`, `#RRGGBB`, `#AARRGGBB`, named colours on a brush property), `FontFamily` and `font-family` literals, and `FontSize` or `font-size` literals. Done when: it prints `file:line: rule: value` per violation and exits 1 when there are any.
- [ ] Exempt the generated `Themes/Tokens.xaml`, `default/assets/tokens.css` and the third-party folders (`phpmyadmin`, `adminer`, `phpliteadmin`). Done when: none of those paths appears in the output.
- [ ] Add `--baseline docs/design/lint-baseline.txt`: violations listed there are reported as known and do not fail; a new one does; a baseline line that no longer matches fails as stale. Done when: the lint exits 0 with the baseline, 1 after a new literal is added, and 1 after a baselined line is fixed without removing it from the file.
- [ ] Add `tokens`, `assets` and `design` checks to `scripts/check-all.ps1` running the two `--check` commands and the lint. Done when: the gate fails when `tokens.json` is edited without regenerating.
- [ ] Add `scripts/tests/test_design_lint.py` with a violating and a clean fixture. Done when: `python -m unittest scripts.tests.test_design_lint` passes and fails when a rule is removed.
- [ ] Commit: `design: lint and generated-file checks in the gate`

**Test checkpoint:** `pwsh scripts/check-all.ps1 -Only tokens,assets,design` exits 0, and exits 1 after `Background="#123456"` is added to any view.

## 2. Base control styles from the tokens

Buttons, inputs, checkboxes, selects, links and scrollbars as the contract's table gives them, with every state.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` section 6.4 (the controls table) and `docs/design/reference/control-panel.dc.html`.
**Job:** Recognise what can be pressed, typed into or followed, and see which control has focus.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** No window of its own: styles applied by every window.

**Build order:**

1. Create `gluon-control/Themes/Controls.xaml` with `PrimaryButton`, `SecondaryButton` and `DestructiveButton` styles: fills, borders, hover and pressed states and the 2 pixel focus outline of section 6.4. Done when: a sample window shows each button in each state matching the reference board.
2. Add `TextBox`, `PasswordBox` and `ComboBox` styles with the `panel` fill, rule border and `phosphor` focus border. Done when: focus changes the border and no chrome from the system theme remains.
3. Add `CheckBox`, `Hyperlink`, `ScrollBar` and `ToolTip` styles. Done when: the scrollbar is 8 pixels with a `rule` thumb.
4. Set default `FontFamily`, `FontSize` and `Foreground` for `Window` and `TextBlock` from the tokens, and a `HeadingText` style in the heading font. Done when: text with no explicit style renders in JetBrains Mono at 13.
5. Honour high contrast: when `SystemParameters.HighContrast` is true, map the brushes to system colours. Done when: with a high-contrast theme on, every control is legible.

- [ ] Create `gluon-control/Themes/Controls.xaml` with `PrimaryButton`, `SecondaryButton` and `DestructiveButton` styles: fills, borders, hover and pressed states and the 2 pixel focus outline of section 6.4. Done when: a sample window shows each button in each state matching the reference board. Cheaper substitute: restyling MaterialDesign's button with setters.
- [ ] Add `TextBox`, `PasswordBox` and `ComboBox` styles with the `panel` fill, rule border and `phosphor` focus border. Done when: focus changes the border and no chrome from the system theme remains.
- [ ] Add `CheckBox`, `Hyperlink`, `ScrollBar` and `ToolTip` styles. Done when: the scrollbar is 8 pixels with a `rule` thumb.
- [ ] Set default `FontFamily`, `FontSize` and `Foreground` for `Window` and `TextBlock` from the tokens, and a `HeadingText` style in the heading font. Done when: text with no explicit style renders in JetBrains Mono at 13.
- [ ] Honour high contrast: when `SystemParameters.HighContrast` is true, map the brushes to system colours. Done when: with a high-contrast theme on, every control is legible.
- [ ] Commit: `design: base control styles`

**Test checkpoint:** `dotnet build GluonStack.slnx -warnaserror` succeeds and `python scripts/design-lint.py --baseline docs/design/lint-baseline.txt` reports no violation in `gluon-control/Themes/Controls.xaml`.

## 3. Composite styles: fact card, log well, table, dialog

The four repeated compositions, built once as controls so every pane uses the same one.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` section 6.4 (fact card, log well, dialog) and `docs/design/reference/control-panel.dc.html`.
**Job:** Read a service's facts and its log, and answer a dialog.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** No window of its own: controls hosted in the detail pane and over the main window.

**Build order:**

1. Add `gluon-control/Controls/FactCard.xaml`: caption, value and one optional link or note. Done when: three cards in a row match the reference board.
2. Add `gluon-control/Controls/LogWell.xaml`: caption row, virtualised lines, warning and error colouring, the block cursor, and follow-tail that stops when the user scrolls up. Done when: a 50 MB log opens without loading the whole file and stays responsive.
3. Add a `DataGrid` style: rule dividers, upper-case `caption` headers, row height 44, no alternating fills. Done when: a table of sites matches section 6.6.
4. Add `gluon-control/Controls/DialogHost.xaml`: scrim, panel box, title, content, right-aligned button row, Escape and Enter handling. Done when: a dialog opens centred over the window and returns focus to the control that opened it.

- [ ] Add `gluon-control/Controls/FactCard.xaml`: caption, value and one optional link or note. Done when: three cards in a row match the reference board.
- [ ] Add `gluon-control/Controls/LogWell.xaml`: caption row, virtualised lines, warning and error colouring, the block cursor, and follow-tail that stops when the user scrolls up. Done when: a 50 MB log opens without loading the whole file and stays responsive. Cheaper substitute: a `TextBox` holding the whole text.
- [ ] Add a `DataGrid` style: rule dividers, upper-case `caption` headers, row height 44, no alternating fills. Done when: a table of sites matches section 6.6.
- [ ] Add `gluon-control/Controls/DialogHost.xaml`: scrim, panel box, title, content, right-aligned button row, Escape and Enter handling. Done when: a dialog opens centred over the window and returns focus to the control that opened it.
- [ ] Commit: `design: fact card, log well, table and dialog`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~LogWell` passes, including a test that reads the tail of a large file in under one second.

## 4. Tokens and styles merged; MaterialDesign removed

The switch. `App.xaml` merges the tokens and the new styles, and the old theme package goes once no view needs it.

**Phase:** 2
**Needs:** none
**Surface:** no

**Build order:**

1. Merge `Themes/Tokens.xaml` and `Themes/Controls.xaml` in `gluon-control/App.xaml` and delete the literal brushes it defines. Done when: `App.xaml` contains no colour literal.
2. Remove the `MaterialDesignThemes` package after D02 T02 has replaced every view that uses it. Done when: `git grep -n -i materialdesign` returns nothing outside `docs/`.
3. Replace `SnackbarMessageQueue` use in the view models with the status line service from D02 T02 §1. Done when: no view model references a MaterialDesign type.
4. Empty `docs/design/lint-baseline.txt` and delete the `--baseline` argument from the gate. Done when: `python scripts/design-lint.py` exits 0 with no baseline.

- [ ] Merge `Themes/Tokens.xaml` and `Themes/Controls.xaml` in `gluon-control/App.xaml` and delete the literal brushes it defines. Done when: `App.xaml` contains no colour literal.
- [ ] Remove the `MaterialDesignThemes` package after D02 T02 has replaced every view that uses it. Done when: `git grep -n -i materialdesign` returns nothing outside `docs/`. Cheaper substitute: keeping the package for one leftover control.
- [ ] Replace `SnackbarMessageQueue` use in the view models with the status line service from D02 T02 §1. Done when: no view model references a MaterialDesign type.
- [ ] Empty `docs/design/lint-baseline.txt` and delete the `--baseline` argument from the gate. Done when: `python scripts/design-lint.py` exits 0 with no baseline.
- [ ] Commit: `design: tokens merged, MaterialDesign removed`

**Test checkpoint:** `python scripts/design-lint.py` exits 0 and `git grep -c -i materialdesign -- gluon-control Directory.Packages.props` prints nothing.
## Verification

- `pwsh scripts/check-all.ps1` exits 0 with the `tokens`, `assets` and `design` checks in it and no baseline.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
