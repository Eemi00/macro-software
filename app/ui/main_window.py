from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout

class MacropadGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.buttons = []

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                btn = QPushButton(f"Key {index + 1}")
                btn.setFixedSize(100, 100)

                self.layout.addWidget(btn, row, col)
                self.buttons.append(btn)