---
schema_version: 1
id: dotnet-11
domain: 00-foundation
status: active
title: "TODO-02 -- .NET 11 and current C#"
depends_on: ["rename-gluonstack"]
---

# TODO-02 -- .NET 11 and current C#

> **Goal:** The control panel targets .NET 11 with the current C# language version, builds with no warnings, and has a test project the gate runs.

> **Current state:** Measured 2026-11-15. `iso-control/Isotone.csproj` targets `net9.0-windows` with no `LangVersion`, references MaterialDesignThemes 5.2.1, CommunityToolkit.Mvvm 8.4.0, System.ServiceProcess.ServiceController 9.0.8, System.Diagnostics.PerformanceCounter 9.0.0 and Newtonsoft.Json 13.0.3, and builds on SDK 11.0.100 with 0 errors and 20 nullable warnings (CS8618, CS8600). There is no test project and no solution at the repository root.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: framework, JSON, test project and solution decisions.
- `dotnet --list-sdks` on the build machine: 11.0.100 is installed.

## Outcome

- `dotnet build GluonStack.slnx -warnaserror` ends with 0 warnings and 0 errors.
- `dotnet test GluonStack.slnx` runs the first tests and passes.

**Adjacency:** all=not-applicable (a framework and tooling change with no user-visible record or setting)

**Adjacency rationale:** The settings file changes serializer, not shape: §4 proves an existing file reads back unchanged.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Target framework, root solution and shared build properties | -- | [ ] |
| 2 | §2 | Package versions under central package management | §1 | [ ] |
| 3 | §3 | Zero warnings with warnings as errors | §2 | [ ] |
| 4 | §4 | System.Text.Json in place of Newtonsoft.Json | §3 | [ ] |
| 5 | §5 | Test project with the first unit tests | §4 | [ ] |
| 6 | §6 | Current C# idioms and one code style | §5 | [ ] |

## 1. Target framework, root solution and shared build properties

One place sets the framework and language for every project, so the test project and any later project cannot drift.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `Directory.Build.props` at the root with `TargetFramework` `net11.0-windows`, `LangVersion` `latest`, `Nullable` `enable` and `ImplicitUsings` `enable`. Done when: `dotnet msbuild gluon-control -getProperty:TargetFramework` prints `net11.0-windows`.
2. Remove the properties `Directory.Build.props` now owns from `gluon-control/GluonStack.Control.csproj`. Done when: the project file names no `TargetFramework`.
3. Create `GluonStack.slnx` with `dotnet new sln --format slnx` and add the control panel project. Done when: `dotnet build GluonStack.slnx` builds the project.
4. Add `global.json` pinning the SDK to `11.0.100` with `rollForward` `latestFeature`. Done when: `dotnet --version` in the repository prints an 11.0 SDK.

- [ ] Create `Directory.Build.props` at the root with `TargetFramework` `net11.0-windows`, `LangVersion` `latest`, `Nullable` `enable` and `ImplicitUsings` `enable`. Done when: `dotnet msbuild gluon-control -getProperty:TargetFramework` prints `net11.0-windows`.
- [ ] Remove the properties `Directory.Build.props` now owns from `gluon-control/GluonStack.Control.csproj`. Done when: the project file names no `TargetFramework`. Cheaper substitute: keeping both, where the project file silently wins.
- [ ] Create `GluonStack.slnx` with `dotnet new sln --format slnx` and add the control panel project. Done when: `dotnet build GluonStack.slnx` builds the project.
- [ ] Add `global.json` pinning the SDK to `11.0.100` with `rollForward` `latestFeature`. Done when: `dotnet --version` in the repository prints an 11.0 SDK.
- [ ] Commit: `build: net11.0-windows, GluonStack.slnx, Directory.Build.props`

**Test checkpoint:** `dotnet build GluonStack.slnx` ends with `0 Error(s)` and `dotnet msbuild gluon-control -getProperty:TargetFramework` prints `net11.0-windows`.

## 2. Package versions under central package management

Package versions move to one file and up to their current releases for .NET 11.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `Directory.Packages.props` with `ManagePackageVersionsCentrally` and one `PackageVersion` per package the project references. Done when: `gluon-control/GluonStack.Control.csproj` has no `Version` attribute on a `PackageReference`.
2. Raise each package to its latest stable release reported by `dotnet list GluonStack.slnx package --outdated`. Done when: the same command reports no outdated package.
3. Run `dotnet list GluonStack.slnx package --vulnerable --include-transitive`. Done when: it reports no vulnerable package, or each one is raised or recorded in `todo/findings.md` with its advisory.

