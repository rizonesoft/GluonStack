---
schema_version: 1
id: release
domain: 06-release
status: active
title: "TODO-02 -- Release pipeline and operator steps"
depends_on: ["documentation"]
---

# TODO-02 -- Release pipeline and operator steps

> **Goal:** Pushing a version tag builds the installer and a portable archive with checksums as a draft release, and the steps only the owner can take are listed and waiting.

> **Current state:** Measured 2026-11-15. There is no release, no tag and no release workflow. The repository folder is `D:\IsotoneStack` and the remote still carries the old name.

## Inputs

- `docs/plans/2026-11-15-gluonstack-modernisation.md`: the phases table, phase 99.
- D05 T01 §6: the installer build script. D00 T03 §3: the CI workflow.

## Outcome

- A tag `v<version>` produces a draft GitHub release holding the installer, the portable zip and a checksum file.

**Adjacency:** all=not-applicable (a build pipeline: no user-facing record)

**Adjacency rationale:** Publishing the draft and renaming the repository are outward-facing and stay with the operator.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Portable archive | -- | [ ] |
| 2 | §2 | Release workflow on a version tag | §1 | [ ] |
| 3 | §3 | Repository folder and GitHub repository renamed | -- | [ ] |
| 4 | §4 | First release published and installer signed | §2 | [ ] |

## 1. Portable archive

The stack is portable by design; the archive is the installer's contents without the installer.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Add `-Portable` to `installer/Build-Installer.ps1`: stage the same file list the installer takes and zip it as `GluonStack-<version>-portable.zip` with its `.sha256`. Done when: the zip unpacks to a folder that `INSTALL.bat` configures and starts.
2. Take the file list from one place used by both the installer script and the archive. Done when: adding a product script to the list puts it in both.

- [ ] Add `-Portable` to `installer/Build-Installer.ps1`: stage the same file list the installer takes and zip it as `GluonStack-<version>-portable.zip` with its `.sha256`. Done when: the zip unpacks to a folder that `INSTALL.bat` configures and starts.
- [ ] Take the file list from one place used by both the installer script and the archive. Done when: adding a product script to the list puts it in both. Cheaper substitute: a second hand-kept list.
- [ ] Commit: `release: portable archive`

**Test checkpoint:** `pwsh installer/Build-Installer.ps1 -Portable` writes the zip and a matching `.sha256`.

## 2. Release workflow on a version tag

The build a release is made from runs in CI, not on a developer machine.

**Phase:** 6
**Needs:** none
**Surface:** no

**Build order:**

1. Create `.github/workflows/release.yml` on tags `v*`: run the gate, build the installer and the portable archive, create a draft release with the three files and the changelog entry as notes. Done when: a tag on a fork produces a draft release.
2. Fail the workflow when the tag does not equal the assembly version. Done when: a mismatched tag fails before building.
3. Pin each action to a commit SHA and give the job only `contents: write`. Done when: no other permission is granted.

- [ ] Create `.github/workflows/release.yml` on tags `v*`: run the gate, build the installer and the portable archive, create a draft release with the three files and the changelog entry as notes. Done when: a tag on a fork produces a draft release.
- [ ] Fail the workflow when the tag does not equal the assembly version. Done when: a mismatched tag fails before building.
- [ ] Pin each action to a commit SHA and give the job only `contents: write`. Done when: no other permission is granted.
- [ ] Commit: `release: workflow on tag`

**Test checkpoint:** `python -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"` exits 0 and `git grep -n -E 'uses: .*@v[0-9]' -- .github` prints nothing.

## 3. Repository folder and GitHub repository renamed

Renaming the checkout folder and the GitHub repository changes paths and URLs other machines and people hold. It is the owner's act.

**Phase:** 99
**Needs:** operator
**Surface:** no

**Build order:**

1. Rename the GitHub repository to `GluonStack` in its settings and update the local remote with `git remote set-url origin`. Done when: `git remote -v` shows the new URL and `git fetch` works.
2. Rename the checkout folder to `GluonStack` with every session closed, and reinstall the campaign shortcuts with `pwsh scripts/start-campaign.ps1 -InstallShortcut`. Done when: the shortcuts start a session in the renamed folder.

- [ ] Rename the GitHub repository to `GluonStack` in its settings and update the local remote with `git remote set-url origin`. Done when: `git remote -v` shows the new URL and `git fetch` works.
- [ ] Rename the checkout folder to `GluonStack` with every session closed, and reinstall the campaign shortcuts with `pwsh scripts/start-campaign.ps1 -InstallShortcut`. Done when: the shortcuts start a session in the renamed folder.
- [ ] Commit: `chore: repository renamed to GluonStack`

**Test checkpoint:** `git remote get-url origin` prints a URL ending in `GluonStack.git`.

## 4. First release published and installer signed

Publishing is outward-facing, and signing needs a certificate only the owner can buy and hold.

**Phase:** 99
**Needs:** operator
**Surface:** no

**Build order:**

1. Decide whether to sign: obtain a code-signing certificate, store it in the vault, and add the signing step to `installer/Build-Installer.ps1` reading it without printing it. Done when: `Get-AuthenticodeSignature` on the installer reports `Valid`, or the decision not to sign is recorded in `docs/plans/2026-11-15-gluonstack-modernisation.md`.
2. Push the first version tag and publish the draft release after installing its installer on a clean machine. Done when: the release is public with its three files.

- [ ] Decide whether to sign: obtain a code-signing certificate, store it in the vault, and add the signing step to `installer/Build-Installer.ps1` reading it without printing it. Done when: `Get-AuthenticodeSignature` on the installer reports `Valid`, or the decision not to sign is recorded in `docs/plans/2026-11-15-gluonstack-modernisation.md`.
- [ ] Push the first version tag and publish the draft release after installing its installer on a clean machine. Done when: the release is public with its three files.
- [ ] Commit: `release: first release`

**Test checkpoint:** `gh release view --json isDraft -q .isDraft` prints `false` for the first tag.
## Verification

- A tag builds a draft release; the two operator sections are the only open rows.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
