# spec-05 · Product demo capture

**Status:** Draft
**Milestone:** M4
**Covers:** spec-00 section 5.6

## Title

As a household member,
I should be able to turn a demo flow file into a Prept product demo reel,
so that we can show the product working without filming a phone by hand.

## Why we're building this

Demo reels show what Prept actually does. Scripted capture keeps them repeatable and quick
to redo when Prept's interface changes.

## Brief

A flow file in `flows/` drives a phone-sized browser through Prept with a dedicated demo
account, saving a video and a timestamped tap log. The assembler zooms toward each tap,
shows a tap marker and speeds up waits. A user can upload their own screen recording instead.

## Acceptance criteria

1. **Run a flow**
   GIVEN a flow file and demo account credentials in `.env`
   WHEN a demo reel is generated
   THEN the recorder logs in, runs every step in a phone-sized viewport, and saves a video
   plus a timestamped log of every tap position.

2. **Zoom and markers**
   GIVEN the video and tap log
   WHEN the reel assembles
   THEN it zooms toward each tap, shows a tap marker, and speeds up waits.

3. **Narration per step**
   GIVEN a flow with narration lines
   WHEN the reel renders
   THEN narration and captions line up with their steps.

4. **Broken step**
   GIVEN an element is missing or a step times out
   WHEN the flow runs
   THEN the job fails naming the step that broke, with a saved screenshot shown in the app.

5. **Missing credentials**
   GIVEN `.env` has no demo account
   WHEN a demo reel is requested
   THEN an error state explains what to add. Credentials are never committed.

6. **Manual fallback**
   GIVEN a user's own phone screen recording
   WHEN they upload it for a demo topic
   THEN it is used as the visual source and the rest of the reel renders as normal.

## Engineering notes

- **Open:** are all Prept features worth showing available on the web, or some app-only?
  App-only features use the manual fallback.
- **Open:** who creates the Prept demo account and its fake data.
- **Untested:** auto-zoom from the tap log. Prove it on one flow first.
- Playwright (Python). Document the flow file format in the README.

## QA notes

- Change a selector in a flow so it breaks; the error names the step and shows a screenshot.
- Watch a finished demo reel on a phone: zooms land on the tapped element.

## Wireframe

None.

## Decisions made

<Filled in at release.>
