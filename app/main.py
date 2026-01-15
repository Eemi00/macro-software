import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, Signal, QTimer, QEvent
from PySide6.QtGui import QIcon, QAction

UI_ONLY = True

from ui.main_window import MainView
from core.preset_manager import PresetManager
from core.serial_manager import SerialManager
from core.action_executor import ActionExecutor


class MainWindow(QMainWindow):
    show_ui_signal = Signal()

    def __init__(self):
        super().__init__()

        self.test_mode = False

        self.setFixedSize(1000, 800)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.show_ui_signal.connect(self.show_interface)

        self.setWindowTitle("Macropad Controller")

        base = Path(__file__).resolve().parent
        self.presets = PresetManager(base / "presets")
        data = self.presets.load_preset("default")
        print("[MainWindow] Loaded preset:", data.get("name"), "with", len(data.get("keys", [])), "keys")

        self.executor = ActionExecutor()

        self.view = MainView(self.presets, self)
        self.setCentralWidget(self.view)

        self.load_stylesheet()

        if not UI_ONLY:
            self.serial = SerialManager(
                port="COM6",
                callback=self.handle_key_press
            )
            self.serial.start()
        else:
            self.serial = None
            print("[UI MODE] SerialManager disabled")

        self.setup_tray_icon()

        self.show()

    def setup_tray_icon(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("app/icon.png"))
        self.tray.setVisible(True)

        menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)

        show_action.triggered.connect(self.show_interface)
        quit_action.triggered.connect(self.quit_app)

        menu.addAction(show_action)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_interface()

    def quit_app(self):
        if self.serial:
            self.serial.running = False
        QApplication.quit()

    def show_interface(self):
        self.setWindowState(Qt.WindowNoState)
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                QTimer.singleShot(0, self.hide)
        super().changeEvent(event)

    def load_stylesheet(self):
        css_path = Path(__file__).parent / "styles" / "main.css"
        if css_path.exists():
            with open(css_path, "r") as f:
                self.setStyleSheet(f.read())

    def handle_key_press(self, key_index):
        key_index -= 1

        if key_index >= 12:
            bottom_index = key_index - 12

            if bottom_index == 0:
                self.show_ui_signal.emit()
                return

            return

        if not self.presets.current_preset_data:
            return

        keys = self.presets.current_preset_data.get("keys", [])
        if key_index < 0 or key_index >= len(keys):
            return

        action = keys[key_index]
        if not UI_ONLY:
            self.executor.execute(action)
        else:
            print("[UI MODE] Would execute:", action)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()