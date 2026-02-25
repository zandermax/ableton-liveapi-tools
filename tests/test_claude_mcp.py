"""
Tests for ClaudeMCP: socket server lifecycle, command dispatch, queue processing,
lifecycle stubs, and the create_instance factory.
"""

import json
import queue
from unittest.mock import MagicMock, patch

import pytest

from ClaudeMCP_Remote import ClaudeMCP, __version__, create_instance

# ---------------------------------------------------------------------------
# Fixture: a ClaudeMCP instance with socket and thread mocked out
# ---------------------------------------------------------------------------


@pytest.fixture
def mcp(c_instance):
    with patch("ClaudeMCP_Remote.socket.socket"), patch("ClaudeMCP_Remote.threading.Thread"):
        instance = ClaudeMCP(c_instance)
    return instance


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------


def test_init_sets_c_instance_and_song(c_instance):
    with patch("ClaudeMCP_Remote.socket.socket"), patch("ClaudeMCP_Remote.threading.Thread"):
        instance = ClaudeMCP(c_instance)
    assert instance.c_instance is c_instance
    assert instance.song is c_instance.song()


def test_init_creates_tools(mcp):
    from ClaudeMCP_Remote.liveapi_tools import LiveAPITools

    assert isinstance(mcp.tools, LiveAPITools)


def test_init_creates_queues(mcp):
    assert isinstance(mcp.command_queue, queue.Queue)
    assert isinstance(mcp.response_queues, dict)
    assert mcp.request_counter == 0


def test_init_starts_socket_server(c_instance):
    with patch("ClaudeMCP_Remote.socket.socket") as mock_sock_cls, patch(
        "ClaudeMCP_Remote.threading.Thread"
    ) as mock_thread_cls:
        ClaudeMCP(c_instance)
    mock_sock_cls.assert_called_once()
    mock_thread_cls.assert_called_once()


def test_start_socket_server_logs_error_on_exception(c_instance):
    """If socket binding fails the error is logged, not raised."""
    with patch("ClaudeMCP_Remote.socket.socket") as mock_sock_cls, patch(
        "ClaudeMCP_Remote.threading.Thread"
    ):
        mock_sock_cls.return_value.bind.side_effect = OSError("address in use")
        instance = ClaudeMCP(c_instance)
    # The error should have been logged; the script still initialises.
    assert instance is not None
    c_instance.log_message.assert_called()


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------


def test_log_prefixes_message(mcp, c_instance):
    mcp.log("test message")
    c_instance.log_message.assert_called_with("[ClaudeMCP] test message")


def test_log_converts_non_string(mcp, c_instance):
    mcp.log(42)
    c_instance.log_message.assert_called_with("[ClaudeMCP] 42")


# ---------------------------------------------------------------------------
# _process_command - built-in actions
# ---------------------------------------------------------------------------


def test_process_command_ping(mcp):
    result = mcp._process_command({"action": "ping"})
    assert result["ok"] is True
    assert result["message"] == "pong (queue-based, thread-safe)"
    assert result["script"] == "ClaudeMCP_Remote"
    assert result["version"] == __version__


def test_process_command_health_check(mcp):
    result = mcp._process_command({"action": "health_check"})
    assert result["ok"] is True
    assert result["version"] == __version__
    assert "tool_count" in result
    assert "queue_size" in result
    assert "ableton_version" in result


def test_process_command_unknown_action(mcp):
    result = mcp._process_command({"action": "nonexistent_action"})
    assert result["ok"] is False
    assert "Unknown action" in result["error"]
    assert isinstance(result["available_actions"], list)


def test_process_command_dispatches_to_tools(mcp):
    mcp.tools.ping = MagicMock(return_value={"ok": True, "custom": "value"})
    result = mcp._process_command({"action": "ping"})
    # ping is handled before getattr dispatch - ensure built-in takes priority
    assert result["ok"] is True

    # Test a real tool dispatch
    mcp.tools.start_playback = MagicMock(return_value={"ok": True, "dispatched": True})
    result = mcp._process_command({"action": "start_playback"})
    mcp.tools.start_playback.assert_called_once_with()
    assert result["dispatched"] is True


