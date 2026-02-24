"""
Clip extras: annotations, fades, RAM mode, and follow actions.
"""


class ClipsExtrasMixin:
    # ========================================================================
    # CLIP ANNOTATIONS
    # ========================================================================

    def get_clip_annotation(self, track_index, clip_index):
        """Get clip annotation text"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "annotation"):
                return {"ok": True, "annotation": str(clip.annotation)}
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_annotation(self, track_index, clip_index, annotation_text):
        """Set clip annotation text"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "annotation"):
                clip.annotation = str(annotation_text)
                return {"ok": True, "annotation": str(clip.annotation)}
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP FADE IN/OUT
    # ========================================================================

    def get_clip_fade_in(self, track_index, clip_index):
        """Get clip fade in time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_in_time"):
                return {"ok": True, "fade_in_time": float(clip.fade_in_time)}
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_in(self, track_index, clip_index, fade_time):
        """Set clip fade in time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_in_time"):
                clip.fade_in_time = float(fade_time)
                return {"ok": True, "fade_in_time": float(clip.fade_in_time)}
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_fade_out(self, track_index, clip_index):
        """Get clip fade out time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_out_time"):
                return {"ok": True, "fade_out_time": float(clip.fade_out_time)}
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_out(self, track_index, clip_index, fade_time):
        """Set clip fade out time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_out_time"):
                clip.fade_out_time = float(fade_time)
                return {"ok": True, "fade_out_time": float(clip.fade_out_time)}
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP RAM MODE
    # ========================================================================

    def get_clip_ram_mode(self, track_index, clip_index):
        """Get clip RAM mode setting"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "ram_mode"):
                return {"ok": True, "ram_mode": bool(clip.ram_mode)}
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_ram_mode(self, track_index, clip_index, ram_mode):
        """Set clip RAM mode (load into RAM vs stream from disk)"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "ram_mode"):
                clip.ram_mode = bool(ram_mode)
                return {"ok": True, "ram_mode": bool(clip.ram_mode)}
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # FOLLOW ACTIONS
    # ========================================================================

    def get_clip_follow_action(self, track_index, clip_index):
        """Get clip follow action settings"""
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

            action_names = {
                0: "Stop",
                1: "Play Again",
                2: "Previous",
                3: "Next",
                4: "First",
                5: "Last",
                6: "Any",
                7: "Other",
                8: "Jump",
            }

            result = {"ok": True, "track_index": track_index, "clip_index": clip_index}

            if hasattr(clip, "follow_action_A"):
                result["follow_action_A"] = int(clip.follow_action_A)
                result["follow_action_A_name"] = action_names.get(
                    int(clip.follow_action_A), "Unknown"
                )

            if hasattr(clip, "follow_action_B"):
                result["follow_action_B"] = int(clip.follow_action_B)
                result["follow_action_B_name"] = action_names.get(
                    int(clip.follow_action_B), "Unknown"
                )

            if hasattr(clip, "follow_action_time"):
                result["follow_action_time"] = float(clip.follow_action_time)

            if hasattr(clip, "follow_action_chance_A"):
                result["follow_action_chance_A"] = float(clip.follow_action_chance_A)

            if hasattr(clip, "follow_action_chance_B"):
                result["follow_action_chance_B"] = float(clip.follow_action_chance_B)

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_follow_action(self, track_index, clip_index, action_A, action_B, chance_A=1.0):
        """Set clip follow action (0-8: Stop, Play Again, Previous, Next, First, Last, Any, Other, Jump)"""
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

            if hasattr(clip, "follow_action_A"):
                clip.follow_action_A = int(max(0, min(8, action_A)))

            if hasattr(clip, "follow_action_B"):
                clip.follow_action_B = int(max(0, min(8, action_B)))

            if hasattr(clip, "follow_action_chance_A"):
                clip.follow_action_chance_A = float(max(0.0, min(1.0, chance_A)))

            if hasattr(clip, "follow_action_chance_B"):
                clip.follow_action_chance_B = 1.0 - float(max(0.0, min(1.0, chance_A)))

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "follow_action_A": int(clip.follow_action_A)
                if hasattr(clip, "follow_action_A")
                else None,
                "follow_action_B": int(clip.follow_action_B)
                if hasattr(clip, "follow_action_B")
                else None,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_follow_action_time(self, track_index, clip_index, time_in_bars):
        """Set follow action time in bars"""
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

            if hasattr(clip, "follow_action_time"):
                clip.follow_action_time = float(max(0.0, time_in_bars))
                return {"ok": True, "follow_action_time": float(clip.follow_action_time)}
            else:
                return {"ok": False, "error": "Follow action time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
