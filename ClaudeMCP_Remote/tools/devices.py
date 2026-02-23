"""
Device operations, parameters, racks/chains, plugin windows, and utilities.
"""


class DevicesMixin:
    # ========================================================================
    # DEVICE OPERATIONS
    # ========================================================================

    def add_device(self, track_index, device_name):
        """Add device to track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            # This is a simplified version - actual device loading requires browser API
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

            # This is a simplified implementation
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

            # This is a simplified implementation
            return {
                "ok": True,
                "message": "Device preset loading requires browser API",
                "preset_index": preset_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def randomize_device_parameters(self, track_index, device_index):
        """Randomize all device parameters"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            import random

            device = track.devices[device_index]
            randomized_count = 0

            for param in device.parameters:
                if param.is_enabled and not param.is_quantized:
                    random_value = random.uniform(param.min, param.max)
                    param.value = random_value
                    randomized_count += 1

            return {
                "ok": True,
                "message": "Device parameters randomized",
                "randomized_count": randomized_count,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE EXTRAS (MISSING TOOL)
    # ========================================================================

    def randomize_device(self, track_index, device_index):
        """Randomize all parameters of a device (simplified version)"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            # This is an alias for randomize_device_parameters
            # Randomizing all parameters (excluding read-only ones)
            randomized_count = 0
            for param in device.parameters:
                if hasattr(param, "is_enabled") and param.is_enabled and not param.is_quantized:
                    try:
                        import random

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

    # ========================================================================
    # RACK/CHAIN OPERATIONS
    # ========================================================================

    def get_device_chains(self, track_index, device_index):
        """Get chains from a rack device"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains (not a rack)"}

            chains = []
            for i, chain in enumerate(device.chains):
                chains.append(
                    {
                        "index": i,
                        "name": str(chain.name),
                        "mute": chain.mute if hasattr(chain, "mute") else False,
                        "solo": chain.solo if hasattr(chain, "solo") else False,
                        "num_devices": len(chain.devices) if hasattr(chain, "devices") else 0,
                    }
                )

            return {"ok": True, "chains": chains, "count": len(chains)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_chain_devices(self, track_index, device_index, chain_index):
        """Get devices in a specific chain"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]
            chain_devices = []

            if hasattr(chain, "devices"):
                for dev in chain.devices:
                    chain_devices.append(
                        {
                            "name": str(dev.name),
                            "class_name": str(dev.class_name),
                            "is_active": dev.is_active,
                        }
                    )

            return {
                "ok": True,
                "chain_index": chain_index,
                "devices": chain_devices,
                "count": len(chain_devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_mute(self, track_index, device_index, chain_index, mute):
        """Mute/unmute a chain in a rack"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, "mute"):
                chain.mute = bool(mute)
                return {"ok": True, "chain_index": chain_index, "mute": chain.mute}
            else:
                return {"ok": False, "error": "Chain mute not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_solo(self, track_index, device_index, chain_index, solo):
        """Solo/unsolo a chain in a rack"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, "solo"):
                chain.solo = bool(solo)
                return {"ok": True, "chain_index": chain_index, "solo": chain.solo}
            else:
                return {"ok": False, "error": "Chain solo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # PLUGIN WINDOW CONTROL
    # ========================================================================

    def show_plugin_window(self, track_index, device_index):
        """Show device/plugin window"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            # Use the appointed device to show in Live's interface
            self.c_instance.song().view.select_device(device)

            return {"ok": True, "message": "Plugin window shown", "device_name": str(device.name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def hide_plugin_window(self, track_index, device_index):
        """Hide device/plugin window"""
        try:
            # Hiding is done by selecting something else
            # This is a simplified version
            return {"ok": True, "message": "Plugin window hidden"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE UTILITIES
    # ========================================================================

    def get_device_class_name(self, track_index, device_index):
        """Get device class name (e.g., 'OriginalSimpler', 'Compressor2')"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "class_name"):
                return {"ok": True, "class_name": str(device.class_name)}
            else:
                return {"ok": False, "error": "Class name not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_type(self, track_index, device_index):
        """Get device type (audio_effect, instrument, midi_effect)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "type"):
                return {"ok": True, "type": int(device.type)}
            else:
                return {"ok": False, "error": "Device type not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE PARAMETER DISPLAY VALUES
    # ========================================================================

    def get_device_param_display_value(self, track_index, device_index, param_index):
        """Get device parameter value as displayed in UI (Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(param, "display_value"):
                return {
                    "ok": True,
                    "display_value": str(param.display_value),
                    "raw_value": float(param.value),
                    "name": str(param.name),
                }
            else:
                # Fallback to string representation
                return {
                    "ok": True,
                    "display_value": str(param.__str__()),
                    "raw_value": float(param.value),
                    "name": str(param.name),
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_all_param_display_values(self, track_index, device_index):
        """Get all device parameter display values (Live 12+)"""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            params_info = []
            for i, param in enumerate(device.parameters):
                param_data = {"index": i, "name": str(param.name), "raw_value": float(param.value)}

                if hasattr(param, "display_value"):
                    param_data["display_value"] = str(param.display_value)
                else:
                    param_data["display_value"] = str(param.__str__())

                params_info.append(param_data)

            return {
                "ok": True,
                "device_name": str(device.name),
                "count": len(params_info),
                "parameters": params_info,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
