from PySide6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt
from ui.action_editor import ActionEditor


class MacropadGrid(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window

        layout = QGridLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(layout)

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                btn = QPushButton()
                btn.setFixedSize(120, 120)

                if row == 3:
                    labels = ["Open App", "Overlay", "Prev", "Next"]
                    btn.setText(labels[col])
                    btn.setProperty("class", "fixed-key")
                    btn.clicked.connect(lambda _, c=col: self.main_window.handle_key_press(13 + c))
                else:
                    btn.setText(f"Key {index + 1}")
                    btn.setProperty("class", "macro-key")
                    btn.clicked.connect(lambda _, i=index: self.edit_key(i))

                layout.addWidget(btn, row, col)

    def edit_key(self, index):
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

        sidebar = self.build_sidebar()
        root.addWidget(sidebar)

        self.pages = QStackedWidget()
        root.addWidget(self.pages, 1)

        self.dashboard_page = self.build_dashboard_page()
        self.keys_page = self.build_keys_page()
        self.presets_page = self.build_presets_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.keys_page)
        self.pages.addWidget(self.presets_page)

        self.pages.setCurrentWidget(self.dashboard_page)

    def build_sidebar(self):
        frame = QFrame()
        frame.setObjectName("sidebar")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(16)
        frame.setLayout(layout)

        title = QLabel("Macropad")
        title.setObjectName("sidebarTitle")
        subtitle = QLabel("Controller")
        subtitle.setObjectName("sidebarSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)

        btn_dashboard = QPushButton("Dashboard")
        btn_dashboard.setObjectName("navButton")
        btn_dashboard.clicked.connect(lambda: self.pages.setCurrentWidget(self.dashboard_page))

        btn_keys = QPushButton("Keys")
        btn_keys.setObjectName("navButton")
        btn_keys.clicked.connect(lambda: self.pages.setCurrentWidget(self.keys_page))

        btn_presets = QPushButton("Presets")
        btn_presets.setObjectName("navButton")
        btn_presets.clicked.connect(lambda: self.pages.setCurrentWidget(self.presets_page))

        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_keys)
        layout.addWidget(btn_presets)

        layout.addStretch(1)

        status_label = QLabel("Connected")
        status_label.setObjectName("statusLabel")
        layout.addWidget(status_label)

        return frame

    def build_dashboard_page(self):
        page = QFrame()
        page.setObjectName("dashboardPage")
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        page.setLayout(layout)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Overview of your macropad and active preset.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        info_row = QHBoxLayout()
        info_row.setSpacing(24)
        layout.addLayout(info_row)

        preset_name = self.preset_manager.current_preset or "default"
        preset_card = self.build_info_card("Active Preset", preset_name)
        keys_card = self.build_info_card("Configured Keys", str(len(self.preset_manager.current_preset_data.get("keys", []))))
        status_card = self.build_info_card("Status", "Connected")

        info_row.addWidget(preset_card)
        info_row.addWidget(keys_card)
        info_row.addWidget(status_card)
        info_row.addStretch(1)

        layout.addStretch(1)

        return page

    def build_keys_page(self):
        page = QFrame()
        page.setObjectName("keysPage")
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        page.setLayout(layout)

        title_row = QHBoxLayout()
        title = QLabel("Keys")
        title.setObjectName("pageTitle")
        title_row.addWidget(title)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        subtitle = QLabel("Click a key to configure its action.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        grid_frame = QFrame()
        grid_frame.setObjectName("keysGridFrame")
        grid_layout = QVBoxLayout()
        grid_layout.setContentsMargins(16, 16, 16, 16)
        grid_layout.setSpacing(12)
        grid_frame.setLayout(grid_layout)

        grid = MacropadGrid(self.preset_manager, self.main_window)
        grid.setObjectName("keysGrid")
        grid_layout.addWidget(grid, alignment=Qt.AlignTop)

        layout.addWidget(grid_frame)
        layout.addStretch(1)

        return page

    def build_presets_page(self):
        page = QFrame()
        page.setObjectName("presetsPage")
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        page.setLayout(layout)

        title = QLabel("Presets")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Preset management UI will be added here later.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        list_widget = QListWidget()
        list_widget.setObjectName("presetList")

        item = QListWidgetItem(self.preset_manager.current_preset or "default")
        list_widget.addItem(item)

        layout.addWidget(list_widget)
        layout.addStretch(1)

        return page

    def build_info_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("infoCard")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        frame.setLayout(layout)

        title_label = QLabel(title)
        title_label.setObjectName("infoCardTitle")
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setObjectName("infoCardValue")
        layout.addWidget(value_label)

        return frame