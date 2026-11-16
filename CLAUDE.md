# CLAUDE.md

Standing instructions for Claude Code working in this repo.

## What ReelForge is

A local Mac app that makes 4 ready-to-post vertical reels a day (Instagram Reels, TikTok,
YouTube Shorts) for Prept (prept.fyi), at zero running cost wherever possible.

- Three reel formats: AI-human talking head, product demo (screen capture of Prept),
  faceless text plus voiceover.
- Pipeline: topic → script → voice → captions → visual → assemble → review → export.
- Users: two households, one install each, four people. Two of them never use a terminal.
- Upload to platforms is manual in v1. No auto-publishing, no scheduler, no comment automation.

The full reference is `specs/spec-00-master.md`. Read it before starting any spec.

## Where things are

| File | What it holds |
| --- | --- |
| `ARCHITECTURE.md` | Components, how one reel is made, folder layout, adapters |
| `DECISIONS.md` | Numbered decision log (D-001, ...) |
| `DESIGN.md` | Design system for the app's own screens |
| `README.md` | Setup, daily use, troubleshooting, for humans |
| `specs/TRACKER.md` | Status of every spec. Single source of truth |
| `specs/README.md` | How we work (spec format, build and release flow) |
| `specs/_template.md` | Template for new specs |
| `docs/` | Spike results, benchmarks, licences |

## Commands

Not built yet. They arrive with spec-02 (skeleton). Planned:

- `./setup.sh`: install everything (Homebrew packages, Python deps, Playwright browser,
  model weights). Re-runnable, prints pass or fail per step.
- `./run.sh`: start the app at `http://localhost:8000` and print the LAN address.
- `make check`: run tests plus a 10-second smoke render. Must be green before a PR.

Update this section when the commands exist.

## Stack (do not change without a decision entry)

- Python 3.11, managed with `uv`. FastAPI with server-rendered pages and HTMX.
- SQLite for local state. One in-process worker renders one reel at a time.
- ffmpeg assembles video, with captions as styled ASS subtitles.
- Local AI: Ollama (script), mlx-audio with Kokoro (voice), mlx-whisper (word timings),
  lip-sync model chosen by the spike (AI human), Playwright (demo capture).
- **Never** use Remotion (licence does not cover 4 users) or Docker (models need the GPU).
- No paid service on the default path. Paid options sit behind an adapter, off by default.

## Coding conventions

- Every engine (script, voice, captions, AI human, visual source) sits behind a small
  interface with one default implementation. Swapping one must not touch the others.
- Long jobs must survive a closed lid: an interrupted job restarts cleanly on next launch,
  and a retry resumes from the failed step using assets already made.
- Generated media lives on disk; the database stores paths only.
- Shared through git: code, `assets/character/`, `content/`, templates, `flows/`.
  Local only (git-ignored): the SQLite file, generated audio and video, `exports/`, `.env`.
- Secrets (Prept demo account, optional API keys, household id, PIN) live in `.env` only.
  Never commit them. Keep `.env.example` current.
- Tests cover at least: the script validator, job state changes, retry-from-failed-step.
- Any claim marked **untested** in a spec must be proven before code depends on it.

## Interface work

- Read `DESIGN.md` before any interface work.
- Build pages only from the standard components. A one-off style on a page is a defect.
- No raw colour codes or pixel values in component or page styles: use tokens.
- Icons: Lucide only. No emoji as icons.
- New components go on the `/styleguide` page first, then get used.
- Check every new screen against `/styleguide` before opening a pull request.
- Every screen handles empty, loading, error and success states.
- The app's design system and Prept's reel branding (`content/brand/`) are never mixed.

## Workflow rules

`master` is the only long-lived branch. No `develop` or staging branch.

1. Pick the next spec marked **Ready** in `specs/TRACKER.md`. One spec at a time.
2. Branch from `master`, named after the spec: `spec-01-ai-human-spike`.
3. Set the tracker row to **In progress** with the branch name and start date.
4. Build. Prefix every commit with the spec number: `spec-01: add lip-sync benchmark script`.
5. When every acceptance criterion passes and `make check` is green, set the status to
   **In review** and open a pull request to `master`.
6. Zeeshan or Sarosh approves. Nothing merges without a human approval.
7. Release: merge to `master`, tag it `spec-NN`, delete the branch.
8. In the same merge: set the spec to **Released**, fill in **Decisions made**, copy those
   into `DECISIONS.md`, update the tracker row with the release date, and update
   `ARCHITECTURE.md` and `README.md` if anything changed.

Rules:

- Changes to specs, the tracker or docs alone may be committed straight to `master`.
- New spec number = highest number in `specs/TRACKER.md` plus one. Numbers are never reused.
- A spec that turns out too big is split into new numbered specs, not stretched.
- If you must deviate from a spec: stop, record the reason in the spec, and ask first.
- Update `README.md` in the same change as any behaviour it describes.
- Record real render times on the Air in `docs/benchmarks.md`. If 4 reels take more than
  2 hours in total, stop and report before continuing.
