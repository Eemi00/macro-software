import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QTimer, Signal

from ui.main_window import MacropadGrid
from core.preset_manager import PresetManager
from core.serial_manager import SerialManager
from core.action_executor import ActionExecutor


class MainWindow(QMainWindow):
    show_ui_signal = Signal()

    def __init__(self):
        super().__init__()

        self.show_ui_signal.connect(self.show_interface)

        print("[MainWindow] init")

        self.setWindowTitle("Macropad Controller")

        # Presets
        self.presets = PresetManager("presets")
        data = self.presets.load_preset("default")
        print("[MainWindow] Loaded preset:", data.get("name"), "with", len(data.get("keys", [])), "keys")

        # Executor
        self.executor = ActionExecutor()

        # UI
        self.grid = MacropadGrid(self.presets, self)
        self.setCentralWidget(self.grid)

        # Stylesheet
        self.load_stylesheet()

        # Serial
        self.serial = SerialManager(
            port="COM6",
            callback=self.handle_key_press
        )
        self.serial.start()

        # Start hidden
        self.hide()

    def show_interface(self):
        print("[MainWindow] show_interface called")

        self.setWindowState(Qt.WindowNoState) 
        self.show() 
        self.raise_() 
        self.activateWindow()

    def closeEvent(self, event):
        event.ignore()          # Prevent the window from closing
        self.hide()             # Hide the window instead
        print("[MainWindow] Window hidden instead of closed")

    def load_stylesheet(self):
        css_path = Path(__file__).parent / "styles" / "main.css"
        if css_path.exists():
            with open(css_path, "r") as f:
                self.setStyleSheet(f.read())

    def handle_key_press(self, key_index):
        print(f"[MainWindow] handle_key_press called with key_index={key_index}")

        # hardware sends 1–16, convert to 0–15
        key_index -= 1

        # Bottom row (Open App, Overlay, Prev, Next)
        if key_index >= 12:
            bottom_index = key_index - 12
            print(f"[MainWindow] Function key index={bottom_index}")

            if bottom_index == 0:
                print("[MainWindow] Function key: Open App")
                self.show_ui_signal.emit()
                return

            print("[MainWindow] Other function key pressed (not implemented)")
            return

        # Normal keys (0–11)
        if not self.presets.current_preset_data:
            print("[MainWindow] No preset data loaded")
            return

        keys = self.presets.current_preset_data.get("keys", [])
        if key_index < 0 or key_index >= len(keys):
            print("[MainWindow] key_index out of range:", key_index)
            return

        action = keys[key_index]
        print("[MainWindow] Executing action:", action)
        self.executor.execute(action)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()