"""
Core track management: create, delete, rename, volume, pan, arm, solo, mute, info, color.
"""


class TracksCoreMixin:
    # ========================================================================
    # TRACK MANAGEMENT
    # ========================================================================

    def create_midi_track(self, name=None):
        """Create a new MIDI track"""
        try:
            track_index = len(self.song.tracks)
            self.song.create_midi_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "MIDI track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_track(self, name=None):
        """Create a new audio track"""
        try:
            track_index = len(self.song.tracks)
            self.song.create_audio_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Audio track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_return_track(self):
        """Create a new return track"""
        try:
            self.song.create_return_track()
            return_index = len(self.song.return_tracks) - 1
            return {"ok": True, "message": "Return track created", "return_index": return_index}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_track(self, track_index):
        """Delete track by index"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.delete_track(track_index)
            return {"ok": True, "message": "Track deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_track(self, track_index):
        """Duplicate track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.duplicate_track(track_index)
            return {"ok": True, "message": "Track duplicated", "new_index": track_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_track(self, track_index, name):
        """Rename track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].name = str(name)
            return {"ok": True, "message": "Track renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_volume(self, track_index, volume):
        """Set track volume (0.0 to 1.0)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            volume = float(volume)
            if volume < 0.0 or volume > 1.0:
                return {"ok": False, "error": "Volume must be between 0.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.volume.value = volume

            return {
                "ok": True,
                "message": "Track volume set",
                "track_index": track_index,
                "volume": float(track.mixer_device.volume.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_pan(self, track_index, pan):
        """Set track pan (-1.0 to 1.0)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            pan = float(pan)
            if pan < -1.0 or pan > 1.0:
                return {"ok": False, "error": "Pan must be between -1.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.panning.value = pan

            return {
                "ok": True,
                "message": "Track pan set",
                "track_index": track_index,
                "pan": float(track.mixer_device.panning.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def arm_track(self, track_index, armed=True):
        """Arm or disarm track for recording"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if track.can_be_armed:
                track.arm = bool(armed)
                return {
                    "ok": True,
                    "message": "Track armed" if armed else "Track disarmed",
                    "armed": track.arm,
                }
            else:
                return {"ok": False, "error": "Track cannot be armed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def solo_track(self, track_index, solo=True):
        """Solo or unsolo track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].solo = bool(solo)
            return {"ok": True, "message": "Track soloed" if solo else "Track unsoloed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def mute_track(self, track_index, mute=True):
        """Mute or unmute track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].mute = bool(mute)
            return {"ok": True, "message": "Track muted" if mute else "Track unmuted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_info(self, track_index):
        """Get detailed track information"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            return {
                "ok": True,
                "track_index": track_index,
                "name": str(track.name),
                "color": track.color if hasattr(track, "color") else None,
                "is_foldable": track.is_foldable,
                "mute": track.mute,
                "solo": track.solo,
                "arm": track.arm if track.can_be_armed else False,
                "has_midi_input": track.has_midi_input,
                "has_audio_input": track.has_audio_input,
                "volume": float(track.mixer_device.volume.value),
                "pan": float(track.mixer_device.panning.value),
                "num_devices": len(track.devices),
                "num_clips": len([cs for cs in track.clip_slots if cs.has_clip]),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_color(self, track_index, color_index):
        """Set track color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if hasattr(track, "color"):
                track.color = int(color_index)
                return {"ok": True, "message": "Track color set", "color": track.color}
            else:
                return {"ok": False, "error": "Track color not supported"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
