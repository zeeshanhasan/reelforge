# How we work

Copied from `spec-00-master.md`, sections 10.2 and 10.3.

## Specs and the tracker

- Every feature gets its own file: `specs/spec-NN-short-name.md`. Numbers start at 01, go up
  by one, and are never reused, even if a spec is dropped.
- Before creating a spec, read `specs/TRACKER.md` and take the highest number plus one.
- Each spec follows `_template.md`: **Title** (As a / I should / so that), **Why we're
  building this**, **Brief** (2 to 3 sentences), **Acceptance criteria** (GIVEN / WHEN / THEN,
  covering happy and unhappy paths and every screen state), **Engineering notes**,
  **QA notes**, **Wireframe** (link, if any), **Decisions made**, **Status**.
- Specs describe what, not how. Each should be small enough to release on its own.
- `TRACKER.md` is one table: spec number, title, status, branch, started, released, notes.
- Statuses: Draft, Ready, In progress, In review, Released, Dropped.

## Build and release flow

1. Pick the next spec marked Ready in the tracker. Work on one spec at a time.
2. Create the branch from `master`, named after the spec: `spec-01-ai-human-spike`.
3. Set the tracker row to In progress, with the branch name and start date.
4. Build. Prefix every commit with the spec number: `spec-01: add lip-sync benchmark script`.
5. When every acceptance criterion passes and `make check` is green, set the status to
   In review and open a pull request to `master`.
6. Zeeshan or Sarosh approves. Nothing merges without a human approval.
7. Release: merge to `master`, tag it `spec-01`, delete the branch.
8. Close the spec in the same merge: set its status to Released, fill in **Decisions made**,
   copy those decisions into `DECISIONS.md`, update the tracker row with the release date,
   and update `ARCHITECTURE.md` and `README.md` if anything changed.

## Rules

- No `develop` or staging branch for now. Everything lands in `master`.
- Changes to specs, the tracker or docs alone may be committed straight to `master`.
- A spec that turns out too big is split into new numbered specs, not stretched.
- If the builder has to deviate from a spec, it stops, records the reason in the spec, and
  asks before continuing.
