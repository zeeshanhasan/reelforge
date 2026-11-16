# spec-01 · AI-human spike

**Status:** Ready
**Milestone:** M0
**Covers:** spec-00 section 4

## Title

As the Prept team,
I should know whether a free, local AI human can be made on a MacBook Air,
so that we commit to the main reel format only if it actually works.

## Why we're building this

The AI human is the only part of ReelForge with no proven free path on a MacBook. Nothing
else is built until this returns a go or no-go. Time-box: one day.

## Brief

Produce one 30-second vertical clip of a photoreal AI-generated person speaking a Prept
script, made entirely on Zeeshan's Mac. Record timings, memory, throttling and quality, and
write a go or no-go in `docs/spike.md`.

## Acceptance criteria

1. **Machine recorded**
   GIVEN Zeeshan's Mac
   WHEN the spike starts
   THEN `docs/spike.md` records the chip, RAM and macOS version.

2. **Character created**
   GIVEN the AI human's look has been decided (gender, age range, accent, name)
   WHEN a free image generator makes one photoreal face of a person who does not exist
   THEN it is saved as `assets/character/face.png` and the generator and its terms are noted.

3. **Base video**
   GIVEN `face.png`
   WHEN an open-source portrait animator (LivePortrait first) runs on the Mac
   THEN a 10 to 20 second idle clip (blinking, small head movement) exists in
   `assets/character/`, or `docs/spike.md` records why it could not be made.

4. **Narration**
   GIVEN a 30-second Prept script
   WHEN mlx-audio with Kokoro voices it
   THEN a WAV file exists and its render time is recorded.

5. **Lip-sync attempts**
   GIVEN the base video and narration
   WHEN the MuseTalk Mac port runs (and the LatentSync MLX port if quality is poor)
   THEN each attempt records render time, peak memory, whether the Mac throttled, and an
   honest note on mouth, teeth and identity drift.

6. **Go decision**
   GIVEN the attempts
   WHEN a 30-second clip renders in under 15 minutes, four clips render back to back without
   a crash, and two people who did not build it say the face is acceptable for social media
   THEN `docs/spike.md` says **Go**, names the winning method, and links a sample clip.

7. **No-go decision**
   GIVEN any go condition fails
   WHEN the spike ends
   THEN `docs/spike.md` says **No-go**, says which condition failed, and recommends the
   fallback in order: hook-only face; real-person footage lip-synced; paid avatar service.

8. **Licences**
   GIVEN every model used
   WHEN the spike ends
   THEN each model's code and weight licence, and whether it allows commercial use, is
   listed in `docs/licences.md`.

## Engineering notes

- Everything here is **untested** on these Macs. That is the point of the spike.
- Machine: 16 GB RAM (D-012). Close other model processes during timing runs.
- Spike code is throwaway. Keep it in `spike/`, not in `app/`.
- The sample clip is large: keep it out of git, or use Git LFS only if agreed.
- Candidates: fast-lipsync / MuseTalk port, LatentSync MLX, LivePortrait.

## QA notes

- Two people who did not build it watch the clip on a phone and give a yes or no.
- Re-run the four-clip back-to-back test with the lid open, on battery and on power.

## Wireframe

None.

## Decisions made

<Filled in at release.>
