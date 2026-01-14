from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from ui.action_editor import ActionEditor


class MacropadGrid(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        print("[MacropadGrid] init")

        self.preset_manager = preset_manager
        self.main_window = main_window

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.buttons = []

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                btn = QPushButton()

                if row == 3:
                    labels = ["Open App", "Overlay", "Prev Preset", "Next Preset"]
                    btn.setText(labels[col])
                    btn.setProperty("class", "fixed-key")

                    # Map UI function keys to hardware key numbers 13–16
                    btn.clicked.connect(
                        lambda _, c=col: self._on_function_button_clicked(c)
                    )
                else:
                    btn.setText(f"Key {index + 1}")

                    # Map UI keys to hardware key numbers 1–12
                    btn.clicked.connect(
                        lambda _, i=index: self._on_key_button_clicked(i)
                    )

                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, row, col)
                self.buttons.append(btn)

    def _on_key_button_clicked(self, index):
        print(f"[MacropadGrid] UI key clicked index={index}")
        # mimic hardware: send 1–12
        self.main_window.handle_key_press(index + 1)

    def _on_function_button_clicked(self, col):
        print(f"[MacropadGrid] UI function key clicked col={col}")
        # mimic hardware: 13–16
        self.main_window.handle_key_press(13 + col)

    def handle_custom_key(self, index):
        editor = ActionEditor(index, self.preset_manager)
        editor.exec()

    def handle_fixed_key(self, col):
        # currently handled in MainWindow.handle_key_press
        pass