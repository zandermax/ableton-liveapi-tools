"""
TCP socket server mixin for receiving and dispatching commands from clients.
"""

import json
import socket
import threading
import traceback

try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3

from .constants import PORT, RESPONSE_TIMEOUT_SECONDS, SOCKET_TIMEOUT_SECONDS


class SocketServerMixin:
    """
    Manages the TCP socket server lifecycle and per-client I/O.
    Subclasses must provide: self.running, self.command_queue,
    self.response_queues, self.request_counter, self.request_lock, self.log().
    """

    def start_socket_server(self):
        """Start the socket server in a background thread"""
        try:
            self.running = True
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_server.bind(("127.0.0.1", PORT))
            self.socket_server.listen(5)

            self.socket_thread = threading.Thread(target=self._socket_listener)
            self.socket_thread.daemon = True
            self.socket_thread.start()

            self.log("Socket server started successfully on port " + str(PORT))
        except Exception as e:
            self.log("ERROR starting socket server: " + str(e))
            self.log(traceback.format_exc())

    def _socket_listener(self):
        """Background thread that listens for client connections"""
        while self.running:
            try:
                client_socket, address = self.socket_server.accept()
                self.log("Client connected from " + str(address))

                client_thread = threading.Thread(
                    target=self._handle_client, args=(client_socket,), daemon=True
                )
                client_thread.start()

            except Exception as e:
                if self.running:
                    self.log("Socket listener error: " + str(e))

    def _handle_client(self, client_socket):
        """
        Handle commands from a connected client (runs in socket thread).

        Receives commands from the socket, puts them in command_queue,
        waits for a response from response_queue, and sends it back.
        """
        buffer = ""

        try:
            client_socket.settimeout(SOCKET_TIMEOUT_SECONDS)

            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    buffer += data.decode("utf-8")

                    while "\n" in buffer:
                        message, buffer = buffer.split("\n", 1)
                        message = message.strip()

                        if message:
                            with self.request_lock:
                                request_id = self.request_counter
                                self.request_counter += 1
                                self.response_queues[request_id] = queue.Queue()

                            try:
                                command = json.loads(message)
                                self.command_queue.put((request_id, command))

                                try:
                                    response = self.response_queues[request_id].get(
                                        timeout=RESPONSE_TIMEOUT_SECONDS
                                    )
                                except queue.Empty:
                                    response = {
                                        "ok": False,
                                        "error": "Command processing timeout - main thread may be busy",
                                    }

                                with self.request_lock:
                                    if request_id in self.response_queues:
                                        del self.response_queues[request_id]

                                client_socket.sendall((json.dumps(response) + "\n").encode("utf-8"))

                            except Exception as e:
                                error_resp = {"ok": False, "error": str(e)}
                                try:
                                    client_socket.sendall(
                                        (json.dumps(error_resp) + "\n").encode("utf-8")
                                    )
                                except Exception:
                                    pass

                except socket.timeout:
                    continue
                except Exception as e:
                    self.log("Receive error: " + str(e))
                    break

        except Exception as e:
            self.log("Client handler error: " + str(e))
        finally:
            try:
                client_socket.close()
            except Exception:
                pass
