# Architecture

How ReelForge is put together. Update this file whenever a spec changes the structure.
Source: `specs/spec-00-master.md`, section 3.

## Shape

One Python app with a browser front end, a SQLite file, and a single background worker that
renders one reel at a time. Python because every local AI model involved is Python-first.
One render at a time because the M5 Air has no fan.

```
browser (HTMX pages)  ──HTTP──▶  FastAPI app  ──▶  SQLite (topics, scripts, reels, jobs, ...)
                                     │
                                     └──▶  worker (one job at a time)
                                              ├─ script engine   (Ollama by default)
                                              ├─ voice engine    (mlx-audio + Kokoro)
                                              ├─ caption engine  (mlx-whisper word timings)
                                              ├─ visual source   (AI human | demo capture | footage)
                                              └─ assembler       (ffmpeg + ASS subtitles)
```

## How one reel is made

1. Pick a topic and a format.
2. **Script engine** writes the script as structured JSON (hook, 3 to 5 beats, CTA,
   on-screen text, post text per platform).
3. **Voice engine** turns the narration into WAV, one file per beat.
4. **Caption engine** gets word-level timings from that audio.
5. **Visual source** produces the picture: AI-human clip, recorded Prept demo, or background
   footage.
6. **Assembler** combines picture, audio, captions, logo and music into a 1080x1920,
   30 fps, H.264/AAC MP4.
7. The reel lands in the review queue. A person approves, regenerates or rejects it.
8. Approved reels export to `exports/YYYY-MM-DD/<slug>/` with one text file per platform.

Job steps: `script → voice → captions → visual → assemble`. Each step's output is saved as
an asset. A failed job records the step and error; a retry resumes from that step.

## Adapters

Every engine sits behind a small interface with one default implementation.

| Interface | Default | Alternatives (off by default) |
| --- | --- | --- |
| Script engine | Local model via Ollama | Hosted model with an API key |
| Voice engine | mlx-audio with Kokoro | — |
| Caption engine | mlx-whisper | — |
| AI human | Decided by the spike (spec-01) | LatentSync MLX, real-person footage, paid avatar service |
| Visual source | Per format: AI human, Playwright demo capture, background footage | Uploaded phone screen recording |

## Data

SQLite holds everything local to one Mac; media files live on disk and the database stores
their paths. Tables: `topics`, `scripts`, `reels`, `assets`, `jobs`, `posts`, `settings`.
See `specs/spec-00-master.md` section 6 for fields and statuses.

Reel statuses: draft, queued, rendering, review, approved, rejected, failed.

## Folder layout (planned)

Folders appear as specs build them. Bold entries are git-ignored.

```
reelforge/
├─ app/                 FastAPI app, pages, worker, engines (adapters)
├─ assets/              shared media the team has rights to use
│  └─ character/        the AI human's face and base video
├─ content/
│  ├─ topics.yaml       shared topic list, each topic owned by household A or B
│  ├─ brand.md          Prept brand brief for the script engine
│  ├─ voice.yaml        the brand voice
│  └─ brand/            Prept logo, colours, fonts, caption style for reels
├─ flows/               product demo flow files
├─ templates/           reel layout per format
├─ docs/                spike, benchmarks, licences
├─ specs/               numbered specs and the tracker
├─ tests/
├─ **data/**            SQLite file, generated audio and video
├─ **exports/**         approved reels and post text
└─ **.env**             household id, PIN, demo account, optional API keys
```

## Sharing between households

Each household runs its own install. Code and `content/` are shared through git; the
database and media are not. Each topic has an `owner` (A or B) and the app only picks
topics owned by its own household, set once in `.env`.
