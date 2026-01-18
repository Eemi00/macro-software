# ui/overlay.py

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QApplication, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
import qtawesome as qta


class OverlayWindow(QWidget):
    def __init__(self, preset_manager):
        super().__init__()
        self.preset_manager = preset_manager

        self.setWindowTitle("Macropad Overlay")

        # Floating, always-on-top, frameless overlay window
        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.build_ui()

    def build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(5, 5, 5, 235);
                border: 2px solid #10b981;
                border-radius: 12px;
            }
        """)
        outer_layout.addWidget(frame)

        main_layout = QVBoxLayout(frame)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # --- TOP BAR ---
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: #888;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.hide)
        top_bar.addWidget(close_btn)
        main_layout.addLayout(top_bar)

        # --- GRID OF KEYS ---
        grid = QGridLayout()
        grid.setSpacing(10)
        main_layout.addLayout(grid)

        self.labels = []

        for row in range(4):
            for col in range(4):
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setWordWrap(True) # Solution for long labels
                label.setFixedSize(85, 85) # Perfect Squares
                label.setContentsMargins(5, 5, 5, 5) # Internal padding

                grid.addWidget(label, row, col)
                self.labels.append(label)

        self.refresh()

    def refresh(self):
        """Refresh overlay contents based on current preset."""
        data = self.preset_manager.current_preset_data or {}
        keys = data.get("keys", [])

        for i, label in enumerate(self.labels):
            # MACRO KEYS (1-12)
            if i < 12:
                if i < len(keys):
                    action = keys[i]
                    action_type = action.get("type", "none")
                    icon_path = action.get("icon", "")
                    
                    if action_type == "none":
                        label.clear()
                        label.setText(f"<i style='color:#444;'>{i+1}</i>")
                        label.setStyleSheet("background-color: rgba(15, 15, 15, 150); border: 1px solid #222;")
                    else:
                        label.clear()
                        icon_set = False
                        
                        # 1. Custom File
                        if icon_path and os.path.exists(icon_path):
                            pix = QPixmap(icon_path)
                            if not pix.isNull():
                                label.setPixmap(pix.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                                icon_set = True

                        # 2. FontAwesome Icon
                        if not icon_set and icon_path:
                            try:
                                # Simple check for fa prefix or assumes it might be an ID if not a file
                                if "fa" in icon_path or "." in icon_path:
                                    icon = qta.icon(icon_path, color="white")
                                    pix = icon.pixmap(60, 60)
                                    if not pix.isNull():
                                        label.setPixmap(pix)
                                        icon_set = True
                            except:
                                pass
                        
                        if not icon_set:
                            display_name = action.get("label") or action_type.replace("_", " ").title()
                            # FORCE styling using span and css injection directly
                            label.setText(f"<html><head/><body><p align='center'>"
                                          f"<span style='font-size:9pt; font-weight:400; color:#10b981;'>{i+1}</span><br/>"
                                          f"<span style='font-size:11pt; font-weight:400; color:#ffffff;'>{display_name}</span>"
                                          f"</p></body></html>")
                            
                        # Remove ambiguous selector. Apply properties directly.
                        label.setStyleSheet("""
                            background-color: #111; 
                            border: 1px solid #10b981; 
                            color: white; 
                            font-weight: normal;
                            font-family: Arial, sans-serif;
                        """)
                else:
                    label.setText(f"<i style='color:#444;'>{i+1}</i>")
            
            # FUNCTION KEYS (13-16) - Match Main Page Styling
            else:
                names = ["App", "Layer", "Prev", "Next"]
                label.setText(f"<div style='font-size: 12px;'>{names[i - 12]}</div>")
                # Styled to match 'fixed-key' class from main.css
                label.setStyleSheet("""
                    background-color: #0f1210; 
                    color: #34d399; 
                    border: 1px solid #064e3b;
                    font-weight: bold;
                """)

    def show_on_primary_bottom_left(self):
        self.adjustSize()
        screen = QApplication.primaryScreen().geometry()
        x = screen.left() + 30
        y = screen.bottom() - self.height() - 30
        self.move(x, y)
        self.show()
        self.raise_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: self.hide()
        else: super().keyPressEvent(event)