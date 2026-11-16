# ReelForge — Build Spec

Nov 16, 2026 · @Zeeshan Hasan

## 1. Goal and scope

Build ReelForge, a local Mac app that produces 4 ready-to-post vertical reels a day for Prept (prept.fyi), for Instagram Reels, TikTok and YouTube Shorts, at zero running cost wherever possible.

**In scope for v1**

- Three reel formats: AI-human talking head, product demo (screen capture of Prept), and faceless text plus voiceover.
- Script generation from a topic list, local AI voiceover, burned-in captions, branding, 9:16 export.
- A local web app to queue, preview, approve, regenerate and download reels.
- Caption and hashtag text per platform, exported next to each video for manual upload.

**Out of scope for v1**

- Auto-publishing to any platform. Upload is manual.
- Comment-to-link automation. See section 8.
- A text-post scheduler. Use an existing open-source tool if needed later (section 8).

**Hard constraints**

- Runs on Apple Silicon MacBooks, including a fanless M5 Air. RAM is not yet known (section 9).
- No paid service is required for the default path. Any paid option sits behind an adapter and is off by default.
- Every claim in this spec marked **untested** must be proven by the builder before code depends on it.

## 2. Users and setup

Four people in two households use it: Zeeshan and his wife on one Mac, Sarosh and his wife on another. Each household runs its own install.

**Install and run**

- One private GitHub repo: https://github.com/zeeshanhasan/reelforge.git. `git clone`, then `./setup.sh`, then `./run.sh`.
- `setup.sh` installs everything: Homebrew packages (ffmpeg, Python 3.11, uv), Python dependencies, Playwright's browser, and model weights. It must be re-runnable and print a clear pass or fail per step.
- `run.sh` starts the app at `http://localhost:8000` and prints the local network address so the second person in the house can open it from their own device on the same wifi.
- No accounts or login. An optional shared PIN protects the local network address.

**What is shared and what is local**

- Shared through git: code, the AI human's face and base video, the brand voice settings, templates, demo flow scripts, and the topic list.
- Local to each Mac: the SQLite database, generated audio and video, and exports. These are git-ignored.
- To stop both households making the same reel, each topic in the shared topic list has an `owner` field (household A or B). The app only picks topics owned by its own household. The household is set once in a local `.env` file.

**Non-technical users**

The two wives should never need a terminal after setup. Everything they do happens in the web app: pick topics, generate, review, download.

## 3. Stack and architecture

One Python app with a browser front end, a SQLite file, and a single background worker that renders one reel at a time. Python is chosen because every local AI model involved is Python-first.

**How one reel is made**

1. Pick a topic and a format.
2. Script engine writes the script as structured JSON.
3. Voice engine turns the narration into a WAV file.
4. Caption engine gets word-level timings from that audio.
5. Visual source produces the picture: AI-human clip, recorded Prept demo, or background footage.
6. Assembler combines picture, audio, captions, logo and music into a 1080x1920 MP4.
7. The reel lands in the review queue. A person approves, regenerates or rejects it.
8. Approved reels are exported with their caption text.

**Components**

| Part | Choice | Licence and cost | Status |
| --- | --- | --- | --- |
| Web app and API | FastAPI, server-rendered pages with HTMX | Free, permissive | Standard, low risk |
| Database | SQLite | Free | Standard, low risk |
| Job queue | One in-process worker, jobs stored in SQLite | Free | Low risk. One render at a time, because the Air has no fan |
| Script engine | Adapter: local model through Ollama by default, optional API key for a hosted model | Free by default | **Untested** which local model writes good enough hooks on this RAM |
| Voice | mlx-audio with Kokoro as default voice | Free, runs on Apple Silicon | Reported to work on Apple Silicon. **Untested** on these Macs |
| Captions timing | Whisper running locally (mlx-whisper), word timestamps | Free | **Untested**: confirm word-level timestamps before relying on them |
| AI human | Lip-sync model with a Mac port (MuseTalk port first, LatentSync MLX port as the quality alternative) | Free code. **Check model weight licences for commercial use** | **Untested**. Decided by the Phase 0 spike |
| Demo capture | Playwright (Python) recording a phone-sized browser | Free, Apache-2.0 | Recording is standard. Auto-zoom is **untested** |
| Assembler | ffmpeg, with captions as styled ASS subtitles | Free | Standard, low risk |

