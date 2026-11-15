---
schema_version: 1
id: control-panel-shell
domain: 02-design
status: active
title: "TODO-02 -- Control panel shell in the chosen design"
depends_on: ["postgresql"]
---

# TODO-02 -- Control panel shell in the chosen design

> **Goal:** The control panel is the window the design contract describes: header with a command bar, a list of services and workspace entries, a detail pane per entry, a status line, the splash and the tray, with every existing capability reachable in it.

> **Current state:** Measured 2026-11-15. `gluon-control/MainWindow.xaml` (450 lines) is a MaterialDesign window with a navigation rail; `Views/DashboardView.xaml` (1139 lines) shows service cards; `ServicesView`, `PhpView` and `SettingsView` work; `DatabaseView` and `LogsView` are stubs; `ComingSoonView` stands in for the rest. `SplashScreen.xaml` exists in the old look. There is no tray icon. `Services/ViewCache.cs` caches views.

## Inputs

- `docs/design/SPEC.md` sections 6, 7, 8 and 11.
- D02 T01 §2 and §3: the styles and composite controls every pane uses.
- D01 T02 §7: the service list read from the manifest.

## Outcome

- Starting `GluonStack.exe` shows the splash, then the window of section 6 with a row per installed service.
- Every action is available as a typed command and as a button running the same command.

**Adjacency:** list=applicable @ D02 T02 §2; document=not-applicable (the shell shows state owned elsewhere); settings=applicable @ D02 T02 §1; reporting=not-applicable (the shell shows state owned elsewhere); notifications=applicable @ D02 T02 §7; permissions=not-applicable (the shell shows state owned elsewhere); audit=applicable @ D02 T02 §1; exchange=not-applicable (the shell shows state owned elsewhere); reverse=not-applicable (the shell shows state owned elsewhere)

**Adjacency rationale:** The list is the left list; the shell's own settings are window size, position and last entry, saved by §1; the notification is the tray's failure notice; the trail of what was done is the status line, which §1 also writes to the application log.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Main window regions and the status line | T01 §3 | [ ] |
| 2 | §2 | Service and workspace list with keyboard selection | §1 | [ ] |
| 3 | §3 | Command registry and command bar | §2 | [ ] |
| 4 | §4 | Service panes for Apache, PHP, MariaDB, PostgreSQL and Mailpit | §3 | [ ] |
| 5 | §5 | Pane states and the error dialog | §4 | [ ] |
| 6 | §6 | Splash in the chosen design | §1 | [ ] |
| 7 | §7 | Tray icon, menu and failure notice | §3 | [ ] |
| 8 | §8 | Accessibility pass over the shell | §5 | [ ] |
| 9 | §9 | Old views and the coming-soon placeholder removed | §8 | [ ] |

## 1. Main window regions and the status line

The frame everything else sits in.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.1) and `docs/design/reference/control-panel.dc.html`.
**Job:** See the whole stack at once and always know the result of the last action.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The whole main window: header, list, detail pane and status line.

**Build order:**

1. Rebuild `gluon-control/MainWindow.xaml` as a four-region grid: header, list, detail pane, status line, with the sizes of section 6.1. Done when: the window matches the reference board's frame at 1280 by 800.
2. Add `gluon-control/Services/StatusLine.cs`: `Report(text, level)`, a live region for screen readers, and a copy of each line in `logs\gluonstack\control.log`. Done when: an action's result appears on the status line and in the log.
3. Save and restore window size, position and the selected entry in the settings file. Done when: the window reopens where it was, on the entry it showed.
4. Enforce the minimum window size from the tokens and scroll the list and the pane instead of clipping. Done when: at the minimum size nothing is cut off.

