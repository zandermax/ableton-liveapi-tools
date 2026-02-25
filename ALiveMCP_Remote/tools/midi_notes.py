"""
MIDI note operations: add, get, remove, select, and extended note queries.
"""


class MidiNotesMixin:
    # ========================================================================
    # MIDI NOTE OPERATIONS
    # ========================================================================

    def add_notes(self, track_index, clip_index, notes):
        """
        Add MIDI notes to a clip

        Args:
            track_index: Track index
            clip_index: Clip slot index on the track
            notes: List of note dicts with keys:
                   - pitch: MIDI note number (0-127)
                   - start: Start time in beats
                   - duration: Note duration in beats
                   - velocity: MIDI velocity (0-127)
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid scene/clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            for note in notes:
                pitch = int(note.get("pitch", 60))
                start = float(note.get("start", 0.0))
                duration = float(note.get("duration", 1.0))
                velocity = int(note.get("velocity", 100))

                if pitch < 0 or pitch > 127:
                    continue
                if velocity < 0 or velocity > 127:
                    continue
                if duration <= 0:
                    continue

                clip.set_notes(((pitch, start, duration, velocity, False),))

            return {
                "ok": True,
                "message": "Notes added",
                "track_index": track_index,
                "clip_index": clip_index,
                "note_count": len(notes),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_notes(self, track_index, clip_index):
        """
        Get all MIDI notes from a clip

        Args:
            track_index: Track index
            clip_index: Clip slot index
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            notes_data = clip.get_notes(0, 0, clip.length, 128)

            notes = []
            for note_tuple in notes_data:
                notes.append(
                    {
                        "pitch": note_tuple[0],
                        "start_time": float(note_tuple[1]),
                        "duration": float(note_tuple[2]),
                        "velocity": note_tuple[3],
                        "muted": note_tuple[4],
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "notes": notes,
                "count": len(notes),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_notes(
        self, track_index, clip_index, pitch_from=0, pitch_to=127, time_from=0.0, time_to=999.0
    ):
        """Remove MIDI notes from clip"""
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
            clip.remove_notes(
                float(time_from),
                int(pitch_from),
                float(time_to - time_from),
                int(pitch_to - pitch_from),
            )
            return {"ok": True, "message": "Notes removed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MIDI NOTE EXTRAS
    # ========================================================================

    def select_all_notes(self, track_index, clip_index):
        """Select all notes in clip"""
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
            clip.select_all_notes()
            return {"ok": True, "message": "All notes selected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def deselect_all_notes(self, track_index, clip_index):
        """Deselect all notes in clip"""
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
            clip.deselect_all_notes()
            return {"ok": True, "message": "All notes deselected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def replace_selected_notes(self, track_index, clip_index, notes):
        """Replace selected notes with new notes"""
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

            note_tuples = []
            for note in notes:
                pitch = int(note.get("pitch", 60))
                start = float(note.get("start", 0.0))
                duration = float(note.get("duration", 1.0))
                velocity = int(note.get("velocity", 100))
                muted = bool(note.get("muted", False))
                note_tuples.append((pitch, start, duration, velocity, muted))

            clip.replace_selected_notes(tuple(note_tuples))
            return {"ok": True, "message": "Selected notes replaced", "note_count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_notes_extended(
        self, track_index, clip_index, start_time, time_span, start_pitch, pitch_span
    ):
        """Get notes with extended filtering options"""
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
            notes_data = clip.get_notes_extended(
                from_time=float(start_time),
                from_pitch=int(start_pitch),
                time_span=float(time_span),
                pitch_span=int(pitch_span),
            )

            notes = []
            for note_tuple in notes_data:
                notes.append(
                    {
                        "pitch": note_tuple[0],
                        "start_time": float(note_tuple[1]),
                        "duration": float(note_tuple[2]),
                        "velocity": note_tuple[3],
                        "muted": note_tuple[4],
                    }
                )

            return {"ok": True, "notes": notes, "count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
