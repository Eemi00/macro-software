# ui/action_editor.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QHBoxLayout, QStackedWidget, QFileDialog, QWidget
)
from PySide6.QtCore import Qt

class KeyRecorder(QLineEdit):
    """A textbox that records key combinations in order and resets on release."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Press keys... (e.g., CTRL+ALT+I)")
        self.setReadOnly(True)
        self.active_keys = []
        self.keys_pressed_count = 0 

    def keyPressEvent(self, event):
        if event.isAutoRepeat(): return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.clearFocus()
            return

        self.keys_pressed_count += 1
        key_map = {
            Qt.Key_Control: "CTRL",
            Qt.Key_Shift: "SHIFT",
            Qt.Key_Alt: "ALT",
            Qt.Key_Meta: "WINDOWS",
        }
        
        key_text = key_map.get(event.key(), event.text().upper())
        if not key_text or key_text.isspace():
            key_text = event.key().name.upper()

        if key_text not in self.active_keys:
            self.active_keys.append(key_text)
        
        self.setText("+".join(self.active_keys))

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat(): return
        if self.keys_pressed_count > 0:
            self.keys_pressed_count -= 1
        if self.keys_pressed_count == 0:
            self.active_keys = []

class ActionEditor(QDialog):
    def __init__(self, key_index, preset_manager):
        super().__init__()
        self.key_index = key_index
        self.preset_manager = preset_manager

        preset_name = str(self.preset_manager.current_preset).replace("_", " ").title()
        self.setWindowTitle(f"Config Key {key_index + 1}")
        self.setMinimumWidth(450)

        # Main Layout with cleaner spacing
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # 1. Header (Clean, No underlines)
        header = QLabel(f"Editing Preset: {preset_name}")
        header.setStyleSheet("color: #10b981; font-weight: 800; font-size: 14px; border: none;")
        layout.addWidget(header)

        # 2. Display Name
        layout.addWidget(QLabel("Overlay Label:"))
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText("Enter custom text...")
        layout.addWidget(self.label_input)

        # 3. Action Type
        layout.addWidget(QLabel("Action Type:"))
        self.type_box = QComboBox()
        self.type_box.addItems(["None", "Open Website", "Open App", "Run Command", "Key Combo", "Type Text"])
        layout.addWidget(self.type_box)

        # 4. Input Stack
        self.input_stack = QStackedWidget()
        layout.addWidget(self.input_stack)
        self.setup_inputs()
        self.type_box.currentIndexChanged.connect(self.input_stack.setCurrentIndex)

        # 5. Buttons
        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.load_data()

    def setup_inputs(self):
        # 0: None
        self.input_stack.addWidget(QLabel("No configuration needed."))
        # 1: Website
        self.web_in = QLineEdit(); self.web_in.setPlaceholderText("https://...")
        self.input_stack.addWidget(self.web_in)
        # 2: App
        app_w = QWidget(); app_l = QHBoxLayout(app_w); app_l.setContentsMargins(0,0,0,0)
        self.app_in = QLineEdit()
        btn = QPushButton("BROWSE"); btn.clicked.connect(self.browse_app)
        app_l.addWidget(self.app_in); app_l.addWidget(btn)
        self.input_stack.addWidget(app_w)
        # 3: Command
        self.cmd_in = QLineEdit()
        self.input_stack.addWidget(self.cmd_in)
        # 4: Key Combo
        self.recorder = KeyRecorder()
        self.input_stack.addWidget(self.recorder)
        # 5: Type Text
        self.text_in = QLineEdit()
        self.input_stack.addWidget(self.text_in)

    def browse_app(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select App", "", "Executable (*.exe)")
        if path: self.app_in.setText(path)

    def load_data(self):
        keys = self.preset_manager.current_preset_data.get("keys", [])
        if self.key_index < len(keys):
            curr = keys[self.key_index]
            self.label_input.setText(curr.get("label", ""))
            
            # Map saved snake_case to UI Display Names
            mapping = {"none": 0, "open_website": 1, "open_app": 2, "run_command": 3, "key_combo": 4, "type_text": 5}
            idx = mapping.get(curr.get("type", "none"), 0)
            self.type_box.setCurrentIndex(idx)
            
            val = curr.get("value", "")
            if idx == 1: self.web_in.setText(val)
            elif idx == 2: self.app_in.setText(val)
            elif idx == 3: self.cmd_in.setText(val)
            elif idx == 4: self.recorder.setText(val)
            elif idx == 5: self.text_in.setText(val)

    def save(self):
        idx = self.type_box.currentIndex()
        mapping = ["none", "open_website", "open_app", "run_command", "key_combo", "type_text"]
        vals = ["", self.web_in.text(), self.app_in.text(), self.cmd_in.text(), self.recorder.text(), self.text_in.text()]
        
        keys = self.preset_manager.current_preset_data.get("keys", [])
        while len(keys) <= self.key_index:
            keys.append({"type": "none", "value": "", "label": ""})
            
        keys[self.key_index] = {
            "type": mapping[idx],
            "value": vals[idx],
            "label": self.label_input.text()
        }
        self.preset_manager.save_data(self.preset_manager.current_preset, self.preset_manager.current_preset_data)
        self.accept()