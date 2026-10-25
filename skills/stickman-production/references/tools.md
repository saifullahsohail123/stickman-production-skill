# Runtime adapters

`production.py init` creates a local JSON config and a small episode manifest.
Executable commands are argument arrays; subprocesses never evaluate a shell
string. Resolve a chosen workspace relative to the local config. Media references
are workspace-relative; the helpers reject escapes, including resolved symlinks.

## VectorCraft

Tested tools include `run_command`, `draw_shape`, `draw_path`, `save_file`,
`open_file`, `command_batch` and `export`. A configured command commonly uses
`vectorcraft-cli mcp --headless` with explicit automation read/write roots.
`doctor` records the current tool list in local logs; discover command schemas
instead of assuming every release has identical APIs.

The demo uses `file.new`, returned shape/group IDs, `object.group`,
`object.setProps` and `object.transform`. Transforms are sampled from a reopened
base file, preventing accidental accumulation. Exported PNG frames are encoded
into silent MP4 by PyAV.

## Voicebox

The HTTP adapter uses `/health`, `/models/status`, `/profiles`, `/generate`,
`/history/{id}` and `/audio/{id}`. Choose an existing authorized profile in local
configuration. Original requests/history are saved, and changed take requests
cannot silently reuse an old WAV. Generation waits are bounded; a preserved job
ID lets the next run inspect/resume rather than submit a duplicate.

Use personality rewriting only if requested; the default keeps exact text. An
English-only model is not a fallback for Hindi/Urdu. Environmental effects in the
verified workflow were synthesized separately; do not attribute them to Voicebox
when its actual installed API only offers speech and voice effects.

The helpers do not install models or start services. An agent can start an
already-installed service within the user's authorized production scope. Normal
app database/cache writes may need the host's permission mechanism. Do not create
a second empty database to bypass a permission failure.

## Concat

Typical headless command: `concat --mcp headless`; `CONCAT_MCP_ROOTS` is set to the
episode workspace. Assembly uses the actual app engine, not a similarly named
ffmpeg concat operation. `export_wait` completes with `state: done`.

Edit state is in memory until `project_save`. Existing projects require reexport
mode; avoid two GUI/headless editors on the same project. Put caption lanes above
picture. Some sandbox runs exported successfully while title-cache writes were
denied; decode the export and inspect captions before delivery. Use the host's
normal permission handling when necessary rather than accepting missing text.

Rich-text karaoke was not documented in the tested build. One working approach
uses separate word titles and matching colored overlays positioned from the same
shaped metrics. Keep them in screen space and label their time estimates. This
package's generic assembler provides phrase captions; author the extra word
layers through the actual API when that feature is needed.
