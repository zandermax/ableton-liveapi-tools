"""
Clip operations, extras, color, annotations, fades, RAM mode, and follow actions.
"""


class ClipsMixin:
    # ========================================================================
    # CLIP OPERATIONS
    # ========================================================================

    def create_midi_clip(self, track_index, scene_index, length=4.0):
        """
        Create a new MIDI clip

        Args:
            track_index: Track index
            scene_index: Scene index
            length: Clip length in bars (default: 4.0)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            clip_slot = track.clip_slots[scene_index]

            if clip_slot.has_clip:
                return {"ok": False, "error": "Clip slot already has a clip"}

            # Create clip
            clip_slot.create_clip(float(length))

            return {
                "ok": True,
                "message": "MIDI clip created",
                "track_index": track_index,
                "scene_index": scene_index,
                "length": float(length),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_clip(self, track_index, scene_index):
        """Delete clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.delete_clip()
            return {"ok": True, "message": "Clip deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_clip(self, track_index, scene_index):
        """Duplicate clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.duplicate_clip_to(clip_slot)
            return {"ok": True, "message": "Clip duplicated"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def launch_clip(self, track_index, scene_index):
        """Launch clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.fire()
            return {"ok": True, "message": "Clip launched"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_clip(self, track_index, scene_index):
        """Stop clip"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].stop_all_clips()
            return {"ok": True, "message": "Clip stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_all_clips(self):
        """Stop all playing clips"""
        try:
            self.song.stop_all_clips()
            return {"ok": True, "message": "All clips stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_info(self, track_index, scene_index):
        """Get clip information"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            return {
                "ok": True,
                "name": str(clip.name),
                "length": float(clip.length),
                "loop_start": float(clip.loop_start),
                "loop_end": float(clip.loop_end),
                "is_midi_clip": clip.is_midi_clip,
                "is_audio_clip": clip.is_audio_clip,
                "is_playing": clip.is_playing,
                "muted": clip.muted,
                "color": clip.color if hasattr(clip, "color") else None,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_name(self, track_index, scene_index, name):
        """Set clip name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            clip_slot = self.song.tracks[track_index].clip_slots[scene_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip_slot.clip.name = str(name)
            return {"ok": True, "message": "Clip renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

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

            # Set color if available
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
    # CLIP FADE IN/OUT (4 tools)
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
    # CLIP RAM MODE (2 tools)
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
