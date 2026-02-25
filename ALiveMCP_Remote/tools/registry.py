"""
Registry of all available tool names exposed by LiveAPITools.
"""

AVAILABLE_TOOLS = [
    "ping",
    "health_check",
    # Session control (14 tools)
    "start_playback",
    "stop_playback",
    "start_recording",
    "stop_recording",
    "continue_playing",
    "get_session_info",
    "set_tempo",
    "set_time_signature",
    "set_loop_start",
    "set_loop_length",
    "set_metronome",
    "tap_tempo",
    "undo",
    "redo",
    # Transport (8 tools)
    "jump_to_time",
    "get_current_time",
    "set_arrangement_overdub",
    "set_back_to_arranger",
    "set_punch_in",
    "set_punch_out",
    "nudge_up",
    "nudge_down",
    # Automation (6 tools)
    "re_enable_automation",
    "get_session_automation_record",
    "set_session_automation_record",
    "get_session_record",
    "set_session_record",
    "capture_midi",
    # Track management (13 tools)
    "create_midi_track",
    "create_audio_track",
    "create_return_track",
    "delete_track",
    "duplicate_track",
    "rename_track",
    "set_track_volume",
    "set_track_pan",
    "arm_track",
    "solo_track",
    "mute_track",
    "get_track_info",
    "set_track_color",
    # Track extras (5 tools)
    "set_track_fold_state",
    "set_track_input_routing",
    "set_track_output_routing",
    "set_track_send",
    "get_track_sends",
    # Clip operations (8 tools)
    "create_midi_clip",
    "delete_clip",
    "duplicate_clip",
    "launch_clip",
    "stop_clip",
    "stop_all_clips",
    "get_clip_info",
    "set_clip_name",
    # Clip extras (10 tools)
    "set_clip_looping",
    "set_clip_loop_start",
    "set_clip_loop_end",
    "set_clip_start_marker",
    "set_clip_end_marker",
    "set_clip_muted",
    "set_clip_gain",
    "set_clip_pitch_coarse",
    "set_clip_pitch_fine",
    "set_clip_signature_numerator",
    # MIDI notes (3 tools)
    "add_notes",
    "get_clip_notes",
    "remove_notes",
    # MIDI extras (4 tools)
    "select_all_notes",
    "deselect_all_notes",
    "replace_selected_notes",
    "get_notes_extended",
    # Devices (3 tools)
    "add_device",
    "get_track_devices",
    "set_device_param",
    # Device extras (9 tools)
    "set_device_on_off",
    "get_device_parameters",
    "get_device_parameter_by_name",
    "set_device_parameter_by_name",
    "delete_device",
    "get_device_presets",
    "set_device_preset",
    "randomize_device_parameters",
    # Scenes (6 tools)
    "create_scene",
    "delete_scene",
    "duplicate_scene",
    "launch_scene",
    "rename_scene",
    "get_scene_info",
    # Groove & Quantize (5 tools)
    "set_clip_groove_amount",
    "quantize_clip",
    "quantize_clip_pitch",
    "get_groove_amount",
    "set_groove_amount",
    # Monitoring & Input (4 tools)
    "set_track_current_monitoring_state",
    "get_track_available_input_routing_types",
    "get_track_available_output_routing_types",
    "get_track_input_routing_type",
    # Project & Arrangement (6 tools)
    "get_project_root_folder",
    "trigger_session_record",
    "get_can_jump_to_next_cue",
    "get_can_jump_to_prev_cue",
    "jump_to_next_cue",
    "jump_to_prev_cue",
    # Browser operations (4 tools)
    "browse_devices",
    "browse_plugins",
    "load_device_from_browser",
    "get_browser_items",
    # Loop & Locator operations (6 tools)
    "set_loop_enabled",
    "get_loop_enabled",
    "create_locator",
    "delete_locator",
    "get_locators",
    "jump_by_amount",
    # Clip color (1 tool)
    "set_clip_color",
    # Track routing extras (3 tools)
    "get_track_output_routing",
    "set_track_input_sub_routing",
    "set_track_output_sub_routing",
    # Device extras - missing tool (1 tool)
    "randomize_device",
    # Max for Live (M4L) operations (5 tools)
    "is_max_device",
    "get_m4l_devices",
    "set_device_param_by_name",
    "get_m4l_param_by_name",
    "get_cv_tools_devices",
    # Master Track Control (4 tools)
    "get_master_track_info",
    "set_master_volume",
    "set_master_pan",
    "get_master_devices",
    # Return Track Operations (3 tools)
    "get_return_track_count",
    "get_return_track_info",
    "set_return_track_volume",
    # Audio Clip Operations (5 tools)
    "get_clip_warp_mode",
    "set_clip_warp_mode",
    "get_clip_file_path",
    "set_clip_warping",
    "get_warp_markers",
    # Follow Actions (3 tools)
    "get_clip_follow_action",
    "set_clip_follow_action",
    "set_follow_action_time",
    # Crossfader (3 tools)
    "get_crossfader_assignment",
    "set_crossfader_assignment",
    "get_crossfader_position",
    # Track Groups (4 tools)
    "create_group_track",
    "group_tracks",
    "get_track_is_grouped",
    "ungroup_track",
    # View/Navigation (4 tools)
    "show_clip_view",
    "show_arrangement_view",
    "focus_track",
    "scroll_view_to_time",
    # Color Utilities (2 tools)
    "get_clip_color",
    "get_track_color",
    # Groove Pool (2 tools)
    "get_groove_pool_grooves",
    "set_clip_groove",
    # Rack/Chain Operations (4 tools)
    "get_device_chains",
    "get_chain_devices",
    "set_chain_mute",
    "set_chain_solo",
    # Clip Automation Envelopes (6 tools)
    "get_clip_automation_envelope",
    "create_automation_envelope",
    "clear_automation_envelope",
    "insert_automation_step",
    "remove_automation_step",
    "get_automation_envelope_values",
    # Track Freeze/Flatten (3 tools)
    "freeze_track",
    "unfreeze_track",
    "flatten_track",
    # Clip Fade In/Out (4 tools)
    "get_clip_fade_in",
    "set_clip_fade_in",
    "get_clip_fade_out",
    "set_clip_fade_out",
    # Scene Color (2 tools)
    "get_scene_color",
    "set_scene_color",
    # Track Annotations (2 tools)
    "get_track_annotation",
    "set_track_annotation",
    # Clip Annotations (2 tools)
    "get_clip_annotation",
    "set_clip_annotation",
    # Track Delay Compensation (2 tools)
    "get_track_delay",
    "set_track_delay",
    # Arrangement View Clips (3 tools)
    "get_arrangement_clips",
    "duplicate_to_arrangement",
    "consolidate_clip",
    # Plugin Window Control (2 tools)
    "show_plugin_window",
    "hide_plugin_window",
    # Metronome Volume (2 tools)
    "get_metronome_volume",
    "set_metronome_volume",
    # MIDI CC/Program Change (2 tools)
    "send_midi_cc",
    "send_program_change",
    # Sample/Simpler Operations (3 tools)
    "get_sample_length",
    "get_sample_playback_mode",
    "set_sample_playback_mode",
    # Clip RAM Mode (2 tools)
    "get_clip_ram_mode",
    "set_clip_ram_mode",
    # Device Utilities (2 tools)
    "get_device_class_name",
    "get_device_type",
    # Take Lanes Support (8 tools) - Live 12
    "get_take_lanes",
    "create_take_lane",
    "get_take_lane_name",
    "set_take_lane_name",
    "create_audio_clip_in_lane",
    "create_midi_clip_in_lane",
    "get_clips_in_take_lane",
    "delete_take_lane",
    # Application Methods (4 tools) - Live 12
    "get_build_id",
    "get_variant",
    "show_message_box",
    "get_application_version",
    # Device Parameter Display Values (2 tools) - Live 12
    "get_device_param_display_value",
    "get_all_param_display_values",
    # Missing Track/Clip/Scene Properties (10 tools)
    "get_clip_start_time",
    "set_clip_start_time",
    "get_track_is_foldable",
    "get_track_is_frozen",
    "get_scene_is_empty",
    "get_scene_tempo",
    "get_arrangement_overdub",
    "set_record_mode",
    "get_signature_numerator",
    "get_signature_denominator",
]
