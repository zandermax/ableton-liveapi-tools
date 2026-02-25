#!/usr/bin/env python3
"""
Mock Ableton TCP server for development, testing, and UI demos.

Listens on 127.0.0.1:9004 (same port as the real ClaudeMCP Remote Script)
and responds to JSON commands with realistic mock data. Maintains in-memory
session state that mutates on write commands, so the web dashboard and any
client script behaves as though a real Ableton session is running.

Usage:
    python examples/mock_server.py
    # Server prints ready message, then leave it running.
    # Start the web dashboard or run any example script against it.

Stop with Ctrl+C.
"""

import json
import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = 9004
VERSION = "1.1.3-mock"

_lock = threading.Lock()

_state = {
    "tempo": 120.0,
    "time_signature_numerator": 4,
    "time_signature_denominator": 4,
    "is_playing": False,
    "is_recording": False,
    "current_time": 0.0,
    "loop_start": 0.0,
    "loop_length": 4.0,
    "loop_enabled": False,
    "metronome": False,
    "tracks": [
        {
            "index": 0,
            "name": "Kick",
            "type": "audio",
            "volume": 0.85,
            "pan": 0.0,
            "muted": False,
            "soloed": False,
            "armed": False,
        },
        {
            "index": 1,
            "name": "Bass",
            "type": "midi",
            "volume": 0.75,
            "pan": 0.0,
            "muted": False,
            "soloed": False,
            "armed": False,
        },
        {
            "index": 2,
            "name": "Lead Synth",
            "type": "midi",
            "volume": 0.70,
            "pan": 0.1,
            "muted": False,
            "soloed": False,
            "armed": False,
        },
    ],
    "scenes": [
        {"index": 0, "name": "Verse"},
        {"index": 1, "name": "Chorus"},
    ],
    "clips": {
        "0,0": {"name": "Kick Loop", "length": 4.0, "looping": True, "muted": False},
        "1,0": {"name": "Bass Line", "length": 4.0, "looping": True, "muted": False},
        "2,1": {"name": "Chorus Lead", "length": 8.0, "looping": True, "muted": False},
    },
}


# ── Dispatch ───────────────────────────────────────────────────────────────────


def _dispatch(command):
    action = command.get("action", "")
    params = {k: v for k, v in command.items() if k != "action"}
    with _lock:
        return _handle(action, params)


def _track(p):
    """Return track dict or error response for track_index param."""
    idx = p.get("track_index", -1)
    if not (0 <= idx < len(_state["tracks"])):
        return None, {"ok": False, "error": "Track index out of range"}
    return _state["tracks"][idx], None


def _scene(p):
    """Return scene dict or error response for scene_index param."""
    idx = p.get("scene_index", -1)
    if not (0 <= idx < len(_state["scenes"])):
        return None, {"ok": False, "error": "Scene index out of range"}
    return _state["scenes"][idx], None


