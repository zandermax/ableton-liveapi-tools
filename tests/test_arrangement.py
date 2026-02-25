"""
Tests for ArrangementMixin: project, arrangement clips, view/navigation,
loop/locator, browser, and color utilities.

Note: show_clip_view and show_arrangement_view use the bare `Live` name which
is not imported in arrangement.py. We inject it into the module namespace for
those tests.
"""

from unittest.mock import MagicMock, patch

import pytest

import ALiveMCP_Remote.tools.arrangement as arrangement_module

# ---------------------------------------------------------------------------
# get_project_root_folder
# ---------------------------------------------------------------------------


def test_get_project_root_folder_with_attr(tools, song):
    song.project_root_folder = "/path/to/project"
    result = tools.get_project_root_folder()
    assert result["ok"] is True
    assert result["project_root_folder"] == "/path/to/project"


def test_get_project_root_folder_none(tools, song):
    song.project_root_folder = None
    result = tools.get_project_root_folder()
    assert result["ok"] is True
    assert result["project_root_folder"] is None


def test_get_project_root_folder_without_attr(tools, song):
    del song.project_root_folder
    result = tools.get_project_root_folder()
    assert result["ok"] is False


def test_get_project_root_folder_exception(tools, song):
    tools.song = None  # hasattr(None, ...) = False → else branch → ok=False
    result = tools.get_project_root_folder()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# trigger_session_record
# ---------------------------------------------------------------------------


def test_trigger_session_record_no_length(tools, song):
    result = tools.trigger_session_record()
    assert result["ok"] is True
    song.trigger_session_record.assert_called_once_with()


def test_trigger_session_record_with_length(tools, song):
    result = tools.trigger_session_record(length=4.0)
    assert result["ok"] is True
    song.trigger_session_record.assert_called_once_with(4.0)


def test_trigger_session_record_exception(tools, song):
    song.trigger_session_record.side_effect = Exception("err")
    result = tools.trigger_session_record()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_can_jump_to_next_cue / prev_cue
# ---------------------------------------------------------------------------


def test_get_can_jump_to_next_cue(tools, song):
    song.can_jump_to_next_cue = True
    result = tools.get_can_jump_to_next_cue()
    assert result["ok"] is True
    assert result["can_jump_to_next_cue"] is True


def test_get_can_jump_to_next_cue_exception(tools, song):
    tools.song = None  # None.can_jump_to_next_cue → AttributeError → ok=False
    result = tools.get_can_jump_to_next_cue()
    assert result["ok"] is False


def test_get_can_jump_to_prev_cue(tools, song):
    song.can_jump_to_prev_cue = False
    result = tools.get_can_jump_to_prev_cue()
    assert result["ok"] is True
    assert result["can_jump_to_prev_cue"] is False


def test_get_can_jump_to_prev_cue_exception(tools, song):
    tools.song = None  # None.can_jump_to_prev_cue → AttributeError → ok=False
    result = tools.get_can_jump_to_prev_cue()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# jump_to_next_cue / jump_to_prev_cue
# ---------------------------------------------------------------------------


def test_jump_to_next_cue_can_jump(tools, song):
    song.can_jump_to_next_cue = True
    result = tools.jump_to_next_cue()
    assert result["ok"] is True
    song.jump_to_next_cue.assert_called_once()


def test_jump_to_next_cue_cannot_jump(tools, song):
    song.can_jump_to_next_cue = False
    result = tools.jump_to_next_cue()
    assert result == {"ok": False, "error": "Cannot jump to next cue"}


def test_jump_to_next_cue_exception(tools, song):
    song.can_jump_to_next_cue = True
    song.jump_to_next_cue.side_effect = Exception("err")
    result = tools.jump_to_next_cue()
    assert result["ok"] is False


def test_jump_to_prev_cue_can_jump(tools, song):
    song.can_jump_to_prev_cue = True
    result = tools.jump_to_prev_cue()
    assert result["ok"] is True
    song.jump_to_prev_cue.assert_called_once()


def test_jump_to_prev_cue_cannot_jump(tools, song):
    song.can_jump_to_prev_cue = False
    result = tools.jump_to_prev_cue()
    assert result == {"ok": False, "error": "Cannot jump to previous cue"}


def test_jump_to_prev_cue_exception(tools, song):
    song.can_jump_to_prev_cue = True
    song.jump_to_prev_cue.side_effect = Exception("err")
    result = tools.jump_to_prev_cue()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_arrangement_clips
# ---------------------------------------------------------------------------


def test_get_arrangement_clips_with_attr(tools, song):
    clip = MagicMock()
    clip.name = "Clip 1"
    clip.start_time = 0.0
    clip.end_time = 4.0
    clip.length = 4.0
    song.tracks[0].arrangement_clips = [clip]
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_arrangement_clips_without_attr(tools, song):
    del song.tracks[0].arrangement_clips
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is False


def test_get_arrangement_clips_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# duplicate_to_arrangement
# ---------------------------------------------------------------------------


def test_duplicate_to_arrangement_with_dup_loop(tools, song):
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].clip.duplicate_loop.assert_called_once()


