"""
Mixing operations: sends, master track, return tracks, crossfader, groove, and quantization.
"""

from .mixing_groove import MixingGrooveMixin


class MixingMixin(MixingGrooveMixin):
    # ========================================================================
    # SEND OPERATIONS
    # ========================================================================

    def set_track_send(self, track_index, send_index, value):
        """Set track send level"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            sends = track.mixer_device.sends

            if send_index < 0 or send_index >= len(sends):
                return {"ok": False, "error": "Invalid send index"}

            sends[send_index].value = float(value)
            return {"ok": True, "send_index": send_index, "value": float(sends[send_index].value)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_sends(self, track_index):
        """Get all send levels for track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            sends = []

            for i, send in enumerate(track.mixer_device.sends):
                sends.append(
                    {
                        "index": i,
                        "value": float(send.value),
                        "name": str(send.name) if hasattr(send, "name") else "Send " + chr(65 + i),
                    }
                )

            return {"ok": True, "track_index": track_index, "sends": sends, "count": len(sends)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MASTER TRACK CONTROL
    # ========================================================================

    def get_master_track_info(self):
        """Get master track information"""
        try:
            master = self.song.master_track

            info = {
                "ok": True,
                "name": str(master.name),
                "volume": float(master.mixer_device.volume.value)
                if hasattr(master, "mixer_device")
                else 0.0,
                "pan": float(master.mixer_device.panning.value)
                if hasattr(master, "mixer_device")
                else 0.0,
                "num_devices": len(master.devices) if hasattr(master, "devices") else 0,
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_volume(self, volume):
        """Set master track volume (0.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device"):
                master.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))
                return {"ok": True, "volume": float(master.mixer_device.volume.value)}
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_pan(self, pan):
        """Set master track pan (-1.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device"):
                master.mixer_device.panning.value = float(max(-1.0, min(1.0, pan)))
                return {"ok": True, "pan": float(master.mixer_device.panning.value)}
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_master_devices(self):
        """Get all devices on master track"""
        try:
            master = self.song.master_track
            devices = []

            if hasattr(master, "devices"):
                for device in master.devices:
                    devices.append(
                        {
                            "name": str(device.name),
                            "class_name": str(device.class_name),
                            "is_active": device.is_active,
                        }
                    )

            return {"ok": True, "devices": devices, "count": len(devices)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # RETURN TRACK OPERATIONS
    # ========================================================================

    def get_return_track_count(self):
        """Get number of return tracks"""
        try:
            return {"ok": True, "count": len(self.song.return_tracks)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_return_track_info(self, return_index):
        """Get return track information"""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]

            info = {
                "ok": True,
                "index": return_index,
                "name": str(return_track.name),
                "volume": float(return_track.mixer_device.volume.value),
                "pan": float(return_track.mixer_device.panning.value),
                "mute": return_track.mute,
                "solo": return_track.solo,
                "num_devices": len(return_track.devices),
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_return_track_volume(self, return_index, volume):
        """Set return track volume"""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]
            return_track.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))

            return {
                "ok": True,
                "return_index": return_index,
                "volume": float(return_track.mixer_device.volume.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CROSSFADER
    # ========================================================================

    def get_crossfader_assignment(self, track_index):
        """Get track crossfader assignment (0=None, 1=A, 2=B)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            assignment_names = {0: "None", 1: "A", 2: "B"}

            if hasattr(track, "mixer_device") and hasattr(track.mixer_device, "crossfade_assign"):
                assignment = int(track.mixer_device.crossfade_assign)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": assignment,
                    "assignment_name": assignment_names.get(assignment, "Unknown"),
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_crossfader_assignment(self, track_index, assignment):
        """Set track crossfader assignment (0=None, 1=A, 2=B)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, "mixer_device") and hasattr(track.mixer_device, "crossfade_assign"):
                track.mixer_device.crossfade_assign = int(max(0, min(2, assignment)))
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": int(track.mixer_device.crossfade_assign),
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_crossfader_position(self):
        """Get master crossfader position (-1.0 to 1.0)"""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device") and hasattr(master.mixer_device, "crossfader"):
                return {"ok": True, "position": float(master.mixer_device.crossfader.value)}
            else:
                return {"ok": False, "error": "Crossfader not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