def test_process_command_passes_params_to_tool(mcp):
    mcp.tools.set_tempo = MagicMock(return_value={"ok": True})
    mcp._process_command({"action": "set_tempo", "bpm": 120})
    mcp.tools.set_tempo.assert_called_once_with(bpm=120)


def test_process_command_exception_returns_error_with_traceback(mcp):
    mcp.tools.start_playback = MagicMock(side_effect=RuntimeError("boom"))
    result = mcp._process_command({"action": "start_playback"})
    assert result["ok"] is False
    assert "boom" in result["error"]
    assert "traceback" in result


# ---------------------------------------------------------------------------
# update_display - queue processing
# ---------------------------------------------------------------------------


def _put_command(mcp, request_id, command):
    """Helper: register a response queue and enqueue a command."""
    mcp.response_queues[request_id] = queue.Queue()
    mcp.command_queue.put((request_id, command))


def test_update_display_empty_queue_is_noop(mcp):
    mcp.update_display()  # should not raise


def test_update_display_processes_single_command(mcp):
    _put_command(mcp, 0, {"action": "ping"})
    mcp.update_display()
    response = mcp.response_queues[0].get_nowait()
    assert response["ok"] is True


def test_update_display_puts_response_in_correct_queue(mcp):
    _put_command(mcp, 7, {"action": "ping"})
    _put_command(mcp, 8, {"action": "ping"})
    mcp.update_display()
    assert not mcp.response_queues[7].empty()
    assert not mcp.response_queues[8].empty()


def test_update_display_caps_at_five_commands_per_tick(mcp):
    for i in range(6):
        _put_command(mcp, i, {"action": "ping"})
    mcp.update_display()
    assert mcp.command_queue.qsize() == 1


def test_update_display_skips_missing_response_queue(mcp):
    """Command whose response queue was already cleaned up should not raise."""
    mcp.command_queue.put((999, {"action": "ping"}))
    # No entry in response_queues for id 999 - should not blow up
    mcp.update_display()


def test_update_display_handles_exception_in_processing(mcp):
    """An exception during command processing should be caught gracefully."""
    _put_command(mcp, 0, {"action": "ping"})
    mcp._process_command = MagicMock(side_effect=RuntimeError("unexpected"))
    mcp.update_display()  # should not raise


# ---------------------------------------------------------------------------
# Ableton lifecycle stubs
# ---------------------------------------------------------------------------


def test_connect_script_instances_returns_none(mcp):
    assert mcp.connect_script_instances([]) is None


def test_can_lock_to_devices_returns_false(mcp):
    assert mcp.can_lock_to_devices() is False


def test_refresh_state_returns_none(mcp):
    assert mcp.refresh_state() is None


def test_build_midi_map_returns_none(mcp):
    assert mcp.build_midi_map(MagicMock()) is None


# ---------------------------------------------------------------------------
# disconnect
# ---------------------------------------------------------------------------


def test_disconnect_sets_running_false(mcp):
    assert mcp.running is True
    mcp.disconnect()
    assert mcp.running is False


def test_disconnect_closes_socket(mcp):
    mock_server = MagicMock()
    mcp.socket_server = mock_server
    mcp.disconnect()
    mock_server.close.assert_called_once()


def test_disconnect_handles_socket_close_error(mcp):
    mock_server = MagicMock()
    mock_server.close.side_effect = OSError("already closed")
    mcp.socket_server = mock_server
    mcp.disconnect()  # should not raise
    assert mcp.running is False


# ---------------------------------------------------------------------------
# create_instance factory
# ---------------------------------------------------------------------------


def test_create_instance_returns_claude_mcp(c_instance):
    with patch("ClaudeMCP_Remote.socket.socket"), patch("ClaudeMCP_Remote.threading.Thread"):
        instance = create_instance(c_instance)
    assert isinstance(instance, ClaudeMCP)


