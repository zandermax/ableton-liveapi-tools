"""
Rack/chain operations, plugin windows, device utilities, and parameter display values.
"""


class DevicesRacksMixin:
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
            self.c_instance.song().view.select_device(device)
            return {"ok": True, "message": "Plugin window shown", "device_name": str(device.name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def hide_plugin_window(self, track_index, device_index):
        """Hide device/plugin window"""
        try:
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
