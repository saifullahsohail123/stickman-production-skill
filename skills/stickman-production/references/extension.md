# Stable extension points

- **Speech adapter:** exact text/profile/language → original WAV + request/job
  provenance. Do not hide provider failures behind an unapproved model change.
- **Timing:** measured utterances + intentional gaps → performance clock;
  invertible anchors → action clock. No implicit speed-up to meet a target slot.
- **Rig/renderer:** named native groups + pivots + expressions + articulation +
  prop constraints → rendered frames and silent shots. Keep document IDs scoped.
- **Editor:** integer picture cuts + audio layers + captions/camera keys → native
  Concat project and final export. Reexport idempotently without duplicating clips.
- **QA:** decoded measurements + inspected artifacts + listening notes → a report
  that states its limits. Store language-aware immutable deliveries separately.

Prefer additive modules and data parameters over copying a whole episode script.
Keep the short SKILL.md focused on routing and invariants; put language/backend
specific procedures here or in linked references. Convert a useful lesson from a
production into a small reproducible regression case before broadening a rule.

Schema version 1 is intentionally compact. The stdlib validator in `core.py` is
the canonical executable validation for this release:

- `identity`: positive episode/version, lowercase slug and language.
- `format`: width, height, integer fps and duration_frames.
- `cast`: stable role IDs/designs, offscreen status and local voice key.
- `lines`: unique ID, known speaker, exact text, optional seed/gap_after.
- `shots`: consecutive integer bounds, relative media file, optional camera scale.
- `audio`: relative media file, start, volume and role/name.
- `captions`: start/end/text; style and vertical offset are independent of camera.

The agent can carry richer project-specific acting/story data alongside this
manifest. A schema change is only necessary when the shared CLI consumes it.
