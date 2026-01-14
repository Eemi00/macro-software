from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QWidget, QFormLayout
)


class ActionEditor(QDialog):
    def __init__(self, key_index):
        super().__init__()

        self.key_index = key_index
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

        # "None" has no fields

    def save_action(self):
        action = self.action_type.currentText()

        if action == "None":
            print(f"Key {self.key_index + 1} set to: None")

        elif action == "Open Application":
            print(f"Key {self.key_index + 1} will open app: {self.path_input.text()}")

        elif action == "Open Website":
            print(f"Key {self.key_index + 1} will open website: {self.url_input.text()}")

        elif action == "Run Command":
            print(f"Key {self.key_index + 1} will run command: {self.cmd_input.text()}")

        self.close()