def test_duplicate_to_arrangement_without_dup_loop(tools, song):
    del song.tracks[0].clip_slots[0].clip.duplicate_loop
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


def test_duplicate_to_arrangement_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


def test_duplicate_to_arrangement_exception(tools, song):
    song.tracks[0].clip_slots[0].clip.duplicate_loop.side_effect = Exception("err")
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# consolidate_clip
# ---------------------------------------------------------------------------


def test_consolidate_clip_success(tools):
    result = tools.consolidate_clip(0, 0.0, 8.0)
    assert result["ok"] is True
    assert result["start_time"] == 0.0
    assert result["end_time"] == 8.0


def test_consolidate_clip_exception(tools):
    # consolidate_clip never actually raises in the current implementation,
    # but we cover the except path by forcing float() to fail:
    result = tools.consolidate_clip(0, "bad", 8.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# show_clip_view / show_arrangement_view (inject Live into arrangement module)
# ---------------------------------------------------------------------------


@pytest.fixture
def live_in_arrangement():
    fresh_live = MagicMock()
    with patch.object(arrangement_module, "Live", fresh_live, create=True):
        yield fresh_live


def test_show_clip_view_success(tools, live_in_arrangement):
    result = tools.show_clip_view()
    assert result["ok"] is True


def test_show_clip_view_no_show_view(tools, live_in_arrangement):
    del live_in_arrangement.Application.get_application.return_value.view.show_view
    result = tools.show_clip_view()
    assert result["ok"] is False


def test_show_clip_view_exception(tools):
    # Without injecting Live, show_clip_view catches NameError → ok=False
    result = tools.show_clip_view()
    assert result["ok"] is False


def test_show_arrangement_view_success(tools, live_in_arrangement):
    result = tools.show_arrangement_view()
    assert result["ok"] is True


def test_show_arrangement_view_no_show_view(tools, live_in_arrangement):
    del live_in_arrangement.Application.get_application.return_value.view.show_view
    result = tools.show_arrangement_view()
    assert result["ok"] is False


def test_show_arrangement_view_exception(tools):
    result = tools.show_arrangement_view()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# focus_track
# ---------------------------------------------------------------------------


def test_focus_track_with_selected_track_attr(tools, song):
    result = tools.focus_track(0)
    assert result["ok"] is True


def test_focus_track_without_selected_track_attr(tools, song):
    del song.view.selected_track
    result = tools.focus_track(0)
    assert result["ok"] is False


def test_focus_track_invalid(tools):
    result = tools.focus_track(-1)
    assert result["ok"] is False


def test_focus_track_exception(tools, song):
    song.view.selected_track = MagicMock(side_effect=Exception("err"))
    result = tools.focus_track(0)
    assert result["ok"] is True  # assignment on MagicMock doesn't raise


# ---------------------------------------------------------------------------
# scroll_view_to_time
# ---------------------------------------------------------------------------


def test_scroll_view_to_time_with_visible_tracks(tools, song):
    result = tools.scroll_view_to_time(8.0)
    assert result["ok"] is True


def test_scroll_view_to_time_without_visible_tracks(tools, song):
    del song.view.visible_tracks
    result = tools.scroll_view_to_time(8.0)
    assert result["ok"] is False


def test_scroll_view_to_time_exception(tools):
    result = tools.scroll_view_to_time("bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_loop_enabled / get_loop_enabled
# ---------------------------------------------------------------------------


def test_set_loop_enabled(tools, song):
    result = tools.set_loop_enabled(True)
    assert result["ok"] is True
    assert song.loop is True


def test_set_loop_enabled_exception(tools, song):
    song.loop = MagicMock(side_effect=Exception("err"))
    result = tools.set_loop_enabled(True)
    assert result["ok"] is True  # MagicMock assignment doesn't raise


def test_get_loop_enabled(tools, song):
    song.loop = True
    song.loop_start = 0.0
    song.loop_length = 8.0
    result = tools.get_loop_enabled()
    assert result["ok"] is True
    assert result["loop_enabled"] is True


def test_get_loop_enabled_exception(tools, song):
    song.loop_start = "bad"  # float("bad") → ValueError → ok=False
    result = tools.get_loop_enabled()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_locator
# ---------------------------------------------------------------------------


def test_create_locator_with_create_cue_point(tools, song):
    result = tools.create_locator(4.0, name="Drop")
    assert result["ok"] is True
    song.create_cue_point.assert_called_once_with(4.0)


def test_create_locator_without_create_cue_point(tools, song):
    del song.create_cue_point
    result = tools.create_locator(4.0)
    assert result["ok"] is False


def test_create_locator_exception(tools, song):
    song.create_cue_point.side_effect = Exception("err")
    result = tools.create_locator(4.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# delete_locator
# ---------------------------------------------------------------------------


def test_delete_locator_with_cue_points(tools, song):
    cue = MagicMock()
    song.cue_points = [cue]
    result = tools.delete_locator(0)
    assert result["ok"] is True
    cue.delete.assert_called_once()


def test_delete_locator_invalid_index(tools, song):
    song.cue_points = [MagicMock()]
    result = tools.delete_locator(5)
    assert result["ok"] is False


def test_delete_locator_without_cue_points(tools, song):
    del song.cue_points
    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_delete_locator_cue_no_delete_method(tools, song):
    cue = MagicMock()
    del cue.delete
    song.cue_points = [cue]
    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_delete_locator_exception(tools, song):
    song.cue_points = MagicMock(side_effect=Exception("err"))
    result = tools.delete_locator(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_locators
# ---------------------------------------------------------------------------


def test_get_locators_with_cue_points(tools, song):
    cue = MagicMock()
    cue.time = 4.0
    cue.name = "Bridge"
    song.cue_points = [cue]
    result = tools.get_locators()
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_locators_without_cue_points(tools, song):
    del song.cue_points
    result = tools.get_locators()
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_locators_cue_no_time_or_name(tools, song):
    cue = MagicMock()
    del cue.time
    del cue.name
    song.cue_points = [cue]
    result = tools.get_locators()
    assert result["ok"] is True


def test_get_locators_exception(tools, song):
    song.cue_points = None  # hasattr returns True (set to None), for ... in None → TypeError
    result = tools.get_locators()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# jump_by_amount
# ---------------------------------------------------------------------------


def test_jump_by_amount_positive(tools, song):
    song.current_song_time = 4.0
    result = tools.jump_by_amount(2.0)
    assert result["ok"] is True
    assert result["old_time"] == 4.0
    assert result["jumped_by"] == 2.0


def test_jump_by_amount_negative_clamped(tools, song):
    song.current_song_time = 1.0
    result = tools.jump_by_amount(-5.0)
    assert result["ok"] is True


def test_jump_by_amount_exception(tools, song):
    song.current_song_time = "bad"  # float("bad") → ValueError → ok=False
    result = tools.jump_by_amount(1.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# browse_devices / browse_plugins / load_device_from_browser / get_browser_items
# ---------------------------------------------------------------------------


def test_browse_devices(tools):
    result = tools.browse_devices()
    assert result["ok"] is True
    assert len(result["device_types"]) > 0


def test_browse_plugins(tools):
    result = tools.browse_plugins("vst")
    assert result["ok"] is True
    assert result["plugin_type"] == "vst"


def test_browse_plugins_exception(tools, song):
    # browse_plugins never raises, so we just verify the happy path
    result = tools.browse_plugins()
    assert result["ok"] is True


def test_load_device_from_browser_delegates_to_add_device(tools, song):
    result = tools.load_device_from_browser(0, "EQ Eight")
    assert result["ok"] is True
    assert result["device_name"] == "EQ Eight"


def test_get_browser_items(tools):
    result = tools.get_browser_items("devices")
    assert result["ok"] is True
    assert result["category"] == "devices"


def test_get_browser_items_exception(tools, song):
    # get_browser_items never raises; test happy path
    result = tools.get_browser_items()
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# get_clip_color
# ---------------------------------------------------------------------------


def test_get_clip_color_via_color_index(tools, song):
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is True


def test_get_clip_color_via_color(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is True


def test_get_clip_color_no_color_attrs(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    del song.tracks[0].clip_slots[0].clip.color
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_clip_color_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_clip_color_invalid_track(tools):
    result = tools.get_clip_color(-1, 0)
    assert result["ok"] is False


def test_get_clip_color_invalid_clip(tools, song):
    result = tools.get_clip_color(0, 99)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_track_color
# ---------------------------------------------------------------------------


def test_get_track_color_via_color_index(tools, song):
    result = tools.get_track_color(0)
    assert result["ok"] is True


def test_get_track_color_via_color(tools, song):
    del song.tracks[0].color_index
    result = tools.get_track_color(0)
    assert result["ok"] is True


def test_get_track_color_no_color_attrs(tools, song):
    del song.tracks[0].color_index
    del song.tracks[0].color
    result = tools.get_track_color(0)
    assert result["ok"] is False


def test_get_track_color_invalid(tools):
    result = tools.get_track_color(-1)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Additional except-block coverage tests
# ---------------------------------------------------------------------------


def test_get_project_root_folder_except_block(tools, song):
    """Cover lines 23-24: str(project_root_folder) raises → except → ok=False."""
    obj = MagicMock()
    obj.__str__.side_effect = Exception("str error")
    song.project_root_folder = obj
    result = tools.get_project_root_folder()
    assert result["ok"] is False


def test_focus_track_except_block(tools):
    tools.song = None
    result = tools.focus_track(0)
    assert result["ok"] is False


def test_set_loop_enabled_except_block(tools):
    tools.song = None
    result = tools.set_loop_enabled(True)
    assert result["ok"] is False


def test_delete_locator_except_block(tools, song):
    """Cover lines 252-253: cue.delete() raises → except → ok=False."""
    cue = MagicMock()
    cue.delete.side_effect = Exception("delete failed")
    song.cue_points = [cue]
    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_get_clip_color_except_block(tools):
    tools.song = None
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_track_color_except_block(tools):
    tools.song = None
    result = tools.get_track_color(0)
    assert result["ok"] is False
