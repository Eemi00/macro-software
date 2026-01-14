from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QWidget, QFormLayout
)


class ActionEditor(QDialog):
    def __init__(self, key_index, preset_manager):
        super().__init__()

        self.key_index = key_index
        self.preset_manager = preset_manager

        self.setWindowTitle(f"Edit Key {key_index + 1}")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title = QLabel(f"Configure action for key {key_index + 1}")
        self.layout.addWidget(title)

        # Action type dropdown
        self.action_type = QComboBox()
        self.action_type.addItems([
            "None",
            "Open Application",
            "Open Website",
            "Run Command"
        ])
        self.action_type.currentIndexChanged.connect(self.update_fields)
        self.layout.addWidget(self.action_type)

        # Dynamic fields container
        self.fields_container = QWidget()
        self.fields_layout = QFormLayout()
        self.fields_container.setLayout(self.fields_layout)
        self.layout.addWidget(self.fields_container)

        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_action)
        self.layout.addWidget(save_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        self.layout.addWidget(close_btn)

        # Initialize fields
        self.update_fields()

    def update_fields(self):
        # Clear old fields
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        action = self.action_type.currentText()

        if action == "Open Application":
            self.path_input = QLineEdit()
            self.fields_layout.addRow("Application Path:", self.path_input)

        elif action == "Open Website":
            self.url_input = QLineEdit()
            self.fields_layout.addRow("URL:", self.url_input)

        elif action == "Run Command":
            self.cmd_input = QLineEdit()
            self.fields_layout.addRow("Command:", self.cmd_input)

    def save_action(self):
        action_type = self.action_type.currentText()

        # Build action dictionary
        action_data = {"type": action_type}

        if action_type == "Open Application":
            action_data["path"] = self.path_input.text()

        elif action_type == "Open Website":
            action_data["url"] = self.url_input.text()

        elif action_type == "Run Command":
            action_data["command"] = self.cmd_input.text()

        # Save into preset data
        self.preset_manager.current_preset_data["keys"][self.key_index] = action_data

        # Write to disk
        self.preset_manager.save_preset()

        print(f"Saved action for key {self.key_index + 1}: {action_data}")

        self.close()