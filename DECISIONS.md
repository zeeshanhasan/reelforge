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
