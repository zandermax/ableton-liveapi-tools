# CLAUDE.md — Project Orientation for AI Agents

## What This Project Is

ALiveMCP Remote Script is an Ableton Live Remote Script (Python) that exposes **220 LiveAPI tools** over a TCP socket on `127.0.0.1:9004`. Clients send newline-delimited JSON commands and receive JSON responses. The project is designed for use with AI agents (including Claude via MCP), algorithmic composition tools, and any external software that needs to control Ableton Live programmatically.

---

## Directory Map

```
ableton-liveapi-tools/
├── ALiveMCP_Remote/          # The Remote Script package — installed into Ableton
│   ├── __init__.py            # Entry point: ALiveMCP class + create_instance()
│   ├── liveapi_tools.py       # LiveAPITools: composes all mixin classes
│   ├── socket_server.py       # SocketServerMixin: TCP listener on port 9004
│   └── tools/                 # 30 domain-specific mixin modules
│       ├── base.py            # BaseMixin: self.song, self.c_instance, log()
│       ├── registry.py        # AVAILABLE_TOOLS list (220 names)
│       ├── session_transport.py / session_automation.py
│       ├── tracks.py / tracks_core.py / tracks_routing.py / tracks_advanced.py
│       ├── clips.py / clips_core.py / clips_extras.py / clips_properties.py
│       ├── midi.py / midi_notes.py / midi_cc.py
│       ├── devices.py / devices_core.py / devices_racks.py
│       ├── mixing.py / mixing_groove.py
│       ├── scenes.py
│       ├── arrangement.py / arrangement_browser.py
│       ├── automation.py
│       └── m4l_and_live12.py / m4l_devices.py / m4l_audio.py
│           live12_lanes.py / live12_properties.py
├── docs/
│   ├── API_REFERENCE.md       # Complete tool reference (all 220 tools)
│   ├── ARCHITECTURE.md        # Thread-safety design, sequence diagrams
│   ├── INSTALLATION.md        # Installation steps for macOS/Windows
│   └── TROUBLESHOOTING.md     # Common problems and solutions
├── examples/                  # Standalone client scripts (connect, basic usage, etc.)
├── tests/                     # Pytest test suite (mocked Live module)
├── scripts/
│   ├── check_file_length.py   # Pre-commit: fails if any .py file > 300 lines
│   └── check_version_bump.sh
├── .github/workflows/ci.yml   # CI: lint (ruff), tests, file length, shellcheck
├── README.md
├── MAX4LIVE_INTEGRATION.md
├── CONTRIBUTING.md
└── pyproject.toml
```

---

## How a Tool Call Works (End-to-End)

```
Client                 Socket Thread            Command Queue        Main Thread (update_display)
  |                         |                        |                        |
  |-- JSON + "\n" --------> |                        |                        |
  |                         |-- enqueue(id, cmd) --> |                        |
  |                         |-- wait on resp[id] ----|--------  ~0-16ms ----> |
  |                         |                        |<-- dequeue(id, cmd) ---|
  |                         |                        |         LiveAPI call   |
  |                         |                        |<-- enqueue result -----|
  |<-- JSON + "\n" ---------|<-- dequeue result -----|                        |
```

Key constraint: **All LiveAPI calls must execute on the main thread** (the one that calls `update_display()`). Socket threads only enqueue and wait. This is why the queue exists — Ableton's Python API is not thread-safe.

`update_display()` is called by Ableton at ~60 Hz and processes up to 5 commands per tick.

---

## How to Add a New Tool

1. **Implement the method** in the appropriate mixin file under `ALiveMCP_Remote/tools/`. Follow the existing pattern — wrap everything in `try/except` and return `{"ok": True, ...}` or `{"ok": False, "error": str(e)}`. Keep files under **300 lines** (the pre-commit hook enforces this; create a new mixin if needed).

   ```python
   def my_new_tool(self, track_index, some_param):
       """Brief one-line description"""
       try:
           track = self.song.tracks[track_index]
           result = track.some_property
           return {"ok": True, "result": result}
       except Exception as e:
           return {"ok": False, "error": str(e)}
   ```

2. **Register the name** in `ALiveMCP_Remote/tools/registry.py` by adding the method name string to `AVAILABLE_TOOLS`.

3. **Dispatch is automatic.** `ALiveMCP._process_command()` uses `getattr(self.tools, action, None)` — no dispatcher switch-case needed.

4. **Write tests** in the `tests/` directory following the existing pattern. The `Live` module is mocked via `tests/conftest.py`.

5. **Add documentation** to `docs/API_REFERENCE.md`.

---

## Key Constraints

| Constraint | Detail |
|---|---|
| **Main thread only** | Never call `self.song.*` from a socket thread. Use the queue. |
| **300-line limit** | Each `.py` file in `ALiveMCP_Remote/` must be ≤ 300 lines. Many files are already near the limit — split into a new mixin if needed. |
| **Python 2.7 compatible syntax** | Ableton Live bundles Python 2.7. Avoid f-strings, type annotations, walrus operators, and other Python 3-only syntax. (The few existing f-strings in the codebase are in locations where Live 11+ ships Python 3.) |
| **No external dependencies** | The Remote Script runs inside Ableton's bundled Python. Standard library only — no `pip install`. |
| **Localhost only** | The socket binds to `127.0.0.1`, not `0.0.0.0`. Remote access requires an SSH tunnel or explicit reconfiguration. |
| **`scene_index` alias** | For clip-slot operations (`create_midi_clip`, `delete_clip`, `duplicate_clip`, `launch_clip`, `stop_clip`, `get_clip_info`, `set_clip_name`, `add_notes`), the canonical parameter is `clip_index`. Legacy clients sending `scene_index` are still supported via `PARAM_ALIASES` in `ALiveMCP_Remote/__init__.py`. **Do not remove this alias** — it is part of the public API. |

---

## Protocol Quick Reference

**Request:**
```json
{"action": "set_tempo", "bpm": 128}
```

**Success response:**
```json
{"ok": true, "bpm": 128.0, "message": "Tempo set"}
```

**Error response:**
```json
{"ok": false, "error": "BPM must be between 20 and 999"}
```

Messages are newline-delimited (`\n`), UTF-8 encoded.

---

## Full Tool List

See [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) for all 220 tools with parameters and response fields.

For a quick list of tool names only, see [`ALiveMCP_Remote/tools/registry.py`](ALiveMCP_Remote/tools/registry.py).
