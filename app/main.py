import sys
import ctypes
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QAction, QIcon

# SET TO FALSE WHEN HARDWARE IS CONNECTED
UI_ONLY = False 

from ui.main_window import MainView
from core.preset_manager import PresetManager
from core.serial_manager import SerialManager
from core.action_executor import ActionExecutor
from ui.overlay import OverlayWindow

# Windows Taskbar Icon Fix
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("macropad.controller.v3")
except:
    pass

class MainWindow(QMainWindow):
    show_ui_signal = Signal()

    def __init__(self):
        super().__init__()
        
        self.base_path = Path(__file__).resolve().parent
        os.chdir(self.base_path)
        icon_path = str(self.base_path / "icon.png")
        self.app_icon = QIcon(icon_path)

        self.test_mode = False
        self.overlay = None

        self.setFixedSize(1000, 800)
        self.setWindowTitle("Macropad Controller")
        self.setWindowIcon(self.app_icon)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # Managers
        self.presets = PresetManager(self.base_path / "presets")
        self.presets.ensure_default_preset()
        self.presets.load_preset("default")
        self.executor = ActionExecutor()

        # UI
        self.view = MainView(self.presets, self)
        self.setCentralWidget(self.view)

        # Stylesheet
        css_path = self.base_path / "styles" / "main.css"
        if css_path.exists():
            with open(css_path, "r") as f:
                self.setStyleSheet(f.read())

        # Serial Connection
        if not UI_ONLY:
            self.serial = SerialManager(port="COM6", callback=self.handle_key_press)
            self.serial.connection_status.connect(self.view.update_connection_state)
            self.serial.start()
        else:
            self.view.update_connection_state(False)

        self.show_ui_signal.connect(self.show_interface)
        self.setup_tray(icon_path)

    def setup_tray(self, icon_path):
        self.tray = QSystemTrayIcon(self.app_icon, self)
        self.tray.setIcon(QIcon(icon_path))
        self.tray.setToolTip("Macropad Controller")
        menu = QMenu()
        menu.addAction("Show Grid", self.show_interface)
        menu.addSeparator()
        menu.addAction("Exit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.activated.connect(lambda r: self.show_interface() if r == QSystemTrayIcon.DoubleClick else None)

    def show_interface(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.hide()
        super().changeEvent(event)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def show_overlay(self):
        if not self.overlay:
            self.overlay = OverlayWindow(self.presets)
        if self.overlay.isVisible():
            self.overlay.hide()
        else:
            self.overlay.show_on_primary_bottom_left()

    def switch_preset(self, name):
        if not name: return
        self.presets.load_preset(name)
        
        # --- NEW NOTIFICATION LOGIC ---
        if self.isHidden() and hasattr(self, 'tray'):
            self.tray.showMessage(
                "Preset Switched",
                f"Active Profile: {name.upper()}",
                QSystemTrayIcon.Information,
                500 # Duration in milliseconds
            )
        # ------------------------------

        if self.overlay: self.overlay.refresh()
        self.view.reload_all_pages()
        
        # Fix for the "Offline" bug: update connection state after reloading UI
        is_connected = False
        if hasattr(self, 'serial') and self.serial.ser and self.serial.ser.is_open:
            is_connected = True
        self.view.update_connection_state(is_connected)

    def next_preset(self):
        n = self.presets.get_next_preset()
        if n: self.switch_preset(n)

    def prev_preset(self):
        n = self.presets.get_prev_preset()
        if n: self.switch_preset(n)

    def handle_key_press(self, key_index):
        idx = key_index - 1
        if idx >= 12:
            cmd = idx - 12
            if cmd == 0: 
                self.show_ui_signal.emit()
            elif cmd == 1: 
                self.show_overlay()
            elif cmd == 2: 
                self.prev_preset()
            elif cmd == 3: 
                self.next_preset()
        else:
            keys = self.presets.current_preset_data.get("keys", [])
            if 0 <= idx < len(keys):
                # Ensure we pass the dictionary to the executor
                self.executor.execute(keys[idx], force=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # --- ADD THESE TWO LINES TO FIX THE "WEIRD NAME" ---
    app.setApplicationName("Macropad Controller")
    app.setApplicationDisplayName("Macropad Controller")
    # --------------------------------------------------

    current_dir = Path(__file__).resolve().parent
    import os
    os.chdir(current_dir)

    window = MainWindow()

    # LOGIC: Check if we should start in tray
    # If you want it to ALWAYS start in tray, just use window.hide()
    # If you want it only via shortcut, use the --minimized check
    if "--minimized" in sys.argv or True: # Force True for tray-start by default
        window.hide()
        # Ensure the tray icon is definitely visible
        if hasattr(window, 'tray'):
            window.tray.show()
    else:
        window.show()
            
    sys.exit(app.exec())