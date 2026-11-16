# spec-02 · App skeleton and design system

**Status:** Draft
**Milestone:** M1
**Covers:** spec-00 sections 2 and 11

## Title

As a household member,
I should be able to install ReelForge with one command and open it in a browser,
so that every later feature has a working, consistent home.

## Why we're building this

Every feature needs the install scripts, the app shell, the database and the design system.
Building them once, first, keeps every screen consistent and every install repeatable.

## Brief

`./setup.sh` installs everything and `./run.sh` starts the app at `localhost:8000`, prints
the LAN address, creates the database, and loads topics from `content/topics.yaml`. The
design system (`DESIGN.md`, tokens, Lucide icons, standard components, `/styleguide`) is set
up before any other screen.

## Acceptance criteria

1. **Clean install**
   GIVEN a clean Apple Silicon Mac with Homebrew
   WHEN a person runs `./setup.sh`
   THEN it installs ffmpeg, Python 3.11, uv, Python dependencies, Playwright's browser and
   model weights, printing pass or fail per step.

2. **Re-runnable setup**
   GIVEN setup already ran
   WHEN `./setup.sh` runs again
   THEN it skips what is installed, changes nothing else, and passes.

3. **Setup failure**
   GIVEN a step fails (no network, no Homebrew)
   WHEN `./setup.sh` runs
   THEN that step prints fail with a plain reason and what to do, and the script exits non-zero.

4. **Run**
   GIVEN setup passed
   WHEN a person runs `./run.sh`
   THEN the app opens at `http://localhost:8000` and the LAN address is printed.

5. **Database created**
   GIVEN no database exists
   WHEN the app starts
   THEN the SQLite file is created with all seven tables in a git-ignored folder.

6. **Topics load**
   GIVEN `content/topics.yaml` and `HOUSEHOLD` set in `.env`
   WHEN the app starts
   THEN topics mirror into the `topics` table and the home screen lists this household's topics.

7. **No topics**
   GIVEN `topics.yaml` has no topics for this household
   WHEN the home screen loads
   THEN it shows the empty state with how to add a topic.

8. **Missing household**
   GIVEN `.env` has no `HOUSEHOLD`
   WHEN the app starts
   THEN it shows an error state explaining how to set it, not a crash.

9. **PIN**
   GIVEN a PIN is set in `.env`
   WHEN someone opens the LAN address from another device
   THEN they must enter the PIN once; `localhost` does not ask.

10. **Design system**
    GIVEN the chosen `DESIGN.md`
    WHEN `/styleguide` is opened
    THEN it shows every standard component (button, input, select, checkbox, card, table,
    status badge, tabs, modal, toast, progress bar, empty state, error state, video preview
    frame) in each state (default, hover, focus, disabled, loading, error), in light and dark.

11. **Tokens only**
    GIVEN the app's stylesheets
    WHEN they are checked
    THEN no component or page style contains a raw colour code or pixel value.

## Engineering notes

- Design pick from getdesign.md is open: builder proposes two options with a one-line reason
  each. Verify `npx getdesign@latest add <slug>` against the current README before running it.
  Use the style only, never a brand's name, logo or assets.
- Plain CSS custom properties, no build step. Lucide icons only.
- `.env.example` documents `HOUSEHOLD`, `PIN`, and later keys.
- `make check` exists from here on: tests plus (from spec-04) a smoke render.

## QA notes

- Fresh macOS user account: clone, `./setup.sh`, `./run.sh`, open on a phone on the same wifi.
- Toggle the system theme; every styleguide component reads correctly in both.

## Wireframe

None.

## Decisions made

<Filled in at release.>
