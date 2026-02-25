"""
Shared constants for the ALiveMCP Remote Script.

Centralising these here means socket_server.py and __init__.py stay in sync
without magic numbers scattered across files.
"""

PORT = 9004

# How long a client socket waits before timing out an idle connection.
SOCKET_TIMEOUT_SECONDS = 30.0

# How long a socket thread blocks waiting for the main thread to process a command.
# Must be less than SOCKET_TIMEOUT_SECONDS so the socket stays alive during the wait.
RESPONSE_TIMEOUT_SECONDS = 25.0

# Maximum commands processed per update_display() tick (~60 Hz).
# Keeping this low prevents one busy client from starving the main thread.
MAX_COMMANDS_PER_TICK = 5
