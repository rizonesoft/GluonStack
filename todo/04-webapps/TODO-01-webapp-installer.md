---
schema_version: 1
id: webapp-installer
domain: 04-webapps
status: active
title: "TODO-01 -- Web application installer"
depends_on: ["control-logs-sites", "control-databases"]
---

# TODO-01 -- Web application installer

> **Goal:** A new WordPress, Laravel or other PHP project is one command or one dialog: downloaded, given a database and a site, and opened.

> **Current state:** Measured 2026-11-15. Nothing exists: no `scripts/Install-WebApp.ps1`, no `config/webapps/`. The pieces it needs are owned elsewhere: Composer (D01 T03 §5), sites (D03 T02 §3), databases (D03 T01), Mailpit's SMTP port.

## Inputs

- `docs/legacy-todo.md`, Web Application Installer: the behaviours wanted.
- D03 T02 §3: `SiteStore` and the per-site configuration files. D01 T03 §5: Composer.

## Outcome

- `scripts/Install-WebApp.ps1 -App wordpress -Name blog` ends with `http://blog.test` showing WordPress, its database created and its mail going to Mailpit.

**Adjacency:** list=applicable @ D04 T01 §1; document=not-applicable (no such surface for a project scaffolder); settings=applicable @ D04 T01 §1; reporting=not-applicable (no such surface for a project scaffolder); notifications=not-applicable (no such surface for a project scaffolder); permissions=not-applicable (no such surface for a project scaffolder); audit=not-applicable (no such surface for a project scaffolder); exchange=not-applicable (no such surface for a project scaffolder); reverse=applicable @ D04 T01 §2

**Adjacency rationale:** The list is `-ListApps`; the reverse of an install is `-Remove`, which removes the site and offers to drop the database and never deletes the folder without `-DeleteFiles`; a recipe's keys are its settings.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | Recipe format and the recipe folder | -- | [ ] |
| 2 | §2 | Install-WebApp.ps1: fetch, database, site, remove | §1 | [ ] |
| 3 | §3 | WordPress recipe | §2 | [ ] |
| 4 | §4 | Laravel recipe | §2 | [ ] |
| 5 | §5 | Drupal, Joomla, Symfony and CodeIgniter recipes | §2 | [ ] |
| 6 | §6 | New project in the control panel | §3 | [ ] |
| 7 | §7 | Projects on the web dashboard | §3 | [ ] |

## 1. Recipe format and the recipe folder

A recipe describes how to get one application: where it comes from, what it needs, what to write and what to run.

**Phase:** 4
**Needs:** none
**Surface:** no

**Build order:**

1. Write `config/webapps/recipe.schema.json`: `id`, `name`, `source` (`zip` with a URL and checksum feed, or `composer` with a package), `php` minimum, `database` (`mariadb`, `postgres`, `none`), `templates` to render, `post_install` steps. Done when: the schema loads as JSON.
2. Add `Get-GluonWebAppRecipe` to `scripts/GluonStack.WebApps.psm1`, validating a recipe on read. Done when: a recipe missing `source` is refused naming the key.
3. Add `-ListApps` output: id, name, source type, database. Done when: it lists every recipe in `config/webapps/`.
4. Add a `plain-php` recipe: an `index.php` skeleton and no database. Done when: the recipe validates.

- [ ] Write `config/webapps/recipe.schema.json`: `id`, `name`, `source` (`zip` with a URL and checksum feed, or `composer` with a package), `php` minimum, `database` (`mariadb`, `postgres`, `none`), `templates` to render, `post_install` steps. Done when: the schema loads as JSON.
- [ ] Add `Get-GluonWebAppRecipe` to `scripts/GluonStack.WebApps.psm1`, validating a recipe on read. Done when: a recipe missing `source` is refused naming the key.
- [ ] Add `-ListApps` output: id, name, source type, database. Done when: it lists every recipe in `config/webapps/`.
- [ ] Add a `plain-php` recipe: an `index.php` skeleton and no database. Done when: the recipe validates.
- [ ] Commit: `webapps: recipe format`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/WebApps.Tests.ps1 -CI"` reports 0 failed.

## 2. Install-WebApp.ps1: fetch, database, site, remove

The engine every recipe runs through.

**Phase:** 4
**Needs:** none
**Surface:** no

**Build order:**

