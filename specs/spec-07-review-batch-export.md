# spec-07 · Review queue, daily batch, export, second install

**Status:** Draft
**Milestone:** M6
**Covers:** spec-00 section 5.8

## Title

As a household member,
I should be able to generate today's 4 reels with one button, review them, and export the
approved ones with their captions,
so that posting each day takes minutes, without a terminal.

## Why we're building this

This turns the pipeline into a daily routine anyone in the house can run, and proves the
second household can install it alone.

## Brief

The home screen shows today's target and every reel's state. **Generate today's batch**
picks 4 topics across formats and renders them in sequence. Each reel can be approved,
regenerated or rejected; approved reels export with per-platform text and a posting record.

## Acceptance criteria

1. **Home screen**
   GIVEN any day
   WHEN the home screen loads
   THEN it shows today's target (4) and how many reels are queued, rendering, ready for
   review, approved and failed.

2. **Daily batch**
   GIVEN enough eligible topics
   WHEN a user clicks **Generate today's batch**
   THEN 4 topics across formats are picked and rendered in sequence, unattended.

3. **Too few topics**
   GIVEN fewer than 4 eligible topics
   WHEN the batch is requested
   THEN it renders what it can and says how many more topics are needed.

4. **Review**
   GIVEN a reel ready for review
   WHEN a user opens it
   THEN they see a preview player, the script, the post text, and approve, regenerate
   (whole reel, only voice, or only visuals) and reject-with-reason actions.

5. **Export**
   GIVEN a user approves a reel
   WHEN export runs
   THEN `exports/YYYY-MM-DD/<slug>/` holds the MP4 and one text file per platform, and a
   **Copy caption** button sits beside each platform.

6. **Posting record**
   GIVEN an exported reel
   WHEN a user marks it posted on a platform with the post link
   THEN the `posts` table records the platform, time and link.

7. **States**
   GIVEN any screen in this spec
   WHEN it is empty, loading, in error or successful
   THEN each state is shown with the standard components, and errors offer a retry.

8. **Second install**
   GIVEN Sarosh's Mac and only the README
   WHEN Sarosh installs and runs ReelForge with no help
   THEN the app runs, uses household B's topics, and renders a batch.

## Engineering notes

- Batch runs one render at a time. Record total time for 4 reels in `docs/benchmarks.md`;
  stop and report if over 2 hours.
- Mix formats in every batch and use hook-only mode often (spec-00 risk table).

## QA notes

- Start a batch, close the lid mid-render, reopen: it continues.
- Sarosh's install is the acceptance test for the README.

## Wireframe

None.

## Decisions made

<Filled in at release.>
