# ui/overlay.py

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QApplication, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt


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

        # Transparent background behind the frame
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.build_ui()

    def build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(5, 5, 5, 220);
                border: 1px solid #10b981;
                border-radius: 12px;
            }
        """)
        outer_layout.addWidget(frame)

        main_layout = QVBoxLayout(frame)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- TOP BAR WITH CLOSE BUTTON ---
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: #eee;
                border: 1px solid #444;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #10b981;
                color: black;
                border-color: #10b981;
            }
        """)
        close_btn.clicked.connect(self.close)

        top_bar.addWidget(close_btn)
        main_layout.addLayout(top_bar)

        # --- GRID OF KEYS ---
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(10, 0, 10, 10)
        main_layout.addLayout(grid)

        self.labels = []

        for row in range(4):
            for col in range(4):
                index = row * 4 + col

                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setMinimumSize(100, 60)

                label.setStyleSheet("""
                    QLabel {
                        border: 1px solid #333333;
                        border-radius: 4px;
                        background-color: #111111;
                        color: #e5e5e5;
                        font-family: "Consolas";
                    }
                    QLabel:hover {
                        border-color: #10b981;
                    }
                """)

                grid.addWidget(label, row, col)
                self.labels.append(label)

        self.refresh()

    def refresh(self):
        data = self.preset_manager.current_preset_data or {}
        keys = data.get("keys", [])

        for i, label in enumerate(self.labels):
            if i < 12:
                if i < len(keys):
                    action = keys[i]
                    # Use custom label if it exists, otherwise fallback to type
                    display_text = action.get("label") or action.get("type", "none")
                    v = action.get("value", "")
                    label.setText(f"{i+1:02d}\n{display_text}\n{v}")

    def show_on_primary_bottom_left(self):
        """Show overlay at bottom-left of the primary monitor."""
        self.adjustSize()

        screen = QApplication.primaryScreen().geometry()
        x = screen.left() + 20
        y = screen.bottom() - self.height() - 20

        self.move(x, y)
        self.show()
        self.raise_()

    def keyPressEvent(self, event):
        """Close overlay with ESC."""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)