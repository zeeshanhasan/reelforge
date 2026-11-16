# ReelForge

ReelForge makes ready-to-post vertical reels for [Prept](https://prept.fyi) (Instagram
Reels, TikTok, YouTube Shorts) on your own Mac. Voice, captions and video are all made
locally, with free tools.

## Where it stands (16 Nov 2026)

| Part | State |
| --- | --- |
| **Prototype reel** | **Works.** One command makes a 40-second branded reel. See below. |
| The app (queue, review, daily batch of 4) | Not built yet. Planned in `specs/` |
| AI human presenter | Tested and ruled out for now: it looked too AI-generated (`docs/spike.md`) |

## Make the prototype reel

The prototype turns one script, "Which answer would you give?", into a finished reel in
Prept's style: voiceover, words that light up as they're spoken, 1080x1920, 30 fps, MP4.

### What you need

- A Mac with Apple Silicon (M1 or later). Tested on a MacBook Air M5 with 16 GB RAM.
- [Homebrew](https://brew.sh).
- About 3 GB of free disk space, and an internet connection for the first setup.

### Steps

Open Terminal and run:

```bash
git clone https://github.com/zeeshanhasan/reelforge.git
```

```bash
cd reelforge/prototype
```

```bash
./setup.sh
```

Setup prints PASS or FAIL for each step. It installs ffmpeg and uv if they're missing, a
Python 3.11 environment, the packages, a headless browser, and the voice and timing
models. It takes about 5 minutes the first time and is safe to run again.

Then make the reel:

```bash
./make_reel.sh
```

That takes about 2 to 3 minutes. The reel is saved to `prototype/out/reel.mp4`. AirDrop it
to your phone to watch it the way viewers will.

### What happens inside

1. **Voice:** Kokoro (a free voice model) reads each part of the script from `reel.json`.
2. **Word timings:** Whisper listens to the voiceover and records when each word is said.
3. **Render:** `scene.html` is drawn in a headless browser, frame by frame, with each
   on-screen word lighting up at the moment it's spoken. ffmpeg joins the frames and the
   voice into the MP4.

### Changing it

- **Voice or speed:** edit `voice` and `speed` in `prototype/reel.json`. Other US voices
  include `af_bella` and `am_michael`.
- **Words:** the spoken script lives in `reel.json`, and the on-screen text lives in
  `scene.html`. They have to match, because each on-screen word is linked to its spoken
  word. If you change one, change the other, then run `./make_reel.sh` again. The render
  step reports how many spoken words it found on screen.
- **Post captions:** ready-to-paste captions for Instagram, TikTok and YouTube are in
  `reel.json` under `post_text`.

This is a prototype for one reel. Making any topic into a reel automatically is what the
app will do (spec-03 and spec-04).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `setup.sh` says FAIL | Read the reason on that line. Details are in `/tmp/reelforge-setup.log`. Fix it, then run `./setup.sh` again |
| "Run ./setup.sh first" | Setup hasn't finished. Run `./setup.sh` |
| Download stops partway | Run the same command again. Downloads resume |
| Render says fewer than 106 spoken words were found on screen | The text in `scene.html` no longer matches `reel.json`. Make them say the same words |
| The first run is slow | Models download and warm up once. Later runs are faster |

## What's next

1. **spec-02:** the app itself: `./setup.sh` and `./run.sh` at the repo root, opening at
   `http://localhost:8000`.
2. **spec-03:** topics and the script engine. Still to decide: whether Claude or a local
   model writes the scripts.
3. **spec-04:** reel templates (A-or-B question, checklist, before/after, mistakes list),
   so any topic renders in Prept's style.
4. **spec-07:** review queue and "Generate today's batch".

Progress is tracked in [`specs/TRACKER.md`](specs/TRACKER.md).

## For contributors

| File | What it holds |
| --- | --- |
| `CLAUDE.md` | Instructions for Claude Code, including the workflow |
| `ARCHITECTURE.md` | How ReelForge is put together |
| `DECISIONS.md` | Every decision and why (D-001 onwards) |
| `DESIGN.md` | The app's design system (placeholder until spec-02) |
| `specs/` | One spec per feature, plus the tracker |
| `docs/spike.md` | The AI-human test: timings, quality, verdict |
| `docs/licences.md` | Licence of every model and tool, and what's allowed commercially |
| `content/brand/fonts/` | Prept's fonts (Fraunces, IBM Plex Sans), with their open licences |
| `prototype/` | The working reel prototype |
| `spike/` | Notes and the test script from the AI-human spike |

Work happens one spec at a time on its own branch. Each pull request needs approval from
Zeeshan or Sarosh before it merges into `master`.
