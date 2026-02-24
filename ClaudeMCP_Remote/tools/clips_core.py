"""
Core clip operations: create, delete, duplicate, launch, stop, info, and name.
"""


class ClipsCoreMixin:
    # ========================================================================
    # CLIP OPERATIONS
    # ========================================================================

    def create_midi_clip(self, track_index, scene_index, length=4.0):
        """Create a new MIDI clip"""
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
