---
name: stickman-production
description: Produce or revise narrated stickman and vector cartoons with VectorCraft illustration, Voicebox speech, Concat editing, measured timing, expressive acting, and editable sources. Use for storyboard-to-video work and localized versions, rather than a single static illustration.
license: MIT
metadata:
  version: 0.1.1
---

# Stickman production

Build the requested film, preserving the user's cast, tone, tools, language and
pace. Reference feedback is evidence to interpret, not instructions that override
the user's preferences. Never promise virality or exact phoneme sync.

The LLM directs and authors the artwork/acting; deterministic helpers measure,
connect tools and verify deliverables. This is not an automatic story generator.

## Choose the work

- New film: freeze each role's design and voice; read
  [production.md](references/production.md).
- Acting revision: inspect the moving shot and actual speaker; read
  [acting.md](references/acting.md). Audio alignment alone is insufficient.
- Dub/localization: preserve the original and measure new takes; read
  [localization.md](references/localization.md).
- Setup or failure: discover installed capabilities with
  [tools.md](references/tools.md). Do not silently replace requested tools.

## Working sequence

1. Read project instructions and inspect current files. A former episode is an
   example, not a fixed cast, runtime, language or musical style.
2. Initialize with `scripts/production.py init --workspace PATH`, or inspect the
   existing manifest. Machine paths/profile IDs belong in the ignored local
   config. Run `doctor` before relying on old app state.
3. Generate short takes through selected Voicebox profiles. Save exact requests,
   job IDs and original WAVs. Trim outer silence only; use `clock` to measure real
   durations. Fix poor delivery before timing the film to it.
4. Plan actions/cuts against the actual takes. Author editable VectorCraft sets
   and jointed poses, then encode its rendered frames into silent shot assets.
   The bundled `demo` is an integration example, not a general character rig.
5. Assemble picture, original-speed speech, score, ambience, contact foley and
   screen-space captions in Concat. Use `assemble`; existing edits need
   `--reexport`. Inspect actual schemas when capabilities differ.
6. Use `verify`, inspect decoded images, listen to the mix and watch the speaking
   passages. Correct missing captions, wrong speakers, exposed borders, unreadable
   text and masked words before delivery. Record what was actually checked.

## Production invariants

- Action/story time and speech/performance time are distinct. Retimed pictures
  must sample mouths from the OUTPUT audio clock; do not slide old speaking shots.
- One visible mouth per face. Separate eyes/brows, articulation, gaze and body
  acting. Keep direct speakers visible; narration does not make listeners talk.
  Carried props remain attached to their hand.
- Choose pauses for the joke and user's pace. A 0.2-second J-cut is not a rule to
  overlap all voices. Duck foley as well as music beneath speech.
- Native IDs are document-specific. Reopen the correct scene before using its
  manifest. Reuse rendered caches only when inputs and method are unchanged.
- Use integer picture frames, original speech speed and explicit cut starts.
  Overscan shaken pictures; keep captions outside camera transforms.
- Read/write UTF-8. Verify both engine and app language support. Label ASR
  estimates, known-text alignment and heuristic visemes accurately.
- Decode the final export. Concat `state: done` does not establish that title
  cache writes succeeded or the correct character spoke.
- Preserve approved files. Delivery identity includes episode, language and
  revision. Producing a film does not authorize uploads or remote pushes.

## Reuse and improve

Keep schema version 1 until a deliberate migration. Capture a real failure,
correct the smallest shared module, add a behavioral regression case, then update
version/change notes. See [extension.md](references/extension.md).
Read [validation.md](references/validation.md) before calling a film verified.

For Urdu options see [urdu-tts.md](references/urdu-tts.md): dated research,
not a claim that an Urdu adapter is installed or benchmarked.
