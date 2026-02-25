"""
ClaudeMCP Remote Script - Thread-Safe Socket Server for LiveAPI Communication
Ableton Live Remote Script that receives commands via TCP port 9004
and executes LiveAPI operations in the main thread using a queue-based approach.

Author: Claude Code
License: MIT
"""

__version__ = "1.1.2"

import socket  # noqa: F401 - re-exported so tests can patch ClaudeMCP_Remote.socket
import threading
import traceback

import Live

try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3

from .liveapi_tools import LiveAPITools
from .socket_server import SocketServerMixin


class ClaudeMCP(SocketServerMixin):
    """
    Main Remote Script class loaded by Ableton Live

    Uses a queue-based approach to ensure thread safety:
    1. Socket threads receive commands and add them to command_queue
    2. update_display() (main thread) processes commands from queue
    3. Results are put in response_queue for socket threads to retrieve
    """

    def __init__(self, c_instance):
        """
        Initialize the Remote Script

        Args:
            c_instance: The ControlSurface instance provided by Live
        """
        self.c_instance = c_instance
        self.song = c_instance.song()

        self.tools = LiveAPITools(self.song, self.c_instance)

        self.command_queue = queue.Queue()
        self.response_queues = {}
        self.request_counter = 0
        self.request_lock = threading.Lock()

        self.socket_server = None
        self.socket_thread = None
        self.running = False

        self.start_socket_server()

        self.log("ClaudeMCP Remote Script initialized (Queue-based, Thread-Safe)")
        self.log("Socket server listening on port 9004")

    def log(self, message):
        """Log message to Ableton's Log.txt"""
        self.c_instance.log_message("[ClaudeMCP] " + str(message))

    def _process_command(self, command):
        """
        Process a JSON command and return JSON response.
        THIS RUNS IN THE MAIN THREAD (called from update_display).

        Uses getattr-based dispatch: action names map directly to method names
        on self.tools, and all remaining command keys are passed as **kwargs.
        """
        try:
            action = command.get("action", "")

            if action == "ping":
                return {
                    "ok": True,
                    "message": "pong (queue-based, thread-safe)",
                    "script": "ClaudeMCP_Remote",
                    "version": __version__,
                }

            if action == "health_check":
                return {
                    "ok": True,
                    "message": "ClaudeMCP Remote Script running (thread-safe)",
                    "version": __version__,
                    "tool_count": len(self.tools.get_available_tools()),
                    "ableton_version": str(Live.Application.get_application().get_major_version()),
                    "queue_size": self.command_queue.qsize(),
                }

            method = getattr(self.tools, action, None)
            if method is None:
                return {
                    "ok": False,
                    "error": "Unknown action: " + action,
                    "available_actions": self.tools.get_available_tools(),
                }

            params = {k: v for k, v in command.items() if k != "action"}
            return method(**params)

        except Exception as e:
            self.log("ERROR processing command: " + str(e))
            self.log(traceback.format_exc())
            return {"ok": False, "error": str(e), "traceback": traceback.format_exc()}

    def update_display(self):
        """
        Called by Ableton Live on each tick to update displays.
        RUNS IN MAIN THREAD - safe to call LiveAPI here.

        Processes commands from the queue to ensure thread safety.
        """
        commands_processed = 0
        max_commands_per_tick = 5

        while commands_processed < max_commands_per_tick:
            try:
                request_id, command = self.command_queue.get_nowait()
                response = self._process_command(command)

                if request_id in self.response_queues:
                    self.response_queues[request_id].put(response)

                commands_processed += 1

            except queue.Empty:
                break
            except Exception as e:
                self.log("Error in update_display: " + str(e))
                break

    def connect_script_instances(self, instanciated_scripts):
        """Required by Ableton's Remote Script API"""
        pass

    def can_lock_to_devices(self):
        """Required by Ableton's Remote Script API"""
        return False

    def refresh_state(self):
        """Required by Ableton's Remote Script API"""
        pass

    def build_midi_map(self, midi_map_handle):
        """Required by Ableton's Remote Script API"""
        pass

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log("Shutting down ClaudeMCP Remote Script...")
        self.running = False

        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception:
                pass

        self.log("ClaudeMCP Remote Script stopped")


# Required entry points for Ableton
def create_instance(c_instance):
    """Factory function called by Live to create the script instance"""
    return ClaudeMCP(c_instance)