# ---------------------------------------------------------------------------
# _socket_listener
# ---------------------------------------------------------------------------


def test_socket_listener_exits_immediately_when_not_running(mcp):
    mcp.running = False
    mcp.socket_server = MagicMock()
    mcp._socket_listener()
    mcp.socket_server.accept.assert_not_called()


def test_socket_listener_spawns_thread_per_connection(mcp):
    mock_client = MagicMock()
    call_count = 0

    def accept_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return mock_client, ("127.0.0.1", 12345)
        mcp.running = False
        raise OSError("server closed")

    mcp.socket_server = MagicMock()
    mcp.socket_server.accept.side_effect = accept_side_effect

    with patch("ClaudeMCP_Remote.threading.Thread") as mock_thread_cls:
        mock_thread_cls.return_value = MagicMock()
        mcp._socket_listener()

    mock_thread_cls.assert_called_once()


def test_socket_listener_logs_error_when_running(mcp):
    call_count = 0

    def accept_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("random error")
        mcp.running = False
        raise RuntimeError("stop")

    mcp.socket_server = MagicMock()
    mcp.socket_server.accept.side_effect = accept_side_effect
    mcp._socket_listener()
    mcp.c_instance.log_message.assert_called()


# ---------------------------------------------------------------------------
# _handle_client
# ---------------------------------------------------------------------------


def _make_intercept(mcp):
    """Intercept command_queue.put and immediately fulfil the response queue."""
    original_put = mcp.command_queue.put

    def intercept(item):
        request_id, command = item
        original_put(item)
        response = mcp._process_command(command)
        if request_id in mcp.response_queues:
            mcp.response_queues[request_id].put(response)

    return intercept


def test_handle_client_success(mcp):
    mock_client = MagicMock()
    json_message = json.dumps({"action": "ping"}) + "\n"
    mock_client.recv.side_effect = [json_message.encode(), b""]
    mcp.command_queue.put = _make_intercept(mcp)

    mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is True
    assert response["message"] == "pong (queue-based, thread-safe)"


def test_handle_client_json_parse_error(mcp):
    mock_client = MagicMock()
    mock_client.recv.side_effect = [b"not valid json\n", b""]

    mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is False


def test_handle_client_response_timeout(mcp):
    """When no response is placed in the queue within the timeout, a timeout error is sent."""
    mock_client = MagicMock()
    json_message = json.dumps({"action": "ping"}) + "\n"
    mock_client.recv.side_effect = [json_message.encode(), b""]

    # Patch the response queue's get() to immediately raise queue.Empty
    with patch("ClaudeMCP_Remote.queue.Queue.get", side_effect=queue.Empty):
        mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is False
    assert "timeout" in response["error"].lower()


def test_handle_client_closes_socket_on_exit(mcp):
    mock_client = MagicMock()
    mock_client.recv.return_value = b""
    mcp._handle_client(mock_client)
    mock_client.close.assert_called_once()


def test_handle_client_socket_timeout_continues(mcp):
    """A socket.timeout should cause the loop to continue, not exit."""
    import socket as socket_mod

    mock_client = MagicMock()
    mock_client.recv.side_effect = [socket_mod.timeout, b""]
    # Should not raise; just finish cleanly
    mcp._handle_client(mock_client)


def test_handle_client_exits_when_not_running(mcp):
    mock_client = MagicMock()
    mcp.running = False
    mock_client.recv.return_value = b"irrelevant"
    mcp._handle_client(mock_client)
    mock_client.close.assert_called_once()


def test_handle_client_multiple_messages_in_buffer(mcp):
    """Two newline-separated messages in a single recv call are both processed."""
    mock_client = MagicMock()
    msg1 = json.dumps({"action": "ping"})
    msg2 = json.dumps({"action": "ping"})
    payload = (msg1 + "\n" + msg2 + "\n").encode()
    mock_client.recv.side_effect = [payload, b""]
    mcp.command_queue.put = _make_intercept(mcp)

    mcp._handle_client(mock_client)

    assert mock_client.sendall.call_count == 2
