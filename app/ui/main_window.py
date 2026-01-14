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
                btn = QPushButton()

                if row == 3:
                    # Bottom row (fixed keys)
                    labels = ["Open App", "Overlay", "Prev Preset", "Next Preset"]
                    btn.setText(labels[col])
                    btn.styleSheet("background-color: #444; color: white;")
                else:
                    # Customizable keys
                    btn.setText(f"Key {index + 1}")
                    btn.setStyleSheet("background-color: #222; color: white;")

                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, row, col)
                self.buttons.append(btn)