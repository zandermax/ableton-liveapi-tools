"""
Clip property setters: looping, loop points, markers, mute, gain, pitch, signature, and color.
"""


class ClipsPropertiesMixin:
    # ========================================================================
    # CLIP EXTRAS
    # ========================================================================

    def set_clip_looping(self, track_index, clip_index, looping):
        """Enable/disable clip looping"""
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
            clip.looping = bool(looping)
            return {"ok": True, "looping": clip.looping}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_start(self, track_index, clip_index, loop_start):
        """Set clip loop start position"""
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
            clip.loop_start = float(loop_start)
            return {"ok": True, "loop_start": float(clip.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_end(self, track_index, clip_index, loop_end):
        """Set clip loop end position"""
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
            clip.loop_end = float(loop_end)
            return {"ok": True, "loop_end": float(clip.loop_end)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_start_marker(self, track_index, clip_index, start_marker):
        """Set clip start marker"""
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
            clip.start_marker = float(start_marker)
            return {"ok": True, "start_marker": float(clip.start_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_end_marker(self, track_index, clip_index, end_marker):
        """Set clip end marker"""
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
            clip.end_marker = float(end_marker)
            return {"ok": True, "end_marker": float(clip.end_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_muted(self, track_index, clip_index, muted):
        """Mute or unmute clip"""
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
            clip.muted = bool(muted)
            return {"ok": True, "muted": clip.muted}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_gain(self, track_index, clip_index, gain):
        """Set clip gain/volume"""
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
            if hasattr(clip, "gain"):
                clip.gain = float(gain)
                return {"ok": True, "gain": float(clip.gain)}
            else:
                return {"ok": False, "error": "Clip does not support gain"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_coarse(self, track_index, clip_index, semitones):
        """Transpose clip by semitones"""
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
            if hasattr(clip, "pitch_coarse"):
                clip.pitch_coarse = int(semitones)
                return {"ok": True, "pitch_coarse": clip.pitch_coarse}
            else:
                return {"ok": False, "error": "Clip does not support pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_fine(self, track_index, clip_index, cents):
        """Fine-tune clip pitch in cents"""
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
            if hasattr(clip, "pitch_fine"):
                clip.pitch_fine = int(cents)
                return {"ok": True, "pitch_fine": clip.pitch_fine}
            else:
                return {"ok": False, "error": "Clip does not support fine pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_signature_numerator(self, track_index, clip_index, numerator):
        """Set clip time signature numerator"""
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
            clip.signature_numerator = int(numerator)
            return {"ok": True, "signature_numerator": clip.signature_numerator}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP COLOR
    # ========================================================================

    def set_clip_color(self, track_index, clip_index, color_index):
        """Set clip color"""
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

            if hasattr(clip, "color_index"):
                clip.color_index = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color_index": int(color_index),
                }
            elif hasattr(clip, "color"):
                clip.color = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color": int(color_index),
                }
            else:
                return {"ok": False, "error": "Clip color not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
