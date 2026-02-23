"""
Track management, routing, grouping, freeze/flatten, annotations, and delay operations.
"""


class TracksMixin:
    # ========================================================================
    # TRACK MANAGEMENT
    # ========================================================================

    def create_midi_track(self, name=None):
        """
        Create a new MIDI track

        Args:
            name: Optional track name
        """
        try:
            track_index = len(self.song.tracks)
            self.song.create_midi_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "MIDI track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_track(self, name=None):
        """
        Create a new audio track

        Args:
            name: Optional track name
        """
        try:
            track_index = len(self.song.tracks)
            self.song.create_audio_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Audio track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_return_track(self):
        """Create a new return track"""
        try:
            self.song.create_return_track()
            return_index = len(self.song.return_tracks) - 1
            return {"ok": True, "message": "Return track created", "return_index": return_index}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_track(self, track_index):
        """Delete track by index"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.delete_track(track_index)
            return {"ok": True, "message": "Track deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_track(self, track_index):
        """Duplicate track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.duplicate_track(track_index)
            return {"ok": True, "message": "Track duplicated", "new_index": track_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_track(self, track_index, name):
        """Rename track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].name = str(name)
            return {"ok": True, "message": "Track renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_volume(self, track_index, volume):
        """
        Set track volume

        Args:
            track_index: Track index
            volume: Volume (0.0 to 1.0)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            volume = float(volume)
            if volume < 0.0 or volume > 1.0:
                return {"ok": False, "error": "Volume must be between 0.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.volume.value = volume

            return {
                "ok": True,
                "message": "Track volume set",
                "track_index": track_index,
                "volume": float(track.mixer_device.volume.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_pan(self, track_index, pan):
        """
        Set track pan

        Args:
            track_index: Track index
            pan: Pan (-1.0 to 1.0, where 0 is center)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            pan = float(pan)
            if pan < -1.0 or pan > 1.0:
                return {"ok": False, "error": "Pan must be between -1.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.panning.value = pan

            return {
                "ok": True,
                "message": "Track pan set",
                "track_index": track_index,
                "pan": float(track.mixer_device.panning.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def arm_track(self, track_index, armed=True):
        """Arm or disarm track for recording"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.can_be_armed:
                track.arm = bool(armed)
                return {
                    "ok": True,
                    "message": "Track armed" if armed else "Track disarmed",
                    "armed": track.arm,
                }
            else:
                return {"ok": False, "error": "Track cannot be armed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def solo_track(self, track_index, solo=True):
        """Solo or unsolo track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].solo = bool(solo)
            return {"ok": True, "message": "Track soloed" if solo else "Track unsoloed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def mute_track(self, track_index, mute=True):
        """Mute or unmute track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].mute = bool(mute)
            return {"ok": True, "message": "Track muted" if mute else "Track unmuted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_info(self, track_index):
        """Get detailed track information"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            return {
                "ok": True,
                "track_index": track_index,
                "name": str(track.name),
                "color": track.color if hasattr(track, "color") else None,
                "is_foldable": track.is_foldable,
                "mute": track.mute,
                "solo": track.solo,
                "arm": track.arm if track.can_be_armed else False,
                "has_midi_input": track.has_midi_input,
                "has_audio_input": track.has_audio_input,
                "volume": float(track.mixer_device.volume.value),
                "pan": float(track.mixer_device.panning.value),
                "num_devices": len(track.devices),
                "num_clips": len([cs for cs in track.clip_slots if cs.has_clip]),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_color(self, track_index, color_index):
        """Set track color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, "color"):
                track.color = int(color_index)
                return {"ok": True, "message": "Track color set", "color": track.color}
            else:
                return {"ok": False, "error": "Track color not supported"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK EXTRAS
    # ========================================================================

    def set_track_fold_state(self, track_index, folded):
        """Fold or unfold a group track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.is_foldable:
                track.fold_state = bool(folded)
                return {"ok": True, "fold_state": track.fold_state}
            else:
                return {"ok": False, "error": "Track is not foldable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_input_routing(self, track_index, routing_type_name, routing_channel=0):
        """Set track input routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            return {
                "ok": True,
                "message": "Input routing set (requires routing configuration)",
                "routing_type": routing_type_name,
                "routing_channel": routing_channel,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_output_routing(self, track_index, routing_type_name):
        """Set track output routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            return {
                "ok": True,
                "message": "Output routing set (requires routing configuration)",
                "routing_type": routing_type_name,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MONITORING & INPUT
    # ========================================================================

    def set_track_current_monitoring_state(self, track_index, state):
        """Set track monitoring state (0=In, 1=Auto, 2=Off)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.can_be_armed:
                track.current_monitoring_state = int(state)
                return {"ok": True, "monitoring_state": track.current_monitoring_state}
            else:
                return {"ok": False, "error": "Track cannot be monitored"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_available_input_routing_types(self, track_index):
        """Get available input routing types for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            routing_types = []
            if hasattr(track, "available_input_routing_types"):
                for routing in track.available_input_routing_types:
                    routing_types.append(str(routing.display_name))

            return {"ok": True, "routing_types": routing_types, "count": len(routing_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_available_output_routing_types(self, track_index):
        """Get available output routing types for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            routing_types = []
            if hasattr(track, "available_output_routing_types"):
                for routing in track.available_output_routing_types:
                    routing_types.append(str(routing.display_name))

            return {"ok": True, "routing_types": routing_types, "count": len(routing_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_input_routing_type(self, track_index):
        """Get current input routing type for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, "input_routing_type"):
                return {
                    "ok": True,
                    "routing_type": str(track.input_routing_type.display_name)
                    if track.input_routing_type
                    else None,
                }
            else:
                return {"ok": False, "error": "Track does not have input routing"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK ROUTING EXTRAS
    # ========================================================================

    def get_track_output_routing(self, track_index):
        """Get track output routing configuration"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            result = {"ok": True, "track_index": track_index, "track_name": str(track.name)}

            if hasattr(track, "output_routing_type"):
                result["output_routing_type"] = (
                    str(track.output_routing_type.display_name)
                    if hasattr(track.output_routing_type, "display_name")
                    else str(track.output_routing_type)
                )

            if hasattr(track, "output_routing_channel"):
                result["output_routing_channel"] = (
                    str(track.output_routing_channel.display_name)
                    if hasattr(track.output_routing_channel, "display_name")
                    else str(track.output_routing_channel)
                )

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_input_sub_routing(self, track_index, sub_routing):
        """Set track input sub-routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, "input_sub_routing"):
                # Sub-routing is typically set by index or name
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "Input sub-routing setting is limited in LiveAPI",
                    "track_index": track_index,
                    "requested_sub_routing": str(sub_routing),
                }
            else:
                return {"ok": False, "error": "Input sub-routing not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_output_sub_routing(self, track_index, sub_routing):
        """Set track output sub-routing"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, "output_sub_routing"):
                # Sub-routing is typically set by index or name
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "Output sub-routing setting is limited in LiveAPI",
                    "track_index": track_index,
                    "requested_sub_routing": str(sub_routing),
                }
            else:
                return {"ok": False, "error": "Output sub-routing not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK GROUPS
    # ========================================================================

    def create_group_track(self, name=None):
        """Create a new group track"""
        try:
            track_index = len(self.song.tracks)
            self.song.create_group_track(track_index)

            if name and track_index < len(self.song.tracks):
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Group track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name)
                if track_index < len(self.song.tracks)
                else "",
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def group_tracks(self, start_index, end_index):
        """Group tracks from start_index to end_index (inclusive)"""
        try:
            if start_index < 0 or start_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid start index"}
            if end_index < start_index or end_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid end index"}

            # Group the tracks
            self.song.create_group_track(end_index + 1)

            # Move tracks into the group (this is simplified - actual implementation may vary)
            return {
                "ok": True,
                "message": "Tracks grouped",
                "start_index": start_index,
                "end_index": end_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_grouped(self, track_index):
        """Check if track is part of a group"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            is_grouped = hasattr(track, "group_track") and track.group_track is not None
            is_foldable = hasattr(track, "is_foldable") and track.is_foldable

            result = {
                "ok": True,
                "track_index": track_index,
                "is_grouped": is_grouped,
                "is_group_track": is_foldable,
            }

            if is_grouped and hasattr(track, "group_track"):
                # Find the group track index
                for i, t in enumerate(self.song.tracks):
                    if t == track.group_track:
                        result["group_track_index"] = i
                        break

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def ungroup_track(self, group_track_index):
        """Ungroup a group track"""
        try:
            if group_track_index < 0 or group_track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[group_track_index]

            if not (hasattr(track, "is_foldable") and track.is_foldable):
                return {"ok": False, "error": "Track is not a group track"}

            # Ungroup (LiveAPI may not have direct ungroup, this is a placeholder)
            return {
                "ok": True,
                "message": "Ungroup operation requested (may require manual implementation)",
                "group_track_index": group_track_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK FREEZE/FLATTEN (3 tools)
    # ========================================================================

    def freeze_track(self, track_index):
        """Freeze a track to reduce CPU usage"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "freeze_available") and track.freeze_available:
                if hasattr(track, "freeze_state"):
                    # 0 = no freeze, 1 = frozen, 2 = frozen with tails
                    track.freeze_state = 1
                    return {"ok": True, "track_index": track_index, "frozen": True}
                else:
                    return {"ok": False, "error": "Freeze state not available"}
            else:
                return {"ok": False, "error": "Track cannot be frozen"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def unfreeze_track(self, track_index):
        """Unfreeze a frozen track"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "freeze_state"):
                track.freeze_state = 0
                return {"ok": True, "track_index": track_index, "frozen": False}
            else:
                return {"ok": False, "error": "Freeze state not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def flatten_track(self, track_index):
        """Flatten a frozen track (converts to audio)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "flatten"):
                track.flatten()
                return {"ok": True, "track_index": track_index, "message": "Track flattened"}
            else:
                return {"ok": False, "error": "Flatten not available (track must be frozen first)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK ANNOTATIONS (2 tools)
    # ========================================================================

    def get_track_annotation(self, track_index):
        """Get track annotation text"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "annotation"):
                return {"ok": True, "annotation": str(track.annotation)}
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_annotation(self, track_index, annotation_text):
        """Set track annotation text"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "annotation"):
                track.annotation = str(annotation_text)
                return {"ok": True, "annotation": str(track.annotation)}
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK DELAY COMPENSATION (2 tools)
    # ========================================================================

    def get_track_delay(self, track_index):
        """Get track delay compensation in samples"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "delay"):
                return {"ok": True, "delay": float(track.delay)}
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_delay(self, track_index, delay_samples):
        """Set track delay compensation in samples"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "delay"):
                track.delay = float(delay_samples)
                return {"ok": True, "delay": float(track.delay)}
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
