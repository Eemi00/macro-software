import json
from pathlib import Path

class PresetManager:
    """Manages loading, saving, and modification of key presets."""

    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)
        self.current_preset = "default"
        self.current_preset_data = {"name": "default", "keys": []}

    def count_total_mapped_keys(self):
        """Counts total mapped keys across all presets."""
        total = 0
        for p_file in self.folder.glob("*.json"):
            try:
                with open(p_file, "r") as f:
                    data = json.load(f)
                    keys = data.get("keys", [])
                    # Count keys where type is not "none"
                    total += sum(1 for k in keys if k.get("type") != "none")
            except (json.JSONDecodeError, OSError):
                continue
        return total

    def ensure_default_preset(self):
        """Creates a default preset if none exists."""
        if not (self.folder / "default.json").exists():
            self.create_preset("default")

    def load_preset(self, name):
        """Loads a preset by name."""
        path = self.folder / f"{name}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.current_preset_data = json.load(f)
            self.current_preset = name
        return self.current_preset_data

    def create_preset(self, name):
        """Creates a new preset with default empty keys."""
        data = {"name": name, "keys": [{"type": "none", "value": "", "label": ""} for _ in range(12)]}
        self.save_data(name, data)

    def save_data(self, name, data):
        """Saves preset data to disk."""
        with open(self.folder / f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def list_presets(self):
        """Returns a list of all preset names."""
        return [f.stem for f in self.folder.glob("*.json")]

    def rename_preset(self, old_name, new_name):
        """Renames a preset file and updates internal state if necessary."""
        old_path = self.folder / f"{old_name}.json"
        new_path = self.folder / f"{new_name}.json"
        
        if old_path.exists():
            old_path.rename(new_path)
            # Update the internal tracking if this was the active preset
            if self.current_preset == old_name:
                self.current_preset = new_name
                # Also update the 'name' key inside the JSON data
                self.current_preset_data["name"] = new_name
                self.save_data(new_name, self.current_preset_data)

    def delete_preset(self, name):
        """Deletes a preset file."""
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