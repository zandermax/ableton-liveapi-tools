"""
Groove, quantization, and groove pool operations.
"""


class MixingGrooveMixin:
    # ========================================================================
    # GROOVE & QUANTIZATION
    # ========================================================================

    def set_clip_groove_amount(self, track_index, clip_index, amount):
        """Set clip groove amount (0.0-1.0)"""
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
            if hasattr(clip, "groove_amount"):
                clip.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(clip.groove_amount)}
            else:
                return {"ok": False, "error": "Clip does not support groove"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def quantize_clip(self, track_index, clip_index, quantize_to):
        """Quantize MIDI clip to grid"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "quantize"):
                clip.quantize(float(quantize_to), 1.0)
                return {"ok": True, "message": "Clip quantized", "quantize_to": quantize_to}
            else:
                return {"ok": False, "error": "Clip does not support quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def quantize_clip_pitch(self, track_index, clip_index, pitch=60):
        """Quantize MIDI clip pitch"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "quantize_pitch"):
                clip.quantize_pitch(int(pitch), int(pitch), 1.0)
                return {"ok": True, "message": "Clip pitch quantized", "pitch": pitch}
            else:
                return {"ok": False, "error": "Clip does not support pitch quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_groove_amount(self):
        """Get song groove amount"""
        try:
            if hasattr(self.song, "groove_amount"):
                return {"ok": True, "groove_amount": float(self.song.groove_amount)}
            else:
                return {"ok": False, "error": "Song does not support groove_amount"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_groove_amount(self, amount):
        """Set song groove amount (0.0-1.0)"""
        try:
            if hasattr(self.song, "groove_amount"):
                self.song.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(self.song.groove_amount)}
            else:
                return {"ok": False, "error": "Song does not support groove_amount"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # GROOVE POOL
    # ========================================================================

    def get_groove_pool_grooves(self):
        """Get list of grooves in groove pool"""
        try:
            grooves = []

            if hasattr(self.song, "groove_pool"):
                for i, groove in enumerate(self.song.groove_pool):
                    groove_info = {
                        "index": i,
                        "name": str(groove.name) if hasattr(groove, "name") else f"Groove {i}",
                    }

                    if hasattr(groove, "timing_amount"):
                        groove_info["timing_amount"] = float(groove.timing_amount)
                    if hasattr(groove, "random_amount"):
                        groove_info["random_amount"] = float(groove.random_amount)
                    if hasattr(groove, "velocity_amount"):
                        groove_info["velocity_amount"] = float(groove.velocity_amount)

                    grooves.append(groove_info)

            return {"ok": True, "grooves": grooves, "count": len(grooves)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_groove(self, track_index, clip_index, groove_index):
        """Set groove for clip"""
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

            if (
                hasattr(self.song, "groove_pool")
                and groove_index >= 0
                and groove_index < len(self.song.groove_pool)
            ):
                if hasattr(clip, "groove"):
                    clip.groove = self.song.groove_pool[groove_index]
                    return {"ok": True, "message": "Groove set", "groove_index": groove_index}
                else:
                    return {"ok": False, "error": "Clip groove property not available"}
            else:
                return {"ok": False, "error": "Invalid groove index"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
