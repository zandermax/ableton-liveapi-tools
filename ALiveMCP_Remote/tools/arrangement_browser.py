"""
Browser operations and color utility queries.
"""


class ArrangementBrowserMixin:
    # ========================================================================
    # BROWSER OPERATIONS
    # ========================================================================

    def browse_devices(self):
        """Get list of available devices from browser"""
        try:
            device_types = [
                "Instrument",
                "Audio Effect",
                "MIDI Effect",
                "Drum Rack",
                "Instrument Rack",
                "Effect Rack",
            ]
            return {"ok": True, "device_types": device_types, "count": len(device_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def browse_plugins(self, plugin_type="vst"):
        """Browse available plugins (VST, AU, etc.)"""
        try:
            return {
                "ok": True,
                "message": "Plugin browsing via LiveAPI is limited",
                "plugin_type": plugin_type,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_device_from_browser(self, track_index, device_name):
        """Load a device from browser onto track (alias for add_device)"""
        return self.add_device(track_index, device_name)

    def get_browser_items(self, category="devices"):
        """Get browser items by category"""
        try:
            categories = ["devices", "plugins", "instruments", "audio_effects", "midi_effects"]
            return {
                "ok": True,
                "category": category,
                "available_categories": categories,
                "message": "Browser item enumeration is limited in LiveAPI",
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # COLOR UTILITIES
    # ========================================================================

    def get_clip_color(self, track_index, clip_index):
        """Get clip color"""
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
                return {"ok": True, "color_index": int(clip.color_index)}
            elif hasattr(clip, "color"):
                return {"ok": True, "color": int(clip.color)}
            else:
                return {"ok": False, "error": "Clip color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_color(self, track_index):
        """Get track color"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(track, "color_index"):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color_index": int(track.color_index),
                }
            elif hasattr(track, "color"):
                return {"ok": True, "track_index": track_index, "color": int(track.color)}
            else:
                return {"ok": False, "error": "Track color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
