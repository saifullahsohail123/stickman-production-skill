# Production decisions

## Brief and actual speech

Identify the audience, delivery format, duration preference, language, cast and
requested tools from the user's brief. Make ordinary creative decisions without
an unnecessary intake questionnaire. Keep one canonical design/voice description
per recurring role and name which lines are narration versus direct dialogue.

Write the story as actions: anticipation, contact, reaction and consequence. A
visual hook should actually be visible in the decoded first second, rather than
only exist in the narration. Background changes establish where the story is;
an insert or reaction shot must advance the same action rather than merely zoom.

Generate short voice takes before final timing. Save original speed, exact text,
profile/preset, engine, language, seed, request and job response. The helper's
`generate` creates a separate outer-silence edit without modifying original PCM.
`clock` measures those edits and deliberate gaps; it does not choose the cuts.

Do not force a natural take into an arbitrary scene slot. Rewrite/regenerate a
bad performance or extend/reblock the shot. Localization can legitimately change
runtime while preserving the story and reaction gaps.

## Editable illustration and motion

VectorCraft is used as an illustration/pose renderer here, not as an assumed
native animation timeline. Create scenes with named groups and a saved manifest
of document IDs, parentage, pivots, expressions and mouth groups. Read actual tool
schemas; draw returned IDs, not numbers copied from a different document.

For each frame reopen the base scene, sample the rig at the chosen action time,
sample articulation at the output speech time, set exactly one mouth and export.
Encoding the resulting PNGs with PyAV is packaging; it is not a replacement for
VectorCraft illustration or Concat editing. Cache keys must include artwork,
timing, methods and source inputs before any renderer resume is trusted.

The bundled demo shows the basic path: native groups/pivot rotation, independent
blink selection, per-frame reopening/export, silent encoding, editor assembly.
Its fixed three-second wave is not a reusable walking or lip-sync engine.

## Sound and editing

Keep dry narration, music, ambience and foley separate. Let sound contacts follow
physical events, and use anticipatory sound when a J-cut helps. Avoid blanket
dialogue overlap: it can mask words and remove the pause a joke needs. A short
intentional dropout is different from an unplanned empty transition.

Duck busy foley as well as music during speech. Leave headroom; do not normalize
each effect to maximum just to make it feel cinematic. Exaggeration should come
from the appropriate attack, body, pitch and decay, not uncontrolled clipping.

In Concat import each silent shot at its integer-frame start. Trim probe tails
when necessary. Later tracks paint above earlier ones; put captions above opaque
picture, independent of camera keys. Reserve overscan for offset shakes and slow
pushes. Save the project before exporting; do not open it concurrently in GUI
and headless clients. Reuse the existing edit for reexports instead of duplicating
all clips. Final files get their language/revision identity only after review.