1. Create `scripts/Install-WebApp.ps1` and its launcher with `-App`, `-Name`, `-Database`, `-ListApps`, `-Remove`. Done when: the help lists them with examples.
2. Fetch a `zip` source to staging, verify its checksum, and extract to `www\<name>`; run `composer create-project` for a `composer` source with the stack's PHP. Done when: the folder holds the application.
3. Create the database and a user with a generated password on the recipe's server, refusing an existing database name. Done when: the database exists and the password is in the rendered configuration only.
4. Create the site `<name>.test` through the same per-site file format `SiteStore` reads, with the hosts entry. Done when: the site appears in the control panel's Sites pane.
5. Render the recipe's templates with the database, URL and Mailpit values, then run `post_install`. Done when: the application's configuration file holds the values.
6. On any failed step undo the steps already done: remove the site, drop the database it created, delete the folder it created. Done when: a failed download leaves nothing behind.
7. Implement `-Remove`: remove the site, ask before dropping the database, keep the folder unless `-DeleteFiles`. Done when: the site is gone and the folder remains.

- [ ] Create `scripts/Install-WebApp.ps1` and its launcher with `-App`, `-Name`, `-Database`, `-ListApps`, `-Remove`. Done when: the help lists them with examples.
- [ ] Fetch a `zip` source to staging, verify its checksum, and extract to `www\<name>`; run `composer create-project` for a `composer` source with the stack's PHP. Done when: the folder holds the application.
- [ ] Create the database and a user with a generated password on the recipe's server, refusing an existing database name. Done when: the database exists and the password is in the rendered configuration only.
- [ ] Create the site `<name>.test` through the same per-site file format `SiteStore` reads, with the hosts entry. Done when: the site appears in the control panel's Sites pane.
- [ ] Render the recipe's templates with the database, URL and Mailpit values, then run `post_install`. Done when: the application's configuration file holds the values.
- [ ] On any failed step undo the steps already done: remove the site, drop the database it created, delete the folder it created. Done when: a failed download leaves nothing behind. Cheaper substitute: leaving a half-installed project.
- [ ] Implement `-Remove`: remove the site, ask before dropping the database, keep the folder unless `-DeleteFiles`. Done when: the site is gone and the folder remains.
- [ ] Commit: `webapps: Install-WebApp.ps1`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/Install-WebApp.Tests.ps1 -CI"` reports 0 failed. The failed-step test asserts nothing is left.

## 3. WordPress recipe

The most common request.

**Phase:** 4
**Needs:** none
**Surface:** no

**Build order:**

1. Add `config/webapps/wordpress.json`: the latest zip and its SHA-1 from the `wordpress.org` version-check API, a `wp-config.php` template with salts from the secret-key API. Done when: an install shows WordPress's setup page.
2. Point WordPress mail at Mailpit with a must-use plugin written by the recipe. Done when: a password reset mail arrives in the Mailpit inbox.
3. Add an optional headless setup through WP-CLI when `-AdminUser` is given. Done when: the site opens on its front page with the admin created.

- [ ] Add `config/webapps/wordpress.json`: the latest zip and its SHA-1 from the `wordpress.org` version-check API, a `wp-config.php` template with salts from the secret-key API. Done when: an install shows WordPress's setup page.
- [ ] Point WordPress mail at Mailpit with a must-use plugin written by the recipe. Done when: a password reset mail arrives in the Mailpit inbox.
- [ ] Add an optional headless setup through WP-CLI when `-AdminUser` is given. Done when: the site opens on its front page with the admin created.
- [ ] Commit: `webapps: WordPress recipe`

**Test checkpoint:** `pwsh scripts/Install-WebApp.ps1 -App wordpress -Name wptest` then `curl -s -o NUL -w "%{http_code}" http://wptest.test/` prints `200` or `302`.

## 4. Laravel recipe

The most common framework.

**Phase:** 4
**Needs:** none
**Surface:** no

**Build order:**

1. Add `config/webapps/laravel.json`: `composer create-project laravel/laravel`, an `.env` template with the database and Mailpit values, the document root at `public`. Done when: the site shows Laravel's welcome page.
2. Run `php artisan key:generate` and `php artisan migrate` as `post_install`. Done when: the migrations table exists.
3. Offer `-Database postgres`. Done when: the `.env` uses `pgsql` and migrations run on PostgreSQL.

- [ ] Add `config/webapps/laravel.json`: `composer create-project laravel/laravel`, an `.env` template with the database and Mailpit values, the document root at `public`. Done when: the site shows Laravel's welcome page.
- [ ] Run `php artisan key:generate` and `php artisan migrate` as `post_install`. Done when: the migrations table exists.
- [ ] Offer `-Database postgres`. Done when: the `.env` uses `pgsql` and migrations run on PostgreSQL.
- [ ] Commit: `webapps: Laravel recipe`

**Test checkpoint:** `pwsh scripts/Install-WebApp.ps1 -App laravel -Name lvtest` then `curl -s -o NUL -w "%{http_code}" http://lvtest.test/` prints `200`.

