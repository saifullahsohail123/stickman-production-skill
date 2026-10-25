# Stickman Production Skill

An agent-independent production workflow for narrated vector cartoons using
**VectorCraft + Voicebox + Concat**. Version **0.1.1**; original package code and
documentation are MIT licensed. It contains portable instructions, configurable
tool adapters, timing/revision utilities and a small original integration demo.

The LLM still authors the story, native artwork and acting. This package does not
turn every topic into a polished film with one command. It deliberately separates
creative direction from repeatable timing, tool calls and delivery checks.

## Repository and quick start

Repository: https://github.com/saifullahsohail123/stickman-production-skill

```sh
git clone https://github.com/saifullahsohail123/stickman-production-skill.git
cd stickman-production-skill
python -m venv .venv
```

Activate the virtual environment (`.venv\Scripts\Activate.ps1` in PowerShell,
or `source .venv/bin/activate` on macOS/Linux), then run:

```sh
python -m pip install -r requirements-media.txt
python -m unittest discover -s tests -v
```

Install [VectorCraft](https://github.com/storytold/vectorcraft),
[Voicebox](https://github.com/jamiepine/voicebox) and
[Concat](https://github.com/jub0t/concat) separately. Follow their upstream setup
instructions and select/download a TTS model inside Voicebox. This repository
provides adapters; it does not bundle the applications or model weights.

## Use with OpenCode or another agent

Copy `skills/stickman-production/` into the destination project's
`.opencode/skills/stickman-production/` or `.agents/skills/stickman-production/`.
OpenCode documents both discovery locations in its
[official Agent Skills guide](https://opencode.ai/docs/skills/).

For an agent without skill discovery, ask it to read that folder's `SKILL.md` and
follow its linked references. The scripts are ordinary Python CLIs; they do not
depend on a particular model's proprietary tool names. The harness must provide
file/shell access and the three applications. OpenCode itself was not installed
in the packaging environment, so its live harness integration is not claimed.

For a global Codex installation, copy the same skill folder to
`~/.codex/skills/stickman-production/`. The optional `agents/openai.yaml` supplies
UI metadata; other agents can ignore it. No global agent settings are changed.

Example request:

> Use the stickman-production skill to make a warm 45-second original cartoon
> about losing a recipe. Use two characters and measured English voice takes.
> Keep the speaking character visible and preserve editable native sources.

## Setup and original smoke demo

Python 3.11+ is sufficient for planning, manifests, timing, API/MCP clients and
unit tests. Media commands additionally need `av`, `numpy` and `Pillow`; install
`requirements-media.txt` in a project virtual environment. Install the three
applications separately. Their binaries/models are not distributed here.

From this repository root:

```sh
python skills/stickman-production/scripts/production.py init --workspace work/demo
```

Edit `work/demo/config.local.json`: set the executable argument lists for your
installed VectorCraft and Concat. Commands are argument arrays, not shell strings.
`{workspace}` is substituted without shell evaluation. Use a running local
Voicebox URL and select your own profile IDs only when generating dialogue.
The default configuration uses binary names on PATH and no embedded personal IDs.

```sh
python skills/stickman-production/scripts/production.py doctor --config work/demo/config.local.json
python skills/stickman-production/scripts/production.py demo --config work/demo/config.local.json
python skills/stickman-production/scripts/production.py assemble --config work/demo/config.local.json
python skills/stickman-production/scripts/production.py verify --config work/demo/config.local.json
```

The three-second demo authors a new native vector character, renders a wave/blink
sequence, encodes silent shots, synthesizes original chimes, and exports through
Concat with a caption. It has **no generated narration**. Listen/watch the result
and inspect the decoded QC frames. After that review, `verify --deliver` archives a
hash-checked copy. Existing Concat projects require `assemble --reexport`.

For dialogue, add `{id, speaker, text, seed, gap_after}` entries to the episode's
`lines` array, configure that cast role's voice, run `generate` and then `clock`.
Generation saves original requests/history/WAVs and creates byte-preserving
outer-silence trims. `clock.json` gives actual take timing; the agent uses it to
author the real shots/animation and mix. It does not invent scene timing for you.

## Reuse without copying an episode

- The skill contains the production decisions and known failure modes.
- Episode manifests hold cast, format, cuts, audio layers and captions.
- Local config holds executable locations, service URLs and voice profile IDs.
- Native scenes, audio, renders and editor projects stay in the episode workspace.

The included illustration is an original generic demo. No uploaded reference
video/audio, private character designs, cloned profiles, models or application
binaries are bundled. Source and model licences are distinct; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Improve and release

This standalone repository is named `stickman-production-skill`.
Keep this lightweight skill/runtime separate from large episode assets. Add
improvements to the smallest shared module, add a regression case from the failure,
then update `CHANGELOG.md` and release a semantic version. See
[CONTRIBUTING.md](CONTRIBUTING.md). A GitHub Actions workflow runs the portable
unit tests; application integration still needs the external apps.

```sh
python -m unittest discover -s tests -v
python scripts/package_release.py --check
python scripts/package_release.py
```

The release builder audits source files and creates a deterministic source ZIP.
It excludes local configuration, generated media, caches and workspaces.
Only source and public examples belong in Git. Keep API keys, local profile IDs,
cloned voice samples, models and generated episode workspaces out of commits.
Use the Issues page for reproducible failures and pull requests for improvements.

## Practical limits

The original production pipeline and this package's smoke integration were tested
on Windows. Python core tests are platform-neutral; other application builds need
their own verification. Numeric mux alignment is not proof of lip-sync quality.
The generic verifier checks dimensions, frames, duration and audio presence, and
exports QC images; caption visibility, acting and the final mix require review.
Pacing and voice quality remain creative decisions. No viral outcome is promised.

## Repository map

| Location | Purpose |
|---|---|
| `skills/stickman-production/SKILL.md` | Agent entrypoint and workflow routing |
| `skills/stickman-production/references/` | Directing, acting, localization, tools and QA |
| `skills/stickman-production/scripts/` | Configurable tool adapters and production helpers |
| `skills/stickman-production/assets/` | Public configuration and episode examples |
| `tests/` | Portable behavior regression tests |
| `TESTED.md` | What has actually been exercised and remaining limits |
| `CONTRIBUTING.md` | How to improve the workflow and version releases |

The originating film project remains separate. Future production lessons should
be generalized here with a regression example; do not copy a private production
workspace wholesale into the skill.
