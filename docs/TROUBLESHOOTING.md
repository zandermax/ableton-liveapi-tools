# Troubleshooting

Solutions for common problems with the ClaudeMCP Remote Script.

---

## Script Not Loading

**Symptom:** Ableton Live starts but the script is not available in Preferences → MIDI → Control Surfaces, or it does not appear at all.

**Causes and fixes:**

1. **Wrong folder.** The `ClaudeMCP_Remote/` directory must be placed directly inside Ableton's Remote Scripts folder, not inside a sub-folder.
   - macOS: `~/Music/Ableton/User Library/Remote Scripts/ClaudeMCP_Remote/`
   - Windows: `%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\ClaudeMCP_Remote\`

2. **Missing `__init__.py`.** The folder must contain `__init__.py` with the `create_instance` function. Verify it exists:
   ```
   ClaudeMCP_Remote/
   ├── __init__.py      ← required
   ├── liveapi_tools.py
   └── ...
   ```

3. **Ableton not restarted.** Remote Scripts are loaded at startup. After copying the files, fully quit and relaunch Ableton Live.

4. **Python syntax error.** A syntax error in any file prevents the script from loading. Check `Log.txt` (see [Reading the Log](#reading-the-log)).

---

## Connection Refused on Port 9004

**Symptom:** `ConnectionRefusedError: [Errno 111] Connection refused` when connecting to `127.0.0.1:9004`.

**Causes and fixes:**

1. **Script not selected.** Open Ableton Preferences → Link/Tempo/MIDI → Control Surfaces. Select `ClaudeMCP_Remote` from the drop-down. Restart Ableton if needed.

2. **Script crashed at startup.** Check `Log.txt` for `[ClaudeMCP]` errors. A failed import (e.g. missing file) will prevent the socket from opening.

3. **Wrong port.** The script listens on `9004` by default. Confirm your client is connecting to `127.0.0.1:9004`.

4. **Port already in use.** Another process may hold port 9004. Check with:
   ```bash
   lsof -i :9004   # macOS / Linux
   netstat -ano | findstr :9004   # Windows
   ```
   If another process owns it, kill it and restart Ableton.

---

## `ok: false` Responses

All error responses follow this structure:
```json
{"ok": false, "error": "Error description"}
```

**Common causes:**

| Error message | Meaning |
|---|---|
| `"Invalid track index"` | `track_index` is out of range. Call `get_session_info` to find `num_tracks`. |
| `"Invalid scene index"` | `scene_index` is out of range. Call `get_session_info` to find `num_scenes`. |
| `"No clip in slot"` | The target slot is empty. Create a clip first with `create_midi_clip`. |
| `"Clip slot already has a clip"` | `create_midi_clip` target slot is occupied. Delete it first with `delete_clip`. |
| `"Track is not a MIDI track"` | Operation requires a MIDI track. Check `has_midi_input` from `get_track_info`. |
| `"Clip is not an audio clip"` | Audio-only operation (warp, fade, RAM mode) called on a MIDI clip. |
| `"Invalid device index"` | `device_index` is out of range. Call `get_track_devices` first. |
| `"Invalid parameter index"` | `param_index` is out of range. Call `get_device_parameters` first. |
| `"Unknown action: ..."` | The `action` value does not match any tool name. Check spelling against the [API Reference](API_REFERENCE.md). Available actions are also returned in the error response. |
| `"BPM must be between 20 and 999"` | `set_tempo` received an out-of-range value. |

---

## Timeout / No Response

**Symptom:** The client sends a command and never receives a response.

**Causes and fixes:**

1. **Command queue backed up.** Ableton processes at most 5 commands per `update_display()` tick (~16 ms). Under heavy load, commands queue up. Wait and retry, or reduce command frequency.

2. **Ableton blocked.** A modal dialog (e.g. save prompt, plugin window) can block the main thread. Dismiss any open dialogs.

3. **recv() loop issue.** The client must read until it receives a `\n` newline character (the message delimiter). A client that does not loop on `recv()` may block waiting for more data. See the example in [Basic Usage](../README.md#basic-usage).

4. **Connection closed by peer.** If Ableton crashes mid-command, the socket closes. Reconnect.

---

## Live 12-Only Tools on Live 11

Certain tools only work on Ableton Live 12. Calling them on Live 11 returns `ok: false`.

**Live 12-only tools:**
- Take lanes: `get_take_lanes`, `create_take_lane`, `get_take_lane_name`, `set_take_lane_name`, `create_audio_clip_in_lane`, `create_midi_clip_in_lane`, `get_clips_in_take_lane`, `delete_take_lane`
- Application info: `get_build_id`, `get_variant`, `show_message_box`
- Display values: `get_device_param_display_value`, `get_all_param_display_values` (falls back gracefully on Live 11 with string conversion)

**Detection:** Use `get_application_version` to check the major version before calling Live 12-specific tools:
```python
info = send_command('get_application_version')
if info['major_version'] >= 12:
    lanes = send_command('get_take_lanes', track_index=0)
```

---

## Max for Live / CV Tools Issues

**Symptom:** `get_m4l_devices` returns an empty list even though M4L devices are present.

**Cause:** M4L detection uses internal class names (`MxDeviceAudioEffect`, `MxDeviceMidiEffect`, `MxDeviceInstrument`). Custom M4L patches that export with non-standard class names will not be detected by `get_m4l_devices`, but their parameters are still accessible via the standard device tools (`get_track_devices`, `set_device_param`).

**CV Tools detection:** `get_cv_tools_devices` filters by `"CV"` in the device name. Rename your CV Tools devices to include "CV" if they are not being found.

---

## Notes Not Appearing in Clip

**Symptom:** `add_notes` returns `ok: true` but the clip appears empty.

**Causes and fixes:**

1. **Notes outside clip length.** Notes with `start` ≥ `clip.length` are placed outside the visible range. Either extend the clip with `set_clip_loop_end` or use `start` values within the clip length.

2. **Clip not a MIDI clip.** `add_notes` only works on MIDI clips. Check `get_clip_info` → `is_midi_clip`.

3. **Invalid notes silently skipped.** Notes with `pitch` outside 0–127, `velocity` outside 0–127, or `duration` ≤ 0 are silently dropped. Validate your note data before sending.

---

## Reading the Log

Ableton writes Remote Script output to its log file. Errors are prefixed with `[ClaudeMCP]`.

- **macOS:** `~/Library/Preferences/Ableton/Live x.x.x/Log.txt`
- **Windows:** `%APPDATA%\Ableton\Live x.x.x\Preferences\Log.txt`

Tail the log while reproducing an issue:
```bash
tail -f ~/Library/Preferences/Ableton/Live\ 12*/Log.txt | grep ClaudeMCP
```

---

## Verifying the Installation

Run the connection test after installation:
```bash
python3 examples/test_connection.py
```

Expected output:
```
Connected to ClaudeMCP Remote Script
Version: x.x.x
Tool count: 220
```

If it fails, check the script is selected in Ableton Preferences and that Ableton has been restarted since installation.
