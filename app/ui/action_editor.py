from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ActionEditor(QDialog):
    def __init__(self, key_index):
        super().__init__()

        self.setWindowTitle(f"Edit key {key_index + 1}")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(f"Configure action for key {key_index + 1}")
        layout.addWidget(label)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)