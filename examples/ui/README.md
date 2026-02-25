# ClaudeMCP Web Dashboard

A browser-based dashboard for controlling Ableton Live via the ClaudeMCP Remote Script.

## Architecture

```
Browser (index.html)
    ↕  WebSocket  ws://localhost:8080/ws
Python bridge (server.py)
    ↕  TCP JSON  127.0.0.1:9004
Ableton Live + ClaudeMCP Remote Script
```

The bridge accepts a persistent WebSocket connection from the browser and
proxies each JSON command to the Ableton TCP socket, returning the response.

## Requirements

- Ableton Live with the ClaudeMCP Remote Script installed and loaded
- Python 3.8+

## Quick start

```bash
# From this directory — create a venv and install dependencies:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the bridge:
uvicorn server:app --port 8080

# Then open:
open http://localhost:8080
```

## Panels

**Transport bar** — Play, Stop, Record buttons; BPM display with ± adjustment.

**Session info** — Shows BPM, time signature, track count, scene count, and
playback state. Refreshes automatically on connect and via the Refresh button.

**Command console** — Send any raw JSON command to the Remote Script and see
color-coded responses. Supports:
- Full JSON: `{"action": "set_tempo", "bpm": 130}`
- Bare action name shorthand: `ping`
- Up/Down arrow keys to cycle through the last 50 commands