def _handle(action, p):  # noqa: C901 — intentionally flat dispatch
    s = _state

    # ── Connection / health ────────────────────────────────────────────────────
    if action == "ping":
        return {
            "ok": True,
            "message": "pong (mock server)",
            "script": "ClaudeMCP_Remote",
            "version": VERSION,
        }

    if action == "health_check":
        return {
            "ok": True,
            "message": "Mock server running",
            "version": VERSION,
            "tool_count": 220,
            "ableton_version": "12",
            "queue_size": 0,
        }

    # ── Session state ──────────────────────────────────────────────────────────
    if action == "get_session_info":
        return {
            "ok": True,
            "tempo": s["tempo"],
            "time_signature_numerator": s["time_signature_numerator"],
            "time_signature_denominator": s["time_signature_denominator"],
            "is_playing": s["is_playing"],
            "is_recording": s["is_recording"],
            "num_tracks": len(s["tracks"]),
            "num_scenes": len(s["scenes"]),
            "loop_start": s["loop_start"],
            "loop_length": s["loop_length"],
            "loop_enabled": s["loop_enabled"],
        }

    if action == "set_tempo":
        bpm = float(p.get("bpm", 120))
        if not (20 <= bpm <= 999):
            return {"ok": False, "error": "BPM must be between 20 and 999"}
        s["tempo"] = bpm
        return {"ok": True, "bpm": bpm, "message": "Tempo set"}

    if action == "set_time_signature":
        s["time_signature_numerator"] = int(p.get("numerator", 4))
        s["time_signature_denominator"] = int(p.get("denominator", 4))
        return {
            "ok": True,
            "numerator": s["time_signature_numerator"],
            "denominator": s["time_signature_denominator"],
        }

    if action == "get_current_time":
        return {"ok": True, "current_time": s["current_time"]}

    if action == "set_metronome":
        s["metronome"] = bool(p.get("enabled", False))
        return {"ok": True, "enabled": s["metronome"]}

    if action in ("undo", "redo", "tap_tempo"):
        return {"ok": True, "message": f"{action} performed"}

    # ── Transport ──────────────────────────────────────────────────────────────
    if action == "start_playback":
        s["is_playing"] = True
        return {"ok": True, "message": "Playback started"}

    if action == "stop_playback":
        s["is_playing"] = False
        s["is_recording"] = False
        return {"ok": True, "message": "Playback stopped"}

    if action == "continue_playing":
        s["is_playing"] = True
        return {"ok": True, "message": "Playback continued"}

    if action == "start_recording":
        s["is_playing"] = True
        s["is_recording"] = True
        return {"ok": True, "message": "Recording started"}

    if action == "stop_recording":
        s["is_recording"] = False
        return {"ok": True, "message": "Recording stopped"}

    # ── Tracks ─────────────────────────────────────────────────────────────────
    if action in ("create_midi_track", "create_audio_track"):
        track_type = "midi" if "midi" in action else "audio"
        idx = len(s["tracks"])
        name = p.get("name", f"{track_type.capitalize()} {idx + 1}")
        s["tracks"].append(
            {
                "index": idx,
                "name": name,
                "type": track_type,
                "volume": 0.85,
                "pan": 0.0,
                "muted": False,
                "soloed": False,
                "armed": False,
            }
        )
        return {"ok": True, "track_index": idx, "name": name}

    if action == "delete_track":
        t, err = _track(p)
        if err:
            return err
        s["tracks"].remove(t)
        for i, tr in enumerate(s["tracks"]):
            tr["index"] = i
        return {"ok": True, "message": "Track deleted"}

    if action == "rename_track":
        t, err = _track(p)
        if err:
            return err
        t["name"] = p.get("name", t["name"])
        return {"ok": True, "name": t["name"]}

    if action == "get_track_info":
        t, err = _track(p)
        if err:
            return err
        return {"ok": True, **t}

    if action == "set_track_volume":
        t, err = _track(p)
        if err:
            return err
        t["volume"] = float(p.get("volume", t["volume"]))
        return {"ok": True, "volume": t["volume"]}

    if action == "set_track_pan":
        t, err = _track(p)
        if err:
            return err
        t["pan"] = float(p.get("pan", t["pan"]))
        return {"ok": True, "pan": t["pan"]}

    if action == "mute_track":
        t, err = _track(p)
        if err:
            return err
        t["muted"] = bool(p.get("muted", not t["muted"]))
        return {"ok": True, "muted": t["muted"]}

    if action == "solo_track":
        t, err = _track(p)
        if err:
            return err
        t["soloed"] = bool(p.get("solo", not t["soloed"]))
        return {"ok": True, "solo": t["soloed"]}

    if action == "arm_track":
        t, err = _track(p)
        if err:
            return err
        t["armed"] = bool(p.get("armed", not t["armed"]))
        return {"ok": True, "armed": t["armed"]}

    if action == "get_track_devices":
        _, err = _track(p)
        if err:
            return err
        return {"ok": True, "devices": [], "count": 0}

    # ── Scenes ─────────────────────────────────────────────────────────────────
    if action == "create_scene":
        idx = len(s["scenes"])
        name = p.get("name", f"Scene {idx + 1}")
        s["scenes"].append({"index": idx, "name": name})
        return {"ok": True, "scene_index": idx, "name": name}

    if action == "delete_scene":
        sc, err = _scene(p)
        if err:
            return err
        s["scenes"].remove(sc)
        for i, sc2 in enumerate(s["scenes"]):
            sc2["index"] = i
        return {"ok": True, "message": "Scene deleted"}

    if action == "rename_scene":
        sc, err = _scene(p)
        if err:
            return err
        sc["name"] = p.get("name", sc["name"])
        return {"ok": True, "name": sc["name"]}

    if action == "get_scene_info":
        sc, err = _scene(p)
        if err:
            return err
        return {"ok": True, **sc}

    if action == "launch_scene":
        _, err = _scene(p)
        if err:
            return err
        s["is_playing"] = True
        return {"ok": True, "message": "Scene launched"}

    # ── Clips ──────────────────────────────────────────────────────────────────
    if action == "create_midi_clip":
        ti = p.get("track_index", 0)
        ci = p.get("clip_index", p.get("scene_index", 0))
        length = float(p.get("length", 4.0))
        s["clips"][f"{ti},{ci}"] = {
            "name": "MIDI Clip",
            "length": length,
            "looping": False,
            "muted": False,
        }
        return {"ok": True, "length": length}

    if action == "get_clip_info":
        ti = p.get("track_index", 0)
        ci = p.get("clip_index", p.get("scene_index", 0))
        clip = s["clips"].get(f"{ti},{ci}")
        if clip is None:
            return {"ok": False, "error": "No clip at this slot"}
        return {"ok": True, **clip}

    if action == "set_clip_name":
        ti = p.get("track_index", 0)
        ci = p.get("clip_index", p.get("scene_index", 0))
        key = f"{ti},{ci}"
        if key not in s["clips"]:
            return {"ok": False, "error": "No clip at this slot"}
        s["clips"][key]["name"] = p.get("name", "")
        return {"ok": True, "name": s["clips"][key]["name"]}

    if action == "delete_clip":
        ti = p.get("track_index", 0)
        ci = p.get("clip_index", p.get("scene_index", 0))
        s["clips"].pop(f"{ti},{ci}", None)
        return {"ok": True, "message": "Clip deleted"}

    if action == "add_notes":
        return {"ok": True, "message": "Notes added (mock — notes not stored)"}

    if action == "get_clip_notes":
        return {"ok": True, "notes": [], "count": 0}

    if action in ("launch_clip", "stop_clip", "stop_all_clips"):
        return {"ok": True, "message": f"{action} (mock)"}

    # ── Fallback ───────────────────────────────────────────────────────────────
    return {"ok": False, "error": f"Action '{action}' not implemented in mock server"}


# ── TCP server ─────────────────────────────────────────────────────────────────


def _handle_client(conn, addr):
    try:
        buf = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    command = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError as e:
                    response = {"ok": False, "error": "Invalid JSON: " + str(e)}
                else:
                    response = _dispatch(command)
                conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
    except Exception:
        pass
    finally:
        conn.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((HOST, PORT))
    except OSError as e:
        print(f"Error: cannot bind to {HOST}:{PORT} — {e}")
        print("Is the real Ableton Remote Script (or another mock) already running?")
        sys.exit(1)

    srv.listen(5)
    print(f"ClaudeMCP mock server listening on {HOST}:{PORT}")
    print(
        "Initial state: {} tracks, {} scenes, {} clips".format(
            len(_state["tracks"]), len(_state["scenes"]), len(_state["clips"])
        )
    )
    print("Stop with Ctrl+C\n")

    try:
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=_handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nMock server stopped.")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
