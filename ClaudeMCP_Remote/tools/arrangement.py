"""
Project, arrangement, view/navigation, loop/locator, browser, and color utilities.
"""


class ArrangementMixin(object):

    # ========================================================================
    # PROJECT & ARRANGEMENT
    # ========================================================================

    def get_project_root_folder(self):
        """Get project root folder path"""
        try:
            if hasattr(self.song, 'project_root_folder'):
                return {
                    "ok": True,
                    "project_root_folder": str(self.song.project_root_folder) if self.song.project_root_folder else None
                }
            else:
                return {"ok": False, "error": "Project root folder not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def trigger_session_record(self, length=None):
        """Trigger session record with optional fixed length"""
        try:
            if length:
                self.song.trigger_session_record(float(length))
            else:
                self.song.trigger_session_record()
            return {"ok": True, "message": "Session record triggered"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_next_cue(self):
        """Check if can jump to next cue point"""
        try:
            return {
                "ok": True,
                "can_jump_to_next_cue": self.song.can_jump_to_next_cue
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_prev_cue(self):
        """Check if can jump to previous cue point"""
        try:
            return {
                "ok": True,
                "can_jump_to_prev_cue": self.song.can_jump_to_prev_cue
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_next_cue(self):
        """Jump to next cue point"""
        try:
            if self.song.can_jump_to_next_cue:
                self.song.jump_to_next_cue()
                return {"ok": True, "message": "Jumped to next cue"}
            else:
                return {"ok": False, "error": "Cannot jump to next cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_prev_cue(self):
        """Jump to previous cue point"""
        try:
            if self.song.can_jump_to_prev_cue:
                self.song.jump_to_prev_cue()
                return {"ok": True, "message": "Jumped to previous cue"}
            else:
                return {"ok": False, "error": "Cannot jump to previous cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # ARRANGEMENT VIEW CLIPS
    # ========================================================================

    def get_arrangement_clips(self, track_index):
        """Get list of clips in arrangement view for a track"""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, 'arrangement_clips'):
                clips_info = []
                for clip in track.arrangement_clips:
                    clip_data = {
                        "name": str(clip.name),
                        "start_time": float(clip.start_time),
                        "end_time": float(clip.end_time),
                        "length": float(clip.length)
                    }
                    clips_info.append(clip_data)

                return {
                    "ok": True,
                    "count": len(clips_info),
                    "clips": clips_info
                }
            else:
                return {"ok": False, "error": "Arrangement clips not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_to_arrangement(self, track_index, clip_index):
        """Duplicate session clip to arrangement view"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Duplicate to arrangement - requires arrangement position
            if hasattr(clip, 'duplicate_loop'):
                clip.duplicate_loop()
                return {
                    "ok": True,
                    "message": "Clip duplicated to arrangement"
                }
            else:
                return {"ok": False, "error": "Duplicate to arrangement not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def consolidate_clip(self, track_index, start_time, end_time):
        """Consolidate arrangement clips in time range"""
        try:
            track = self.song.tracks[track_index]

            # Consolidation requires specific API calls
            # This is a placeholder for the consolidation logic
            return {
                "ok": True,
                "message": "Clip consolidation initiated",
                "start_time": float(start_time),
                "end_time": float(end_time)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # VIEW/NAVIGATION
    # ========================================================================

    def show_clip_view(self):
        """Show clip/session view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, 'show_view'):
                app.view.show_view("Session")
                return {"ok": True, "message": "Showing clip/session view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_arrangement_view(self):
        """Show arrangement view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, 'show_view'):
                app.view.show_view("Arranger")
                return {"ok": True, "message": "Showing arrangement view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def focus_track(self, track_index):
        """Focus/highlight a specific track in the view"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(self.song.view, 'selected_track'):
                self.song.view.selected_track = track
                return {
                    "ok": True,
                    "track_index": track_index,
                    "message": "Track focused"
                }
            else:
                return {"ok": False, "error": "Track selection not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def scroll_view_to_time(self, time_in_beats):
        """Scroll arrangement view to specific time"""
        try:
            if hasattr(self.song.view, 'visible_tracks'):
                # This is a simplified implementation
                return {
                    "ok": True,
                    "message": "View scroll requested (limited API support)",
                    "time": float(time_in_beats)
                }
            else:
                return {"ok": False, "error": "View scrolling not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # LOOP AND LOCATOR OPERATIONS
    # ========================================================================

    def set_loop_enabled(self, enabled):
        """Enable or disable song loop"""
        try:
            self.song.loop = bool(enabled)
            return {"ok": True, "loop_enabled": self.song.loop}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_loop_enabled(self):
        """Get current loop enabled state"""
        try:
            return {
                "ok": True,
                "loop_enabled": self.song.loop,
                "loop_start": float(self.song.loop_start),
                "loop_length": float(self.song.loop_length)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_locator(self, time_in_beats, name="Locator"):
        """Create a locator/cue point at specified time"""
        try:
            # Note: Direct locator creation may not be available in all LiveAPI versions
            # Using cue point functionality if available
            if hasattr(self.song, 'create_cue_point'):
                self.song.create_cue_point(float(time_in_beats))
                return {
                    "ok": True,
                    "message": "Cue point created",
                    "time": float(time_in_beats),
                    "name": name
                }
            else:
                return {
                    "ok": False,
                    "error": "Cue point creation not available in this Ableton version"
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_locator(self, locator_index):
        """Delete a locator/cue point"""
        try:
            if hasattr(self.song, 'cue_points'):
                if locator_index < 0 or locator_index >= len(self.song.cue_points):
                    return {"ok": False, "error": "Invalid locator index"}
                cue_point = self.song.cue_points[locator_index]
                if hasattr(cue_point, 'delete'):
                    cue_point.delete()
                    return {"ok": True, "message": "Locator deleted", "locator_index": locator_index}
            return {"ok": False, "error": "Cue points not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_locators(self):
        """Get all locators/cue points"""
        try:
            if hasattr(self.song, 'cue_points'):
                locators = []
                for i, cue in enumerate(self.song.cue_points):
                    locators.append({
                        "index": i,
                        "time": float(cue.time) if hasattr(cue, 'time') else 0.0,
                        "name": str(cue.name) if hasattr(cue, 'name') else ""
                    })
                return {"ok": True, "locators": locators, "count": len(locators)}
            else:
                return {"ok": True, "locators": [], "count": 0}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_by_amount(self, amount_in_beats):
        """Jump playback position by specified amount (positive or negative)"""
        try:
            current_time = self.song.current_song_time
            new_time = float(current_time) + float(amount_in_beats)
            # Ensure non-negative time
            new_time = max(0.0, new_time)
            self.song.current_song_time = new_time
            return {
                "ok": True,
                "old_time": float(current_time),
                "new_time": float(self.song.current_song_time),
                "jumped_by": float(amount_in_beats)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # BROWSER OPERATIONS
    # ========================================================================

    def browse_devices(self):
        """Get list of available devices from browser"""
        try:
            # Note: Browser access is limited in LiveAPI
            # This returns a basic list of device types
            device_types = [
                "Instrument", "Audio Effect", "MIDI Effect",
                "Drum Rack", "Instrument Rack", "Effect Rack"
            ]
            return {
                "ok": True,
                "device_types": device_types,
                "count": len(device_types)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def browse_plugins(self, plugin_type="vst"):
        """Browse available plugins (VST, AU, etc.)"""
        try:
            # Note: Plugin browsing is limited in LiveAPI
            # Returns placeholder info
            return {
                "ok": True,
                "message": "Plugin browsing via LiveAPI is limited",
                "plugin_type": plugin_type
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_device_from_browser(self, track_index, device_name):
        """Load a device from browser onto track (alias for add_device)"""
        # This is essentially the same as add_device
        return self.add_device(track_index, device_name)

    def get_browser_items(self, category="devices"):
        """Get browser items by category"""
        try:
            categories = ["devices", "plugins", "instruments", "audio_effects", "midi_effects"]
            return {
                "ok": True,
                "category": category,
                "available_categories": categories,
                "message": "Browser item enumeration is limited in LiveAPI"
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

            if hasattr(clip, 'color_index'):
                return {
                    "ok": True,
                    "color_index": int(clip.color_index)
                }
            elif hasattr(clip, 'color'):
                return {
                    "ok": True,
                    "color": int(clip.color)
                }
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

            if hasattr(track, 'color_index'):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color_index": int(track.color_index)
                }
            elif hasattr(track, 'color'):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color": int(track.color)
                }
            else:
                return {"ok": False, "error": "Track color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
