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
                    btn.setProperty("class", "fixed-key")

                    # Connect fixed keys
                    btn.clicked.connect(lambda _, c=col: self.handle_fixed_key(c))
                else:
                    # Customizable keys
                    btn.setText(f"Key {index + 1}")

                    # Connect customizable keys
                    btn.clicked.connect(lambda _, i=index: self.handle_custom_key(i))

                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, row, col)
                self.buttons.append(btn)

    def handle_custom_key(self, index):
        print(f"Custom key pressed: {index + 1}")

    def handle_fixed_key(self, col):
        actions = ["Open App", "Overlay", "Prev Preset", "Next Preset"]
        print(f"Fixed key pressed: {actions[col]}")