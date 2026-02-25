"""
Live 12 application methods and miscellaneous track/clip/scene property queries.
"""


class Live12PropertiesMixin:
    # ========================================================================
    # APPLICATION METHODS - LIVE 12
    # ========================================================================

    def get_build_id(self):
        """Get Ableton Live build identifier (Live 12+)"""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "get_build_id"):
                return {"ok": True, "build_id": str(app.get_build_id())}
            else:
                return {"ok": False, "error": "get_build_id not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_variant(self):
        """Get Ableton Live variant (Suite, Standard, Intro) (Live 12+)"""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "get_variant"):
                return {"ok": True, "variant": str(app.get_variant())}
            else:
                return {"ok": False, "error": "get_variant not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_message_box(self, message, title="Message"):
        """Show message box dialog to user (Live 12+)"""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "show_message"):
                result = app.show_message(str(message))
                return {
                    "ok": True,
                    "message": "Message shown",
                    "button_pressed": int(result) if result is not None else 0,
                }
            else:
                return {"ok": False, "error": "show_message not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_application_version(self):
        """Get full Ableton Live version information"""
        try:
            import Live

            app = Live.Application.get_application()

            version_info = {
                "ok": True,
                "major_version": int(app.get_major_version()),
                "minor_version": int(app.get_minor_version()),
                "bugfix_version": int(app.get_bugfix_version()),
            }

            if hasattr(app, "get_build_id"):
                version_info["build_id"] = str(app.get_build_id())

            if hasattr(app, "get_variant"):
                version_info["variant"] = str(app.get_variant())

            return version_info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # MISSING TRACK/CLIP/SCENE PROPERTIES
    # ========================================================================

    def get_clip_start_time(self, track_index, clip_index):
        """Get clip start time (observable in Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "start_time"):
                return {"ok": True, "start_time": float(clip.start_time)}
            else:
                return {"ok": False, "error": "start_time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_start_time(self, track_index, clip_index, start_time):
        """Set clip start time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "start_time"):
                clip.start_time = float(start_time)
                return {"ok": True, "start_time": float(clip.start_time)}
            else:
                return {"ok": False, "error": "start_time not settable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_foldable(self, track_index):
        """Check if track can be folded (group tracks)"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "is_foldable"):
                return {"ok": True, "is_foldable": bool(track.is_foldable)}
            else:
                return {"ok": False, "error": "is_foldable not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_frozen(self, track_index):
        """Check if track is currently frozen"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "is_frozen"):
                return {"ok": True, "is_frozen": bool(track.is_frozen)}
            else:
                return {"ok": False, "error": "is_frozen not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_is_empty(self, scene_index):
        """Check if scene has no clips"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, "is_empty"):
                return {"ok": True, "is_empty": bool(scene.is_empty)}
            else:
                is_empty = True
                for track in self.song.tracks:
                    if track.clip_slots[scene_index].has_clip:
                        is_empty = False
                        break

                return {"ok": True, "is_empty": is_empty}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_tempo(self, scene_index):
        """Get scene tempo override (if set)"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, "tempo"):
                return {
                    "ok": True,
                    "tempo": float(scene.tempo) if scene.tempo else None,
                    "has_tempo": bool(scene.tempo),
                }
            else:
                return {"ok": False, "error": "Scene tempo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_arrangement_overdub(self):
        """Get arrangement overdub state"""
        try:
            if hasattr(self.song, "arrangement_overdub"):
                return {"ok": True, "arrangement_overdub": bool(self.song.arrangement_overdub)}
            else:
                return {"ok": False, "error": "arrangement_overdub not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_record_mode(self, mode):
        """Set session/arrangement record mode (0=session, 1=arrangement)"""
        try:
            if hasattr(self.song, "record_mode"):
                self.song.record_mode = int(mode)
                return {"ok": True, "record_mode": int(self.song.record_mode)}
            else:
                return {"ok": False, "error": "record_mode not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_numerator(self):
        """Get global time signature numerator"""
        try:
            if hasattr(self.song, "signature_numerator"):
                return {"ok": True, "signature_numerator": int(self.song.signature_numerator)}
            else:
                return {"ok": False, "error": "signature_numerator not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_signature_denominator(self):
        """Get global time signature denominator"""
        try:
            if hasattr(self.song, "signature_denominator"):
                return {"ok": True, "signature_denominator": int(self.song.signature_denominator)}
            else:
                return {"ok": False, "error": "signature_denominator not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
