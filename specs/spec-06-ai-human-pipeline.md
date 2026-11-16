# spec-06 · AI human in the pipeline

**Status:** Draft
**Milestone:** M5
**Covers:** spec-00 section 5.5

## Title

As a household member,
I should be able to render reels fronted by Prept's AI human,
so that the brand has one consistent face across both households.

## Why we're building this

The talking head is the main format. spec-01 decides how it is made; this spec puts that
method into the pipeline as an adapter.

## Brief

The spike's winning method runs behind the AI-human adapter. Given narration audio, it
produces a lip-synced vertical clip of the one fixed character in `assets/character/`, in
full talking-head or hook-only mode.

## Acceptance criteria

1. **Full mode**
   GIVEN an ai_human topic and narration audio
   WHEN the reel renders in full mode
   THEN the character speaks the whole narration, lip-synced, at 1080x1920.

2. **Hook-only mode**
   GIVEN the same topic
   WHEN the reel renders in hook-only mode
   THEN the character speaks the first 3 seconds, then the reel cuts to demo or faceless visuals.

3. **One face**
   GIVEN both households
   WHEN either renders an AI-human reel
   THEN both use the same character from `assets/character/`.

4. **Re-voice without re-lipsync where possible**
   GIVEN a reel where only visuals are regenerated
   WHEN it renders
   THEN existing narration is reused.

5. **Memory**
   GIVEN 16 GB RAM
   WHEN the AI human renders
   THEN no other model is loaded at the same time, and the render does not crash.

6. **Failure**
   GIVEN the lip-sync step fails
   WHEN the user retries
   THEN it resumes from the visual step, with the reason shown.

7. **Licences**
   GIVEN every model and weight used
   WHEN this spec is reviewed
   THEN `docs/licences.md` confirms commercial use is allowed for each.

## Engineering notes

- Implementation depends on spec-01's result (D-009). If the spike was no-go, use its
  recommended fallback.
- Check each platform's current AI-content labelling rule before the first post and note it
  in the README.
- Record render times in `docs/benchmarks.md`.

## QA notes

- Render one reel in each mode and watch on a phone.
- Render four AI-human reels back to back on the Air without a crash.

## Wireframe

None.

## Decisions made

<Filled in at release.>
