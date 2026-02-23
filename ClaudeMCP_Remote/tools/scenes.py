"""
Scene operations and scene color management.
"""


class ScenesMixin:
    # ========================================================================
    # SCENE OPERATIONS
    # ========================================================================

    def create_scene(self, name=None):
        """Create a new scene"""
        try:
            scene_index = len(self.song.scenes)
            self.song.create_scene(scene_index)

            if name:
                self.song.scenes[scene_index].name = str(name)

            return {
                "ok": True,
                "message": "Scene created",
                "scene_index": scene_index,
                "name": str(self.song.scenes[scene_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_scene(self, scene_index):
        """Delete scene by index"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.delete_scene(scene_index)
            return {"ok": True, "message": "Scene deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_scene(self, scene_index):
        """Duplicate scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.duplicate_scene(scene_index)
            return {"ok": True, "message": "Scene duplicated", "new_index": scene_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def launch_scene(self, scene_index):
        """Launch a scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.scenes[scene_index].fire()
            return {"ok": True, "message": "Scene launched", "scene_index": scene_index}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_scene(self, scene_index, name):
        """Rename scene"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            self.song.scenes[scene_index].name = str(name)
            return {"ok": True, "message": "Scene renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_scene_info(self, scene_index):
        """Get scene information"""
        try:
            if scene_index < 0 or scene_index >= len(self.song.scenes):
                return {"ok": False, "error": "Invalid scene index"}

            scene = self.song.scenes[scene_index]
            return {
                "ok": True,
                "scene_index": scene_index,
                "name": str(scene.name),
                "color": scene.color if hasattr(scene, "color") else None,
                "tempo": float(scene.tempo) if hasattr(scene, "tempo") else None,
                "time_signature_numerator": scene.time_signature_numerator
                if hasattr(scene, "time_signature_numerator")
                else None,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # SCENE COLOR (2 tools)
    # ========================================================================

    def get_scene_color(self, scene_index):
        """Get scene color index"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, "color"):
                return {"ok": True, "color": int(scene.color)}
            else:
                return {"ok": False, "error": "Scene color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_scene_color(self, scene_index, color_index):
        """Set scene color index"""
        try:
            scene = self.song.scenes[scene_index]

            if hasattr(scene, "color"):
                scene.color = int(color_index)
                return {"ok": True, "color": int(scene.color)}
            else:
                return {"ok": False, "error": "Scene color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
