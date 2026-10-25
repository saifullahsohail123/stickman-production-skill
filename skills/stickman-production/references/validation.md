# Delivery and evidence

The bundled `verify` checks the decoded frame count, resolution, frame rate,
duration and presence of expected audio. It saves first/middle/last QC images.
It explicitly leaves caption visibility, lip sync and subjective mix review for
the agent/user; it does not certify them from project JSON.

For a full episode, inspect additional decoded frames at caption cue centers,
contact effects, mouth transitions, camera extremes and first/last shots. Check
moving playback as well as stills. An offscreen narrator can legitimately have no
visible lips; a direct speaker should be the person actually moving their mouth.

When a clean dialogue reference exists, cross-correlate multiple early/late
windows against the decoded mix to detect offset/drift. Report the analysis sample
rate and measured precision. Also inspect rendered articulation; a zero mux offset
is not a phoneme alignment result. Listen to the final mix for masked words,
clipping, awkward overlaps, music tone and cartoon contacts. Distinguish machine
checks from listening and user approval in the report.

`verify --deliver` archives by (number, language, revision), verifies content
hashes and refuses a changed existing filename. A hash-checked review copy is not
automatically user-approved. No upload/publishing step is bundled.

Before a skill release, run the portable unit tests and source release audit.
An app integration test should use a fresh episode workspace and original small
assets. Preserve the prior release and record supported platforms/tools actually
tested. Do not infer OpenCode live execution from a frontmatter validator, or
narrated production quality from the silent wave/chime demo.
