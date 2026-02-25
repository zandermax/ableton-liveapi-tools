"""
Max for Live device operations: detect, list, set/get parameters, CV Tools.
"""


class M4LDevicesMixin:
    # ========================================================================
    # MAX FOR LIVE (M4L) DEVICE OPERATIONS
    # ========================================================================

    def is_max_device(self, track_index, device_index):
        """Check if device is a Max for Live device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            m4l_classes = ["MxDeviceAudioEffect", "MxDeviceMidiEffect", "MxDeviceInstrument"]
            is_m4l = device.class_name in m4l_classes

            return {
                "ok": True,
                "is_m4l": is_m4l,
                "class_name": str(device.class_name),
                "class_display_name": str(device.class_display_name)
                if hasattr(device, "class_display_name")
                else str(device.class_name),
                "device_name": str(device.name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_m4l_devices(self, track_index):
        """Get all Max for Live devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            m4l_devices = []
            m4l_classes = ["MxDeviceAudioEffect", "MxDeviceMidiEffect", "MxDeviceInstrument"]

            for i, device in enumerate(track.devices):
                if device.class_name in m4l_classes:
                    device_type = self._get_m4l_type(device.class_name)
                    m4l_devices.append(
                        {
                            "index": i,
                            "name": str(device.name),
                            "class_name": str(device.class_name),
                            "type": device_type,
                            "is_active": device.is_active,
                            "num_parameters": len(device.parameters),
                        }
                    )

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "devices": m4l_devices,
                "count": len(m4l_devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _get_m4l_type(self, class_name):
        """Get M4L device type from class name"""
        type_map = {
            "MxDeviceAudioEffect": "audio_effect",
            "MxDeviceMidiEffect": "midi_effect",
            "MxDeviceInstrument": "instrument",
        }
        return type_map.get(class_name, "unknown")

    def set_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name (delegates to set_device_parameter_by_name)"""
        return self.set_device_parameter_by_name(track_index, device_index, param_name, value)

    def get_m4l_param_by_name(self, track_index, device_index, param_name):
        """Get M4L device parameter value by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            for i, param in enumerate(device.parameters):
                if str(param.name) == param_name:
                    return {
                        "ok": True,
                        "param_index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_enabled": param.is_enabled if hasattr(param, "is_enabled") else True,
                    }

            return {"ok": False, "error": f"Parameter '{param_name}' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_cv_tools_devices(self, track_index):
        """Get all CV Tools devices on track (subset of M4L devices)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            cv_devices = []

            for i, device in enumerate(track.devices):
                device_name = str(device.name)
                if "CV" in device_name or "cv" in device_name.lower():
                    cv_devices.append(
                        {
                            "index": i,
                            "name": device_name,
                            "class_name": str(device.class_name),
                            "is_active": device.is_active,
                            "num_parameters": len(device.parameters),
                        }
                    )

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "cv_devices": cv_devices,
                "count": len(cv_devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
