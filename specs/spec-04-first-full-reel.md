# spec-04 · First full reel: voice, captions, assembler

**Status:** Draft
**Milestone:** M3
**Covers:** spec-00 sections 5.3, 5.4 and 5.7

## Title

As a household member,
I should be able to turn a topic into a finished faceless reel with one click,
so that we have a postable video before the harder formats exist.

## Why we're building this

This proves the whole pipeline end to end with the lowest-risk format: script, voice,
captions, assembly, and the job queue that survives a closed lid.

## Brief

One click on a topic runs script, voice, captions, visual (background footage) and assemble
as resumable jobs, and produces a captioned, voiced, branded 1080x1920 MP4 that plays
correctly on a phone.

## Acceptance criteria

1. **One click**
   GIVEN a faceless topic with a valid script
   WHEN a user clicks generate
   THEN a 1080x1920, 30 fps, H.264/AAC MP4 is produced and the reel moves to review.

2. **Voice per beat**
   GIVEN a script
   WHEN narration renders
   THEN one WAV per beat is made in the brand voice from `content/voice.yaml`, loudness
   normalised, and a single beat can be re-voiced without redoing the others.

3. **Captions**
   GIVEN the narration audio
   WHEN captions render
   THEN they are burned in 2 to 4 words at a time, the current word highlighted, in the
   brand caption style, inside the platform safe area.

4. **Layers**
   GIVEN a template for the faceless format
   WHEN the reel assembles
   THEN it has background footage, captions, logo, optional music ducked under the voice,
   and an end card with the call to action.

5. **Templates**
   GIVEN a change to a template file
   WHEN the next reel renders
   THEN the change applies with no code changes elsewhere.

6. **Progress**
   GIVEN a reel is rendering
   WHEN a user looks at it
   THEN it shows the current step, progress and a time estimate.

7. **Failure and retry**
   GIVEN a step fails
   WHEN the user retries
   THEN the job resumes from the failed step using assets already made, and the error shows
   the step and a clear reason.

8. **Closed lid**
   GIVEN a render is interrupted (lid closed, app quit)
   WHEN the app next launches
   THEN the job restarts cleanly from its last unfinished step.

9. **No assets**
   GIVEN `assets/` has no background footage or music
   WHEN a faceless reel is requested
   THEN an error state explains what to add and where. The tool ships with none.

## Engineering notes

- **Untested:** mlx-audio with Kokoro on these Macs; mlx-whisper word-level timestamps.
  Prove both before building on them.
- Captions as ASS subtitles via ffmpeg (D-005). One render at a time.
- Record real render times in `docs/benchmarks.md`. Stop and report if 4 reels would take
  more than 2 hours.

## QA notes

- `make check` adds a 10-second smoke render.
- Tests: job state changes, retry-from-failed-step, interrupted-job recovery.
- AirDrop the MP4 to a phone and play it in each platform's upload preview.

## Wireframe

None.

## Decisions made

<Filled in at release.>
