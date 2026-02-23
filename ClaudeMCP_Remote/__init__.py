"""
ClaudeMCP Remote Script - Thread-Safe Socket Server for LiveAPI Communication
Ableton Live Remote Script that receives commands via TCP port 9004
and executes LiveAPI operations in the main thread using a queue-based approach.

Author: Claude Code
License: MIT
"""

__version__ = "1.1.0"

import Live
import socket
import threading
import json
import traceback
try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3
from .liveapi_tools import LiveAPITools


class ClaudeMCP:
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

        # Initialize LiveAPI tools
        self.tools = LiveAPITools(self.song, self.c_instance)

        # Thread-safe queues for command processing
        self.command_queue = queue.Queue()  # Commands from socket threads
        self.response_queues = {}  # {request_id: Queue} for responses
        self.request_counter = 0
        self.request_lock = threading.Lock()

        # Socket server state
        self.socket_server = None
        self.socket_thread = None
        self.running = False

        # Start socket server
        self.start_socket_server()

        self.log("ClaudeMCP Remote Script initialized (Queue-based, Thread-Safe)")
        self.log("Socket server listening on port 9004")

    def log(self, message):
        """Log message to Ableton's Log.txt"""
        self.c_instance.log_message("[ClaudeMCP] " + str(message))

    def start_socket_server(self):
        """Start the socket server in a background thread"""
        try:
            self.running = True
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_server.bind(('127.0.0.1', 9004))
            self.socket_server.listen(5)

            # Start listening thread
            self.socket_thread = threading.Thread(target=self._socket_listener)
            self.socket_thread.daemon = True
            self.socket_thread.start()

            self.log("Socket server started successfully on port 9004")
        except Exception as e:
            self.log("ERROR starting socket server: " + str(e))
            self.log(traceback.format_exc())

    def _socket_listener(self):
        """Background thread that listens for client connections"""
        while self.running:
            try:
                client_socket, address = self.socket_server.accept()
                self.log("Client connected from " + str(address))

                # Spawn a new thread for each client
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()

            except Exception as e:
                if self.running:
                    self.log("Socket listener error: " + str(e))

    def _handle_client(self, client_socket):
        """
        Handle commands from a connected client (runs in socket thread)

        This method DOES NOT call LiveAPI directly - instead it:
        1. Receives commands from socket
        2. Puts them in command_queue
        3. Waits for response from response_queue
        4. Sends response back to socket
        """
        buffer = ""

        try:
            client_socket.settimeout(30.0)  # Increased timeout

            while self.running:
                try:
                    # Read data from socket
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    # Decode data
                    decoded = data.decode('utf-8')
                    buffer += decoded

                    # Process complete messages (terminated by newline)
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        message = message.strip()

                        if message:
                            # Generate unique request ID
                            with self.request_lock:
                                request_id = self.request_counter
                                self.request_counter += 1
                                # Create response queue for this request
                                self.response_queues[request_id] = queue.Queue()

                            try:
                                # Parse command
                                command = json.loads(message)

                                # Put command in queue for main thread to process
                                self.command_queue.put((request_id, command))

                                # Wait for response from main thread (with timeout)
                                try:
                                    response = self.response_queues[request_id].get(timeout=25.0)
                                except queue.Empty:
                                    response = {
                                        "ok": False,
                                        "error": "Command processing timeout - main thread may be busy"
                                    }

                                # Clean up response queue
                                with self.request_lock:
                                    if request_id in self.response_queues:
                                        del self.response_queues[request_id]

                                # Send response back to client
                                response_str = json.dumps(response) + '\n'
                                client_socket.sendall(response_str.encode('utf-8'))

                            except Exception as e:
                                error_resp = {"ok": False, "error": str(e)}
                                try:
                                    client_socket.sendall((json.dumps(error_resp) + '\n').encode('utf-8'))
                                except:
                                    pass

                except socket.timeout:
                    continue  # Client might be idle
                except Exception as e:
                    self.log("Receive error: " + str(e))
                    break

        except Exception as e:
            self.log("Client handler error: " + str(e))
        finally:
            try:
                client_socket.close()
            except:
                pass

    def _process_command(self, command):
        """
        Process a JSON command and return JSON response.
        THIS RUNS IN THE MAIN THREAD (called from update_display).

        Uses getattr-based dispatch: action names map directly to method names
        on self.tools, and all remaining command keys are passed as **kwargs.
        """
        try:
            action = command.get('action', '')

            if action == 'ping':
                return {"ok": True, "message": "pong (queue-based, thread-safe)", "script": "ClaudeMCP_Remote", "version": __version__}

            if action == 'health_check':
                return {
                    "ok": True,
                    "message": "ClaudeMCP Remote Script running (thread-safe)",
                    "version": __version__,
                    "tool_count": len(self.tools.get_available_tools()),
                    "ableton_version": str(Live.Application.get_application().get_major_version()),
                    "queue_size": self.command_queue.qsize()
                }

            method = getattr(self.tools, action, None)
            if method is None:
                return {
                    "ok": False,
                    "error": "Unknown action: " + action,
                    "available_actions": self.tools.get_available_tools()
                }

            params = {}
            for k, v in command.items():
                if k != 'action':
                    params[k] = v
            return method(**params)

        except Exception as e:
            self.log("ERROR processing command: " + str(e))
            self.log(traceback.format_exc())
            return {
                "ok": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def update_display(self):
        """
        Called by Ableton Live on each tick to update displays
        RUNS IN MAIN THREAD - safe to call LiveAPI here

        We process commands from the queue here to ensure thread safety
        """
        # Process up to 5 commands per tick to avoid blocking the UI
        commands_processed = 0
        max_commands_per_tick = 5

        while commands_processed < max_commands_per_tick:
            try:
                # Try to get a command from queue (non-blocking)
                request_id, command = self.command_queue.get_nowait()

                # Process command in main thread (safe for LiveAPI)
                response = self._process_command(command)

                # Put response in the request's response queue
                if request_id in self.response_queues:
                    self.response_queues[request_id].put(response)

                commands_processed += 1

            except queue.Empty:
                # No more commands in queue
                break
            except Exception as e:
                self.log("Error in update_display: " + str(e))
                break

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by Live to connect this script with other scripts
        Required by Ableton's Remote Script API
        """
        pass

    def can_lock_to_devices(self):
        """
        Called by Live to check if this script can lock to devices
        Required by Ableton's Remote Script API
        """
        return False

    def refresh_state(self):
        """
        Called by Live to refresh the script's state
        Required by Ableton's Remote Script API
        """
        pass

    def build_midi_map(self, midi_map_handle):
        """
        Called by Live to build MIDI mapping
        Required by Ableton's Remote Script API
        """
        pass

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log("Shutting down ClaudeMCP Remote Script...")

        # Stop socket server
        self.running = False

        if self.socket_server:
            try:
                self.socket_server.close()
            except:
                pass

        self.log("ClaudeMCP Remote Script stopped")


# Required entry points for Ableton
def create_instance(c_instance):
    """Factory function called by Live to create the script instance"""
    return ClaudeMCP(c_instance)
