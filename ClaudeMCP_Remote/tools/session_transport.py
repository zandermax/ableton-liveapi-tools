"""
Session, transport, automation, and metronome operations.
"""

from .session_automation import SessionAutomationMixin


class SessionTransportMixin(SessionAutomationMixin):
    # ========================================================================
    # SESSION CONTROL
    # ========================================================================

    def start_playback(self):
        """Start Ableton playback"""
        try:
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Playback started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_playback(self):
        """Stop Ableton playback"""
        try:
            if self.song.is_playing:
                self.song.stop_playing()
            return {"ok": True, "message": "Playback stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def start_recording(self):
        """Start recording"""
        try:
            self.song.record_mode = True
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Recording started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_recording(self):
        """Stop recording"""
        try:
            self.song.record_mode = False
            return {"ok": True, "message": "Recording stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def continue_playing(self):
        """Continue playback from current position"""
        try:
            self.song.continue_playing()
            return {"ok": True, "message": "Playback continued"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_info(self):
        """Get current session state information"""
        try:
            return {
                "ok": True,
                "is_playing": self.song.is_playing,
                "tempo": float(self.song.tempo),
                "time_signature_numerator": self.song.signature_numerator,
                "time_signature_denominator": self.song.signature_denominator,
                "current_song_time": float(self.song.current_song_time),
                "loop_start": float(self.song.loop_start),
                "loop_end": float(self.song.loop_start + self.song.loop_length),
                "loop_length": float(self.song.loop_length),
                "num_tracks": len(self.song.tracks),
                "num_scenes": len(self.song.scenes),
                "record_mode": self.song.record_mode,
                "metronome": self.song.metronome,
                "nudge_up": self.song.nudge_up,
                "nudge_down": self.song.nudge_down,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_tempo(self, bpm):
        """
        Set session tempo

        Args:
            bpm: Tempo in BPM (20-999)
        """
        try:
            bpm = float(bpm)
            if bpm < 20 or bpm > 999:
                return {"ok": False, "error": "BPM must be between 20 and 999"}
            self.song.tempo = bpm
            return {"ok": True, "message": "Tempo set", "bpm": float(self.song.tempo)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_time_signature(self, numerator, denominator):
        """
        Set time signature

        Args:
            numerator: Top number (1-99)
            denominator: Bottom number (1, 2, 4, 8, 16)
        """
        try:
            numerator = int(numerator)
            denominator = int(denominator)

            if numerator < 1 or numerator > 99:
                return {"ok": False, "error": "Numerator must be between 1 and 99"}
            if denominator not in [1, 2, 4, 8, 16]:
                return {"ok": False, "error": "Denominator must be 1, 2, 4, 8, or 16"}

            self.song.signature_numerator = numerator
            self.song.signature_denominator = denominator

            return {
                "ok": True,
                "message": "Time signature set",
                "numerator": self.song.signature_numerator,
                "denominator": self.song.signature_denominator,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_start(self, position):
        """Set loop start position in beats"""
        try:
            self.song.loop_start = float(position)
            return {"ok": True, "loop_start": float(self.song.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_length(self, length):
        """Set loop length in beats"""
        try:
            self.song.loop_length = float(length)
            return {"ok": True, "loop_length": float(self.song.loop_length)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome(self, enabled):
        """Enable or disable metronome"""
        try:
            self.song.metronome = bool(enabled)
            return {"ok": True, "metronome": self.song.metronome}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def tap_tempo(self):
        """Tap tempo"""
        try:
            self.song.tap_tempo()
            return {"ok": True, "message": "Tempo tapped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def undo(self):
        """Undo last action"""
        try:
            self.song.undo()
            return {"ok": True, "message": "Undo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def redo(self):
        """Redo last undone action"""
        try:
            self.song.redo()
            return {"ok": True, "message": "Redo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
