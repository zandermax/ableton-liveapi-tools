# API Reference

Complete reference for all 220 tools exposed by the ALiveMCP Remote Script over TCP port 9004.

## How to Use This Reference

Send a JSON object with an `"action"` key and any required parameters. Receive a JSON response. All responses include `"ok": true` on success or `"ok": false, "error": "..."` on failure.

```python
import socket, json

def send_command(action, **params):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9004))
    message = json.dumps({'action': action, **params}) + '\n'
    sock.sendall(message.encode('utf-8'))
    response = b''
    while b'\n' not in response:
        response += sock.recv(4096)
    sock.close()
    return json.loads(response.decode('utf-8'))
```

---

## Index

- [Utility](#utility)
- [Session Control](#session-control)
- [Transport](#transport)
- [Automation Recording](#automation-recording)
- [Metronome Volume](#metronome-volume)
- [Track Management](#track-management)
- [Track Routing & Monitoring](#track-routing--monitoring)
- [Track Groups](#track-groups)
- [Track Freeze / Flatten](#track-freeze--flatten)
- [Track Annotations](#track-annotations)
- [Track Delay Compensation](#track-delay-compensation)
- [Clip Operations](#clip-operations)
- [Clip Properties](#clip-properties)
- [Clip Annotations](#clip-annotations)
- [Clip Fades](#clip-fades)
- [Clip RAM Mode](#clip-ram-mode)
- [Follow Actions](#follow-actions)
- [MIDI Notes](#midi-notes)
- [MIDI CC / Program Change](#midi-cc--program-change)
- [Devices](#devices)
- [Rack / Chain Operations](#rack--chain-operations)
- [Plugin Windows](#plugin-windows)
- [Device Utilities](#device-utilities)
- [Mixing: Sends](#mixing-sends)
- [Mixing: Master Track](#mixing-master-track)
- [Mixing: Return Tracks](#mixing-return-tracks)
- [Crossfader](#crossfader)
- [Groove & Quantize](#groove--quantize)
- [Groove Pool](#groove-pool)
- [Scenes](#scenes)
- [Project & Arrangement](#project--arrangement)
- [Arrangement View Clips](#arrangement-view-clips)
- [View / Navigation](#view--navigation)
- [Loop & Locators](#loop--locators)
- [Browser](#browser)
- [Color Utilities](#color-utilities)
- [Clip Automation Envelopes](#clip-automation-envelopes)
- [Audio Clips (Warp)](#audio-clips-warp)
- [Sample / Simpler](#sample--simpler)
- [Max for Live Devices](#max-for-live-devices)
- [Take Lanes (Live 12+)](#take-lanes-live-12)
- [Application Info (Live 12+)](#application-info-live-12)
- [Device Parameter Display Values (Live 12+)](#device-parameter-display-values-live-12)
- [Additional Properties](#additional-properties)

---

## Utility

### `ping`

Check that the Remote Script is running.

**Parameters:** none

**Response:**
- `ok`: true
- `message`: `"pong (queue-based, thread-safe)"`
- `script`: `"ALiveMCP_Remote"`
- `version`: version string

---

### `health_check`

Get detailed health status including Ableton version and queue depth.

**Parameters:** none

**Response:**
- `ok`: true
- `message`: status string
- `version`: script version string
- `tool_count`: number of available tools (int)
- `ableton_version`: major version of Ableton Live (string)
- `queue_size`: current command queue depth (int)

---

## Session Control

### `start_playback`

Start Ableton playback (no-op if already playing).

**Parameters:** none

**Response:** `ok`, `message`

---

### `stop_playback`

Stop Ableton playback (no-op if not playing).

**Parameters:** none

**Response:** `ok`, `message`

---

### `start_recording`

Enable record mode and start playback.

**Parameters:** none

**Response:** `ok`, `message`

---

### `stop_recording`

Disable record mode (does not stop playback).

**Parameters:** none

**Response:** `ok`, `message`

---

### `continue_playing`

Continue playback from the current position.

**Parameters:** none

**Response:** `ok`, `message`

---

### `get_session_info`

Get a snapshot of the current session state.

**Parameters:** none

**Response:**
- `ok`: true
- `is_playing`: bool
- `tempo`: float (BPM)
- `time_signature_numerator`: int
- `time_signature_denominator`: int
- `current_song_time`: float (beats)
- `loop_start`: float (beats)
- `loop_end`: float (beats)
- `loop_length`: float (beats)
- `num_tracks`: int
- `num_scenes`: int
- `record_mode`: bool
- `metronome`: bool
- `nudge_up`: bool
- `nudge_down`: bool

---

### `set_tempo`

Set session tempo. Valid range: 20–999 BPM.

**Parameters:**
- `bpm` (float, required)

**Response:** `ok`, `message`, `bpm`

---

### `set_time_signature`

Set session time signature.

**Parameters:**
- `numerator` (int, required) — 1–99
- `denominator` (int, required) — must be 1, 2, 4, 8, or 16

**Response:** `ok`, `message`, `numerator`, `denominator`

---

### `set_loop_start`

Set arrangement loop start position.

**Parameters:**
- `position` (float, required) — position in beats

**Response:** `ok`, `loop_start`

---

### `set_loop_length`

Set arrangement loop length.

**Parameters:**
- `length` (float, required) — length in beats

**Response:** `ok`, `loop_length`

---

### `set_metronome`

Enable or disable the metronome.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `metronome`

---

### `tap_tempo`

Send a tap-tempo pulse.

**Parameters:** none

**Response:** `ok`, `message`

---

### `undo`

Undo the last action.

**Parameters:** none

**Response:** `ok`, `message`

---

### `redo`

Redo the last undone action.

**Parameters:** none

**Response:** `ok`, `message`

---

## Transport

### `jump_to_time`

Move the playback position to a specific beat.

**Parameters:**
- `time_in_beats` (float, required)

**Response:** `ok`, `time`

---

### `get_current_time`

Get the current playback position.

**Parameters:** none

**Response:** `ok`, `current_song_time` (float), `is_playing` (bool)

---

### `set_arrangement_overdub`

Enable or disable arrangement overdub.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `arrangement_overdub`

---

### `set_back_to_arranger`

Enable or disable "Back to Arrangement" mode.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `back_to_arranger`

---

### `set_punch_in`

Enable or disable punch-in recording.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `punch_in`

---

### `set_punch_out`

Enable or disable punch-out recording.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `punch_out`

---

### `nudge_up`

Nudge the playback position up.

**Parameters:** none

**Response:** `ok`, `message`

---

### `nudge_down`

Nudge the playback position down.

**Parameters:** none

**Response:** `ok`, `message`

---

## Automation Recording

### `re_enable_automation`

Re-enable all automation that has been overridden.

**Parameters:** none

**Response:** `ok`, `message`

---

### `get_session_automation_record`

Get the session automation recording state.

**Parameters:** none

**Response:** `ok`, `session_automation_record` (bool)

---

### `set_session_automation_record`

Enable or disable session automation recording.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `session_automation_record`

---

### `get_session_record`

Get the session record state.

**Parameters:** none

**Response:** `ok`, `session_record` (bool)

---

### `set_session_record`

Enable or disable session recording.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `session_record`

---

### `capture_midi`

Capture the last-played MIDI notes into a clip.

**Parameters:** none

**Response:** `ok`, `message`

---

## Metronome Volume

### `get_metronome_volume`

Get the metronome volume.

**Parameters:** none

**Response:** `ok`, `volume` (float)

---

### `set_metronome_volume`

Set the metronome volume.

**Parameters:**
- `volume` (float, required) — 0.0 to 1.0

**Response:** `ok`, `volume`

---

## Track Management

### `create_midi_track`

Create a new MIDI track at the end of the track list.

**Parameters:**
- `name` (string, optional) — track name

**Response:** `ok`, `message`, `track_index`, `name`

---

### `create_audio_track`

Create a new audio track at the end of the track list.

**Parameters:**
- `name` (string, optional) — track name

**Response:** `ok`, `message`, `track_index`, `name`

---

### `create_return_track`

Create a new return track.

**Parameters:** none

**Response:** `ok`, `message`, `return_index`

---

### `delete_track`

Delete a track by index.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `message`

---

### `duplicate_track`

Duplicate a track. The copy is inserted immediately after the original.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `message`, `new_index`

---

### `rename_track`

Rename a track.

**Parameters:**
- `track_index` (int, required)
- `name` (string, required)

**Response:** `ok`, `message`, `name`

---

### `set_track_volume`

Set a track's volume.

**Parameters:**
- `track_index` (int, required)
- `volume` (float, required) — 0.0 to 1.0

**Response:** `ok`, `message`, `track_index`, `volume`

---

### `set_track_pan`

Set a track's panning.

**Parameters:**
- `track_index` (int, required)
- `pan` (float, required) — -1.0 (full left) to 1.0 (full right)

**Response:** `ok`, `message`, `track_index`, `pan`

---

### `arm_track`

Arm or disarm a track for recording.

**Parameters:**
- `track_index` (int, required)
- `armed` (bool, optional, default `true`)

**Response:** `ok`, `message`, `armed`

---

### `solo_track`

Solo or unsolo a track.

**Parameters:**
- `track_index` (int, required)
- `solo` (bool, optional, default `true`)

**Response:** `ok`, `message`

---

### `mute_track`

Mute or unmute a track.

**Parameters:**
- `track_index` (int, required)
- `mute` (bool, optional, default `true`)

**Response:** `ok`, `message`

---

### `get_track_info`

Get detailed information about a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `name`, `color`, `is_foldable`, `mute`, `solo`, `arm`, `has_midi_input`, `has_audio_input`, `volume`, `pan`, `num_devices`, `num_clips`

---

### `set_track_color`

Set a track's color.

**Parameters:**
- `track_index` (int, required)
- `color_index` (int, required) — Ableton color index

**Response:** `ok`, `message`, `color`

---

## Track Routing & Monitoring

### `set_track_fold_state`

Fold or unfold a group track.

**Parameters:**
- `track_index` (int, required)
- `folded` (bool, required)

**Response:** `ok`, `fold_state`

---

### `set_track_input_routing`

Set a track's input routing type.

**Parameters:**
- `track_index` (int, required)
- `routing_type_name` (string, required)
- `routing_channel` (int, optional, default `0`)

**Response:** `ok`, `message`, `routing_type`, `routing_channel`

---

### `set_track_output_routing`

Set a track's output routing type.

**Parameters:**
- `track_index` (int, required)
- `routing_type_name` (string, required)

**Response:** `ok`, `message`, `routing_type`

---

### `set_track_current_monitoring_state`

Set track monitoring state.

**Parameters:**
- `track_index` (int, required)
- `state` (int, required) — 0=In, 1=Auto, 2=Off

**Response:** `ok`, `monitoring_state`

---

### `get_track_available_input_routing_types`

List available input routing type names for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `routing_types` (list of strings), `count`

---

### `get_track_available_output_routing_types`

List available output routing type names for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `routing_types` (list of strings), `count`

---

### `get_track_input_routing_type`

Get the current input routing type for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `routing_type` (string or null)

---

### `get_track_output_routing`

Get the current output routing configuration for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `track_name`, `output_routing_type`, `output_routing_channel`

---

### `set_track_input_sub_routing`

Set a track's input sub-routing channel.

**Parameters:**
- `track_index` (int, required)
- `sub_routing` (string, required)

**Response:** `ok`, `message`, `track_index`, `requested_sub_routing`

---

### `set_track_output_sub_routing`

Set a track's output sub-routing channel.

**Parameters:**
- `track_index` (int, required)
- `sub_routing` (string, required)

**Response:** `ok`, `message`, `track_index`, `requested_sub_routing`

---

### `set_track_send`

Set a send level for a track.

**Parameters:**
- `track_index` (int, required)
- `send_index` (int, required) — 0-based index into return tracks
- `value` (float, required) — 0.0 to 1.0

**Response:** `ok`, `send_index`, `value`

---

### `get_track_sends`

Get all send levels for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `sends` (list of `{index, value, name}`), `count`

---

## Track Groups

### `create_group_track`

Create a new empty group track.

**Parameters:**
- `name` (string, optional)

**Response:** `ok`, `message`, `track_index`, `name`

---

### `group_tracks`

Group a range of tracks together.

**Parameters:**
- `start_index` (int, required)
- `end_index` (int, required) — inclusive

**Response:** `ok`, `message`, `start_index`, `end_index`

---

### `get_track_is_grouped`

Check whether a track is a member of a group.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `is_grouped` (bool), `is_group_track` (bool), `group_track_index` (int, if grouped)

---

### `ungroup_track`

Ungroup a group track.

**Parameters:**
- `group_track_index` (int, required)

**Response:** `ok`, `message`, `group_track_index`

---

## Track Freeze / Flatten

### `freeze_track`

Freeze a track to reduce CPU usage. Requires `freeze_available` on the track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `frozen`

---

### `unfreeze_track`

Unfreeze a frozen track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `frozen`

---

### `flatten_track`

Flatten a frozen track to audio. The track must be frozen first.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `message`

---

## Track Annotations

### `get_track_annotation`

Get the annotation text for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `annotation`

---

### `set_track_annotation`

Set the annotation text for a track.

**Parameters:**
- `track_index` (int, required)
- `annotation_text` (string, required)

**Response:** `ok`, `annotation`

---

## Track Delay Compensation

### `get_track_delay`

Get a track's delay compensation value.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `delay` (float, samples)

---

### `set_track_delay`

Set a track's delay compensation.

**Parameters:**
- `track_index` (int, required)
- `delay_samples` (float, required) — delay in samples

**Response:** `ok`, `delay`

---

## Clip Operations

### `create_midi_clip`

Create a new empty MIDI clip in the Session view.

**Parameters:**
- `track_index` (int, required) — must be a MIDI track
- `scene_index` (int, required) — slot must be empty
- `length` (float, optional, default `4.0`) — clip length in beats

**Response:** `ok`, `message`, `track_index`, `scene_index`, `length`

---

### `delete_clip`

Delete the clip in a slot.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)

**Response:** `ok`, `message`

---

### `duplicate_clip`

Duplicate the clip in a slot to the same slot (extends).

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)

**Response:** `ok`, `message`

---

### `launch_clip`

Launch (fire) a clip.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)

**Response:** `ok`, `message`

---

### `stop_clip`

Stop all clips on a track.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required) — only `track_index` is used; all clips on the track are stopped

**Response:** `ok`, `message`

---

### `stop_all_clips`

Stop all playing clips across all tracks.

**Parameters:** none

**Response:** `ok`, `message`

---

### `get_clip_info`

Get information about a clip.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)

**Response:** `ok`, `name`, `length`, `loop_start`, `loop_end`, `is_midi_clip`, `is_audio_clip`, `is_playing`, `muted`, `color`

---

### `set_clip_name`

Rename a clip.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)
- `name` (string, required)

**Response:** `ok`, `message`, `name`

---

## Clip Properties

### `set_clip_looping`

Enable or disable looping for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `looping` (bool, required)

**Response:** `ok`, `looping`

---

### `set_clip_loop_start`

Set the loop start position within a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `loop_start` (float, required) — position in beats

**Response:** `ok`, `loop_start`

---

### `set_clip_loop_end`

Set the loop end position within a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `loop_end` (float, required) — position in beats

**Response:** `ok`, `loop_end`

---

### `set_clip_start_marker`

Set the start marker (playback start point) of a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `start_marker` (float, required) — position in beats

**Response:** `ok`, `start_marker`

---

### `set_clip_end_marker`

Set the end marker (playback end point) of a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `end_marker` (float, required) — position in beats

**Response:** `ok`, `end_marker`

---

### `set_clip_muted`

Mute or unmute a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `muted` (bool, required)

**Response:** `ok`, `muted`

---

### `set_clip_gain`

Set clip gain (audio clips only).

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `gain` (float, required) — gain value

**Response:** `ok`, `gain`

---

### `set_clip_pitch_coarse`

Transpose a clip by semitones.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `semitones` (int, required)

**Response:** `ok`, `pitch_coarse`

---

### `set_clip_pitch_fine`

Fine-tune a clip's pitch in cents.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `cents` (int, required)

**Response:** `ok`, `pitch_fine`

---

### `set_clip_signature_numerator`

Set a clip's local time signature numerator.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `numerator` (int, required)

**Response:** `ok`, `signature_numerator`

---

### `set_clip_color`

Set a clip's color.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `color_index` (int, required) — Ableton color index

**Response:** `ok`, `track_index`, `clip_index`, `color_index` or `color`

---

## Clip Annotations

### `get_clip_annotation`

Get annotation text for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `annotation`

---

### `set_clip_annotation`

Set annotation text for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `annotation_text` (string, required)

**Response:** `ok`, `annotation`

---

## Clip Fades

Audio clips only.

### `get_clip_fade_in`

Get the fade-in time for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `fade_in_time` (float)

---

### `set_clip_fade_in`

Set the fade-in time for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `fade_time` (float, required)

**Response:** `ok`, `fade_in_time`

---

### `get_clip_fade_out`

Get the fade-out time for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `fade_out_time` (float)

---

### `set_clip_fade_out`

Set the fade-out time for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `fade_time` (float, required)

**Response:** `ok`, `fade_out_time`

---

## Clip RAM Mode

Audio clips only.

### `get_clip_ram_mode`

Check whether an audio clip is loaded into RAM.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `ram_mode` (bool)

---

### `set_clip_ram_mode`

Control whether an audio clip streams from disk or loads into RAM.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `ram_mode` (bool, required)

**Response:** `ok`, `ram_mode`

---

## Follow Actions

### `get_clip_follow_action`

Get the follow action configuration for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `track_index`, `clip_index`, `follow_action_A` (int), `follow_action_A_name`, `follow_action_B` (int), `follow_action_B_name`, `follow_action_time`, `follow_action_chance_A`, `follow_action_chance_B`

Follow action codes: 0=Stop, 1=Play Again, 2=Previous, 3=Next, 4=First, 5=Last, 6=Any, 7=Other, 8=Jump

---

### `set_clip_follow_action`

Set follow actions for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `action_A` (int, required) — 0–8 (see codes above)
- `action_B` (int, required) — 0–8
- `chance_A` (float, optional, default `1.0`) — probability for action A (0.0–1.0); chance B = 1 - chance_A

**Response:** `ok`, `track_index`, `clip_index`, `follow_action_A`, `follow_action_B`

---

### `set_follow_action_time`

Set the time before the follow action triggers.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `time_in_bars` (float, required)

**Response:** `ok`, `follow_action_time`

---

## MIDI Notes

### `add_notes`

Add MIDI notes to a clip. Notes with invalid pitch (outside 0–127) or velocity (outside 0–127) or non-positive duration are silently skipped.

**Parameters:**
- `track_index` (int, required)
- `scene_index` (int, required)
- `notes` (list, required) — list of note objects, each with:
  - `pitch` (int) — MIDI note number, 0–127
  - `start` (float) — start time in beats
  - `duration` (float) — duration in beats (must be > 0)
  - `velocity` (int) — 0–127

**Response:** `ok`, `message`, `track_index`, `scene_index`, `note_count`

**Example:**
```json
{
  "action": "add_notes",
  "track_index": 0,
  "scene_index": 0,
  "notes": [
    {"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100},
    {"pitch": 64, "start": 1.0, "duration": 0.5, "velocity": 80}
  ]
}
```

---

### `get_clip_notes`

Get all MIDI notes from a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `track_index`, `clip_index`, `notes` (list of `{pitch, start_time, duration, velocity, muted}`), `count`

---

### `remove_notes`

Remove MIDI notes from a clip within a pitch and time range.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `pitch_from` (int, optional, default `0`)
- `pitch_to` (int, optional, default `127`)
- `time_from` (float, optional, default `0.0`)
- `time_to` (float, optional, default `999.0`)

**Response:** `ok`, `message`

---

### `select_all_notes`

Select all notes in a MIDI clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `message`

---

### `deselect_all_notes`

Deselect all notes in a MIDI clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `message`

---

### `replace_selected_notes`

Replace the currently selected notes with new notes.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `notes` (list, required) — same format as `add_notes`; each note may also include `muted` (bool)

**Response:** `ok`, `message`, `note_count`

---

### `get_notes_extended`

Get notes with filtering by time and pitch range.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `start_time` (float, required) — filter start, in beats
- `time_span` (float, required) — duration of filter window, in beats
- `start_pitch` (int, required) — lowest pitch to include
- `pitch_span` (int, required) — number of pitches to include

**Response:** `ok`, `notes` (list), `count`

---

## MIDI CC / Program Change

### `send_midi_cc`

Send a MIDI Control Change message.

**Parameters:**
- `track_index` (int, required) — currently unused for routing but required
- `cc_number` (int, required) — 0–127
- `cc_value` (int, required) — 0–127
- `channel` (int, optional, default `0`) — MIDI channel, 0-based (0 = channel 1)

**Response:** `ok`, `cc_number`, `cc_value`, `channel`, `message`

---

### `send_program_change`

Send a MIDI Program Change message.

**Parameters:**
- `track_index` (int, required) — currently unused for routing but required
- `program_number` (int, required) — 0–127
- `channel` (int, optional, default `0`)

**Response:** `ok`, `program_number`, `channel`, `message`

---

## Devices

### `add_device`

Request adding a device to a track. Note: full device loading requires the browser API and returns a placeholder response.

**Parameters:**
- `track_index` (int, required)
- `device_name` (string, required)

**Response:** `ok`, `message`, `device_name`

---

### `get_track_devices`

Get all devices on a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `devices` (list of `{name, class_name, is_active, num_parameters}`), `count`

---

### `set_device_param`

Set a device parameter by index.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)
- `value` (float, required)

**Response:** `ok`, `message`, `value`

---

### `set_device_on_off`

Enable or disable a device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `enabled` (bool, required)

**Response:** `ok`, `is_active`

---

### `get_device_parameters`

Get all parameters for a device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `track_index`, `device_index`, `parameters` (list of `{index, name, value, min, max, is_quantized, is_enabled}`), `count`

---

### `get_device_parameter_by_name`

Find a device parameter by name.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_name` (string, required)

**Response:** `ok`, `index`, `name`, `value`, `min`, `max`

---

### `set_device_parameter_by_name`

Set a device parameter by name.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_name` (string, required)
- `value` (float, required)

**Response:** `ok`, `name`, `value`

---

### `delete_device`

Delete a device from a track.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `message`

---

### `get_device_presets`

Get available presets for a device. Note: preset browsing requires the browser API.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `message`, `device_index`

---

### `set_device_preset`

Load a preset for a device by index. Note: requires browser API.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `preset_index` (int, required)

**Response:** `ok`, `message`, `preset_index`

---

### `randomize_device_parameters`

Randomize all non-quantized parameters of a device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `message`, `randomized_count`

---

### `randomize_device`

Randomize all enabled, non-quantized parameters of a device (alias with richer response).

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `track_index`, `device_index`, `device_name`, `randomized_parameters`

---

## Rack / Chain Operations

### `get_device_chains`

Get the chains of an instrument/effect rack device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required) — must be a rack device

**Response:** `ok`, `chains` (list of `{index, name, mute, solo, num_devices}`), `count`

---

### `get_chain_devices`

Get all devices within a specific rack chain.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `chain_index` (int, required)

**Response:** `ok`, `chain_index`, `devices` (list of `{name, class_name, is_active}`), `count`

---

### `set_chain_mute`

Mute or unmute a rack chain.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `chain_index` (int, required)
- `mute` (bool, required)

**Response:** `ok`, `chain_index`, `mute`

---

### `set_chain_solo`

Solo or unsolo a rack chain.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `chain_index` (int, required)
- `solo` (bool, required)

**Response:** `ok`, `chain_index`, `solo`

---

## Plugin Windows

### `show_plugin_window`

Show the editor window for a device/plugin.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `message`, `device_name`

---

### `hide_plugin_window`

Hide the editor window for a device/plugin.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `message`

---

## Device Utilities

### `get_device_class_name`

Get the internal class name of a device (e.g., `"OriginalSimpler"`, `"Compressor2"`).

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `class_name`

---

### `get_device_type`

Get the device type as an integer.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `type` (int: 0=audio_effect, 1=instrument, 2=midi_effect)

---

## Mixing: Sends

*(Covered under [Track Routing & Monitoring](#track-routing--monitoring): `set_track_send`, `get_track_sends`)*

---

## Mixing: Master Track

### `get_master_track_info`

Get master track information.

**Parameters:** none

**Response:** `ok`, `name`, `volume`, `pan`, `num_devices`

---

### `set_master_volume`

Set master track volume.

**Parameters:**
- `volume` (float, required) — 0.0 to 1.0

**Response:** `ok`, `volume`

---

### `set_master_pan`

Set master track pan.

**Parameters:**
- `pan` (float, required) — -1.0 to 1.0

**Response:** `ok`, `pan`

---

### `get_master_devices`

Get all devices on the master track.

**Parameters:** none

**Response:** `ok`, `devices` (list of `{name, class_name, is_active}`), `count`

---

## Mixing: Return Tracks

### `get_return_track_count`

Get the number of return tracks.

**Parameters:** none

**Response:** `ok`, `count`

---

### `get_return_track_info`

Get information about a return track.

**Parameters:**
- `return_index` (int, required)

**Response:** `ok`, `index`, `name`, `volume`, `pan`, `mute`, `solo`, `num_devices`

---

### `set_return_track_volume`

Set a return track's volume.

**Parameters:**
- `return_index` (int, required)
- `volume` (float, required) — 0.0 to 1.0

**Response:** `ok`, `return_index`, `volume`

---

## Crossfader

### `get_crossfader_assignment`

Get a track's crossfader assignment.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `crossfader_assignment` (int: 0=None, 1=A, 2=B), `assignment_name`

---

### `set_crossfader_assignment`

Set a track's crossfader assignment.

**Parameters:**
- `track_index` (int, required)
- `assignment` (int, required) — 0=None, 1=A, 2=B

**Response:** `ok`, `track_index`, `crossfader_assignment`

---

### `get_crossfader_position`

Get the master crossfader position.

**Parameters:** none

**Response:** `ok`, `position` (float, -1.0 to 1.0)

---

## Groove & Quantize

### `set_clip_groove_amount`

Set groove amount for a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `amount` (float, required) — 0.0 to 1.0

**Response:** `ok`, `groove_amount`

---

### `quantize_clip`

Quantize a MIDI clip to a grid value.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `quantize_to` (float, required) — grid size in beats (e.g. `0.25` for 16th notes)

**Response:** `ok`, `message`, `quantize_to`

---

### `quantize_clip_pitch`

Quantize MIDI clip pitch.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `pitch` (int, optional, default `60`) — target pitch

**Response:** `ok`, `message`, `pitch`

---

### `get_groove_amount`

Get the global song groove amount.

**Parameters:** none

**Response:** `ok`, `groove_amount`

---

### `set_groove_amount`

Set the global song groove amount.

**Parameters:**
- `amount` (float, required) — 0.0 to 1.0

**Response:** `ok`, `groove_amount`

---

## Groove Pool

### `get_groove_pool_grooves`

List all grooves in the groove pool.

**Parameters:** none

**Response:** `ok`, `grooves` (list of `{index, name, timing_amount, random_amount, velocity_amount}`), `count`

---

### `set_clip_groove`

Assign a groove pool groove to a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `groove_index` (int, required) — index into groove pool

**Response:** `ok`, `message`, `groove_index`

---

## Scenes

### `create_scene`

Create a new scene at the end of the scene list.

**Parameters:**
- `name` (string, optional)

**Response:** `ok`, `message`, `scene_index`, `name`

---

### `delete_scene`

Delete a scene.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `message`

---

### `duplicate_scene`

Duplicate a scene. Copy is inserted immediately after the original.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `message`, `new_index`

---

### `launch_scene`

Launch (fire) all clips in a scene.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `message`, `scene_index`

---

### `rename_scene`

Rename a scene.

**Parameters:**
- `scene_index` (int, required)
- `name` (string, required)

**Response:** `ok`, `message`, `name`

---

### `get_scene_info`

Get information about a scene.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `scene_index`, `name`, `color`, `tempo`, `time_signature_numerator`

---

### `get_scene_color`

Get a scene's color index.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `color`

---

### `set_scene_color`

Set a scene's color.

**Parameters:**
- `scene_index` (int, required)
- `color_index` (int, required)

**Response:** `ok`, `color`

---

## Project & Arrangement

### `get_project_root_folder`

Get the project root folder path.

**Parameters:** none

**Response:** `ok`, `project_root_folder` (string or null)

---

### `trigger_session_record`

Trigger session recording with an optional fixed length.

**Parameters:**
- `length` (float, optional) — recording length in beats; omit for open-ended recording

**Response:** `ok`, `message`

---

### `get_can_jump_to_next_cue`

Check whether there is a next cue point to jump to.

**Parameters:** none

**Response:** `ok`, `can_jump_to_next_cue` (bool)

---

### `get_can_jump_to_prev_cue`

Check whether there is a previous cue point to jump to.

**Parameters:** none

**Response:** `ok`, `can_jump_to_prev_cue` (bool)

---

### `jump_to_next_cue`

Jump playback to the next cue point.

**Parameters:** none

**Response:** `ok`, `message`

---

### `jump_to_prev_cue`

Jump playback to the previous cue point.

**Parameters:** none

**Response:** `ok`, `message`

---

## Arrangement View Clips

### `get_arrangement_clips`

Get all clips in the arrangement view for a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `count`, `clips` (list of `{name, start_time, end_time, length}`)

---

### `duplicate_to_arrangement`

Duplicate a session clip to the arrangement view at the current playback position.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `message`

---

### `consolidate_clip`

Initiate consolidation of arrangement clips in a time range.

**Parameters:**
- `track_index` (int, required)
- `start_time` (float, required) — start in beats
- `end_time` (float, required) — end in beats

**Response:** `ok`, `message`, `start_time`, `end_time`

---

## View / Navigation

### `show_clip_view`

Switch to the Session view.

**Parameters:** none

**Response:** `ok`, `message`

---

### `show_arrangement_view`

Switch to the Arrangement view.

**Parameters:** none

**Response:** `ok`, `message`

---

### `focus_track`

Select and focus a track in the current view.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `message`

---

### `scroll_view_to_time`

Request the arrangement view to scroll to a specific time. Note: API support is limited.

**Parameters:**
- `time_in_beats` (float, required)

**Response:** `ok`, `message`, `time`

---

## Loop & Locators

### `set_loop_enabled`

Enable or disable the arrangement loop.

**Parameters:**
- `enabled` (bool, required)

**Response:** `ok`, `loop_enabled`

---

### `get_loop_enabled`

Get the current arrangement loop state and bounds.

**Parameters:** none

**Response:** `ok`, `loop_enabled`, `loop_start`, `loop_length`

---

### `create_locator`

Create a cue point (locator) at a specific time.

**Parameters:**
- `time_in_beats` (float, required)
- `name` (string, optional, default `"Locator"`)

**Response:** `ok`, `message`, `time`, `name`

---

### `delete_locator`

Delete a cue point by index.

**Parameters:**
- `locator_index` (int, required)

**Response:** `ok`, `message`, `locator_index`

---

### `get_locators`

Get all cue points.

**Parameters:** none

**Response:** `ok`, `locators` (list of `{index, time, name}`), `count`

---

### `jump_by_amount`

Move the playback position by a relative offset (positive or negative).

**Parameters:**
- `amount_in_beats` (float, required)

**Response:** `ok`, `old_time`, `new_time`, `jumped_by`

---

## Browser

### `browse_devices`

List Ableton device categories available in the browser.

**Parameters:** none

**Response:** `ok`, `device_types` (list), `count`

---

### `browse_plugins`

Get plugin browsing status. Note: plugin enumeration via LiveAPI is limited.

**Parameters:**
- `plugin_type` (string, optional, default `"vst"`)

**Response:** `ok`, `message`, `plugin_type`

---

### `load_device_from_browser`

Load a device from the browser onto a track (alias for `add_device`).

**Parameters:**
- `track_index` (int, required)
- `device_name` (string, required)

**Response:** see `add_device`

---

### `get_browser_items`

Get browser items for a category. Note: item enumeration is limited.

**Parameters:**
- `category` (string, optional, default `"devices"`) — one of `devices`, `plugins`, `instruments`, `audio_effects`, `midi_effects`

**Response:** `ok`, `category`, `available_categories`, `message`

---

## Color Utilities

### `get_clip_color`

Get the color of a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `color_index` or `color`

---

### `get_track_color`

Get the color of a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `color_index` or `color`

---

## Clip Automation Envelopes

### `get_clip_automation_envelope`

Check whether an automation envelope exists for a device parameter in a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)

**Response:** `ok`, `has_envelope` (bool), `parameter_name`, `device_name`

---

### `create_automation_envelope`

Create an automation envelope for a device parameter in a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)

**Response:** `ok`, `parameter_name`, `device_name`, `message`

---

### `clear_automation_envelope`

Clear (delete) the automation envelope for a device parameter.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)

**Response:** `ok`, `parameter_name`, `message`

---

### `insert_automation_step`

Insert an automation breakpoint at a specific time and value.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)
- `time` (float, required) — time in beats
- `value` (float, required)

**Response:** `ok`, `time`, `value`, `parameter_name`, `message`

---

### `remove_automation_step`

Remove an automation breakpoint at a specific time.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)
- `time` (float, required)

**Response:** `ok`, `time`, `parameter_name`, `message`

---

### `get_automation_envelope_values`

Check whether an automation envelope has any breakpoints.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)

**Response:** `ok`, `parameter_name`, `has_envelope` (bool), `message`

---

## Audio Clips (Warp)

### `get_clip_warp_mode`

Get the warp mode for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `warp_mode` (int), `warp_mode_name` (string), `warping` (bool)

Warp mode codes: 0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro

---

### `set_clip_warp_mode`

Set the warp mode for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `warp_mode` (int, required) — 0–5

**Response:** `ok`, `warp_mode`

---

### `get_clip_file_path`

Get the file path of the audio sample for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `file_path`

---

### `set_clip_warping`

Enable or disable warping for an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `warping` (bool, required)

**Response:** `ok`, `warping`

---

### `get_warp_markers`

Get all warp markers from an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `markers` (list of `{sample_time, beat_time}`), `count`

---

## Sample / Simpler

### `get_sample_length`

Get the raw sample length of an audio clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `sample_length` (float)

---

### `get_sample_playback_mode`

Get the playback mode of a Simpler or Sampler device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `playback_mode` (int)

---

### `set_sample_playback_mode`

Set the playback mode of a Simpler or Sampler device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `mode` (int, required)

**Response:** `ok`, `playback_mode`

---

## Max for Live Devices

### `is_max_device`

Check whether a device is a Max for Live device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `is_m4l` (bool), `class_name`, `class_display_name`, `device_name`

---

### `get_m4l_devices`

List all Max for Live devices on a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `track_name`, `devices` (list of `{index, name, class_name, type, is_active, num_parameters}`), `count`

---

### `set_device_param_by_name`

Set a device parameter value by name. Works with any device including M4L.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_name` (string, required)
- `value` (float, required)

**Response:** `ok`, `track_index`, `device_index`, `param_name`, `param_index`, `value`

---

### `get_m4l_param_by_name`

Get a device parameter value by name.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_name` (string, required)

**Response:** `ok`, `param_index`, `name`, `value`, `min`, `max`, `is_enabled`

---

### `get_cv_tools_devices`

List all CV Tools devices on a track (filtered by name containing "CV").

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `track_index`, `track_name`, `cv_devices` (list of `{index, name, class_name, is_active, num_parameters}`), `count`

---

## Take Lanes (Live 12+)

All take lane tools require Ableton Live 12 or later.

### `get_take_lanes`

Get all take lanes on a track.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `count`, `take_lanes` (list of `{index, name}`)

---

### `create_take_lane`

Create a new take lane on a track.

**Parameters:**
- `track_index` (int, required)
- `name` (string, optional)

**Response:** `ok`, `message`, `name`

---

### `get_take_lane_name`

Get the name of a specific take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)

**Response:** `ok`, `name`

---

### `set_take_lane_name`

Set the name of a take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)
- `name` (string, required)

**Response:** `ok`, `name`

---

### `create_audio_clip_in_lane`

Create an audio clip inside a take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)
- `length` (float, optional, default `4.0`) — length in beats

**Response:** `ok`, `message`, `length`

---

### `create_midi_clip_in_lane`

Create a MIDI clip inside a take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)
- `length` (float, optional, default `4.0`) — length in beats

**Response:** `ok`, `message`, `length`

---

### `get_clips_in_take_lane`

Get all clips inside a take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)

**Response:** `ok`, `count`, `clips` (list of `{name, length, is_midi}`)

---

### `delete_take_lane`

Delete a take lane.

**Parameters:**
- `track_index` (int, required)
- `lane_index` (int, required)

**Response:** `ok`, `message`

---

## Application Info (Live 12+)

### `get_build_id`

Get the Ableton Live build identifier. Requires Live 12+.

**Parameters:** none

**Response:** `ok`, `build_id`

---

### `get_variant`

Get the Ableton Live edition (e.g., `"Suite"`, `"Standard"`, `"Intro"`). Requires Live 12+.

**Parameters:** none

**Response:** `ok`, `variant`

---

### `show_message_box`

Show a message dialog box to the user. Requires Live 12+.

**Parameters:**
- `message` (string, required)
- `title` (string, optional, default `"Message"`)

**Response:** `ok`, `message`, `button_pressed` (int)

---

### `get_application_version`

Get full Ableton Live version information.

**Parameters:** none

**Response:** `ok`, `major_version`, `minor_version`, `bugfix_version`, `build_id` (Live 12+), `variant` (Live 12+)

---

## Device Parameter Display Values (Live 12+)

### `get_device_param_display_value`

Get a parameter's value as it appears in the Live UI (e.g., `"128 Hz"` instead of `0.5`). Requires Live 12+ for full `display_value` support; falls back to string conversion on older versions.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)
- `param_index` (int, required)

**Response:** `ok`, `display_value` (string), `raw_value` (float), `name`

---

### `get_all_param_display_values`

Get display values for all parameters of a device.

**Parameters:**
- `track_index` (int, required)
- `device_index` (int, required)

**Response:** `ok`, `device_name`, `count`, `parameters` (list of `{index, name, raw_value, display_value}`)

---

## Additional Properties

### `get_clip_start_time`

Get the start time property of a clip (Live 12+).

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)

**Response:** `ok`, `start_time` (float)

---

### `set_clip_start_time`

Set the start time of a clip.

**Parameters:**
- `track_index` (int, required)
- `clip_index` (int, required)
- `start_time` (float, required)

**Response:** `ok`, `start_time`

---

### `get_track_is_foldable`

Check whether a track is foldable (i.e. is a group track).

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `is_foldable` (bool)

---

### `get_track_is_frozen`

Check whether a track is currently frozen.

**Parameters:**
- `track_index` (int, required)

**Response:** `ok`, `is_frozen` (bool)

---

### `get_scene_is_empty`

Check whether a scene has no clips across all tracks.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `is_empty` (bool)

---

### `get_scene_tempo`

Get the tempo override set on a scene, if any.

**Parameters:**
- `scene_index` (int, required)

**Response:** `ok`, `tempo` (float or null), `has_tempo` (bool)

---

### `get_arrangement_overdub`

Get the current arrangement overdub state.

**Parameters:** none

**Response:** `ok`, `arrangement_overdub` (bool)

---

### `set_record_mode`

Set session or arrangement record mode.

**Parameters:**
- `mode` (int, required) — 0=session, 1=arrangement

**Response:** `ok`, `record_mode`

---

### `get_signature_numerator`

Get the global time signature numerator.

**Parameters:** none

**Response:** `ok`, `signature_numerator` (int)

---

### `get_signature_denominator`

Get the global time signature denominator.

**Parameters:** none

**Response:** `ok`, `signature_denominator` (int)