- [ ] Create `Directory.Packages.props` with `ManagePackageVersionsCentrally` and one `PackageVersion` per package the project references. Done when: `gluon-control/GluonStack.Control.csproj` has no `Version` attribute on a `PackageReference`.
- [ ] Raise each package to its latest stable release reported by `dotnet list GluonStack.slnx package --outdated`. Done when: the same command reports no outdated package.
- [ ] Run `dotnet list GluonStack.slnx package --vulnerable --include-transitive`. Done when: it reports no vulnerable package, or each one is raised or recorded in `todo/findings.md` with its advisory.
- [ ] Commit: `build: central package versions at current releases`

**Test checkpoint:** `dotnet list GluonStack.slnx package --outdated` prints no package row and `dotnet build GluonStack.slnx` ends with `0 Error(s)`.

## 3. Zero warnings with warnings as errors

Twenty nullable warnings hide real null paths in the view models and converters. They are fixed where the value is produced, then the build refuses new ones.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Fix each CS8618 in `gluon-control/Converters/*.cs` and `gluon-control/ViewModels/*.cs` by initialising the field or declaring it nullable and handling null at its use. Done when: `dotnet build GluonStack.slnx` reports 0 warnings.
2. Fix CS8600 at `gluon-control/ViewModels/MainViewModel.cs` line 57 by handling the null result. Done when: the warning is gone and the view still resolves in a manual start.
3. Set `TreatWarningsAsErrors` `true` and `AnalysisLevel` `latest-recommended` in `Directory.Build.props`. Done when: adding an unused nullable dereference to any file fails the build.

- [ ] Fix each CS8618 in `gluon-control/Converters/*.cs` and `gluon-control/ViewModels/*.cs` by initialising the field or declaring it nullable and handling null at its use. Done when: `dotnet build GluonStack.slnx` reports 0 warnings. Cheaper substitute: `#pragma warning disable`, a null-forgiving `!`, or `NoWarn` in the project.
- [ ] Fix CS8600 at `gluon-control/ViewModels/MainViewModel.cs` line 57 by handling the null result. Done when: the warning is gone and the view still resolves in a manual start.
- [ ] Set `TreatWarningsAsErrors` `true` and `AnalysisLevel` `latest-recommended` in `Directory.Build.props`. Done when: adding an unused nullable dereference to any file fails the build.
- [ ] Commit: `build: zero warnings, warnings as errors`

**Test checkpoint:** `dotnet build GluonStack.slnx -warnaserror` ends with `0 Warning(s)` and `0 Error(s)`.

## 4. System.Text.Json in place of Newtonsoft.Json

The settings and control panel configuration are read with Newtonsoft.Json. The platform serializer with source generation removes the dependency and works with trimming.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Add `gluon-control/Utilities/JsonContext.cs` with a `JsonSerializerContext` for every type `ConfigurationManager` and `PHPManager` read or write. Done when: the context compiles and lists each type.
2. Replace every `JsonConvert` and `JObject` use in `gluon-control/` with `JsonSerializer` and the context. Done when: `git grep -n Newtonsoft -- gluon-control` returns nothing.
3. Remove the Newtonsoft.Json `PackageReference` and `PackageVersion`. Done when: `dotnet list GluonStack.slnx package` does not list it.
4. Read `config/gluonstack-settings.json` and `gluon-control/config.json` as committed, write them back, and compare. Done when: a test in §5 proves each file round-trips with the same keys and values.

- [ ] Add `gluon-control/Utilities/JsonContext.cs` with a `JsonSerializerContext` for every type `ConfigurationManager` and `PHPManager` read or write. Done when: the context compiles and lists each type.
- [ ] Replace every `JsonConvert` and `JObject` use in `gluon-control/` with `JsonSerializer` and the context. Done when: `git grep -n Newtonsoft -- gluon-control` returns nothing. Cheaper substitute: keeping Newtonsoft for one awkward type.
- [ ] Remove the Newtonsoft.Json `PackageReference` and `PackageVersion`. Done when: `dotnet list GluonStack.slnx package` does not list it.
- [ ] Read `config/gluonstack-settings.json` and `gluon-control/config.json` as committed, write them back, and compare. Done when: a test in §5 proves each file round-trips with the same keys and values.
- [ ] Commit: `refactor: System.Text.Json with source generation`