- [ ] Rebuild `gluon-control/MainWindow.xaml` as a four-region grid: header, list, detail pane, status line, with the sizes of section 6.1. Done when: the window matches the reference board's frame at 1280 by 800.
- [ ] Add `gluon-control/Services/StatusLine.cs`: `Report(text, level)`, a live region for screen readers, and a copy of each line in `logs\gluonstack\control.log`. Done when: an action's result appears on the status line and in the log.
- [ ] Save and restore window size, position and the selected entry in the settings file. Done when: the window reopens where it was, on the entry it showed. Cheaper substitute: a separate file beside the exe.
- [ ] Enforce the minimum window size from the tokens and scroll the list and the pane instead of clipping. Done when: at the minimum size nothing is cut off.
- [ ] Commit: `shell: main window regions and status line`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~StatusLine` passes and a manual start shows the four regions.

## 2. Service and workspace list with keyboard selection

The left list is the navigation and the at-a-glance state.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.2) and `docs/design/reference/control-panel.dc.html`.
**Job:** Pick a service or workspace area and see each service's state, version and port.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The left list of the main window.

**Build order:**

1. Create `gluon-control/Views/EntryList.xaml` bound to `MainViewModel.Entries`: service rows from `ServiceManager`, then `sites`, `databases`, `updates`, `logs`, then `settings` pinned below. Done when: a row exists per installed service and none for a missing component.
2. Show each service row's state glyph, name, version and port, refreshed on the existing polling timer. Done when: stopping a service outside the application changes its row within one poll.
3. Implement selection, hover and focus as section 6.2 gives them, with Up, Down and Enter. Done when: the list is fully usable without a pointer.
4. Show the workspace notes: site count, running database servers, `n available` or `current`, each read from its owning service. Done when: the notes are real values, and absent until their owner exists.

- [ ] Create `gluon-control/Views/EntryList.xaml` bound to `MainViewModel.Entries`: service rows from `ServiceManager`, then `sites`, `databases`, `updates`, `logs`, then `settings` pinned below. Done when: a row exists per installed service and none for a missing component.
- [ ] Show each service row's state glyph, name, version and port, refreshed on the existing polling timer. Done when: stopping a service outside the application changes its row within one poll.
- [ ] Implement selection, hover and focus as section 6.2 gives them, with Up, Down and Enter. Done when: the list is fully usable without a pointer.
- [ ] Show the workspace notes: site count, running database servers, `n available` or `current`, each read from its owning service. Done when: the notes are real values, and absent until their owner exists. Cheaper substitute: placeholder counts.
- [ ] Commit: `shell: entry list`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~EntryList` passes, covering a missing component and a state change.

## 3. Command registry and command bar

Every action is a command. Buttons and the command bar run the same registry, so nothing can be done one way and not the other.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.3) and `docs/design/reference/control-panel.dc.html`.
**Job:** Do anything by typing it.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The header of the main window.

**Build order:**

1. Create `gluon-control/Commands/CommandRegistry.cs`: a command has a verb, a target pattern, a completion source and an async handler returning a result line. Done when: the registry lists every command of section 6.3 whose owner exists.
2. Register the service commands (`start`, `stop`, `restart`, `open`, `go`, `log`) over `ServiceManager`. Done when: `start all` starts every installed service.
3. Create `gluon-control/Views/CommandBar.xaml`: the input, Ctrl K, Escape, the completion menu of at most 8 rows and Enter to run. Done when: typing `st` offers `start` and `stop` and Enter runs the first.
4. Report a failed or unknown command on the status line in `fault` and keep the typed text. Done when: `start nothing` reports that no service is named `nothing`.
5. Bind `stop all` and `start all` in the header to the registry. Done when: the header buttons and the typed commands produce the same status line text.
6. Add `CommandRegistryTests` for parsing, completion and an unknown target. Done when: the tests pass and fail when a verb is unregistered.

