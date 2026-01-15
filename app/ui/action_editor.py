# ui/action_editor.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QHBoxLayout
)

class ActionEditor(QDialog):
    def __init__(self, key_index, preset_manager):
        super().__init__()
        self.key_index = key_index
        self.preset_manager = preset_manager

        self.setWindowTitle(f"Edit Key {key_index + 1}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Configure action for Key {key_index + 1}"))

        self.type_box = QComboBox()
        self.type_box.addItems(["none", "open_website", "open_app", "run_command", "key_combo", "type_text"])
        layout.addWidget(self.type_box)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value (URL, path, command, keys, text...)")
        layout.addWidget(self.input_field)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)

        # Load current data
        keys = self.preset_manager.current_preset_data.get("keys", [])
        if self.key_index < len(keys):
            current = keys[self.key_index]
        else:
            current = {"type": "none", "value": ""}

        self.type_box.setCurrentText(current.get("type", "none"))
        self.input_field.setText(current.get("value", ""))

    def save(self):
        # Update the local data dictionary
        keys = self.preset_manager.current_preset_data.get("keys", [])
        
        # Ensure the list is long enough
        while len(keys) <= self.key_index:
            keys.append({"type": "none", "value": ""})
            
        keys[self.key_index] = {
            "type": self.type_box.currentText(),
            "value": self.input_field.text()
        }
        
        # FIX: Use save_data instead of save_preset
        self.preset_manager.save_data(self.preset_manager.current_preset, self.preset_manager.current_preset_data)
        self.accept()