**Test checkpoint:** `git grep -c Newtonsoft -- gluon-control Directory.Packages.props` prints nothing and `dotnet build GluonStack.slnx -warnaserror` succeeds.

## 5. Test project with the first unit tests

There are no tests. The utilities that read configuration and discover PHP versions are pure enough to test first, and the settings round-trip from §4 needs its proof.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Create `gluon-control.tests/GluonStack.Control.Tests.csproj` (xUnit, `Microsoft.NET.Test.Sdk`) referencing the control panel project, and add it to `GluonStack.slnx`. Done when: `dotnet test GluonStack.slnx` discovers the project.
2. Add `ConfigurationManagerTests` covering a missing file, a malformed file and the round-trip of the committed settings file. Done when: the three tests pass and the round-trip test fails when a property is dropped from `JsonContext`.
3. Add `PhpManagerTests` that point `PHPManager` at a temporary folder of fake version folders. Done when: version discovery returns them sorted and ignores a folder without `php.exe`.
4. Make `ConfigurationManager` and `PHPManager` take their root path through the constructor where they now read a static path. Done when: the tests run without touching the real install root.

- [ ] Create `gluon-control.tests/GluonStack.Control.Tests.csproj` (xUnit, `Microsoft.NET.Test.Sdk`) referencing the control panel project, and add it to `GluonStack.slnx`. Done when: `dotnet test GluonStack.slnx` discovers the project.
- [ ] Add `ConfigurationManagerTests` covering a missing file, a malformed file and the round-trip of the committed settings file. Done when: the three tests pass and the round-trip test fails when a property is dropped from `JsonContext`.
- [ ] Add `PhpManagerTests` that point `PHPManager` at a temporary folder of fake version folders. Done when: version discovery returns them sorted and ignores a folder without `php.exe`.
- [ ] Make `ConfigurationManager` and `PHPManager` take their root path through the constructor where they now read a static path. Done when: the tests run without touching the real install root. Cheaper substitute: tests that read the developer's own `C:\GluonStack`.
- [ ] Commit: `test: GluonStack.Control.Tests with configuration and PHP tests`

**Test checkpoint:** `dotnet test GluonStack.slnx --nologo` reports all tests passed, at least 5 tests.

## 6. Current C# idioms and one code style

With the language at its latest, the code moves to the idioms that remove noise, and a style file keeps it there.

**Phase:** 0
**Needs:** none
**Surface:** no

**Build order:**

1. Add `.editorconfig` with file-scoped namespaces, `var` preferences, and the naming rules the code already follows, each at `warning`. Done when: `dotnet format GluonStack.slnx --verify-no-changes` reports the files that differ.
2. Run `dotnet format GluonStack.slnx` and commit the result. Done when: `dotnet format GluonStack.slnx --verify-no-changes` exits 0.
3. Convert the view models to primary constructors and collection expressions where a constructor only stores its arguments. Done when: the build and tests pass and no view model keeps a field that only mirrors a constructor argument.
4. Replace hand-written `INotifyPropertyChanged` members with CommunityToolkit.Mvvm partial properties where a class already derives from `ObservableObject`. Done when: no `OnPropertyChanged(nameof(` call remains for a property the toolkit can generate.

- [ ] Add `.editorconfig` with file-scoped namespaces, `var` preferences, and the naming rules the code already follows, each at `warning`. Done when: `dotnet format GluonStack.slnx --verify-no-changes` reports the files that differ.
- [ ] Run `dotnet format GluonStack.slnx` and commit the result. Done when: `dotnet format GluonStack.slnx --verify-no-changes` exits 0.
- [ ] Convert the view models to primary constructors and collection expressions where a constructor only stores its arguments. Done when: the build and tests pass and no view model keeps a field that only mirrors a constructor argument.
- [ ] Replace hand-written `INotifyPropertyChanged` members with CommunityToolkit.Mvvm partial properties where a class already derives from `ObservableObject`. Done when: no `OnPropertyChanged(nameof(` call remains for a property the toolkit can generate.
- [ ] Commit: `style: current C# idioms and .editorconfig`

**Test checkpoint:** `dotnet format GluonStack.slnx --verify-no-changes` exits 0 and `dotnet test GluonStack.slnx` passes.
## Verification

- `dotnet build GluonStack.slnx -warnaserror` and `dotnet test GluonStack.slnx` both succeed on a clean clone.
- `git grep -n -E 'net9|Newtonsoft'` returns nothing outside `docs/`.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
