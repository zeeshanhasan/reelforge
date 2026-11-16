# ReelForge

A local Mac app that makes 4 ready-to-post vertical reels a day for Prept
(prept.fyi), for Instagram Reels, TikTok and YouTube Shorts. Everything runs on
your own Mac, free by default.

> **Status:** planning. Nothing is installable yet. The first build step is the
> AI-human spike (`specs/spec-01-ai-human-spike.md`). See `specs/TRACKER.md` for
> progress.

## Setup

Needs an Apple Silicon Mac with [Homebrew](https://brew.sh).

```bash
git clone https://github.com/zeeshanhasan/reelforge.git
cd reelforge
./setup.sh
./run.sh
```

`setup.sh` and `run.sh` arrive with spec-02. This section will then cover the
`.env` file (household, PIN, Prept demo account) and opening the app from
another device on the same wifi.

## Daily use

Arrives with spec-07: open the app, click **Generate today's batch**, review
each reel, approve, copy the captions and upload.

## Adding a topic

Arrives with spec-03.

## Adding a demo flow

Arrives with spec-05.

## Troubleshooting

Arrives with spec-02.

## For contributors

- `CLAUDE.md`: instructions for Claude Code, including the workflow.
- `ARCHITECTURE.md`: how the app is put together.
- `DECISIONS.md`: why things are the way they are.
- `DESIGN.md`: the app's design system.
- `specs/`: one spec per feature, plus the tracker.
