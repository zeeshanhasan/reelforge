# spec-01 · AI-human spike results

**Status:** Technical go. Waiting on the people test.
**Date:** 2026-11-16
**Verdict:** **Go on speed and stability.** Final go needs two people who did not build it
to say the face is acceptable (criterion 3).

## Summary

A photoreal AI woman speaking a 30-second Prept script was made entirely on a fanless
M5 MacBook Air with free tools. Once a base video exists, each 30-second talking clip takes
**40 to 55 seconds** to lip-sync. Four clips rendered back to back without a crash.

Winning method: **FLUX.1-schnell face → LivePortrait idle base video (once) → fast-lipsync
(MuseTalk 1.5 on Core ML) per reel.** LatentSync MLX was not tried, because quality was good
enough to put in front of people first.

Sample clip: `spike/output/sample_ai_human_30s.mp4` (720x1280, 25 fps, 3.9 MB). It is not
in git; AirDrop it to a phone to review.

## Machine

| | |
| --- | --- |
| Chip | Apple M5 (MacBook Air, fanless) |
| RAM | 16 GB |
| macOS | 26.5.2 (25F84) |
| Free disk at start | 186 GB |

## Go criteria

| Criterion | Result | Pass? |
| --- | --- | --- |
| 30 s clip renders in under 15 minutes | 4 min 34 s cold (first use of a base video), 42 to 55 s warm | **Yes** |
| Four clips back to back without a crash | 4 of 4 rendered, no thermal warning from macOS | **Yes** |
| Two people who did not build it say the face is acceptable | Not yet asked | **Pending** |

## Pipeline and timings

All runs one at a time, nothing else heavy running, lid open, on power.

| Step | Tool | Runs | Wall time | Peak memory |
| --- | --- | --- | --- | --- |
| Face image | FLUX.1-schnell via mflux, 4-bit, 4 steps, 720x1280 | Once per character | 52 to 78 s per image (plus a one-off 33 GB download, about 90 min) | 10.7 GB |
| Narration | mlx-audio 0.6.5, Kokoro-82M, voice `af_heart` | Per reel | 13 s for 30.3 s of audio | 4.5 GB |
| Base video | LivePortrait, head pose only, driven by example clip `d13` | Once per character | 8 min 4 s for 11.7 s of video | 8.1 GB |
| Loop base video | ffmpeg forward + reverse + forward, 35.2 s | Once per character | Seconds | — |
| Footage cache | fast-lipsync `prepare` (InsightFace boxes, VAE latents) | Once per base video | 178 s for 757 frames | 7.8 GB |
| Lip-sync | fast-lipsync, MuseTalk 1.5 UNet on Core ML, TAESD decoder, `generated` mouth | Per reel | 39 to 52 s for 30.2 s of video | 7.8 GB |

Per-reel AI-human cost, once the character exists: about **1 minute** (narration plus
lip-sync). That leaves plenty of room in the 2-hour budget for 4 reels.

## Lip-sync attempts

| Attempt | Method | Clip length | Render time | Peak memory | Throttled? | Mouth | Teeth | Identity drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | fast-lipsync, generated mouth, cold cache | 30.2 s | 247 s (178 s of it the one-off cache) | 7.8 GB | No warning | Follows speech, believable shapes; slightly soft compared with the rest of the face | Rarely visible: mouth opens only a little | None seen |
| 2 to 5 | Same, warm cache, back to back | 30.2 s each | 39, 42, 50, 52 s | 7.8 GB | No warning; about 30% slower by clip 4 as it warmed up | Same as 1 | Same as 1 | None seen |

Honest quality notes:

- **Good:** the identity holds across the whole clip. Head movement is subtle and natural.
  The mouth moves with the words.
- **Weak:** the mouth area is a little softer than the face around it. Mouth openings are
  small, so teeth rarely show. In some frames a faint blend edge is visible near the jaw
  line.
- **Missing:** no blinking. The base video used head pose only. A version with eye motion
  is the obvious next improvement.
- **Resolution:** the output is 720x1280, because the face and base video were made at that
  size. Reels need 1080x1920: either upscale or remake the base at full size (spec-06).

## What is still needed for a final go

1. Two people who did not build it watch `sample_ai_human_30s.mp4` on a phone and say yes
   or no.
2. If no: try blinking (LivePortrait eye animation), the LatentSync MLX port, then the
   fallbacks in spec-00 section 4.

## Licence blockers before real use

See `docs/licences.md`. Two items block commercial reels until replaced:

- **InsightFace `buffalo_l`** (face detection in LivePortrait and fast-lipsync) is
  non-commercial research only.
- **LivePortrait example driving clip `d13`** is a real person's footage with no stated
  licence. Replace it with our own recorded idle-motion clip.

## Setup notes for spec-02

- Kokoro also needs `misaki[en]` and the spaCy model `en_core_web_sm`, which mlx-audio does
  not install. Without the spaCy model, mlx-audio tries `uv pip install` at runtime, which
  fails outside an activated venv.
- FLUX.1-schnell's official weights are gated: a Hugging Face account, accepted terms, and
  a token that can read gated repos.
- LivePortrait's Mac requirements need `uv --index-strategy unsafe-best-match`, plus
  `requests`, which is missing from its list. Its `grid_sampler_3d` op falls back to the CPU
  on MPS, which is why it is slow.
- fast-lipsync: its `setup.sh` is not re-runnable with current uv (use `UV_VENV_CLEAR=1`).
  `peft` must be pinned to `0.13.2`. Large downloads dropped once while another big download
  ran; retrying resumed.
- The Homebrew ffmpeg has no `drawtext` filter (no freetype). Caption burn-in uses ASS
  subtitles, so check that `libass` is present in spec-04.
- Disk used by spike models: about 33 GB (FLUX) plus 4 GB (lip-sync) plus 0.6 GB
  (LivePortrait).

## How to reproduce

Spike code and environments live in `spike/` (envs and vendor repos are git-ignored).

```bash
# narration
spike/envs/voice/bin/python -m mlx_audio.tts.generate --model mlx-community/Kokoro-82M-bf16 \
  --voice af_heart --lang_code a --text "$(cat spike/script_30s.txt)" \
  --output_path spike/output --file_prefix narration --join_audio
# lip-sync
spike/vendor/fast-lipsync/lipsync.sh assets/character/base_idle.mp4 spike/output/narration.wav out.mp4
```
