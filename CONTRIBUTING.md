# Improving the workflow

Keep the workflow useful to different stories, agents and machines. Do not add a
fixed cast, forced runtime, universal pause length or specific public model as a
default merely because it worked in one episode.

For each change:

1. Describe the observable failure and attach a small original or synthetic case.
2. Fix the relevant module: timing, illustration, speech adapter, edit or QA.
3. Add a behavioral regression test. Clock invertibility, preserved take bytes,
   language-aware revision identity and refusal to duplicate edits are useful
   invariants; tests of a heading's exact wording are not.
4. Run `python -m unittest discover -s tests -v` and the public release audit.
5. For app-affecting changes, run the original demo or a representative acting
   sample with installed applications. Inspect the final export and listen.
6. Update the change notes and tested-capability record with measured facts.

Versioning: patch for a compatible fix, minor for an additive adapter/capability,
major for breaking CLI/schema behavior. Update root VERSION and the skill's
metadata version together. A breaking manifest change needs a migration and a
test that an old manifest either migrates correctly or fails clearly.

Keep interfaces small. A future TTS provider should output original audio plus
request/provenance and measured duration; downstream timing must not depend on its
internal model. New rigs should expose document IDs, pivots, face/mouth selection
and prop ownership; the editor consumes rendered shots, not rig internals.

Do not submit personal configuration, copied reference films, voice profile IDs,
credentials, model weights, machine paths, generated frame sequences or editor
cache files. Public examples should be original and small. This repository can
link a separately licensed demo release instead of committing large episodes.

GitHub CI checks the portable core only. Do not describe that job as a successful
Voicebox generation or VectorCraft/Concat render. OpenCode discovery compatibility
does not establish equivalent creative results across all LLMs.
