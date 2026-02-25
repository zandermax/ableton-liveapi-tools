"""
Tests for M4LAndLive12Mixin: M4L devices, audio clips, sample/simpler,
take lanes, application methods, and missing track/clip/scene properties.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

import ALiveMCP_Remote.tools.m4l_and_live12 as m4l_module

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _m4l_device(class_name="MxDeviceAudioEffect", name="CV Shaper"):
    dev = MagicMock()
    dev.class_name = class_name
    dev.name = name
    dev.is_active = True
    dev.parameters = [MagicMock()]
    return dev


def _audio_clip_slot(is_audio=True, has_clip=True):
    clip = MagicMock()
    clip.is_audio_clip = is_audio
    clip.is_midi_clip = not is_audio
    slot = MagicMock()
    slot.has_clip = has_clip
    slot.clip = clip
    return slot


@pytest.fixture
def live_in_m4l():
    fresh_live = MagicMock()
    with patch.dict(sys.modules, {"Live": fresh_live}):
        with patch.object(m4l_module, "Live", fresh_live, create=True):
            yield fresh_live


# ---------------------------------------------------------------------------
# is_max_device
# ---------------------------------------------------------------------------


def test_is_max_device_true(tools, song):
    dev = _m4l_device(class_name="MxDeviceAudioEffect")
    song.tracks[0].devices = [dev]
    result = tools.is_max_device(0, 0)
    assert result["ok"] is True
    assert result["is_m4l"] is True


def test_is_max_device_false(tools, song):
    dev = _m4l_device(class_name="Compressor2")
    song.tracks[0].devices = [dev]
    result = tools.is_max_device(0, 0)
    assert result["ok"] is True
    assert result["is_m4l"] is False


def test_is_max_device_invalid_track(tools):
    result = tools.is_max_device(-1, 0)
    assert result["ok"] is False


def test_is_max_device_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


def test_is_max_device_exception(tools, song):
    song.tracks[0].devices = MagicMock(side_effect=Exception("err"))
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_m4l_devices
# ---------------------------------------------------------------------------


def test_get_m4l_devices_with_m4l(tools, song):
    dev = _m4l_device(class_name="MxDeviceAudioEffect", name="CV Shaper")
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["devices"][0]["type"] == "audio_effect"


def test_get_m4l_devices_no_m4l(tools, song):
    dev = _m4l_device(class_name="Sampler", name="Sampler")
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_devices(0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_m4l_devices_invalid(tools):
    result = tools.get_m4l_devices(-1)
    assert result["ok"] is False


def test_get_m4l_devices_exception(tools, song):
    song.tracks[0].devices = None  # for dev in None → TypeError → ok=False
    result = tools.get_m4l_devices(0)
    assert result["ok"] is False


def test_get_m4l_type_variants(tools, song):
    """Cover all three M4L class names via get_m4l_devices."""
    for class_name, expected_type in [
        ("MxDeviceAudioEffect", "audio_effect"),
        ("MxDeviceMidiEffect", "midi_effect"),
        ("MxDeviceInstrument", "instrument"),
    ]:
        dev = _m4l_device(class_name=class_name)
        song.tracks[0].devices = [dev]
        result = tools.get_m4l_devices(0)
        assert result["devices"][0]["type"] == expected_type


# ---------------------------------------------------------------------------
# set_device_param_by_name
# ---------------------------------------------------------------------------


def test_set_device_param_by_name_found(tools, song):
    param = MagicMock()
    param.name = "Threshold"
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "Threshold", 0.5)
    assert result["ok"] is True
    assert param.value == 0.5


def test_set_device_param_by_name_not_found(tools, song):
    param = MagicMock()
    param.name = "Gain"
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "Missing", 0.5)
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_set_device_param_by_name_invalid_track(tools):
    result = tools.set_device_param_by_name(-1, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_param_by_name_exception(tools, song):
    dev = MagicMock()
    dev.parameters = MagicMock(side_effect=Exception("err"))
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_m4l_param_by_name
# ---------------------------------------------------------------------------


def test_get_m4l_param_by_name_found(tools, song):
    param = MagicMock()
    param.name = "Cutoff"
    param.value = 0.7
    param.min = 0.0
    param.max = 1.0
    param.is_enabled = True
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "Cutoff")
    assert result["ok"] is True
    assert result["value"] == 0.7


def test_get_m4l_param_by_name_not_found(tools, song):
    param = MagicMock()
    param.name = "Gain"
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "Missing")
    assert result["ok"] is False


def test_get_m4l_param_by_name_invalid(tools):
    result = tools.get_m4l_param_by_name(-1, 0, "x")
    assert result["ok"] is False


def test_get_m4l_param_by_name_no_is_enabled(tools, song):
    param = MagicMock()
    param.name = "P"
    param.value = 0.5
    param.min = 0.0
    param.max = 1.0
    del param.is_enabled
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "P")
    assert result["ok"] is True
    assert result["is_enabled"] is True


def test_get_m4l_param_by_name_exception(tools, song):
    dev = MagicMock()
    dev.parameters = MagicMock(side_effect=Exception("err"))
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_cv_tools_devices
# ---------------------------------------------------------------------------


def test_get_cv_tools_devices_found(tools, song):
    dev = MagicMock()
    dev.name = "CV Shaper"
    dev.class_name = "MxDeviceAudioEffect"
    dev.is_active = True
    dev.parameters = [MagicMock()]
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_cv_tools_devices_lowercase_cv(tools, song):
    dev = MagicMock()
    dev.name = "cv_clock"
    dev.class_name = "MxDeviceAudioEffect"
    dev.is_active = True
    dev.parameters = [MagicMock()]
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_cv_tools_devices_no_cv(tools, song):
    dev = MagicMock()
    dev.name = "EQ Eight"
    dev.class_name = "EQ"
    dev.is_active = True
    dev.parameters = []
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_cv_tools_devices_invalid(tools):
    result = tools.get_cv_tools_devices(-1)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_clip_warp_mode
# ---------------------------------------------------------------------------


def test_get_clip_warp_mode_audio_clip(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is True


def test_get_clip_warp_mode_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_clip_warp_mode(0, 0)
    assert result == {"ok": False, "error": "Clip is not an audio clip"}


def test_get_clip_warp_mode_invalid_track(tools):
    result = tools.get_clip_warp_mode(-1, 0)
    assert result["ok"] is False


def test_get_clip_warp_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is False


def test_get_clip_warp_mode_no_warp_mode_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_mode
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is True  # falls back to default 0


# ---------------------------------------------------------------------------
# set_clip_warp_mode
# ---------------------------------------------------------------------------


def test_set_clip_warp_mode_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is True


def test_set_clip_warp_mode_without_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_mode
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is False


def test_set_clip_warp_mode_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is False


def test_set_clip_warp_mode_invalid(tools):
    result = tools.set_clip_warp_mode(-1, 0, 2)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_clip_file_path
# ---------------------------------------------------------------------------


def test_get_clip_file_path_via_file_path(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    song.tracks[0].clip_slots[0].clip.file_path = "/audio/kick.wav"
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is True
    assert result["file_path"] == "/audio/kick.wav"


def test_get_clip_file_path_via_sample(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    del clip.file_path
    clip.sample.file_path = "/audio/snare.wav"
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is True


def test_get_clip_file_path_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


def test_get_clip_file_path_invalid(tools):
    result = tools.get_clip_file_path(-1, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_warping
# ---------------------------------------------------------------------------


def test_set_clip_warping_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is True


def test_set_clip_warping_without_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warping
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_invalid(tools):
    result = tools.set_clip_warping(-1, 0, True)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_warp_markers
# ---------------------------------------------------------------------------


def test_get_warp_markers_with_markers(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    marker = MagicMock()
    marker.sample_time = 0.0
    marker.beat_time = 0.0
    clip.warp_markers = [marker]
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_warp_markers_no_warp_markers_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_markers
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_warp_markers_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False


def test_get_warp_markers_invalid(tools):
    result = tools.get_warp_markers(-1, 0)
    assert result["ok"] is False


def test_get_warp_markers_no_sample_time(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    marker = MagicMock()
    del marker.sample_time
    del marker.beat_time
    clip.warp_markers = [marker]
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# get_sample_length
# ---------------------------------------------------------------------------


def test_get_sample_length_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.sample_length = 44100.0
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is True
    assert result["sample_length"] == 44100.0


def test_get_sample_length_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.sample_length
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


def test_get_sample_length_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_sample_playback_mode / set_sample_playback_mode
# ---------------------------------------------------------------------------


def test_get_sample_playback_mode_with_attr(tools, song):
    song.tracks[0].devices[0].playback_mode = 0
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is True


def test_get_sample_playback_mode_without_attr(tools, song):
    del song.tracks[0].devices[0].playback_mode
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is False


def test_get_sample_playback_mode_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is False


def test_set_sample_playback_mode_with_attr(tools, song):
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is True


def test_set_sample_playback_mode_without_attr(tools, song):
    del song.tracks[0].devices[0].playback_mode
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_take_lanes
# ---------------------------------------------------------------------------


def test_get_take_lanes_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Take 1"
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lanes(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_take_lanes_lane_no_name(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lanes(0)
    assert result["ok"] is True


def test_get_take_lanes_without_attr(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_take_lanes(0)
    assert result["ok"] is False


def test_get_take_lanes_exception(tools, song):
    song.tracks[0].take_lanes = None  # for lane in None → TypeError → ok=False
    result = tools.get_take_lanes(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_take_lane
# ---------------------------------------------------------------------------


def test_create_take_lane_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "New Take"
    song.tracks[0].create_take_lane.return_value = lane
    result = tools.create_take_lane(0, name="Take A")
    assert result["ok"] is True


def test_create_take_lane_without_create_attr(tools, song):
    del song.tracks[0].create_take_lane
    result = tools.create_take_lane(0)
    assert result["ok"] is False


def test_create_take_lane_no_name_attr_on_lane(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].create_take_lane.return_value = lane
    result = tools.create_take_lane(0)
    assert result["ok"] is True


def test_create_take_lane_exception(tools, song):
    song.tracks[0].create_take_lane.side_effect = Exception("err")
    result = tools.create_take_lane(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_take_lane_name / set_take_lane_name
# ---------------------------------------------------------------------------


def test_get_take_lane_name_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Take 2"
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is True
    assert result["name"] == "Take 2"


def test_get_take_lane_name_no_name(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is True


def test_get_take_lane_name_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is False


def test_set_take_lane_name_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Old"
    song.tracks[0].take_lanes = [lane]
    result = tools.set_take_lane_name(0, 0, "New Name")
    assert result["ok"] is True


def test_set_take_lane_name_no_name_attr(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.set_take_lane_name(0, 0, "New Name")
    assert result["ok"] is False


def test_set_take_lane_name_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.set_take_lane_name(0, 0, "x")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_audio_clip_in_lane / create_midi_clip_in_lane
# ---------------------------------------------------------------------------


def test_create_audio_clip_in_lane_with_attr(tools, song):
    lane = MagicMock()
    song.tracks[0].take_lanes = [lane]
    result = tools.create_audio_clip_in_lane(0, 0, length=4.0)
    assert result["ok"] is True
    lane.create_audio_clip.assert_called_once_with(4.0)


def test_create_audio_clip_in_lane_without_create_attr(tools, song):
    lane = MagicMock()
    del lane.create_audio_clip
    song.tracks[0].take_lanes = [lane]
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_audio_clip_in_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_with_attr(tools, song):
    lane = MagicMock()
    song.tracks[0].take_lanes = [lane]
    result = tools.create_midi_clip_in_lane(0, 0, length=8.0)
    assert result["ok"] is True
    lane.create_midi_clip.assert_called_once_with(8.0)


def test_create_midi_clip_in_lane_without_create_attr(tools, song):
    lane = MagicMock()
    del lane.create_midi_clip
    song.tracks[0].take_lanes = [lane]
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_clips_in_take_lane
# ---------------------------------------------------------------------------


def test_get_clips_in_take_lane_with_clips(tools, song):
    clip = MagicMock()
    clip.name = "audio"
    clip.length = 4.0
    clip.is_midi_clip = False
    lane = MagicMock()
    lane.clips = [clip]
    song.tracks[0].take_lanes = [lane]
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_clips_in_take_lane_no_clips_attr(tools, song):
    lane = MagicMock()
    del lane.clips
    song.tracks[0].take_lanes = [lane]
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_clips_in_take_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# delete_take_lane
# ---------------------------------------------------------------------------


def test_delete_take_lane_with_attr(tools, song):
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is True
    song.tracks[0].delete_take_lane.assert_called_once_with(0)


def test_delete_take_lane_without_attr(tools, song):
    del song.tracks[0].delete_take_lane
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is False


def test_delete_take_lane_exception(tools, song):
    song.tracks[0].delete_take_lane.side_effect = Exception("err")
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Application methods: get_build_id, get_variant, show_message_box,
# get_application_version  (all use `import Live` inline)
# ---------------------------------------------------------------------------


def test_get_build_id_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.get_build_id.return_value = "12345"
    result = tools.get_build_id()
    assert result["ok"] is True
    assert result["build_id"] == "12345"


def test_get_build_id_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.get_build_id
    result = tools.get_build_id()
    assert result["ok"] is False


def test_get_build_id_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_build_id()
    assert result["ok"] is False


def test_get_variant_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.get_variant.return_value = "Suite"
    result = tools.get_variant()
    assert result["ok"] is True
    assert result["variant"] == "Suite"


def test_get_variant_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.get_variant
    result = tools.get_variant()
    assert result["ok"] is False


def test_get_variant_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_variant()
    assert result["ok"] is False


def test_show_message_box_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.show_message.return_value = 0
    result = tools.show_message_box("Hello")
    assert result["ok"] is True
    assert result["button_pressed"] == 0


def test_show_message_box_result_none(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.show_message.return_value = None
    result = tools.show_message_box("Hello")
    assert result["ok"] is True
    assert result["button_pressed"] == 0


def test_show_message_box_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.show_message
    result = tools.show_message_box("Hello")
    assert result["ok"] is False


def test_show_message_box_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.show_message_box("Hello")
    assert result["ok"] is False


def test_get_application_version_basic(tools, live_in_m4l):
    app = live_in_m4l.Application.get_application.return_value
    app.get_major_version.return_value = 11
    app.get_minor_version.return_value = 3
    app.get_bugfix_version.return_value = 2
    del app.get_build_id
    del app.get_variant
    result = tools.get_application_version()
    assert result["ok"] is True
    assert result["major_version"] == 11


def test_get_application_version_with_build_and_variant(tools, live_in_m4l):
    app = live_in_m4l.Application.get_application.return_value
    app.get_major_version.return_value = 12
    app.get_minor_version.return_value = 0
    app.get_bugfix_version.return_value = 0
    app.get_build_id.return_value = "99"
    app.get_variant.return_value = "Suite"
    result = tools.get_application_version()
    assert result["ok"] is True
    assert result["build_id"] == "99"
    assert result["variant"] == "Suite"


def test_get_application_version_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_application_version()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Missing track/clip/scene properties
# ---------------------------------------------------------------------------


def test_get_clip_start_time_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.start_time = 2.0
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is True
    assert result["start_time"] == 2.0


def test_get_clip_start_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.start_time
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_get_clip_start_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_set_clip_start_time_with_attr(tools, song):
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is True


def test_set_clip_start_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.start_time
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_start_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is False


def test_get_track_is_foldable_with_attr(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is True
    assert result["is_foldable"] is True


def test_get_track_is_foldable_without_attr(tools, song):
    del song.tracks[0].is_foldable
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is False


def test_get_track_is_frozen_with_attr(tools, song):
    song.tracks[0].is_frozen = False
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is True
    assert result["is_frozen"] is False


def test_get_track_is_frozen_without_attr(tools, song):
    del song.tracks[0].is_frozen
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is False


def test_get_scene_is_empty_with_is_empty_attr(tools, song):
    song.scenes[0].is_empty = True
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is True


def test_get_scene_is_empty_manual_check(tools, song):
    del song.scenes[0].is_empty
    clip_slot = MagicMock()
    clip_slot.has_clip = False
    song.tracks[0].clip_slots = [clip_slot]
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is True


def test_get_scene_is_empty_manual_not_empty(tools, song):
    del song.scenes[0].is_empty
    clip_slot = MagicMock()
    clip_slot.has_clip = True
    song.tracks[0].clip_slots = [clip_slot]
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is False


def test_get_scene_is_empty_exception(tools, song):
    song.scenes = None  # None[0] → TypeError → ok=False
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is False


def test_get_scene_tempo_with_attr(tools, song):
    song.scenes[0].tempo = 128.0
    result = tools.get_scene_tempo(0)
    assert result["ok"] is True
    assert result["tempo"] == 128.0


def test_get_scene_tempo_without_attr(tools, song):
    del song.scenes[0].tempo
    result = tools.get_scene_tempo(0)
    assert result["ok"] is False


def test_get_scene_tempo_exception(tools, song):
    song.scenes[0].tempo = "bad"  # float("bad") → ValueError → ok=False
    result = tools.get_scene_tempo(0)
    assert result["ok"] is False


def test_get_arrangement_overdub_with_attr(tools, song):
    song.arrangement_overdub = True
    result = tools.get_arrangement_overdub()
    assert result["ok"] is True
    assert result["arrangement_overdub"] is True


def test_get_arrangement_overdub_without_attr(tools, song):
    del song.arrangement_overdub
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False


def test_get_arrangement_overdub_exception(tools, song):
    tools.song = None  # hasattr(None, "arrangement_overdub") = False → else → ok=False
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False


def test_set_record_mode_with_attr(tools, song):
    result = tools.set_record_mode(1)
    assert result["ok"] is True


def test_set_record_mode_without_attr(tools, song):
    del song.record_mode
    result = tools.set_record_mode(1)
    assert result["ok"] is False


def test_set_record_mode_exception(tools):
    result = tools.set_record_mode("bad")
    assert result["ok"] is False


def test_get_signature_numerator_with_attr(tools, song):
    song.signature_numerator = 4
    result = tools.get_signature_numerator()
    assert result["ok"] is True
    assert result["signature_numerator"] == 4


def test_get_signature_numerator_without_attr(tools, song):
    del song.signature_numerator
    result = tools.get_signature_numerator()
    assert result["ok"] is False


def test_get_signature_numerator_exception(tools, song):
    song.signature_numerator = "bad"  # int("bad") → ValueError → ok=False
    result = tools.get_signature_numerator()
    assert result["ok"] is False


def test_get_signature_denominator_with_attr(tools, song):
    song.signature_denominator = 4
    result = tools.get_signature_denominator()
    assert result["ok"] is True
    assert result["signature_denominator"] == 4


def test_get_signature_denominator_without_attr(tools, song):
    del song.signature_denominator
    result = tools.get_signature_denominator()
    assert result["ok"] is False


def test_get_signature_denominator_exception(tools, song):
    song.signature_denominator = "bad"  # int("bad") → ValueError → ok=False
    result = tools.get_signature_denominator()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Additional coverage: invalid index branches and except blocks
# ---------------------------------------------------------------------------


def test_is_max_device_except_block(tools):
    tools.song = None
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


def test_set_device_param_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_param_by_name_except_block(tools):
    tools.song = None
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_get_m4l_param_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


def test_get_m4l_param_by_name_except_block(tools):
    tools.song = None
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


def test_get_cv_tools_devices_except_block(tools):
    tools.song = None
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is False


def test_get_clip_warp_mode_invalid_clip(tools, song):
    result = tools.get_clip_warp_mode(0, 99)
    assert result["ok"] is False


def test_get_clip_warp_mode_except_block(tools):
    tools.song = None
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is False


def test_set_clip_warp_mode_invalid_clip(tools, song):
    result = tools.set_clip_warp_mode(0, 99, 0)
    assert result["ok"] is False


def test_set_clip_warp_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_warp_mode(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_warp_mode_except_block(tools):
    tools.song = None
    result = tools.set_clip_warp_mode(0, 0, 0)
    assert result["ok"] is False


def test_get_clip_file_path_invalid_clip(tools, song):
    result = tools.get_clip_file_path(0, 99)
    assert result["ok"] is False


def test_get_clip_file_path_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


def test_get_clip_file_path_except_block(tools):
    tools.song = None
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


def test_set_clip_warping_invalid_clip(tools, song):
    result = tools.set_clip_warping(0, 99, True)
    assert result["ok"] is False


def test_set_clip_warping_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_except_block(tools):
    tools.song = None
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_get_warp_markers_invalid_clip(tools, song):
    result = tools.get_warp_markers(0, 99)
    assert result["ok"] is False


def test_get_warp_markers_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False


def test_get_warp_markers_except_block(tools):
    tools.song = None
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False


def test_get_sample_length_except_block(tools):
    tools.song = None
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


def test_set_sample_playback_mode_except_block(tools):
    tools.song = None
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is False


def test_get_take_lane_name_except_block(tools):
    tools.song = None
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is False


def test_set_take_lane_name_except_block(tools):
    tools.song = None
    result = tools.set_take_lane_name(0, 0, "x")
    assert result["ok"] is False


def test_create_audio_clip_in_lane_except_block(tools):
    tools.song = None
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_except_block(tools):
    tools.song = None
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_get_clips_in_take_lane_except_block(tools):
    tools.song = None
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is False


def test_get_clip_start_time_except_block(tools):
    tools.song = None
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_set_clip_start_time_except_block(tools):
    tools.song = None
    result = tools.set_clip_start_time(0, 0, 1.0)
    assert result["ok"] is False


def test_get_track_is_foldable_except_block(tools):
    tools.song = None
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is False


def test_get_track_is_frozen_except_block(tools):
    tools.song = None
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is False


def test_get_arrangement_overdub_except_block(tools):
    tools.song = None
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False
