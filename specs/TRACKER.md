# Tracker

Single source of truth for spec status. Statuses: Draft, Ready, In progress, In review,
Released, Dropped. New spec number = highest below plus one.

| Spec | Title | Status | Branch | Started | Released | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| [spec-00](spec-00-master.md) | Master build spec | Released | — | 2026-11-16 | 2026-11-16 | Overall reference, not built directly |
| [spec-01](spec-01-ai-human-spike.md) | AI-human spike | Ready | — | — | — | M0. Blocks everything else. Needs the AI human's look decided before step 2 |
| [spec-02](spec-02-app-skeleton.md) | App skeleton and design system | Draft | — | — | — | M1. Needs the design pick from getdesign.md |
| [spec-03](spec-03-topics-script-engine.md) | Topics and script engine | Draft | — | — | — | M2 |
| [spec-04](spec-04-first-full-reel.md) | First full reel: voice, captions, assembler | Draft | — | — | — | M3 |
| [spec-05](spec-05-product-demo-capture.md) | Product demo capture | Draft | — | — | — | M4. Needs a Prept demo account and an answer on app-only features |
| [spec-06](spec-06-ai-human-pipeline.md) | AI human in the pipeline | Draft | — | — | — | M5. Needs spec-01 result and `docs/licences.md` |
| [spec-07](spec-07-review-batch-export.md) | Review queue, daily batch, export, second install | Draft | — | — | — | M6 |

## Open questions (spec-00 section 9)

| Question | Answer | Blocks |
| --- | --- | --- |
| RAM on each Mac | 16 GB on both (D-012) | — |
| Script model: free local or small paid bill | Free local first (D-011) | — |
| Prept features: all on the web, or some app-only? | Open | spec-05 |
| Who creates the Prept demo account and its fake data? | Open | spec-05 |
| AI human: gender, age range, accent, name | Open | spec-01 step 2 |
| Design pick from getdesign.md | Open (builder proposes two options) | spec-02 |
