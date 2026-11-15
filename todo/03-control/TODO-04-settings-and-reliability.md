---
schema_version: 1
id: control-settings-reliability
domain: 03-control
status: active
title: "TODO-04 -- Settings pane and reliability"
depends_on: ["control-panel-shell"]
---

# TODO-04 -- Settings pane and reliability

> **Goal:** The Settings pane holds the application's own settings, and service operations retry sensibly, poll less when hidden and never leave a child process behind.

> **Current state:** Measured 2026-11-15. `gluon-control/Views/SettingsView.xaml` (163 lines) and `SettingsViewModel.cs` hold paths and a few switches in the old look. `ServiceManager` polls on a fixed timer whether or not the window is visible. Service operations run once and surface raw exceptions.

## Inputs

- `docs/design/SPEC.md` section 6.6, Settings.
- D02 T02 §1 and §5: the status line and the message voice.

## Outcome

- Every setting in section 6.6 exists, saves when changed and is in effect on the next start.

**Adjacency:** list=not-applicable (no such surface for application settings); document=not-applicable (no such surface for application settings); settings=applicable @ D03 T04 §1; reporting=not-applicable (no such surface for application settings); notifications=not-applicable (no such surface for application settings); permissions=not-applicable (no such surface for application settings); audit=not-applicable (no such surface for application settings); exchange=applicable @ D03 T04 §2; reverse=applicable @ D03 T04 §2

**Adjacency rationale:** The settings are the pane; exchange is export and import of the settings file; the reverse of an import is the `.bak` it keeps.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Settings pane: general, paths and updates | -- | [ ] |
| 2 | §2 | Advanced settings, export, import and About | §1 | [ ] |
| 3 | §3 | Service operations that retry and explain | -- | [ ] |
| 4 | §4 | Quieter polling and clean process ownership | §3 | [ ] |

## 1. Settings pane: general, paths and updates

The application's own switches.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Settings) and `docs/design/reference/control-panel.dc.html`.
**Job:** Decide how the application starts and behaves.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Rebuild `gluon-control/Views/SettingsView.xaml` as section 6.6 with General, Paths and Updates. Done when: each setting saves when changed and the status line says so.
2. Implement `start with windows` through the current user's Run key, pointing at the installed exe with `--minimised`. Done when: the key exists when on and is gone when off.
3. Implement `minimise to tray on close`, `start services on launch` and `check on launch`. Done when: each is in effect on the next start.
4. Register `go settings`. Done when: the command selects the pane.

- [ ] Rebuild `gluon-control/Views/SettingsView.xaml` as section 6.6 with General, Paths and Updates. Done when: each setting saves when changed and the status line says so.
- [ ] Implement `start with windows` through the current user's Run key, pointing at the installed exe with `--minimised`. Done when: the key exists when on and is gone when off.
- [ ] Implement `minimise to tray on close`, `start services on launch` and `check on launch`. Done when: each is in effect on the next start.
- [ ] Register `go settings`. Done when: the command selects the pane.
- [ ] Commit: `settings: general, paths and updates`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~SettingsViewModel` reports all passed.

## 2. Advanced settings, export, import and About

The rest of the pane.

**Phase:** 3
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 6.6, Settings) and `docs/design/reference/control-panel.dc.html`.
**Job:** Move settings between machines and see what version is running.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** The main window's detail pane, under the header and beside the left list.

**Build order:**

1. Add Advanced: log level for the control log. Done when: debug lines appear only at the debug level.
2. Add `export settings` and `import settings`: import validates the file against the settings type, keeps the current file as `.bak` and applies. Done when: an invalid file is refused naming the bad key.
3. Add About: version from the assembly, the licence, the two font licences from `assets/fonts/*-OFL.txt`, `open repository`. Done when: the version equals the built assembly's.
4. Remove every setting the old view had that no code reads. Done when: each remaining setting has a reader.

- [ ] Add Advanced: log level for the control log. Done when: debug lines appear only at the debug level.
- [ ] Add `export settings` and `import settings`: import validates the file against the settings type, keeps the current file as `.bak` and applies. Done when: an invalid file is refused naming the bad key. Cheaper substitute: overwriting the settings with whatever the file holds.
- [ ] Add About: version from the assembly, the licence, the two font licences from `assets/fonts/*-OFL.txt`, `open repository`. Done when: the version equals the built assembly's.
- [ ] Remove every setting the old view had that no code reads. Done when: each remaining setting has a reader.
- [ ] Commit: `settings: advanced, export, import and About`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~SettingsImport` reports all passed.

## 3. Service operations that retry and explain

A start that fails because a port is still closing should not need a second click, and a real failure should say why.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Wrap start, stop and restart in `gluon-control/Services/ServiceOperation.cs`: wait for the target state with a timeout, retry a transient failure twice with backoff. Done when: a start during a slow stop succeeds without user action.
2. Map the common failures (busy port, missing binary, access denied, service not registered) to messages in the contract's voice with the fix. Done when: an unregistered service reports the register command to run.
3. Never swallow an exception: an unmapped failure is reported with its text and logged with its stack. Done when: an unexpected failure appears on the status line and in the log.
4. Add tests for the retry, the timeout and each mapped failure against a fake service controller. Done when: the tests pass and fail when the retry is removed.

- [ ] Wrap start, stop and restart in `gluon-control/Services/ServiceOperation.cs`: wait for the target state with a timeout, retry a transient failure twice with backoff. Done when: a start during a slow stop succeeds without user action.
- [ ] Map the common failures (busy port, missing binary, access denied, service not registered) to messages in the contract's voice with the fix. Done when: an unregistered service reports the register command to run.
- [ ] Never swallow an exception: an unmapped failure is reported with its text and logged with its stack. Done when: an unexpected failure appears on the status line and in the log. Cheaper substitute: an empty catch.
- [ ] Add tests for the retry, the timeout and each mapped failure against a fake service controller. Done when: the tests pass and fail when the retry is removed.
- [ ] Commit: `reliability: service operations`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ServiceOperation` reports all passed.

## 4. Quieter polling and clean process ownership

The application should cost nothing when hidden and never leave a process behind.

**Phase:** 3
**Needs:** none
**Surface:** no

**Build order:**

1. Poll service state every 2 seconds when visible, every 15 when minimised or in the tray, and at once on restore. Done when: CPU use while hidden is near zero and the state is fresh on restore.
2. Run every child process the application starts inside one job object that ends with it. Done when: killing `GluonStack.exe` leaves none of its child processes.
3. Start every console child with no window. Done when: no console window flashes during any operation.
4. Add a test that starts a child that starts a grandchild and asserts both end with the job. Done when: the test passes and fails without the job object.

- [ ] Poll service state every 2 seconds when visible, every 15 when minimised or in the tray, and at once on restore. Done when: CPU use while hidden is near zero and the state is fresh on restore.
- [ ] Run every child process the application starts inside one job object that ends with it. Done when: killing `GluonStack.exe` leaves none of its child processes. Cheaper substitute: tracking only direct children.
- [ ] Start every console child with no window. Done when: no console window flashes during any operation.
- [ ] Add a test that starts a child that starts a grandchild and asserts both end with the job. Done when: the test passes and fails without the job object.
- [ ] Commit: `reliability: polling and process ownership`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~ProcessJob` reports all passed.
## Verification

- With the window hidden for ten minutes the process uses negligible CPU, and ending it leaves no child process.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