## 5. Drupal, Joomla, Symfony and CodeIgniter recipes

The rest of the backlog's list, each a recipe file and nothing more.

**Phase:** 4
**Needs:** none
**Surface:** no

**Build order:**

1. Add `config/webapps/drupal.json` (Composer project, `settings.php` template). Done when: the site shows Drupal's installer.
2. Add `config/webapps/joomla.json` (zip, `configuration.php` left to Joomla's installer, database precreated). Done when: the site shows Joomla's installer.
3. Add `config/webapps/symfony.json` and `config/webapps/codeigniter.json` (Composer projects, `.env` templates). Done when: each site shows its welcome page.
4. Add one test per recipe that validates it and renders its templates with sample values. Done when: the tests pass offline.

- [ ] Add `config/webapps/drupal.json` (Composer project, `settings.php` template). Done when: the site shows Drupal's installer.
- [ ] Add `config/webapps/joomla.json` (zip, `configuration.php` left to Joomla's installer, database precreated). Done when: the site shows Joomla's installer.
- [ ] Add `config/webapps/symfony.json` and `config/webapps/codeigniter.json` (Composer projects, `.env` templates). Done when: each site shows its welcome page.
- [ ] Add one test per recipe that validates it and renders its templates with sample values. Done when: the tests pass offline.
- [ ] Commit: `webapps: Drupal, Joomla, Symfony, CodeIgniter recipes`

**Test checkpoint:** `pwsh -NoProfile -Command "Invoke-Pester scripts/tests/WebApps.Tests.ps1 -CI"` reports 0 failed.

## 6. New project in the control panel

The same engine from the application.

**Phase:** 4
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (sections 6.4 (dialog) and 6.6, Sites) and `docs/design/reference/control-panel.dc.html`.
**Job:** Start a new WordPress, Laravel or other project in one step.
**Treatment:** Tokens from `gluon-control/Themes/Tokens.xaml` only; no raw hex value on a control.
**Chrome:** A dialog over the main window.

**Build order:**

1. Add `new project` to the Sites pane beside `new site`: a dialog with the application (from `-ListApps`), name and database server. Done when: the dialog lists the real recipes.
2. Run `Install-WebApp.ps1` with the step shown on the status line, cancellable, with the whole process tree stopped on cancel. Done when: a cancelled install leaves nothing behind.
3. Register `new project <app> <name>`. Done when: the command opens the dialog filled in.
4. Mark a site created from a recipe with its application in the Sites table. Done when: the row reads `wordpress` beside the name.

- [ ] Add `new project` to the Sites pane beside `new site`: a dialog with the application (from `-ListApps`), name and database server. Done when: the dialog lists the real recipes.
- [ ] Run `Install-WebApp.ps1` with the step shown on the status line, cancellable, with the whole process tree stopped on cancel. Done when: a cancelled install leaves nothing behind.
- [ ] Register `new project <app> <name>`. Done when: the command opens the dialog filled in.
- [ ] Mark a site created from a recipe with its application in the Sites table. Done when: the row reads `wordpress` beside the name.
- [ ] Commit: `webapps: new project in the control panel`

**Test checkpoint:** `dotnet test GluonStack.slnx --filter FullyQualifiedName~NewProject` reports all passed.

## 7. Projects on the web dashboard

The landing page lists what is installed.

**Phase:** 4
**Needs:** none
**Surface:** yes
**Fidelity:** `docs/design/SPEC.md` (section 10, Landing) and `docs/design/reference/other-surfaces.dc.html`.
**Job:** See and open the projects on this machine.
**Treatment:** Tokens from `default/assets/tokens.css` only; no raw hex value in a page.
**Chrome:** A browser page served by the stack's own Apache; no application chrome.

**Build order:**

1. Add a projects list to `default/index.php`: each site with its application and a link, read from the per-site files. Done when: an installed WordPress site is listed and links to it.
2. Show nothing but one sentence when there are no projects. Done when: the empty sentence names the control panel's `new project`.

- [ ] Add a projects list to `default/index.php`: each site with its application and a link, read from the per-site files. Done when: an installed WordPress site is listed and links to it.
- [ ] Show nothing but one sentence when there are no projects. Done when: the empty sentence names the control panel's `new project`.
- [ ] Commit: `webapps: projects on the web dashboard`

**Test checkpoint:** `curl -s http://localhost/ | findstr /C:"wptest.test"` finds the link after the WordPress test install.
## Verification

- WordPress and Laravel each install, open and are removed cleanly, from the script and from the control panel.
- `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` pass.