- [ ] Create `gluon-control/Commands/CommandRegistry.cs`: a command has a verb, a target pattern, a completion source and an async handler returning a result line. Done when: the registry lists every command of section 6.3 whose owner exists.
- [ ] Register the service commands (`start`, `stop`, `restart`, `open`, `go`, `log`) over `ServiceManager`. Done when: `start all` starts every installed service.
- [ ] Create `gluon-control/Views/CommandBar.xaml`: the input, Ctrl K, Escape, the completion menu of at most 8 rows and Enter to run. Done when: typing `st` offers `start` and `stop` and Enter runs the first.
- [ ] Report a failed or unknown command on the status line in `fault` and keep the typed text. Done when: `start nothing` reports that no service is named `nothing`.
- [ ] Bind `stop all` and `start all` in the header to the registry. Done when: the header buttons and the typed commands produce the same status line text.
- [ ] Add `CommandRegistryTests` for parsing, completion and an unknown target. Done when: the tests pass and fail when a verb is unregistered.
- [ ] Commit: `shell: command registry and command bar`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~CommandRegistry` reports all passed.

## 4. Service panes for Apache, PHP, MariaDB, PostgreSQL and Mailpit

One pane template, five services. It carries over everything the old dashboard, services and PHP views could do.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.5) and `docs/design/reference/control-panel.dc.html`.
**Job:** Control one service, read its facts and watch its log.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Create `gluon-control/Views/ServicePane.xaml`: heading row with the state line and buttons, three fact cards, the log well. Done when: selecting `mariadb` shows the pane of the reference board.
2. Fill each service's buttons and fact cards from the table in section 6.5, each button bound to a registry command. Done when: every button in the table exists and works for every installed service.
3. Move PHP version switching and extension management from `Views/PhpView.xaml` into the PHP pane and its `manage` dialog. Done when: switching the PHP version from the pane restarts Apache on the new version.
4. Register `switch php <version>` and `switch mariadb <version>` in the command registry over the existing switch scripts. Done when: both commands complete with the installed versions.
5. Point each pane's log well at the service's log file. Done when: new log lines appear while the service runs.

- [ ] Create `gluon-control/Views/ServicePane.xaml`: heading row with the state line and buttons, three fact cards, the log well. Done when: selecting `mariadb` shows the pane of the reference board.
- [ ] Fill each service's buttons and fact cards from the table in section 6.5, each button bound to a registry command. Done when: every button in the table exists and works for every installed service. Cheaper substitute: a button that is shown but disabled.
- [ ] Move PHP version switching and extension management from `Views/PhpView.xaml` into the PHP pane and its `manage` dialog. Done when: switching the PHP version from the pane restarts Apache on the new version.
- [ ] Register `switch php <version>` and `switch mariadb <version>` in the command registry over the existing switch scripts. Done when: both commands complete with the installed versions.
- [ ] Point each pane's log well at the service's log file. Done when: new log lines appear while the service runs.
- [ ] Commit: `shell: service panes`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ServicePane` passes, and a manual start shows a working pane for each installed service.

## 5. Pane states and the error dialog

Loading, empty, failed and not-running look the same everywhere.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (sections 5 and 6.7) and `docs/design/reference/control-panel.dc.html`.
**Job:** Understand why a pane has nothing to show and what to do about it.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Create `gluon-control/Controls/PaneState.xaml` with the four states of section 6.7. Done when: each state renders with its sentence and, where given, its primary button.
2. Restyle `gluon-control/Windows/ErrorDetailsWindow.xaml` as a dialog with the full text, `copy` and `open log`. Done when: `details` on a failed pane opens it.
3. Rewrite the messages in `gluon-control/Utilities/ErrorHandler.cs` to the voice rules of section 5: what happened, then what to do, with the real value. Done when: a busy port message names the port and the process.

- [ ] Create `gluon-control/Controls/PaneState.xaml` with the four states of section 6.7. Done when: each state renders with its sentence and, where given, its primary button.
- [ ] Restyle `gluon-control/Windows/ErrorDetailsWindow.xaml` as a dialog with the full text, `copy` and `open log`. Done when: `details` on a failed pane opens it.
- [ ] Rewrite the messages in `gluon-control/Utilities/ErrorHandler.cs` to the voice rules of section 5: what happened, then what to do, with the real value. Done when: a busy port message names the port and the process. Cheaper substitute: a generic message with the detail hidden in the dialog.
- [ ] Commit: `shell: pane states and error dialog`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ErrorHandler` passes, including the busy-port message.

## 6. Splash in the chosen design

The splash reports the real start of each service instead of a progress bar.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` section 7 and `docs/design/reference/other-surfaces.dc.html` (Splash).
**Job:** See that the stack is starting and which service is slow or failed.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** A borderless 520 by 300 window of its own.

**Build order:**

1. Rebuild `gluon-control/SplashScreen.xaml` as section 7: mark, wordmark and one line per installed service. Done when: it matches the reference board's splash.
2. Drive each line from the service's actual state during start. Done when: a service that fails to start shows `!!` and its reason.
3. Skip the splash when the application starts minimised. Done when: a start with the tray setting on shows no splash.

- [ ] Rebuild `gluon-control/SplashScreen.xaml` as section 7: mark, wordmark and one line per installed service. Done when: it matches the reference board's splash.
- [ ] Drive each line from the service's actual state during start. Done when: a service that fails to start shows `!!` and its reason. Cheaper substitute: a timed animation.
- [ ] Skip the splash when the application starts minimised. Done when: a start with the tray setting on shows no splash.
- [ ] Commit: `shell: splash`

**Test checkpoint:** A manual start shows the splash with a line per installed service, and `dotnet build GluonStack.slnx -warnaserror` succeeds.

## 7. Tray icon, menu and failure notice

The stack keeps running with the window closed; the tray shows its state.

