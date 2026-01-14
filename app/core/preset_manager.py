import json
from pathlib import Path


class PresetManager:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

        self.current_preset = None
        self.current_preset_data = None

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