"""
Transport position, automation recording, and metronome volume operations.
"""


class SessionAutomationMixin:
    # ========================================================================
    # TRANSPORT OPERATIONS
    # ========================================================================

    def jump_to_time(self, time_in_beats):
        """Jump playback to specific time in beats"""
        try:
            self.song.current_song_time = float(time_in_beats)
            return {"ok": True, "time": float(self.song.current_song_time)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_current_time(self):
        """Get current playback position in beats"""
        try:
            return {
                "ok": True,
                "current_song_time": float(self.song.current_song_time),
                "is_playing": self.song.is_playing,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_arrangement_overdub(self, enabled):
        """Enable/disable arrangement overdub"""
        try:
            self.song.arrangement_overdub = bool(enabled)
            return {"ok": True, "arrangement_overdub": self.song.arrangement_overdub}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_back_to_arranger(self, enabled):
        """Enable/disable back to arrangement"""
        try:
            self.song.back_to_arranger = bool(enabled)
            return {"ok": True, "back_to_arranger": self.song.back_to_arranger}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_in(self, enabled):
        """Enable/disable punch in recording"""
        try:
            self.song.punch_in = bool(enabled)
            return {"ok": True, "punch_in": self.song.punch_in}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_out(self, enabled):
        """Enable/disable punch out recording"""
        try:
            self.song.punch_out = bool(enabled)
            return {"ok": True, "punch_out": self.song.punch_out}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_up(self):
        """Nudge playback position up"""
        try:
            self.song.nudge_up()
            return {"ok": True, "message": "Nudged up"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_down(self):
        """Nudge playback position down"""
        try:
            self.song.nudge_down()
            return {"ok": True, "message": "Nudged down"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # AUTOMATION OPERATIONS
    # ========================================================================

    def re_enable_automation(self):
        """Re-enable all automation"""
        try:
            self.song.re_enable_automation()
            return {"ok": True, "message": "Automation re-enabled"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_automation_record(self):
        """Get session automation recording state"""
        try:
            return {"ok": True, "session_automation_record": self.song.session_automation_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_automation_record(self, enabled):
        """Enable/disable session automation recording"""
        try:
            self.song.session_automation_record = bool(enabled)
            return {"ok": True, "session_automation_record": self.song.session_automation_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_record(self):
        """Get session record state"""
        try:
            return {"ok": True, "session_record": self.song.session_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_record(self, enabled):
        """Enable/disable session recording"""
        try:
            self.song.session_record = bool(enabled)
            return {"ok": True, "session_record": self.song.session_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def capture_midi(self):
        """Capture MIDI from the last played notes"""
        try:
            self.song.capture_midi()
            return {"ok": True, "message": "MIDI captured"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # METRONOME VOLUME
    # ========================================================================

    def get_metronome_volume(self):
        """Get metronome volume"""
        try:
            if hasattr(self.song, "metronome"):
                return {"ok": True, "volume": float(self.song.metronome)}
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome_volume(self, volume):
        """Set metronome volume (0.0 to 1.0)"""
        try:
            if hasattr(self.song, "metronome"):
                self.song.metronome = float(volume)
                return {"ok": True, "volume": float(self.song.metronome)}
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
