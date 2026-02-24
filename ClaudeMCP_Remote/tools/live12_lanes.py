"""
Take lane operations (Live 12+).
"""


class Live12LanesMixin:
    # ========================================================================
    # TAKE LANES SUPPORT - LIVE 12
    # ========================================================================

    def get_take_lanes(self, track_index):
        """Get all take lanes for a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "take_lanes"):
                lanes_info = []
                for i, lane in enumerate(track.take_lanes):
                    lane_data = {
                        "index": i,
                        "name": str(lane.name) if hasattr(lane, "name") else "Take " + str(i + 1),
                    }
                    lanes_info.append(lane_data)

                return {"ok": True, "count": len(lanes_info), "take_lanes": lanes_info}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_take_lane(self, track_index, name=None):
        """Create new take lane on a track (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "create_take_lane"):
                lane = track.create_take_lane()
                if name and hasattr(lane, "name"):
                    lane.name = str(name)

                return {
                    "ok": True,
                    "message": "Take lane created",
                    "name": str(lane.name) if hasattr(lane, "name") else "New Take",
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_take_lane_name(self, track_index, lane_index):
        """Get take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "take_lanes"):
                lane = track.take_lanes[lane_index]
                return {
                    "ok": True,
                    "name": str(lane.name)
                    if hasattr(lane, "name")
                    else "Take " + str(lane_index + 1),
                }
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_take_lane_name(self, track_index, lane_index, name):
        """Set take lane name (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "take_lanes"):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, "name"):
                    lane.name = str(name)
                    return {"ok": True, "name": str(lane.name)}
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

            if hasattr(track, "take_lanes"):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, "create_audio_clip"):
                    lane.create_audio_clip(float(length))
                    return {
                        "ok": True,
                        "message": "Audio clip created in take lane",
                        "length": float(length),
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

            if hasattr(track, "take_lanes"):
                lane = track.take_lanes[lane_index]
                if hasattr(lane, "create_midi_clip"):
                    lane.create_midi_clip(float(length))
                    return {
                        "ok": True,
                        "message": "MIDI clip created in take lane",
                        "length": float(length),
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

            if hasattr(track, "take_lanes"):
                lane = track.take_lanes[lane_index]
                clips_info = []

                if hasattr(lane, "clips"):
                    for clip in lane.clips:
                        clip_data = {
                            "name": str(clip.name),
                            "length": float(clip.length),
                            "is_midi": clip.is_midi_clip,
                        }
                        clips_info.append(clip_data)

                return {"ok": True, "count": len(clips_info), "clips": clips_info}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_take_lane(self, track_index, lane_index):
        """Delete a take lane (Live 12+)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "delete_take_lane"):
                track.delete_take_lane(lane_index)
                return {"ok": True, "message": "Take lane deleted"}
            else:
                return {"ok": False, "error": "Take lanes not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
