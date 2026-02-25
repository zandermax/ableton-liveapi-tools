#!/usr/bin/env python3
"""
Web dashboard bridge for ClaudeMCP Remote Script.

Serves index.html and proxies WebSocket messages to the Ableton TCP socket
on 127.0.0.1:9004.

Usage:
    pip install -r requirements.txt
    uvicorn server:app --port 8080
    # then open http://localhost:8080 in a browser
"""

import asyncio
import json
import socket
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

ABLETON_HOST = "127.0.0.1"
ABLETON_PORT = 9004
ABLETON_TIMEOUT = 5.0

app = FastAPI(title="ClaudeMCP Web Dashboard")

_html_path = Path(__file__).parent / "index.html"


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return _html_path.read_text(encoding="utf-8")


def _send_to_ableton(command: dict) -> dict:
    """
    Open a TCP connection to Ableton, send one JSON command, return the response.
    Runs in a thread pool executor so it does not block the event loop.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(ABLETON_TIMEOUT)
        sock.connect((ABLETON_HOST, ABLETON_PORT))

        message = json.dumps(command) + "\n"
        sock.sendall(message.encode("utf-8"))

        response = b""
        while b"\n" not in response:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        sock.close()

        if response:
            return json.loads(response.decode("utf-8"))
        return {"ok": False, "error": "Empty response from Ableton"}

    except socket.timeout:
        return {"ok": False, "error": "Connection timed out — is Ableton running?"}
    except ConnectionRefusedError:
        return {"ok": False, "error": "Connection refused — is ClaudeMCP Remote Script loaded?"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_event_loop()
    try:
        while True:
            raw = await websocket.receive_text()

            try:
                command = json.loads(raw)
            except json.JSONDecodeError as e:
                await websocket.send_text(
                    json.dumps({"ok": False, "error": "Invalid JSON: " + str(e)})
                )
                continue

            # Proxy to Ableton in the thread pool so the event loop stays free
            response = await loop.run_in_executor(None, _send_to_ableton, command)
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        pass
