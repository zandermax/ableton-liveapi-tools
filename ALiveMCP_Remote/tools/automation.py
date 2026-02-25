"""
Clip automation envelope operations.
"""


class AutomationMixin:
    # ========================================================================
    # CLIP AUTOMATION ENVELOPES (6 tools)
    # ========================================================================

    def get_clip_automation_envelope(self, track_index, clip_index, device_index, param_index):
        """Get automation envelope for a device parameter in a clip"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter
            device = track.devices[device_index]
            param = device.parameters[param_index]

            # Get automation envelope for this parameter
            if hasattr(clip, "automation_envelope"):
                envelope = clip.automation_envelope(param)

                if envelope:
                    return {
                        "ok": True,
                        "has_envelope": True,
                        "parameter_name": str(param.name),
                        "device_name": str(device.name),
                    }
                else:
                    return {
                        "ok": True,
                        "has_envelope": False,
                        "parameter_name": str(param.name),
                        "message": "No automation envelope for this parameter",
                    }
            else:
                return {"ok": False, "error": "automation_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_automation_envelope(self, track_index, clip_index, device_index, param_index):
        """Create automation envelope for a device parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter
            device = track.devices[device_index]
            param = device.parameters[param_index]

            # Create automation envelope
            if hasattr(clip, "create_automation_envelope"):
                clip.create_automation_envelope(param)
                return {
                    "ok": True,
                    "parameter_name": str(param.name),
                    "device_name": str(device.name),
                    "message": "Automation envelope created",
                }
            else:
                return {"ok": False, "error": "create_automation_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def clear_automation_envelope(self, track_index, clip_index, device_index, param_index):
        """Clear automation envelope for a device parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter
            device = track.devices[device_index]
            param = device.parameters[param_index]

            # Clear automation envelope
            if hasattr(clip, "clear_envelope"):
                clip.clear_envelope(param)
                return {
                    "ok": True,
                    "parameter_name": str(param.name),
                    "message": "Automation envelope cleared",
                }
            else:
                return {"ok": False, "error": "clear_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def insert_automation_step(
        self, track_index, clip_index, device_index, param_index, time, value
    ):
        """Insert automation step/breakpoint at specific time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter and envelope
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(clip, "automation_envelope"):
                envelope = clip.automation_envelope(param)
                if envelope and hasattr(envelope, "insert_step"):
                    envelope.insert_step(float(time), float(value))
                    return {
                        "ok": True,
                        "time": float(time),
                        "value": float(value),
                        "parameter_name": str(param.name),
                        "message": "Automation step inserted",
                    }
                else:
                    return {"ok": False, "error": "No envelope or insert_step not available"}
            else:
                return {"ok": False, "error": "automation_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_automation_step(self, track_index, clip_index, device_index, param_index, time):
        """Remove automation step/breakpoint at specific time"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter and envelope
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(clip, "automation_envelope"):
                envelope = clip.automation_envelope(param)
                if envelope and hasattr(envelope, "remove_step"):
                    envelope.remove_step(float(time))
                    return {
                        "ok": True,
                        "time": float(time),
                        "parameter_name": str(param.name),
                        "message": "Automation step removed",
                    }
                else:
                    return {"ok": False, "error": "No envelope or remove_step not available"}
            else:
                return {"ok": False, "error": "automation_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_automation_envelope_values(self, track_index, clip_index, device_index, param_index):
        """Get all automation envelope values for a parameter"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            # Get the device parameter and envelope
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(clip, "automation_envelope"):
                envelope = clip.automation_envelope(param)
                if envelope:
                    # Get envelope value at different time points
                    # Note: Full implementation would iterate through all steps
                    return {
                        "ok": True,
                        "parameter_name": str(param.name),
                        "has_envelope": True,
                        "message": "Use insert_step/remove_step to modify automation",
                    }
                else:
                    return {
                        "ok": True,
                        "parameter_name": str(param.name),
                        "has_envelope": False,
                        "message": "No automation envelope for this parameter",
                    }
            else:
                return {"ok": False, "error": "automation_envelope not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
