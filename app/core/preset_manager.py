import json
from pathlib import Path

class PresetManager:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)
        self.current_preset = "default"
        self.current_preset_data = {"name": "default", "keys": []}

    def count_total_mapped_keys(self):
        total = 0
        for p_file in self.folder.glob("*.json"):
            try:
                with open(p_file, "r") as f:
                    data = json.load(f)
                    keys = data.get("keys", [])
                    # Count keys where type is not "none"
                    total += sum(1 for k in keys if k.get("type") != "none")
            except:
                continue
        return total

    def ensure_default_preset(self):
        if not (self.folder / "default.json").exists():
            self.create_preset("default")

    def load_preset(self, name):
        path = self.folder / f"{name}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.current_preset_data = json.load(f)
            self.current_preset = name
        return self.current_preset_data

    def create_preset(self, name):
        data = {"name": name, "keys": [{"type": "none", "value": ""}] * 12}
        self.save_data(name, data)

    def save_data(self, name, data):
        with open(self.folder / f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def list_presets(self):
        return [f.stem for f in self.folder.glob("*.json")]

    def rename_preset(self, old_name, new_name):
        old_path = self.folder / f"{old_name}.json"
        new_path = self.folder / f"{new_name}.json"
        
        if old_path.exists():
            old_path.rename(new_path)
            # Crucial: Update the internal tracking
            if self.current_preset == old_name:
                self.current_preset = new_name
                # Also update the 'name' key inside the JSON data
                self.current_preset_data["name"] = new_name
                self.save_data(new_name, self.current_preset_data)

    def delete_preset(self, name):
        path = self.folder / f"{name}.json"
        if path.exists():
            path.unlink() # This deletes the actual file
        
        # Reset internal memory if we deleted the active one
        if self.current_preset == name:
            self.current_preset = "default"
            self.load_preset("default")

    def get_next_preset(self):
        p = self.list_presets()
        return p[(p.index(self.current_preset) + 1) % len(p)] if p else None

    def get_prev_preset(self):
        p = self.list_presets()
        return p[(p.index(self.current_preset) - 1) % len(p)] if p else None