from PySide6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, QSize
# Assuming these imports exist in your project structure
from ui.action_editor import ActionEditor 
from ui.animated_button import AnimatedButton
 
class MacropadGrid(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window
 
        layout = QGridLayout()
        # Tighter spacing for the "Pixel Grid" look
        layout.setSpacing(10) 
        layout.setContentsMargins(16, 16, 16, 16)
        self.setLayout(layout)
 
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                # Use standard QPushButton if AnimatedButton isn't strictly needed for complex animations
                # or ensure AnimatedButton inherits the stylesheet correctly.
                btn = QPushButton() 
                btn.setFixedSize(100, 100) # Slightly smaller to allow spacing breathing room
                btn.setCursor(Qt.PointingHandCursor)
 
                if row == 3:
                    labels = ["APP", "LAYER", "PREV", "NEXT"] # Short, tech-style labels
                    btn.setText(labels[col])
                    btn.setProperty("class", "fixed-key")
                    btn.clicked.connect(lambda _, c=col: self.main_window.handle_key_press(13 + c))
                else:
                    # Pad single digits with 0 (e.g., 01, 02) for tech aesthetics
                    btn.setText(f"{index + 1:02d}") 
                    btn.setProperty("class", "macro-key")
                    btn.clicked.connect(lambda _, i=index: self.handle_click(i))
 
                layout.addWidget(btn, row, col)
 
    def handle_click(self, index):
        if self.main_window.test_mode:
            # Safe access to keys
            keys = self.preset_manager.current_preset_data.get("keys", [])
            if index < len(keys):
                action = keys[index]
                self.main_window.executor.execute(action, force=True)
        else:
            editor = ActionEditor(index, self.preset_manager)
            editor.exec()
 
 
class MainView(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window
 
        root = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.setLayout(root)
 
        self.sidebar = self.build_sidebar()
        root.addWidget(self.sidebar)
 
        self.pages = QStackedWidget()
        root.addWidget(self.pages, 1)
 
        self.dashboard_page = self.build_dashboard_page()
        self.keys_page = self.build_keys_page()
        self.presets_page = self.build_presets_page()
 
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.keys_page)
        self.pages.addWidget(self.presets_page)
 
        self.pages.setCurrentWidget(self.dashboard_page)
 
    # Sidebar
    def build_sidebar(self):
        frame = QFrame()
        frame.setObjectName("sidebar")
 
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40) # More top/bottom padding
        layout.setSpacing(10)
        frame.setLayout(layout)
 
        title = QLabel("MACROPAD")
        title.setObjectName("sidebarTitle")
        # Using the letter 'M' from your logo description conceptually
        subtitle = QLabel("MK.III // GRID") 
        subtitle.setObjectName("sidebarSubtitle")
 
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
 
        btn_dashboard = QPushButton("DASHBOARD")
        btn_keys = QPushButton("KEY CONFIG")
        btn_presets = QPushButton("PRESETS")
 
        for b in (btn_dashboard, btn_keys, btn_presets):
            b.setObjectName("navButton")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
 
        def set_page(widget, button):
            self.pages.setCurrentWidget(widget)
            for b in (btn_dashboard, btn_keys, btn_presets):
                b.setChecked(False)
            button.setChecked(True)
 
        btn_dashboard.clicked.connect(lambda: set_page(self.dashboard_page, btn_dashboard))
        btn_keys.clicked.connect(lambda: set_page(self.keys_page, btn_keys))
        btn_presets.clicked.connect(lambda: set_page(self.presets_page, btn_presets))
 
        btn_dashboard.setChecked(True)
 
        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_keys)
        layout.addWidget(btn_presets)
 
        layout.addStretch(1)
 
        status_label = QLabel("SYSTEM ONLINE")
        status_label.setObjectName("statusLabel")
        layout.addWidget(status_label)
 
        return frame
 
    # Dashboard
    def build_dashboard_page(self):
        page = QFrame()
        page.setObjectName("dashboardPage")
 
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50) # More breath
        layout.setSpacing(30)
        page.setLayout(layout)
 
        title = QLabel("Command Center")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        # Removed Subtitle for cleaner look, or keep it minimal
 
        info_row = QHBoxLayout()
        info_row.setSpacing(20)
        layout.addLayout(info_row)
 
        preset_name = self.preset_manager.current_preset or "DEFAULT"
        # Card 1
        preset_card = self.build_info_card("ACTIVE PROFILE", preset_name.upper())
        # Card 2
        key_count = len(self.preset_manager.current_preset_data.get("keys", []))
        keys_card = self.build_info_card("MAPPED KEYS", f"{key_count}/16")
        # Card 3
        status_card = self.build_info_card("CONNECTION", "USB-C")
 
        info_row.addWidget(preset_card)
        info_row.addWidget(keys_card)
        info_row.addWidget(status_card)
        layout.addStretch(1)
        return page
 
    # Keys page
    def build_keys_page(self):
        page = QFrame()
        page.setObjectName("keysPage")
 
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)
        page.setLayout(layout)
 
        header_layout = QHBoxLayout()
        title = QLabel("Grid Layout")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
 
        test_btn = QPushButton("TEST MODE")
        test_btn.setCheckable(True)
        test_btn.setFixedWidth(140)
        test_btn.setCursor(Qt.PointingHandCursor)
 
        def toggle_test():
            enabled = test_btn.isChecked()
            self.main_window.test_mode = enabled
            # Visual feedback in text
            test_btn.setText("TEST ACTIVE" if enabled else "TEST MODE")
 
        test_btn.clicked.connect(toggle_test)
        header_layout.addWidget(test_btn)
        layout.addLayout(header_layout)
 
        grid_frame = QFrame()
        grid_frame.setObjectName("keysGridFrame")
 
        grid_layout = QVBoxLayout()
        grid_layout.setContentsMargins(4, 4, 4, 4)
        grid_frame.setLayout(grid_layout)
 
        grid = MacropadGrid(self.preset_manager, self.main_window)
        grid.setObjectName("keysGrid")
        grid_layout.addWidget(grid, alignment=Qt.AlignCenter)
 
        layout.addWidget(grid_frame)
        layout.addStretch(1)
 
        return page
 
    # Presets page
    def build_presets_page(self):
        page = QFrame()
        page.setObjectName("presetsPage")
 
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        page.setLayout(layout)
 
        title = QLabel("Profiles")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
 
        list_widget = QListWidget()
        list_widget.setObjectName("presetList")
 
        current = self.preset_manager.current_preset or "Default"
        # Dummy data for visualization
        presets = ["Gaming Mode", "Productivity", "Video Editing", current]
        for p in set(presets): # Unique
            item = QListWidgetItem(p)
            list_widget.addItem(item)
            if p == current:
                item.setSelected(True)
 
        layout.addWidget(list_widget)
        layout.addStretch(1)
 
        return page
 
    # Info cards helper
    def build_info_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("infoCard")
        frame.setFixedSize(200, 100) # Uniform size for pro look
 
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        frame.setLayout(layout)
 
        title_label = QLabel(title)
        title_label.setObjectName("infoCardTitle")
 
        value_label = QLabel(value)
        value_label.setObjectName("infoCardValue")
 
        layout.addWidget(title_label)
        layout.addWidget(value_label)
 
        return frame