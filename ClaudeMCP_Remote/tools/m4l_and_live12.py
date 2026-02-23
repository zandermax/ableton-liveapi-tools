"""
Max for Live, audio clips, sample/simpler, take lanes, application methods,
and miscellaneous track/clip/scene property operations.
"""


class M4LAndLive12Mixin(object):

    # ========================================================================
    # MAX FOR LIVE (M4L) DEVICE OPERATIONS
    # ========================================================================

    def is_max_device(self, track_index, device_index):
        """Check if device is a Max for Live device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # M4L devices have specific class names
            m4l_classes = ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']
            is_m4l = device.class_name in m4l_classes

            return {
                "ok": True,
                "is_m4l": is_m4l,
                "class_name": str(device.class_name),
                "class_display_name": str(device.class_display_name) if hasattr(device, 'class_display_name') else str(device.class_name),
                "device_name": str(device.name)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_m4l_devices(self, track_index):
        """Get all Max for Live devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            m4l_devices = []
            m4l_classes = ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']

            for i, device in enumerate(track.devices):
                if device.class_name in m4l_classes:
                    device_type = self._get_m4l_type(device.class_name)
                    m4l_devices.append({
                        "index": i,
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "type": device_type,
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters)
                    })

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "devices": m4l_devices,
                "count": len(m4l_devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _get_m4l_type(self, class_name):
        """Get M4L device type from class name"""
        type_map = {
            'MxDeviceAudioEffect': 'audio_effect',
            'MxDeviceMidiEffect': 'midi_effect',
            'MxDeviceInstrument': 'instrument'
        }
        return type_map.get(class_name, 'unknown')

    def set_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name (useful for M4L devices with custom parameter names)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # Find parameter by name
            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    param.value = float(value)
                    return {
                        "ok": True,
                        "track_index": track_index,
                        "device_index": device_index,
                        "param_name": param_name,
                        "param_index": i,
                        "value": float(param.value)
                    }

            return {"ok": False, "error": "Parameter '{}' not found".format(param_name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_m4l_param_by_name(self, track_index, device_index, param_name):
        """Get M4L device parameter value by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # Find parameter by name
            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    return {
                        "ok": True,
                        "param_index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_enabled": param.is_enabled if hasattr(param, 'is_enabled') else True
                    }

            return {"ok": False, "error": "Parameter '{}' not found".format(param_name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_cv_tools_devices(self, track_index):
        """Get all CV Tools devices on track (subset of M4L devices)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            cv_devices = []

            for i, device in enumerate(track.devices):
                device_name = str(device.name)
                # Check if device name contains "CV" (common in CV Tools)
                if 'CV' in device_name or 'cv' in device_name.lower():
                    cv_devices.append({
                        "index": i,
                        "name": device_name,
                        "class_name": str(device.class_name),
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters)
                    })

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "cv_devices": cv_devices,
                "count": len(cv_devices)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # AUDIO CLIP OPERATIONS
    # ========================================================================

    def get_clip_warp_mode(self, track_index, clip_index):
        """Get audio clip warp mode"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            warp_mode_names = {
                0: "Beats",
                1: "Tones",
                2: "Texture",
                3: "Re-Pitch",
                4: "Complex",
                5: "Complex Pro"
            }

            warp_mode = int(clip.warp_mode) if hasattr(clip, 'warp_mode') else 0

            return {
                "ok": True,
                "warp_mode": warp_mode,
                "warp_mode_name": warp_mode_names.get(warp_mode, "Unknown"),
                "warping": clip.warping if hasattr(clip, 'warping') else False
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warp_mode(self, track_index, clip_index, warp_mode):
        """Set audio clip warp mode (0-5: Beats, Tones, Texture, Re-Pitch, Complex, Complex Pro)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, 'warp_mode'):
                clip.warp_mode = int(max(0, min(5, warp_mode)))
                return {
                    "ok": True,
                    "warp_mode": int(clip.warp_mode)
                }
            else:
                return {"ok": False, "error": "Warp mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_file_path(self, track_index, clip_index):
        """Get audio clip file path"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            file_path = ""
            if hasattr(clip, 'file_path'):
                file_path = str(clip.file_path)
            elif hasattr(clip, 'sample') and hasattr(clip.sample, 'file_path'):
                file_path = str(clip.sample.file_path)

            return {
                "ok": True,
                "file_path": file_path
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warping(self, track_index, clip_index, warping):
        """Enable/disable warping for audio clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, 'warping'):
                clip.warping = bool(warping)
                return {
                    "ok": True,
                    "warping": clip.warping
                }
            else:
                return {"ok": False, "error": "Warping property not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_warp_markers(self, track_index, clip_index):
        """Get warp markers from audio clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            markers = []
            if hasattr(clip, 'warp_markers'):
                for marker in clip.warp_markers:
                    markers.append({
                        "sample_time": float(marker.sample_time) if hasattr(marker, 'sample_time') else 0.0,
                        "beat_time": float(marker.beat_time) if hasattr(marker, 'beat_time') else 0.0
                    })

            return {
                "ok": True,
                "markers": markers,
                "count": len(markers)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SAMPLE/SIMPLER OPERATIONS (3 tools)
    # ========================================================================

    def get_sample_length(self, track_index, clip_index):
        """Get audio sample length for a clip"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'sample_length'):
                return {
                    "ok": True,
                    "sample_length": float(clip.sample_length)
                }
            else:
                return {"ok": False, "error": "Sample length not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_sample_playback_mode(self, track_index, device_index):
        """Get Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'playback_mode'):
                return {
                    "ok": True,
                    "playback_mode": int(device.playback_mode)
                }
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_sample_playback_mode(self, track_index, device_index, mode):
        """Set Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, 'playback_mode'):
                device.playback_mode = int(mode)
                return {
                    "ok": True,
                    "playback_mode": int(device.playback_mode)
                }
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TAKE LANES SUPPORT (8 tools) - LIVE 12 FEATURE
    # ========================================================================

    def get_take_lanes(self, track_index):
        """Get all take lanes for a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lanes_info = []
                for i, lane in enumerate(track.take_lanes):
                    lane_data = {
                        "index": i,
                        "name": str(lane.name) if hasattr(lane, 'name') else "Take " + str(i + 1)
                    }
                    lanes_info.append(lane_data)

                return {
                    "ok": True,
                    "count": len(lanes_info),
                    "take_lanes": lanes_info
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_take_lane(self, track_index, name=None):
        """Create new take lane on a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'create_take_lane'):
                lane = track.create_take_lane()
                if name and hasattr(lane, 'name'):
                    lane.name = str(name)

                return {
                    "ok": True,
                    "message": "Take lane created",
                    "name": str(lane.name) if hasattr(lane, 'name') else "New Take"
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_take_lane_name(self, track_index, lane_index):
        """Get take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                return {
                    "ok": True,
                    "name": str(lane.name) if hasattr(lane, 'name') else "Take " + str(lane_index + 1)
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_take_lane_name(self, track_index, lane_index, name):
        """Set take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'name'):
                    lane.name = str(name)
                    return {
                        "ok": True,
                        "name": str(lane.name)
                    }
                else:
                    return {"ok": False, "error": "Lane name not settable"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_clip_in_lane(self, track_index, lane_index, length=4.0):
        """Create audio clip in take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'create_audio_clip'):
                    clip = lane.create_audio_clip(float(length))
                    return {
                        "ok": True,
                        "message": "Audio clip created in take lane",
                        "length": float(length)
                    }
                else:
                    return {"ok": False, "error": "create_audio_clip not available"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_midi_clip_in_lane(self, track_index, lane_index, length=4.0):
        """Create MIDI clip in take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, 'create_midi_clip'):
                    clip = lane.create_midi_clip(float(length))
                    return {
                        "ok": True,
                        "message": "MIDI clip created in take lane",
                        "length": float(length)
                    }
                else:
                    return {"ok": False, "error": "create_midi_clip not available"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clips_in_take_lane(self, track_index, lane_index):
        """Get all clips in a take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'take_lanes'):
                lane = track.take_lanes[lane_index]
                clips_info = []

                if hasattr(lane, 'clips'):
                    for clip in lane.clips:
                        clip_data = {
                            "name": str(clip.name),
                            "length": float(clip.length),
                            "is_midi": clip.is_midi_clip
                        }
                        clips_info.append(clip_data)

                return {
                    "ok": True,
                    "count": len(clips_info),
                    "clips": clips_info
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_take_lane(self, track_index, lane_index):
        """Delete a take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'delete_take_lane'):
                track.delete_take_lane(lane_index)
                return {
                    "ok": True,
                    "message": "Take lane deleted"
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # APPLICATION METHODS (4 tools) - LIVE 12
    # ========================================================================

    def get_build_id(self):
        """Get Ableton Live build identifier (Live 12+)"""
        try:
            import Live
            app = Live.Application.get_application()

            if hasattr(app, 'get_build_id'):
                return {
                    "ok": True,
                    "build_id": str(app.get_build_id())
                }
            else:
                return {"ok": False, "error": "get_build_id not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_variant(self):
        """Get Ableton Live variant (Suite, Standard, Intro) (Live 12+)"""
        try:
            import Live
            app = Live.Application.get_application()

            if hasattr(app, 'get_variant'):
                return {
                    "ok": True,
                    "variant": str(app.get_variant())
                }
            else:
                return {"ok": False, "error": "get_variant not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_message_box(self, message, title="Message"):
        """Show message box dialog to user (Live 12+)"""
        try:
            import Live
            app = Live.Application.get_application()

            if hasattr(app, 'show_message'):
                result = app.show_message(str(message))
                return {
                    "ok": True,
                    "message": "Message shown",
                    "button_pressed": int(result) if result is not None else 0
                }
            else:
                return {"ok": False, "error": "show_message not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_application_version(self):
        """Get full Ableton Live version information"""
        try:
            import Live
            app = Live.Application.get_application()

            version_info = {
                "ok": True,
                "major_version": int(app.get_major_version()),
                "minor_version": int(app.get_minor_version()),
                "bugfix_version": int(app.get_bugfix_version())
            }

            # Add build_id if available (Live 12+)
            if hasattr(app, 'get_build_id'):
                version_info["build_id"] = str(app.get_build_id())

            # Add variant if available (Live 12+)
            if hasattr(app, 'get_variant'):
                version_info["variant"] = str(app.get_variant())

            return version_info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MISSING TRACK/CLIP/SCENE PROPERTIES (10 tools)
    # ========================================================================

    def get_clip_start_time(self, track_index, clip_index):
        """Get clip start time (observable in Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'start_time'):
                return {
                    "ok": True,
                    "start_time": float(clip.start_time)
                }
            else:
                return {"ok": False, "error": "start_time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_start_time(self, track_index, clip_index, start_time):
        """Set clip start time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, 'start_time'):
                clip.start_time = float(start_time)
                return {
                    "ok": True,
                    "start_time": float(clip.start_time)
                }
            else:
                return {"ok": False, "error": "start_time not settable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_foldable(self, track_index):
        """Check if track can be folded (group tracks)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'is_foldable'):
                return {
                    "ok": True,
                    "is_foldable": bool(track.is_foldable)
                }
            else:
                return {"ok": False, "error": "is_foldable not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_frozen(self, track_index):
        """Check if track is currently frozen"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'is_frozen'):
                return {
                    "ok": True,
                    "is_frozen": bool(track.is_frozen)
                }
            else:
                return {"ok": False, "error": "is_frozen not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_is_empty(self, scene_index):
        """Check if scene has no clips"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'is_empty'):
                return {
                    "ok": True,
                    "is_empty": bool(scene.is_empty)
                }
            else:
                # Manually check if all clip slots are empty
                is_empty = True
                for track in self.song.tracks:
                    if track.clip_slots[scene_index].has_clip:
                        is_empty = False
                        break

                return {
                    "ok": True,
                    "is_empty": is_empty
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_tempo(self, scene_index):
        """Get scene tempo override (if set)"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, 'tempo'):
                return {
                    "ok": True,
                    "tempo": float(scene.tempo) if scene.tempo else None,
                    "has_tempo": bool(scene.tempo)
                }
            else:
                return {"ok": False, "error": "Scene tempo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_arrangement_overdub(self):
        """Get arrangement overdub state"""
        try:
            if hasattr(self.song, 'arrangement_overdub'):
                return {
                    "ok": True,
                    "arrangement_overdub": bool(self.song.arrangement_overdub)
                }
            else:
                return {"ok": False, "error": "arrangement_overdub not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_record_mode(self, mode):
        """Set session/arrangement record mode (0=session, 1=arrangement)"""
        try:
            if hasattr(self.song, 'record_mode'):
                self.song.record_mode = int(mode)
                return {
                    "ok": True,
                    "record_mode": int(self.song.record_mode)
                }
            else:
                return {"ok": False, "error": "record_mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_numerator(self):
        """Get global time signature numerator"""
        try:
            if hasattr(self.song, 'signature_numerator'):
                return {
                    "ok": True,
                    "signature_numerator": int(self.song.signature_numerator)
                }
            else:
                return {"ok": False, "error": "signature_numerator not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_denominator(self):
        """Get global time signature denominator"""
        try:
            if hasattr(self.song, 'signature_denominator'):
                return {
                    "ok": True,
                    "signature_denominator": int(self.song.signature_denominator)
                }
            else:
                return {"ok": False, "error": "signature_denominator not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
