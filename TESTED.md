# Tested capabilities — 2026-10-25

This release was exercised on Windows with installed VectorCraft, Voicebox and
Concat. Machine-specific configuration and generated test artifacts are excluded
from the public package.

| Check | Observed result |
|---|---|
| Portable core suite | 12 tests passed: clocks, integer coverage, Unicode, audio trims, immutable language variants and stdio protocol behavior. |
| Skill validator | Required frontmatter/name/resources valid. |
| MCP discovery | Packaged client discovered 32 VectorCraft and 42 Concat tools. |
| VectorCraft integration | Original native wave/blink scene and posed snapshot; all 72 PNG frames rendered. |
| Concat integration | Packaged assembler imported the demo, original chimes and a caption; native app exported H.264/AAC. |
| Decoded media | Exactly 3s, 640×360, 24fps, 72 frames; audio peak about .0384. |
| Caption inspection | The caption was visible in the decoded middle frame. This was an actual image check, not inferred from project JSON. |
| Voicebox adapter | Generated the original English line “One small victory.” with an existing Kokoro preset profile; preserved request/history/WAV, then trimmed outer silence. |
| Measured voice clock | Trimmed take 1.09s; planned 1.59s including the .5s tail, speed 1. |

The small rendered demo has no narration; the Voicebox write test was separate.
The originating full workflow has produced longer English and Hindi cartoons,
but those private episode assets and settings are not bundled as public fixtures.

OpenCode's documented discovery format was checked; the OpenCode application was
not available for a live harness run. Other platforms and the GitHub CI matrix
are configured for further testing, not claimed as locally executed. No Urdu
engine, cloud service, word-karaoke runtime or general-purpose animation generator
was implemented by this release. Detailed acting/localization techniques are
guidance for the agent to author using the discovered app APIs.