**Rules for the builder**

- Every engine (script, voice, AI human, visual source) sits behind a small interface with one default implementation, so a part can be swapped without touching the rest.
- Do not use Remotion. Its free licence covers only individuals and companies of up to 3 people, and this tool has 4 users.
- No Docker. The models need direct access to the Mac's GPU.
- Long jobs must survive a closed laptop lid: a job interrupted mid-render restarts cleanly on next launch.

Sources: [fast-lipsync](https://github.com/Lulzx/fast-lipsync), [LatentSync MLX](https://github.com/sb1992/latentsync-mlx), [mlx-audio](https://github.com/blaizzy/mlx-audio), [Remotion licence](https://www.remotion.dev/docs/license/faq).

## 4. Phase 0 spike: prove the AI human first

Build nothing else until this spike returns a go or no-go, because the AI human is the only part with no proven free path on a MacBook Air. Time-box it to one day.

**What the spike must produce**

One 30-second vertical clip of a photoreal AI-generated person speaking a Prept script, made entirely on Zeeshan's Mac.

**Steps**

1. Record the Mac's chip, RAM and macOS version in `docs/spike.md`.
2. Create the character: one photoreal face image of a person who does not exist. Any free image generator is fine, since this is done once. Save it to `assets/character/face.png`.
3. Turn the still into a base video: 10 to 20 seconds of the face idling (blinking, small head movement). Try an open-source portrait animator such as LivePortrait. **Untested on Mac.**
4. Generate 30 seconds of narration with the voice engine.
5. Lip-sync the base video to the narration with the MuseTalk Mac port. If quality is poor, try the LatentSync MLX port.
6. Record for each attempt: render time, peak memory, whether the Mac throttled, and an honest quality note on mouth, teeth and identity drift.

**Go if all of these hold**

- A 30-second clip renders in under 15 minutes.
- Four clips can render back to back without a crash.
- Two people who did not build it say the face is acceptable for social media.

**If no-go, in this order**

1. Shrink the face: show the AI human only for the 3-second hook, then cut to demo or text.
2. Record a real person once (2 to 3 minutes of footage) and lip-sync that instead. This path has the strongest evidence of working.
3. Use a paid avatar service through the AI-human adapter, for this step only.

The rest of the build does not change with the outcome. Only the AI-human adapter's implementation does.

## 5. Features

Eight features make up v1. Each lists what it must do, not how.

### 5.1 Topics

- A shared topic list lives in the repo as `content/topics.yaml`. Each topic has: title, angle, format (ai\_human, demo, faceless), owner household, and status.
- Users can add, edit and retire topics in the web app. Edits are written back to the file so they can be committed.
- The app never offers a topic that already has an approved reel on this Mac.

### 5.2 Script engine

- Input: one topic plus the Prept brand brief (`content/brand.md`: what Prept is, audience, tone, banned claims).
- Output: JSON with a hook (under 3 seconds spoken), 3 to 5 beats, a call to action, on-screen text per beat, and total length of 20 to 45 seconds spoken.
- Also outputs post text per platform: Instagram caption with hashtags, TikTok caption, YouTube Shorts title and description. Optional: a LinkedIn post and an X post on the same topic.
- A user can edit any script in the web app before rendering, and can ask for 3 alternative hooks.
- Invalid or over-length output is rejected and retried, up to 3 times, then shown as failed with the reason.

### 5.3 Voice

- One brand voice, set in `content/voice.yaml` and shared by both households.
- Narration is generated per beat so a single beat can be re-voiced without redoing the reel.
- Audio is normalised to a consistent loudness.

### 5.4 Captions

- Word-level timings come from the generated audio.
- Captions are burned in, 2 to 4 words at a time, with the current word highlighted, kept inside the safe area that platform buttons do not cover.
- One caption style per brand, defined in a template file.

### 5.5 AI human

- One fixed character, stored in `assets/character/`, used by both households so the brand has one face.
- Input: narration audio. Output: a lip-synced vertical clip of the character.
- Two modes per reel: full talking head, or hook only (first 3 seconds, then cut away).
- Implementation comes from the Phase 0 spike result.

### 5.6 Product demo capture

- Each demo is a flow file in `flows/` describing the steps: go to a page, tap, type, wait, with an optional narration line per step.
- The recorder logs into a dedicated Prept demo account, runs the flow in a phone-sized viewport, and saves a video plus a timestamped log of every tap position.
- The assembler uses that log to zoom toward each tap, show a tap marker, and speed up waits.
- The demo account's credentials live in the local `.env` and are never committed.
- A flow that fails (element not found, timeout) reports which step broke and saves a screenshot.
- Manual fallback: a user can upload their own phone screen recording and use it as the visual source.

### 5.7 Assembler

- Output: 1080x1920, 30 fps, H.264 video, AAC audio, MP4.
- Layers: visual source, captions, logo, optional background music ducked under the voice, end card with call to action.
- Templates define layout per format. Changing a template must not need code changes elsewhere.
- Music and footage must come from a local `assets/` library the team has rights to use. The tool ships with none.

### 5.8 Review queue and export

- Home screen shows today's target (4), what is queued, rendering, ready for review, approved and failed.
- One button, **Generate today's batch**, picks 4 topics across formats and renders them in sequence.
- Each reel has a preview player, its script, its post text, and three actions: approve, regenerate (whole reel, or only voice, or only visuals), reject with a reason.
- Approved reels export to `exports/YYYY-MM-DD/<slug>/` with the MP4 and one text file per platform. A **Copy caption** button sits beside each platform.
- A user marks each reel as posted per platform, with the post link, so there is a record of what went where.
- Every state needs handling: empty (no topics), loading (rendering with progress and time estimate), error (clear reason and a retry), success.

## 6. Data model

Seven SQLite tables hold everything local to one Mac. Generated media files live on disk and the database stores their paths.

| Table | Holds | Key fields |
| --- | --- | --- |
| `topics` | Mirror of `content/topics.yaml` | id, title, angle, format, owner, status |
| `scripts` | One script version per row | id, topic\_id, version, json, edited\_by\_user, created\_at |
| `reels` | One reel per row | id, topic\_id, script\_id, format, status, video\_path, duration\_s, reject\_reason, created\_at |
| `assets` | Intermediate files for a reel | id, reel\_id, kind (voice, captions, face\_clip, demo\_clip), path, meta\_json |
| `jobs` | Render queue | id, reel\_id, step, status, progress, error, started\_at, finished\_at |
| `posts` | Post text and posting record | id, reel\_id, platform, caption, posted\_at, post\_url |
| `settings` | Local config | key, value |

**Reel statuses:** draft, queued, rendering, review, approved, rejected, failed.

**Job steps:** script, voice, captions, visual, assemble. A failed job records the step and error, and a retry resumes from the failed step using assets already made.

## 7. Build order

Build in seven milestones, each ending in something a person can run and check. Do not start a milestone until the one before it passes.

| # | Milestone | Done when |
| --- | --- | --- |
| M0 | AI-human spike (section 4) | `docs/spike.md` has a go or no-go with timings and a sample clip |
| M1 | Skeleton | On a clean Mac, `./setup.sh` then `./run.sh` opens the app, the database is created, and topics load from the YAML file |
| M2 | Script engine | A topic produces a valid script and post text. A user can edit it and request alternative hooks |
| M3 | First full reel, faceless | One click turns a topic into a captioned, voiced, branded 9:16 MP4 that plays correctly on a phone |
| M4 | Product demo reels | One flow file against the Prept demo account produces a demo reel with zooms and tap markers |
| M5 | AI human in the pipeline | The spike's winning method runs as an adapter. Both full and hook-only modes render |
| M6 | Daily batch and second install | **Generate today's batch** renders 4 reels unattended. Sarosh installs from the README alone, with no help |

**Checks that apply to every milestone**

- Automated tests cover the script validator, job state changes and retry-from-failed-step.
- A `make check` command runs tests and a 10-second smoke render.
- The README is updated in the same change: setup, daily use, how to add a topic, how to add a demo flow, troubleshooting.
- Record real render times on the Air in `docs/benchmarks.md`. If 4 reels take more than 2 hours in total, stop and report before continuing.

## 8. Phase 2, not part of this build

Three things wait until the reel factory works, because each depends on outside approvals or a public server.

**Comment-to-link automation** (someone comments, they get a Prept link)

- It cannot run on localhost. Platforms send comment events to a public web address.
- Instagram: believed possible through Meta's official API with a business account, a Meta app and app review. A hosted tool such as ManyChat is the quick alternative. **Not verified.**
- YouTube: no direct messages exist. A reply to the comment with the link is the most that is possible.
- TikTok: no known official way to auto-message commenters. **Not verified.**
- Design v1 so this can be added: every reel stores its post link per platform (the `posts` table).

**Auto-publishing and text posts**

- Do not build a scheduler. [Postiz](https://github.com/gitroomhq/postiz-app) is open source, self-hostable and covers LinkedIn, X, Instagram, TikTok and YouTube.
- Self-hosting it means registering your own developer apps with Meta, YouTube and TikTok, and approval can take weeks.
- v1 hand-off is the export folder. A later step can push approved reels to Postiz through its public API.

**Performance loop**

- Log views and follows per reel, by hand at first, then feed the best hooks and formats back into the script engine's prompt.

## 9. Open questions and risks

Five questions need an answer from Zeeshan, and the builder should ask them at the start rather than guess.

**Questions**

- [ ] How much RAM does each Mac have? This decides which local models are realistic. Under 16 GB makes the AI human and a local script model unlikely to run together.
- [ ] Is every Prept feature worth showing available on the web, or are some mobile-app only? App-only features need manual screen recordings.
- [ ] Script writing: is a free local model acceptable if hooks are weaker, or is a small paid model bill acceptable for better scripts?
- [ ] Who creates the Prept demo account and its fake data?
- [ ] What does the AI human look and sound like: gender, age range, accent, name?

**Risks**

| Risk | Effect | Mitigation |
| --- | --- | --- |
| Free lip-sync looks fake on a photoreal face | The main format fails | Phase 0 spike first, with three fallbacks in section 4 |
| Fanless Air throttles on long renders | 4 reels a day takes hours | One render at a time, batch overnight, benchmark at every milestone |
| Model weight licences forbid commercial use | Legal exposure for Prept | Builder checks each model's licence and lists them in `docs/licences.md` before M5 |
| Platforms require labels on realistic AI-generated people | Reels limited or removed | Check each platform's current AI-content rule before the first post, and add the label on upload |
| Prept's interface changes | Demo flows break | Flows report the failing step, and are quick to fix |
| Same face and format every day | Viewers tune out | Mix the three formats in each daily batch, and use hook-only mode often |
| Setup fails on the second household's Mac | Sarosh cannot run it | M6 requires a clean install from the README alone |

## 10. Repo and how we work

All work lives in `https://github.com/zeeshanhasan/reelforge.git`, with `master` as the only long-lived branch. Each feature has its own numbered spec, is built on its own short-lived branch, and merges to `master` when released.

### 10.1 Files the builder creates first

This bootstrap is done once, directly on `master`, before any feature work.

| File | Purpose |
| --- | --- |
| `CLAUDE.md` | Standing instructions for Claude Code: what ReelForge is, setup and test commands, coding conventions, the workflow rules in 10.3, and pointers to the files below. Keep it under 150 lines |
| `ARCHITECTURE.md` | Components, how one reel is made, folder layout, adapters. Updated whenever a spec changes the structure |
| `DECISIONS.md` | Numbered decision log (D-001, D-002, ...). Each entry: date, decision, why, alternatives rejected, the spec it came from |
| `DESIGN.md` | The design system (section 11) |
| `README.md` | Setup, daily use, troubleshooting, for humans |
| `specs/README.md` | How we work: a copy of 10.2 and 10.3 |
| `specs/TRACKER.md` | The project tracker: one row per spec. Single source of truth for status |
| `specs/_template.md` | The spec template (10.2) |
| `specs/spec-00-master.md` | This document, kept as the overall reference |

Seed `DECISIONS.md` with the decisions this document already makes: Python app, SQLite, no Docker, no Remotion, ffmpeg assembler, manual upload in v1, no scheduler built, comment automation deferred, AI human decided by spike.

### 10.2 Specs and the tracker

- Every feature gets its own file: `specs/spec-NN-short-name.md`. Numbers start at 01, go up by one, and are never reused, even if a spec is dropped.
- Before creating a spec, read `specs/TRACKER.md` and take the highest number plus one.
- Each spec follows the template: **Title** (As a / I should / so that), **Why we're building this**, **Brief** (2 to 3 sentences), **Acceptance criteria** (GIVEN / WHEN / THEN, covering happy and unhappy paths and every screen state), **Engineering notes**, **QA notes**, **Wireframe** (link, if any), **Decisions made**, **Status**.
- Specs describe what, not how. Each should be small enough to release on its own.
- `specs/TRACKER.md` is one table: spec number, title, status, branch, started, released, notes.
- Statuses: Draft, Ready, In progress, In review, Released, Dropped.

**Starting list**, split out of this document during bootstrap:

| Spec | Feature | Covers |
| --- | --- | --- |
| spec-01 | AI-human spike | Section 4 (milestone M0) |
| spec-02 | App skeleton and design system | Sections 2 and 11 (M1) |
| spec-03 | Topics and script engine | 5.1, 5.2 (M2) |
| spec-04 | First full reel: voice, captions, assembler | 5.3, 5.4, 5.7 (M3) |
| spec-05 | Product demo capture | 5.6 (M4) |
| spec-06 | AI human in the pipeline | 5.5 (M5) |
| spec-07 | Review queue, daily batch, export, second install | 5.8 (M6) |

### 10.3 Build and release flow

1. Pick the next spec marked Ready in the tracker. Work on one spec at a time.
2. Create the branch from `master`, named after the spec: `spec-01-ai-human-spike`.
3. Set the tracker row to In progress, with the branch name and start date.
4. Build. Prefix every commit with the spec number: `spec-01: add lip-sync benchmark script`.
5. When every acceptance criterion passes and `make check` is green, set the status to In review and open a pull request to `master`.
6. Zeeshan or Sarosh approves. Nothing merges without a human approval.
7. Release: merge to `master`, tag it `spec-01`, delete the branch.
8. Close the spec in the same merge: set its status to Released, fill in **Decisions made**, copy those decisions into `DECISIONS.md`, update the tracker row with the release date, and update `ARCHITECTURE.md` and `README.md` if anything changed.

**Rules**

- No `develop` or staging branch for now. Everything lands in `master`.
- Changes to specs, the tracker or docs alone may be committed straight to `master`.
- A spec that turns out too big is split into new numbered specs, not stretched.
- If the builder has to deviate from a spec, it stops, records the reason in the spec, and asks before continuing.

## 11. Design system

The web app follows one design system, defined in a `DESIGN.md` file at the repo root, so every screen uses the same tokens, icons and components. It is set up in spec-02, before any screen is built.

**Source**

- Take the `DESIGN.md` from [getdesign.md](https://getdesign.md/design-md), a catalogue of ready-made design system files written for AI coding agents. Install with `npx getdesign@latest add <slug>`, which places the file at the repo root. **Verify the command against the current README before running it.**
- These files are inspired by well-known brands and are not official. Use the style only. Never copy a brand's name, logo or assets.

* [ ] Zeeshan picks which design from the catalogue. Until then, the builder proposes two options with a one-line reason each.

**Tokens**

- All design tokens live in one file as CSS custom properties: colour (with light and dark themes), type scale, spacing, radius, shadow, motion.
- No raw colour codes or pixel values in component or page styles. Everything references a token.
- Plain CSS, with no build step, to keep setup simple.

**Icons**

- One standard icon set for the whole app: Lucide (open source). No mixing sets, no emoji as icons.

**Components**

- A fixed set of standard components, built once and reused: button, input, select, checkbox, card, table, status badge, tabs, modal, toast, progress bar, empty state, error state, video preview frame.
- Each component covers its states: default, hover, focus, disabled, loading, error.
- A `/styleguide` page in the app shows every component and state. A new component is added there first, then used.
- Pages are built only from these components. A one-off style on a page is a defect.

**Scope**

- This design system governs the ReelForge app's own screens.
- The reels themselves follow Prept's brand, kept separately in `content/brand/` (logo, colours, fonts, caption style). The two are never mixed.

**Rule for the builder**

`CLAUDE.md` must tell Claude Code to read `DESIGN.md` before any interface work, and to check new screens against the styleguide before opening a pull request.

Sources: [getdesign CLI](https://www.pkgstats.com/pkg:getdesign), [DESIGN.md guide](https://betterstack.com/community/guides/ai/design-md-ai/).
