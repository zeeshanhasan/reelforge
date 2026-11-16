# spec-03 · Topics and script engine

**Status:** Draft
**Milestone:** M2
**Covers:** spec-00 sections 5.1 and 5.2

## Title

As a household member,
I should be able to manage topics and turn one into a reviewed script and post text,
so that every reel starts from a script we are happy with.

## Why we're building this

The script is the cheapest place to get a reel right. Hooks and post text decide whether
reels get watched, and they must follow Prept's brand brief.

## Brief

Users add, edit and retire topics in the app, written back to `content/topics.yaml`. A topic
plus `content/brand.md` produces a validated JSON script and post text per platform, which a
user can edit, and can ask for 3 alternative hooks.

## Acceptance criteria

1. **Add topic**
   GIVEN the topics screen
   WHEN a user adds a topic with title, angle and format
   THEN it is saved with this household as owner and status active, and written to `topics.yaml`.

2. **Edit and retire**
   GIVEN an existing topic
   WHEN a user edits or retires it
   THEN the change is written back to `topics.yaml` and the list updates.

3. **Ownership**
   GIVEN topics owned by the other household
   WHEN topics are listed or picked
   THEN they are never offered here.

4. **No repeats**
   GIVEN a topic with an approved reel on this Mac
   WHEN topics are offered for generation
   THEN that topic is not offered.

5. **Generate script**
   GIVEN a topic and the brand brief
   WHEN a user generates a script
   THEN it has a hook under 3 seconds spoken, 3 to 5 beats, a call to action, on-screen text
   per beat, 20 to 45 seconds spoken in total, and post text: Instagram caption with
   hashtags, TikTok caption, YouTube Shorts title and description (LinkedIn and X optional).

6. **Loading**
   GIVEN a script is generating
   WHEN the user waits
   THEN a loading state shows progress, and the page stays usable.

7. **Invalid output**
   GIVEN the model returns invalid or over-length output
   WHEN validation fails
   THEN it retries up to 3 times, then shows failed with the reason and a retry button.

8. **Edit script**
   GIVEN a generated script
   WHEN a user edits any field and saves
   THEN a new script version is stored with `edited_by_user` set, and validation still applies.

9. **Alternative hooks**
   GIVEN a script
   WHEN a user asks for alternative hooks
   THEN 3 hooks are offered and the chosen one replaces the hook in a new version.

10. **Ollama missing**
    GIVEN Ollama is not running or the model is not pulled
    WHEN a script is requested
    THEN an error state says exactly what to start or install.

## Engineering notes

- Free local model via Ollama by default (D-011); hosted adapter built but off.
- **Untested:** which local model writes good enough hooks in 16 GB (D-012). Compare 2 or 3
  candidates on 10 topics and record results before choosing.
- Seed `content/brand.md` (what Prept is, audience, tone, banned claims) with Zeeshan.
- Spoken length estimated from word count until real audio exists (spec-04).

## QA notes

- Unit tests for the script validator: every field, length limits, retry cap.
- Edit `topics.yaml` by hand while the app runs; the app reflects it on reload.

## Wireframe

None.

## Decisions made

<Filled in at release.>
