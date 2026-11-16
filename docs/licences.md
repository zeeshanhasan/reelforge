# Licences

Every model, weight file and tool ReelForge uses, and whether commercial use is allowed.
Prept is a commercial product, so anything marked **No** must be replaced before real
reels are posted. Checked 2026-11-16 from each project's licence file or Hugging Face model
card. Re-check when a version changes.

| Component | Used for | Code licence | Weights or data licence | Commercial use |
| --- | --- | --- | --- | --- |
| FLUX.1-schnell (Black Forest Labs) | Character face image | — | Apache-2.0 (gated download) | Yes |
| mflux | Running FLUX on Apple Silicon | MIT | — | Yes |
| Kokoro-82M | Voice | — | Apache-2.0 | Yes |
| mlx-audio | Running Kokoro | MIT | — | Yes |
| misaki, spaCy `en_core_web_sm` | Kokoro text processing | MIT | MIT | Yes |
| LivePortrait (KlingTeam) | Idle base video | MIT | MIT | Yes |
| LivePortrait example driving clip `d13` | Head motion for the base video | — | **None stated**; footage of a real person | **No, treat as unlicensed.** Replace with our own recording |
| MuseTalk 1.5 (TMElyralab) | Lip-sync model | MIT | "Available for any purpose, even commercially" | Yes |
| fast-lipsync | MuseTalk on Core ML | MIT | — | Yes |
| sd-vae-ft-mse (Stability AI) | MuseTalk VAE encoder | — | MIT | Yes |
| Whisper tiny (OpenAI) | MuseTalk audio features | — | Apache-2.0 | Yes |
| TAESD | Fast latent decoder | — | MIT | Yes |
| MediaPipe hand landmarker | fast-lipsync real-mouth mode only | Apache-2.0 | Apache-2.0 | Yes |
| **InsightFace `buffalo_l`** (`det_10g`, `2d106det`) | Face detection and landmarks in LivePortrait and fast-lipsync | MIT (code) | **Non-commercial research only** | **No.** Replace or license before spec-06 |
| ffmpeg (Homebrew build) | Assembly | LGPL/GPL | — | Yes, when used as a separate program |

## Actions before spec-06 ships

1. **Replace InsightFace `buffalo_l`** with a face detector that allows commercial use, for
   example MediaPipe Face Detection or Face Landmarker (Apache-2.0), or buy an InsightFace
   commercial licence.
2. **Replace driving clip `d13`** with 15 to 20 seconds of our own idle footage (anyone
   sitting still, blinking, small head movements), recorded with their consent.
3. Check each platform's current rule on labelling realistic AI-generated people before the
   first post (spec-00 risk table).
