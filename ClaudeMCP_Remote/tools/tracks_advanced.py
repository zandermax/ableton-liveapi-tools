"""
Track groups, freeze/flatten, annotations, and delay compensation.
"""


class TracksAdvancedMixin:
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

            self.song.create_group_track(end_index + 1)

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

            return {
                "ok": True,
                "message": "Ungroup operation requested (may require manual implementation)",
                "group_track_index": group_track_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # TRACK FREEZE/FLATTEN
    # ========================================================================

    def freeze_track(self, track_index):
        """Freeze a track to reduce CPU usage"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "freeze_available") and track.freeze_available:
                if hasattr(track, "freeze_state"):
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
    # TRACK ANNOTATIONS
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
    # TRACK DELAY COMPENSATION
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
