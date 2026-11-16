# Decisions

Numbered decision log. Numbers are never reused. Each entry: date, decision, why,
alternatives rejected, and the spec it came from.

---

### D-001 · Python app

- **Date:** 2026-11-16
- **Decision:** ReelForge is one Python 3.11 app (FastAPI, server-rendered pages with HTMX).
- **Why:** Every local AI model involved (Kokoro, Whisper, lip-sync ports) is Python-first.
- **Rejected:** A Node or Electron app (would wrap Python anyway); a separate SPA front end
  (needs a build step).
- **Spec:** spec-00

### D-002 · SQLite for local state

- **Date:** 2026-11-16
- **Decision:** All local state lives in one SQLite file per Mac, with media on disk and
  paths in the database.
- **Why:** Zero setup, one user at a time per household, nothing to run.
- **Rejected:** Postgres (a server to install and keep running).
- **Spec:** spec-00

### D-003 · No Docker

- **Date:** 2026-11-16
- **Decision:** Everything runs natively on macOS.
- **Why:** The models need direct access to the Mac's GPU, which Docker on macOS does not give.
- **Rejected:** Docker Compose setup.
- **Spec:** spec-00

### D-004 · No Remotion

- **Date:** 2026-11-16
- **Decision:** Remotion is not used.
- **Why:** Its free licence covers only individuals and companies of up to 3 people; this
  tool has 4 users.
- **Rejected:** Remotion for templated video.
- **Spec:** spec-00

### D-005 · ffmpeg assembler

- **Date:** 2026-11-16
- **Decision:** Reels are assembled with ffmpeg, with captions as styled ASS subtitles.
- **Why:** Free, scriptable, standard, low risk; ASS supports per-word highlight styling.
- **Rejected:** Remotion (D-004); MoviePy as the main path (slower, less control).
- **Spec:** spec-00

### D-006 · Manual upload in v1

- **Date:** 2026-11-16
- **Decision:** v1 exports MP4s plus caption text per platform; people upload by hand.
- **Why:** Auto-publishing needs developer apps and platform approvals that take weeks.
- **Rejected:** Direct platform API publishing in v1.
- **Spec:** spec-00

### D-007 · No scheduler built

- **Date:** 2026-11-16
- **Decision:** ReelForge does not include a post scheduler. If needed later, use Postiz
  (open source, self-hostable) through its API.
- **Why:** A solved problem; building one adds no value.
- **Rejected:** Building a scheduler into ReelForge.
- **Spec:** spec-00

### D-008 · Comment-to-link automation deferred

- **Date:** 2026-11-16
- **Decision:** Comment automation is Phase 2. v1 stores the post link per platform in the
  `posts` table so it can be added later.
- **Why:** It needs a public web address and platform approvals; localhost cannot receive
  comment events.
- **Rejected:** Building it in v1.
- **Spec:** spec-00

### D-009 · AI human decided by spike

- **Date:** 2026-11-16
- **Decision:** The AI-human implementation is chosen by the Phase 0 spike (spec-01) before
  any other build. The rest of the build does not change with the outcome.
- **Why:** It is the only part with no proven free path on a MacBook Air.
- **Rejected:** Committing to a lip-sync model up front; a paid avatar service by default.
- **Spec:** spec-00

### D-010 · `master` is the only long-lived branch

- **Date:** 2026-11-16
- **Decision:** The repo uses `master` as its only long-lived branch, as spec-00 section 10
  says. The branch was first pushed as `main` and renamed.
- **Why:** Matches the spec and the workflow rules.
- **Rejected:** Keeping `main`.
- **Spec:** spec-00

### D-011 · Free local script model first

- **Date:** 2026-11-16
- **Decision:** The script engine defaults to a free local model through Ollama. The hosted
  model adapter is built but off by default.
- **Why:** Zeeshan chose zero running cost over stronger hooks for now. Revisit if hook
  quality is not good enough.
- **Rejected:** A small paid model bill by default.
- **Spec:** spec-00 (open question, section 9)

### D-012 · Both Macs have 16 GB RAM

- **Date:** 2026-11-16
- **Decision:** Plan for 16 GB on both Macs. Models load one at a time; the script model is
  unloaded before the AI human renders.
- **Why:** 16 GB is too tight to hold a local script model and the lip-sync model together.
- **Rejected:** Running engines concurrently.
- **Spec:** spec-00 (open question, section 9)

### D-013 · No full-screen photoreal AI human; faceless reels first

- **Date:** 2026-11-16
- **Decision:** The full-screen photoreal AI human is a no-go. v1 builds faceless and
  product-demo reels first. A face may return later through the AI-human adapter, as a small
  corner presenter box, a stylised mascot, a consenting real person filmed once, or a paid
  avatar service. Footage of real people taken from the internet is never used, for testing
  or production.
- **Why:** The spike passed on speed (40 to 55 s per 30 s clip) and stability, but the free
  lip-sync mouth is visibly blurred and reads as AI. That is not acceptable for commercial
  promotion. The faceless pipeline was proven the same day.
- **Rejected:** Shipping the photoreal face full-screen; LatentSync as a rescue before
  shipping anything (kept as a later option); stranger footage from the internet.
- **Spec:** spec-01

### D-014 · Captions drawn in the rendered scene

- **Date:** 2026-11-16
- **Decision:** Reels are rendered as HTML scenes in headless Chromium (Playwright), frame by
  frame, and piped to ffmpeg for encoding and audio. Captions are part of the scene: the
  on-screen text lights up word by word as it is spoken, and a 2 to 4 word strip appears only
  for narration that is not on screen. Replaces the "captions as ASS subtitles" part of D-005;
  ffmpeg still encodes and muxes.
- **Why:** The Homebrew ffmpeg on these Macs has no `subtitles`/`ass` (or `drawtext`) filter.
  Browser rendering gives the brand's real fonts and layouts, and rendered a 40 s reel in
  49 s.
- **Rejected:** Rebuilding ffmpeg with libass (setup burden on both Macs); a separate subtitle
  strip that repeats the on-screen text.
- **Spec:** spec-01 (found while prototyping the faceless reel)
