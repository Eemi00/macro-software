# main.py

import sys
import ctypes
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QAction, QIcon

# Set this to False when your device is plugged in
UI_ONLY = True 

from ui.main_window import MainView
from core.preset_manager import PresetManager
from core.serial_manager import SerialManager
from core.action_executor import ActionExecutor
from ui.overlay import OverlayWindow

# Windows Taskbar Icon Fix
try:
    myappid = 'mycompany.macropad.mk3.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception as e:
    print("Could not set AppUserModelID:", e)

# --- TASK MANAGER IDENTITY FIX ---
try:
    # This ID must be unique. It forces Windows to group the process 
    # under this name rather than the generic 'python.exe'
    myappid = u'mycompany.macropad.mk3.controller' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception as e:
    print(f"ID Fix failed: {e}")

class MainWindow(QMainWindow):
    show_ui_signal = Signal()

    def __init__(self):
        super().__init__()

        self.test_mode = False
        self.overlay = None

        self.setFixedSize(1000, 800)
        # We allow the minimize button, but disable maximizing
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.show_ui_signal.connect(self.show_interface)
        self.setWindowTitle("Macropad")

        # --- PATH FIXES ---
        base = Path(__file__).resolve().parent
        icon_path = str(base / "icon.png")  # Located in /app/
        css_path = base / "styles" / "main.css"  # Located in /app/styles/
        # ------------------

        self.setWindowIcon(QIcon(icon_path))

        self.presets = PresetManager(base / "presets")
        self.presets.ensure_default_preset()
        self.presets.load_preset("default")

        self.executor = ActionExecutor()

        self.view = MainView(self.presets, self)
        self.setCentralWidget(self.view)

        # Load Stylesheet from new path
        if css_path.exists():
            with open(css_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"[ERROR] CSS not found at {css_path}")

        if not UI_ONLY:
            self.serial = SerialManager(
                port="COM6",
                callback=self.handle_key_press
            )
            self.serial.connection_status.connect(self.view.update_connection_state)
            self.serial.start()
        else:
            self.serial = None
            self.view.update_connection_state(False)

        self.setup_tray(icon_path)

    def setup_tray(self, icon_path):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(icon_path))
        
        menu = QMenu()
        show_action = QAction("Show Grid", self)
        show_action.triggered.connect(self.show_interface)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        
        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        # Double click tray icon to show app
        self.tray.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_interface()

    def show_interface(self):
        self.showNormal() # Restores window if minimized
        self.activateWindow()
        self.raise_()

    def changeEvent(self, event):
        """Handle minimizing to tray."""
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                # This hides the window from the Taskbar entirely
                self.hide()
                event.ignore()
        super().changeEvent(event)

    def closeEvent(self, event):
        """Handle 'X' button closing to tray instead of quitting."""
        event.ignore()
        self.hide()

    # ... keep rest of the methods (show_overlay, switch_preset, handle_key_press, etc) ...

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
        if self.overlay:
            self.overlay.refresh()
        self.view.reload_all_pages()

    def next_preset(self):
        name = self.presets.get_next_preset()
        if name: self.switch_preset(name)

    def prev_preset(self):
        name = self.presets.get_prev_preset()
        if name: self.switch_preset(name)

    def handle_key_press(self, key_index):
        key_index -= 1
        if key_index >= 12:
            idx = key_index - 12
            if idx == 0: self.show_ui_signal.emit()
            elif idx == 1: self.show_overlay()
            elif idx == 2: self.prev_preset()
            elif idx == 3: self.next_preset()
            return
        keys = self.presets.current_preset_data.get("keys", [])
        if 0 <= key_index < len(keys):
            self.executor.execute(keys[key_index], force=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. FORCE THE CORRECT WORKING DIRECTORY
    # This ensures that even if you launch from a shortcut, 
    # Python looks for 'styles' and 'presets' in the right folder.
    current_dir = Path(__file__).resolve().parent
    import os
    os.chdir(current_dir)

    # 2. Setup Icon
    icon_path = str(current_dir / "icon.png")
    app.setWindowIcon(QIcon(icon_path))
    
    try:
        window = MainWindow()
        
        # Check for minimized flag
        if "--minimized" in sys.argv:
            window.hide()
        else:
            window.show()
            
        sys.exit(app.exec())
        
    except Exception as e:
        # If it crashes, this will show a popup instead of just disappearing
        from PySide6.QtWidgets import QMessageBox
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText("Startup Error")
        error_dialog.setInformativeText(str(e))
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()