"""
MIDI CC and program change operations.
"""


class MidiCCMixin:
    # ========================================================================
    # MIDI CC/PROGRAM CHANGE
    # ========================================================================

    def send_midi_cc(self, track_index, cc_number, cc_value, channel=0):
        """Send MIDI CC message to a track"""
        try:
            status_byte = 176 + int(channel)
            midi_bytes = (int(status_byte), int(cc_number), int(cc_value))

            if hasattr(self.song, "send_midi"):
                self.song.send_midi(midi_bytes)
                return {
                    "ok": True,
                    "cc_number": int(cc_number),
                    "cc_value": int(cc_value),
                    "channel": int(channel),
                    "message": "MIDI CC sent",
                }
            else:
                return {"ok": False, "error": "send_midi not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_program_change(self, track_index, program_number, channel=0):
        """Send MIDI Program Change message to a track"""
        try:
            status_byte = 192 + int(channel)
            midi_bytes = (int(status_byte), int(program_number))

            if hasattr(self.song, "send_midi"):
                self.song.send_midi(midi_bytes)
                return {
                    "ok": True,
                    "program_number": int(program_number),
                    "channel": int(channel),
                    "message": "MIDI Program Change sent",
                }
            else:
                return {"ok": False, "error": "send_midi not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
