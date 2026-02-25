"""
Core device operations: add, inspect, parameters, presets, and randomization.
"""

import random


class DevicesCoreMixin:
    # ========================================================================
    # DEVICE OPERATIONS
    # ========================================================================

    def add_device(self, track_index, device_name):
        """Add device to track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            return {
                "ok": True,
                "message": "Device add requested (browser API required for full implementation)",
                "device_name": device_name,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_devices(self, track_index):
        """Get all devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            devices = []

            for device in track.devices:
                devices.append(
                    {
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters),
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "devices": devices,
                "count": len(devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_param(self, track_index, device_index, param_index, value):
        """Set device parameter value"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            if param_index < 0 or param_index >= len(device.parameters):
                return {"ok": False, "error": "Invalid parameter index"}

            param = device.parameters[param_index]
            param.value = float(value)

            return {"ok": True, "message": "Parameter set", "value": float(param.value)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE EXTRAS
    # ========================================================================

    def set_device_on_off(self, track_index, device_index, enabled):
        """Turn device on or off"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            if hasattr(device, "is_active"):
                device.is_active = bool(enabled)
                return {"ok": True, "is_active": device.is_active}
            else:
                return {"ok": False, "error": "Device does not support on/off"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_parameters(self, track_index, device_index):
        """Get all parameters for a device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            parameters = []

            for i, param in enumerate(device.parameters):
                parameters.append(
                    {
                        "index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_quantized": param.is_quantized,
                        "is_enabled": param.is_enabled if hasattr(param, "is_enabled") else True,
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "device_index": device_index,
                "parameters": parameters,
                "count": len(parameters),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_parameter_by_name(self, track_index, device_index, param_name):
        """Get device parameter by name"""
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
                        "index": i,
                        "name": str(param.name),
                        "value": float(param.value),
                        "min": float(param.min),
                        "max": float(param.max),
                    }

            return {"ok": False, "error": "Parameter '" + str(param_name) + "' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_parameter_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            for param in device.parameters:
                if str(param.name) == param_name:
                    param.value = float(value)
                    return {"ok": True, "name": str(param.name), "value": float(param.value)}

            return {"ok": False, "error": "Parameter '" + str(param_name) + "' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_device(self, track_index, device_index):
        """Delete device from track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            track.delete_device(device_index)
            return {"ok": True, "message": "Device deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_presets(self, track_index, device_index):
        """Get available presets for device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            return {
                "ok": True,
                "message": "Device preset browsing requires browser API",
                "device_index": device_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_preset(self, track_index, device_index, preset_index):
        """Load preset for device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            return {
                "ok": True,
                "message": "Device preset loading requires browser API",
                "preset_index": preset_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def randomize_device_parameters(self, track_index, device_index):
        """Randomize all device parameters (delegates to randomize_device)"""
        return self.randomize_device(track_index, device_index)

    def randomize_device(self, track_index, device_index):
        """Randomize all parameters of a device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            randomized_count = 0

            for param in device.parameters:
                if hasattr(param, "is_enabled") and param.is_enabled and not param.is_quantized:
                    try:
                        param.value = random.uniform(float(param.min), float(param.max))
                        randomized_count += 1
                    except Exception:
                        pass

            return {
                "ok": True,
                "track_index": track_index,
                "device_index": device_index,
                "device_name": str(device.name),
                "randomized_parameters": randomized_count,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
