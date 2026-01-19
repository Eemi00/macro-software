# ui/overlay.py

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QApplication, 
    QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QPixmap, QColor
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
        outer_layout.setContentsMargins(10, 10, 10, 10) # Add margin for shadow
        
        frame = QFrame()
        frame.setObjectName("overlayFrame")
        frame.setStyleSheet("""
            #overlayFrame {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 16px;
            }
        """)
        
        # Add soft shadow for depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 100))
        frame.setGraphicsEffect(shadow)
        
        outer_layout.addWidget(frame)

        main_layout = QVBoxLayout(frame)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top Bar
        top_bar = QHBoxLayout()
        title_label = QLabel("MACROPAD")
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("""
            QLabel#titleLabel {
                color: #555; 
                font-weight: 600; 
                font-size: 10px; 
                letter-spacing: 0.5px;
                background: transparent;
                border: none;
            }
        """) 
        top_bar.addWidget(title_label)
        
        top_bar.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.hide)
        top_bar.addWidget(close_btn)
        main_layout.addLayout(top_bar)

        # Grid of Keys
        grid = QGridLayout()
        grid.setSpacing(8)
        main_layout.addLayout(grid)

        self.labels = []

        for row in range(4):
            for col in range(4):
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setWordWrap(True) 
                label.setFixedSize(76, 76) 
                label.setContentsMargins(4, 4, 4, 4)

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
                        label.setText(f"<span style='color:#3a3a3a; font-size:10px;'>{i+1}</span>")
                        label.setStyleSheet("""
                            QLabel {
                                background-color: #252525;
                                border: 1px solid #2e2e2e;
                                border-radius: 12px;
                            }
                        """)
                    else:
                        label.clear()
                        icon_set = False
                        
                        # 1. Custom File
                        if icon_path and os.path.exists(icon_path):
                            pix = QPixmap(icon_path)
                            if not pix.isNull():
                                # Smaller icons (24x24) for more breathing room
                                label.setPixmap(pix.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                                icon_set = True

                        # 2. FontAwesome Icon
                        if not icon_set and icon_path:
                            try:
                                if "fa" in icon_path or "." in icon_path:
                                    icon = qta.icon(icon_path, color="#e0e0e0") 
                                    pix = icon.pixmap(24, 24)
                                    if not pix.isNull():
                                        label.setPixmap(pix)
                                        icon_set = True
                            except:
                                pass
                        
                        if not icon_set:
                            display_name = action.get("label") or action_type.replace("_", " ").title()
                            # Shorten if too long
                            if len(display_name) > 15:
                                display_name = display_name[:12] + "..."
                                
                            label.setText(f"<html><head/><body><p align='center'>"
                                          f"<span style='font-size:8pt; font-weight:600; color:#555;'>{i+1}</span><br/>"
                                          f"<span style='font-size:9pt; font-weight:500; color:#f0f0f0;'>{display_name}</span>"
                                          f"</p></body></html>")
                        
                        label.setStyleSheet("""
                            QLabel {
                                background-color: #333333;
                                border: 1px solid #444444; 
                                border-radius: 12px;
                                color: white;
                            }
                            QLabel:hover {
                                background-color: #3d3d3d;
                                border: 1px solid #555555;
                            }
                        """)
                else:
                    label.setText(f"<span style='color:#333; font-size:10px;'>{i+1}</span>")
                    label.setStyleSheet("""
                            QLabel {
                                background-color: #202020;
                                border: 1px solid #2a2a2a;
                                border-radius: 12px;
                            }
                    """)
            
            # FUNCTION KEYS (13-16)
            else:
                names = ["APP", "LAYER", "PREV", "NEXT"]
                label.setText(f"<div style='font-size: 9px; font-weight:700; color:#888; letter-spacing:1px;'>{names[i - 12]}</div>")
                label.setStyleSheet("""
                    QLabel {
                        background-color: #222222;
                        color: #888; 
                        border: 1px dashed #333;
                        border-radius: 12px;
                    }
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