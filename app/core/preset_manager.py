# core/presets_manager.py

import json
from pathlib import Path


class PresetManager:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

        self.current_preset = None
        self.current_preset_data = None

    def ensure_default_preset(self):
        path = self.folder / "default.json"
        if not path.exists():
            data = {
                "name": "default",
                "keys": [
                    {"type": "none", "value": ""} for _ in range(12)
                ]
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    def load_preset(self, name):
        path = self.folder / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Preset not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            self.current_preset_data = json.load(f)

        self.current_preset = name
        return self.current_preset_data

    def save_preset(self, name):
        path = self.folder / f"{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.current_preset_data, f, indent=4)

    def list_presets(self):
        return sorted(p.stem for p in self.folder.glob("*.json"))

    def get_next_preset(self):
        presets = self.list_presets()
        if not presets or self.current_preset not in presets:
            return None
        idx = presets.index(self.current_preset)
        return presets[(idx + 1) % len(presets)]

    def get_prev_preset(self):
        presets = self.list_presets()
        if not presets or self.current_preset not in presets:
            return None
        idx = presets.index(self.current_preset)
        return presets[(idx - 1) % len(presets)]

    def create_preset(self, name):
        path = self.folder / f"{name}.json"
        data = {
            "name": name,
            "keys": [
                {"type": "none", "value": ""} for _ in range(12)
            ]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def delete_preset(self, name):
        path = self.folder / f"{name}.json"
        if path.exists():
            path.unlink()
        if self.current_preset == name:
            self.current_preset = None
            self.current_preset_data = None

    def rename_preset(self, old_name, new_name):
        old_path = self.folder / f"{old_name}.json"
        new_path = self.folder / f"{new_name}.json"
        if not old_path.exists():
            return
        old_path.rename(new_path)
        if self.current_preset == old_name:
            self.current_preset = new_name
            if self.current_preset_data is not None:
                self.current_preset_data["name"] = new_name
                self.save_preset(new_name)
