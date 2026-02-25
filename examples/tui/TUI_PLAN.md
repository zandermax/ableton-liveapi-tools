# TUI Dashboard — Vision & Iteration Plan

## Goal

A terminal-based interactive dashboard for ALiveMCP that lets you control
Ableton Live, inspect session state, and test any of the 220 tools — all from
the terminal, without a browser or build step.

Built with [Textual](https://github.com/Textualize/textual) (`pip install textual`).
Single entry point: `examples/tui/tui_dashboard.py`.

This is NOT meant to replicate Ableton's UI. It is a power-user tool for
developers, testers, and live coders who want rapid command access and a
readable response log alongside a minimal control surface.

---

## Iteration 1 — Minimal (First Ship)

The first iteration ships the skeleton: connection management, a readable log,
and keyboard-driven command input. No panels, no polling.

### Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  STATUS BAR  [● Connected]  BPM: 120.0  Playing: No  Time: 1.1.1    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  OUTPUT LOG                                                            │
│  (scrollable, color-coded ok / error)                                  │
│                                                                        │
│                                                                        │
│                                                                        │
├──────────────────────────────────────────────────────────────────────┤
│  > {"action": "ping"}                                          [Send] │
└──────────────────────────────────────────────────────────────────────┘
```

### Components

**Status bar (top)**
- Connection indicator: green dot + "Connected" or red dot + "Disconnected"
- BPM (updated from any response that includes `tempo` or `bpm`)
- Playback state: "Playing" / "Stopped"
- Current song time (updated on demand, not polled)

**Output log (center)**
- Scrollable log of all sent commands and received responses
- Outgoing lines in dim blue `→ {"action": "ping"}`
- `ok: true` responses in green `← {"ok": true, "message": "pong"}`
- `ok: false` responses in red `← {"ok": false, "error": "..."}`
- Timestamps on each line

**Command input (bottom)**
- Single-line text input, always focused unless a modal is open
- Enter to send
- Up / Down arrow keys to navigate history (last 50 commands)
- Accepts full JSON or bare action name shorthand (e.g. `ping`)

**Keyboard shortcuts (global)**

| Key | Action |
|-----|--------|
| `p` | `start_playback` |
| `s` | `stop_playback` |
| `r` | `start_recording` |
| `q` / `ctrl+c` | Quit |
| `/` | Focus command input |
| `ctrl+l` | Clear log |
| `F5` | Refresh session info (`get_session_info`) |

### Tech notes
- Single file: `tui_dashboard.py`
- `requirements.txt`: `textual>=0.55`
- TCP connection managed as a background asyncio task; reconnects every 3 s on failure
- No polling — status bar updates only when a response arrives

---

## Iteration 2 — Mini Control Panel

Adds a left sidebar with a minimal mixer strip so common per-track actions
don't require typing full JSON.

### Layout

```
┌─ STATUS BAR ─────────────────────────────────────────────────────────┐
├─ TRACKS (left, 30%) ───┬─ OUTPUT LOG (right, 70%) ──────────────────┤
│  0  Kick    ████░ M S  │  ...                                         │
│  1  Bass    ███░░ M S  │                                              │
│  2  Lead    █████ M S  │                                              │
│  3  FX      ██░░░ M S  │                                              │
├────────────────────────┴──────────────────────────────────────────────┤
│  > command input                                               [Send] │
└──────────────────────────────────────────────────────────────────────┘
```

### New elements
- **Track list**: populated by `get_session_info` on connect; shows index, name,
  volume bar, Mute (M) and Solo (S) toggles
- Track list refreshes on `F5`; no continuous polling
- Clicking a track row focuses it; `m` mutes, `S` solos the selected track
- Volume bar is display-only in this iteration (adjustable in iteration 3)

---

## Iteration 3 — Full TUI

Adds a session grid (clip launcher view), a device inspector, and optional
polling for live status updates.

### Layout

```
┌─ STATUS BAR ─────────────────────────────────────────────────────────┐
├─ TRACKS (left, 25%) ──┬─ SESSION GRID (center, 45%) ─┬─ DEVICES ────┤
│  track strips         │  tracks × scenes clip grid    │  device list │
│  vol / pan / m / s    │  launch / stop per cell        │  + params   │
├───────────────────────┴──────────────────────────────┴───────────────┤
│  > command input                                               [Send] │
└──────────────────────────────────────────────────────────────────────┘
```

### New elements
- **Session grid**: each cell shows clip name (or empty slot); Enter launches,
  Delete stops; color reflects clip state (playing / triggered / stopped)
- **Device inspector**: shows devices on the selected track; expand to see
  parameters and current values
- **Optional polling**: `ctrl+p` toggles a 1 Hz poll of `get_session_info` and
  `get_current_time`; poll interval configurable as a CLI flag (`--poll-ms`)

---

## Non-goals

- Not a replacement for Ableton's own Session View
- No audio playback or waveform rendering
- No MIDI keyboard input capture (the terminal cannot reliably capture raw MIDI)
- No real-time meter/level display (Ableton's LiveAPI does not expose audio meters)
- Polling is opt-in only — the TUI must be usable offline / without a live set loaded
