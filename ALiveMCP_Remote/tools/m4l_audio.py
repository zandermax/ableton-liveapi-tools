"""
Audio clip operations: warp, file path, warping, warp markers, and sample/simpler.
"""


class M4LAudioMixin:
    # ========================================================================
    # AUDIO CLIP OPERATIONS
    # ========================================================================

    def get_clip_warp_mode(self, track_index, clip_index):
        """Get audio clip warp mode"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            warp_mode_names = {
                0: "Beats",
                1: "Tones",
                2: "Texture",
                3: "Re-Pitch",
                4: "Complex",
                5: "Complex Pro",
            }

            warp_mode = int(clip.warp_mode) if hasattr(clip, "warp_mode") else 0

            return {
                "ok": True,
                "warp_mode": warp_mode,
                "warp_mode_name": warp_mode_names.get(warp_mode, "Unknown"),
                "warping": clip.warping if hasattr(clip, "warping") else False,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warp_mode(self, track_index, clip_index, warp_mode):
        """Set audio clip warp mode (0-5: Beats, Tones, Texture, Re-Pitch, Complex, Complex Pro)"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, "warp_mode"):
                clip.warp_mode = int(max(0, min(5, warp_mode)))
                return {"ok": True, "warp_mode": int(clip.warp_mode)}
            else:
                return {"ok": False, "error": "Warp mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_file_path(self, track_index, clip_index):
        """Get audio clip file path"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            file_path = ""
            if hasattr(clip, "file_path"):
                file_path = str(clip.file_path)
            elif hasattr(clip, "sample") and hasattr(clip.sample, "file_path"):
                file_path = str(clip.sample.file_path)

            return {"ok": True, "file_path": file_path}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_warping(self, track_index, clip_index, warping):
        """Enable/disable warping for audio clip"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            if hasattr(clip, "warping"):
                clip.warping = bool(warping)
                return {"ok": True, "warping": clip.warping}
            else:
                return {"ok": False, "error": "Warping property not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_warp_markers(self, track_index, clip_index):
        """Get warp markers from audio clip"""
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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            markers = []
            if hasattr(clip, "warp_markers"):
                for marker in clip.warp_markers:
                    markers.append(
                        {
                            "sample_time": float(marker.sample_time)
                            if hasattr(marker, "sample_time")
                            else 0.0,
                            "beat_time": float(marker.beat_time)
                            if hasattr(marker, "beat_time")
                            else 0.0,
                        }
                    )

            return {"ok": True, "markers": markers, "count": len(markers)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SAMPLE/SIMPLER OPERATIONS
    # ========================================================================

    def get_sample_length(self, track_index, clip_index):
        """Get audio sample length for a clip"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "sample_length"):
                return {"ok": True, "sample_length": float(clip.sample_length)}
            else:
                return {"ok": False, "error": "Sample length not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_sample_playback_mode(self, track_index, device_index):
        """Get Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "playback_mode"):
                return {"ok": True, "playback_mode": int(device.playback_mode)}
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_sample_playback_mode(self, track_index, device_index, mode):
        """Set Simpler/Sampler playback mode"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "playback_mode"):
                device.playback_mode = int(mode)
                return {"ok": True, "playback_mode": int(device.playback_mode)}
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
