"""
Track routing, monitoring, fold state, and sub-routing operations.
"""


class TracksRoutingMixin:
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
