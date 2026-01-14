import json
from pathlib import Path


class PresetManager:
    def __init__(self, presets_folder):
        base = Path(__file__).parent.parent  # app/core → app/
        self.presets_folder = base / presets_folder

        self.current_preset = None
        self.current_preset_data = None

    def load_preset(self, name):
        path = self.presets_folder / f"{name}.json"

        print("[PresetManager] Loading preset from:", path)

        if not path.exists():
            raise FileNotFoundError(f"Preset '{name}' not found at {path}")

        with open(path, "r") as f:
            self.current_preset_data = json.load(f)

        self.current_preset = name
        print("[PresetManager] Loaded preset:", self.current_preset)
        return self.current_preset_data

    def save_preset(self):
        if not self.current_preset:
            return

        path = self.presets_folder / f"{self.current_preset}.json"
        with open(path, "w") as f:
            json.dump(self.current_preset_data, f, indent=4)

        print("[PresetManager] Saved preset to:", path)