**Phase:** 2
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` section 8 and `docs/design/reference/other-surfaces.dc.html` (Tray).
**Job:** See the stack's state and reach its main actions without opening the window.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The Windows notification area: an icon and its menu.

**Build order:**

1. Add a tray icon in `gluon-control/Services/TrayService.cs` that picks one of the four linked tray icons from the services' states, with the tooltip of section 8. Done when: stopping one service changes the icon to the partial form.
2. Build the tray menu as section 8 lists it, each row bound to a registry command. Done when: every row works.
3. Close to the tray when the setting is on; `exit` leaves services running and says so the first time. Done when: after `exit` the services still run.
4. Raise one Windows notification when a service fails while the window is hidden. Done when: killing a service's process with the window hidden raises one notice naming it.
5. Dispose the icon on exit so no dead icon is left in the tray. Done when: the icon disappears the moment the application exits.

- [ ] Add a tray icon in `gluon-control/Services/TrayService.cs` that picks one of the four linked tray icons from the services' states, with the tooltip of section 8. Done when: stopping one service changes the icon to the partial form.
- [ ] Build the tray menu as section 8 lists it, each row bound to a registry command. Done when: every row works.
- [ ] Close to the tray when the setting is on; `exit` leaves services running and says so the first time. Done when: after `exit` the services still run.
- [ ] Raise one Windows notification when a service fails while the window is hidden. Done when: killing a service's process with the window hidden raises one notice naming it.
- [ ] Dispose the icon on exit so no dead icon is left in the tray. Done when: the icon disappears the moment the application exits.
- [ ] Commit: `shell: tray icon and menu`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~TrayService` passes for the four state-to-icon cases.

## 8. Accessibility pass over the shell

The contract's accessibility section, proven on the built window.

**Phase:** 2
**Needs:** display-session
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 11) and `docs/design/reference/control-panel.dc.html`.
**Job:** Use the whole application by keyboard and with a screen reader.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The whole main window: header, list, detail pane and status line.

**Build order:**

1. Set `AutomationProperties.Name` on every control to its label and make the status line a live region. Done when: Accessibility Insights reports no missing name.
2. Fix the focus order to header, list, pane, status line. Done when: Tab walks the regions in that order.
3. Check text scaling at 200% and the Windows high-contrast themes. Done when: nothing clips and every control is legible.
4. Add a UI automation test that starts the application and reads the list's rows by name. Done when: the test passes and fails when a name is removed.

- [ ] Set `AutomationProperties.Name` on every control to its label and make the status line a live region. Done when: Accessibility Insights reports no missing name.
- [ ] Fix the focus order to header, list, pane, status line. Done when: Tab walks the regions in that order.
- [ ] Check text scaling at 200% and the Windows high-contrast themes. Done when: nothing clips and every control is legible.
- [ ] Add a UI automation test that starts the application and reads the list's rows by name. Done when: the test passes and fails when a name is removed.
- [ ] Commit: `shell: accessibility`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter Category=UiAutomation` passes.

## 9. Old views and the coming-soon placeholder removed

Once every capability lives in a pane, the old views go, so nothing shows two looks.

**Phase:** 2
**Needs:** none
**Surface:** no

**Build order:**

1. Delete `Views/DashboardView`, `Views/ServicesView`, `Views/PhpView`, `Views/ComingSoonView` and their view models' dead members. Done when: the files are gone and the build passes.
2. Delete `Services/ViewCache.cs` if no pane needs it. Done when: no reference remains.
3. List every capability the old views had against the pane that now has it in the commit body. Done when: the list has no capability without a pane.

- [ ] Delete `Views/DashboardView`, `Views/ServicesView`, `Views/PhpView`, `Views/ComingSoonView` and their view models' dead members. Done when: the files are gone and the build passes.
- [ ] Delete `Services/ViewCache.cs` if no pane needs it. Done when: no reference remains.
- [ ] List every capability the old views had against the pane that now has it in the commit body. Done when: the list has no capability without a pane. Cheaper substitute: deleting a view whose capability moved nowhere.
- [ ] Commit: `shell: remove old views`

**Test checkpoint:** `git grep -n -E 'ComingSoon|DashboardView|ServicesView|PhpView' -- gluon-control` prints nothing.
## Verification

- A manual pass over `docs/design/SPEC.md` section 6 finds every listed control present and working for the installed services.
- `python scripts/design-lint.py` reports no violation under `gluon-control/Views`.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
