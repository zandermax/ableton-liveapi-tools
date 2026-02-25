# Testing Guide

There are two independent testing layers in this project:

| Layer                                       | What it tests                                                                      | Needs Ableton? |
| ------------------------------------------- | ---------------------------------------------------------------------------------- | -------------- |
| **Unit tests** (`pytest`)                   | The Remote Script itself — tool logic, dispatch, thread safety                     | No             |
| **Mock server** (`examples/mock_server.py`) | Client code, the web dashboard, example scripts — anything that talks to port 9004 | No             |

---

## Unit tests

The test suite lives in `tests/` and uses pytest. Ableton's `Live` module is
stubbed out in `tests/conftest.py`, so tests run in any Python environment.

### Run the tests

```bash
pip install -r requirements-dev.txt
pytest
```

Coverage is reported automatically (`--cov=ALiveMCP_Remote`). To see a
per-file breakdown:

```bash
pytest --cov=ALiveMCP_Remote --cov-report=term-missing
```

### Test layout

```
tests/
├── conftest.py               # Live module stub + shared fixtures (song, tools)
├── test_alivemcp.py        # Dispatch, PARAM_ALIASES, error handling
├── test_session_transport.py # Session/transport tools
├── test_m4l_and_live12.py    # M4L and Live 12 tools
└── ...
```

### Adding tests

Follow the existing pattern — request the `tools` fixture, call the method
directly, assert on the returned dict:

```python
def test_my_new_tool(tools):
    result = tools.my_new_tool(track_index=0, some_param="value")
    assert result["ok"] is True
    assert result["result"] == expected_value
```

---

## Mock server

`examples/mock_server.py` is a standalone TCP server that listens on
`127.0.0.1:9004` — the same address as the real ALiveMCP Remote Script.
It speaks the identical newline-delimited JSON protocol, so any client works
against it without Ableton running.

### Start the mock

```bash
python3 examples/mock_server.py
```

The server prints its initial state and is ready immediately. Stop with `Ctrl+C`.

### Initial session state

The mock starts with a pre-populated session:

| Resource | Contents                                                 |
| -------- | -------------------------------------------------------- |
| Tracks   | Kick (audio), Bass (midi), Lead Synth (midi)             |
| Scenes   | Verse, Chorus                                            |
| Clips    | Kick Loop at 0,0 · Bass Line at 1,0 · Chorus Lead at 2,1 |
| Tempo    | 120.0 BPM, 4/4                                           |
| State    | Stopped, not recording                                   |

State is mutable — write commands (`set_tempo`, `create_midi_track`, etc.)
update in-memory state that subsequent reads reflect. State resets on restart.

### Implemented tools

**Session**
`ping` · `health_check` · `get_session_info` · `set_tempo` · `set_time_signature`
· `get_current_time` · `set_metronome` · `undo` · `redo` · `tap_tempo`

**Transport**
`start_playback` · `stop_playback` · `continue_playing`
· `start_recording` · `stop_recording`

**Tracks**
`create_midi_track` · `create_audio_track` · `delete_track` · `rename_track`
· `get_track_info` · `set_track_volume` · `set_track_pan`
· `mute_track` · `solo_track` · `arm_track` · `get_track_devices`

**Scenes**
`create_scene` · `delete_scene` · `rename_scene` · `get_scene_info` · `launch_scene`

**Clips**
`create_midi_clip` · `get_clip_info` · `set_clip_name` · `delete_clip`
· `launch_clip` · `stop_clip` · `stop_all_clips` · `add_notes` · `get_clip_notes`

Any action not listed returns `{"ok": false, "error": "Action 'xyz' not implemented in mock server"}` — an explicit signal rather than a silent success.

### Test client scripts against the mock

Any script using the `send_command` helper from `examples/test_connection.py`
works unchanged:

```bash
# With mock_server.py already running:
python examples/test_connection.py
python examples/basic_usage.py
```

Or in your own scripts:

```python
result = send_command("ping")
assert "mock" in result["message"]   # confirms you're hitting the mock

send_command("set_tempo", bpm=140)
info = send_command("get_session_info")
assert info["tempo"] == 140.0        # state mutation persists

result = send_command("get_track_info", track_index=999)
assert result["ok"] is False         # errors are explicit
```

### Use with the web dashboard

```bash
# Terminal 1
python3 examples/mock_server.py        # binds 127.0.0.1:9004

# Terminal 2
# - if you haven't set up the venv yet:
python3 -m venv examples/ui/.venv
source examples/ui/.venv/bin/activate
pip install -r examples/ui/requirements.txt

# Run UI
uvicorn examples.ui.server:app --port 8080   # binds 127.0.0.1:8080

# Open http://localhost:8080
```

The connection status pill shows green, session info populates automatically,
and transport buttons update state visible in subsequent responses.

### Port conflict

The mock and the real Remote Script cannot both bind port 9004. If Ableton is
already running with ALiveMCP loaded, the mock will refuse to start:

```
Error: cannot bind to 127.0.0.1:9004 — [Errno 48] Address already in use
```

Disable the ALiveMCP Remote Script in Ableton's preferences first, or free
the port:

```bash
lsof -ti tcp:9004 | xargs kill
```
