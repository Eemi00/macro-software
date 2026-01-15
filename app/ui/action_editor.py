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
        self.active_keys = []  # List to maintain order
        self.keys_pressed_count = 0 

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.clearFocus()
            return

        # Increment physical press counter
        self.keys_pressed_count += 1

        # Map modifiers to standard strings
        key_map = {
            Qt.Key_Control: "CTRL",
            Qt.Key_Shift: "SHIFT",
            Qt.Key_Alt: "ALT",
            Qt.Key_Meta: "WINDOWS",
        }
        
        # Get key name and convert to uppercase
        key_text = key_map.get(event.key(), event.text().upper())
        if not key_text or key_text.isspace():
            key_text = event.key().name().upper()

        # Add to list only if not already present
        if key_text not in self.active_keys:
            self.active_keys.append(key_text)
        
        # Update display in the order pressed
        self.setText("+".join(self.active_keys))

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        if self.keys_pressed_count > 0:
            self.keys_pressed_count -= 1

        # Reset the sequence when all keys are released
        if self.keys_pressed_count == 0:
            self.active_keys = []

class ActionEditor(QDialog):
    def __init__(self, key_index, preset_manager):
        super().__init__()
        self.key_index = key_index
        self.preset_manager = preset_manager

        # Get the current preset name and capitalize it
        preset_name = str(self.preset_manager.current_preset).upper()
        self.setWindowTitle(f"Configure Key {key_index + 1} - [{preset_name}]")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        # 1. Uppercase Preset Header
        preset_header = QLabel(f"CURRENT PRESET: {preset_name}")
        preset_header.setStyleSheet("""
            color: #10b981; 
            font-weight: bold; 
            font-size: 14px; 
            margin-bottom: 5px;
        """)
        layout.addWidget(preset_header)

        # 2. Custom Display Name (for Overlay)
        layout.addWidget(QLabel("Display Name (shown on overlay):"))
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText("e.g., Mute Discord")
        layout.addWidget(self.label_input)

        # 3. Action Type Selection
        layout.addWidget(QLabel("Action Type:"))
        self.type_box = QComboBox()
        self.type_box.addItems(["none", "open_website", "open_app", "run_command", "key_combo", "type_text"])
        layout.addWidget(self.type_box)

        # 4. Input Stack (changes based on selection)
        self.input_stack = QStackedWidget()
        layout.addWidget(self.input_stack)
        self.setup_inputs()
        
        # Connect dropdown to stack
        self.type_box.currentIndexChanged.connect(self.input_stack.setCurrentIndex)

        # 5. Dialog Buttons
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
        # Index 0: None
        self.input_stack.addWidget(QLabel("No configuration needed."))
        
        # Index 1: Website
        self.web_in = QLineEdit(); self.web_in.setPlaceholderText("https://...")
        self.input_stack.addWidget(self.web_in)
        
        # Index 2: App (File Picker)
        app_w = QWidget(); app_l = QHBoxLayout(app_w); app_l.setContentsMargins(0,0,0,0)
        self.app_in = QLineEdit()
        btn = QPushButton("Browse"); btn.clicked.connect(self.browse_app)
        app_l.addWidget(self.app_in); app_l.addWidget(btn)
        self.input_stack.addWidget(app_w)
        
        # Index 3: Command
        self.cmd_in = QLineEdit(); self.cmd_in.setPlaceholderText("system command...")
        self.input_stack.addWidget(self.cmd_in)
        
        # Index 4: Key Combo (Recorder)
        self.recorder = KeyRecorder()
        self.input_stack.addWidget(self.recorder)
        
        # Index 5: Type Text
        self.text_in = QLineEdit(); self.text_in.setPlaceholderText("Text to type out...")
        self.input_stack.addWidget(self.text_in)

    def browse_app(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Application", "", "Executable (*.exe);;All Files (*)")
        if path:
            self.app_in.setText(path)

    def load_data(self):
        keys = self.preset_manager.current_preset_data.get("keys", [])
        if self.key_index < len(keys):
            curr = keys[self.key_index]
            self.label_input.setText(curr.get("label", ""))
            self.type_box.setCurrentText(curr.get("type", "none"))
            val = curr.get("value", "")
            
            # Put the value into the correct input field
            idx = self.type_box.currentIndex()
            if idx == 1: self.web_in.setText(val)
            elif idx == 2: self.app_in.setText(val)
            elif idx == 3: self.cmd_in.setText(val)
            elif idx == 4: self.recorder.setText(val)
            elif idx == 5: self.text_in.setText(val)

    def save(self):
        idx = self.type_box.currentIndex()
        # Map values from the various stack widgets
        vals = ["", self.web_in.text(), self.app_in.text(), self.cmd_in.text(), self.recorder.text(), self.text_in.text()]
        
        keys = self.preset_manager.current_preset_data.get("keys", [])
        while len(keys) <= self.key_index:
            keys.append({"type": "none", "value": "", "label": ""})
            
        keys[self.key_index] = {
            "type": self.type_box.currentText(),
            "value": vals[idx],
            "label": self.label_input.text()
        }
        
        self.preset_manager.save_data(self.preset_manager.current_preset, self.preset_manager.current_preset_data)
        self.accept()