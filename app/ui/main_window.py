from PySide6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QFrame,
    QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt
from ui.action_editor import ActionEditor


class MacropadGrid(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)
        self.setLayout(layout)

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                btn = QPushButton()
                btn.setFixedSize(100, 100)
                btn.setCursor(Qt.PointingHandCursor)

                if row == 3:
                    labels = ["APP", "LAYER", "PREV", "NEXT"]
                    btn.setText(labels[col])
                    btn.setProperty("class", "fixed-key")

                    if col == 0:
                        btn.clicked.connect(self.main_window.show_interface)
                    elif col == 1:
                        btn.clicked.connect(self.main_window.show_overlay)
                    elif col == 2:
                        btn.clicked.connect(self.main_window.prev_preset)
                    elif col == 3:
                        btn.clicked.connect(self.main_window.next_preset)
                else:
                    btn.setText(f"{index + 1:02d}")
                    btn.setProperty("class", "macro-key")
                    btn.clicked.connect(lambda _, i=index: self.handle_click(i))

                layout.addWidget(btn, row, col)

    def handle_click(self, index):
        if self.main_window.test_mode:
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

    def build_sidebar(self):
        frame = QFrame()
        frame.setObjectName("sidebar")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40)
        layout.setSpacing(10)
        frame.setLayout(layout)

        title = QLabel("MACROPAD")
        title.setObjectName("sidebarTitle")
        subtitle = QLabel("MK.III // GRID")
        subtitle.setObjectName("sidebarSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        # FIX 1: Make these buttons instance variables so we can access them later
        self.btn_dashboard = QPushButton("DASHBOARD")
        self.btn_keys = QPushButton("KEY CONFIG")
        self.btn_presets = QPushButton("PRESETS")

        for b in (self.btn_dashboard, self.btn_keys, self.btn_presets):
            b.setObjectName("navButton")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)

        def set_page(widget, button):
            self.pages.setCurrentWidget(widget)
            for b in (self.btn_dashboard, self.btn_keys, self.btn_presets):
                b.setChecked(False)
            button.setChecked(True)

        self.btn_dashboard.clicked.connect(lambda: set_page(self.dashboard_page, self.btn_dashboard))
        self.btn_keys.clicked.connect(lambda: set_page(self.keys_page, self.btn_keys))
        self.btn_presets.clicked.connect(lambda: set_page(self.presets_page, self.btn_presets))

        self.btn_dashboard.setChecked(True)

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_keys)
        layout.addWidget(self.btn_presets)

        layout.addStretch(1)

        status_label = QLabel("SYSTEM ONLINE")
        status_label.setObjectName("statusLabel")
        layout.addWidget(status_label)

        return frame

    def build_dashboard_page(self):
        page = QFrame()
        page.setObjectName("dashboardPage")

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        page.setLayout(layout)

        title = QLabel("Command Center")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        info_row = QHBoxLayout()
        info_row.setSpacing(20)
        layout.addLayout(info_row)

        preset_name = self.preset_manager.current_preset or "DEFAULT"
        preset_card = self.build_info_card("ACTIVE PROFILE", preset_name.upper())

        key_count = len(self.preset_manager.current_preset_data.get("keys", []))
        keys_card = self.build_info_card("MAPPED KEYS", f"{key_count}/16")

        status_card = self.build_info_card("CONNECTION", "USB-C")

        info_row.addWidget(preset_card)
        info_row.addWidget(keys_card)
        info_row.addWidget(status_card)
        layout.addStretch(1)
        return page

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

        preset_label = QLabel(f"Active Preset: {self.preset_manager.current_preset.upper()}")
        preset_label.setObjectName("pageSubtitle")
        layout.addWidget(preset_label)

        test_btn = QPushButton("TEST MODE")
        test_btn.setCheckable(True)
        test_btn.setFixedWidth(140)
        test_btn.setCursor(Qt.PointingHandCursor)

        # FIX 2: Check current state when rebuilding the page
        if self.main_window.test_mode:
            test_btn.setChecked(True)
            test_btn.setText("TEST ACTIVE")

        def toggle_test():
            enabled = test_btn.isChecked()
            self.main_window.test_mode = enabled
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

        presets = self.preset_manager.list_presets()
        current = self.preset_manager.current_preset or "default"

        for p in presets:
            item = QListWidgetItem(p)
            list_widget.addItem(item)
            if p == current:
                item.setSelected(True)

        list_widget.itemClicked.connect(self.on_preset_selected)
        self.preset_list_widget = list_widget

        layout.addWidget(list_widget)

        btn_row = QHBoxLayout()
        new_btn = QPushButton("New Preset")
        del_btn = QPushButton("Delete Preset")
        rename_btn = QPushButton("Rename Preset")

        new_btn.clicked.connect(self.create_preset)
        del_btn.clicked.connect(self.delete_preset)
        rename_btn.clicked.connect(self.rename_preset)

        btn_row.addWidget(new_btn)
        btn_row.addWidget(del_btn)
        btn_row.addWidget(rename_btn)
        layout.addLayout(btn_row)

        layout.addStretch(1)
        return page

    def on_preset_selected(self, item):
        name = item.text()
        self.main_window.switch_preset(name)

    def create_preset(self):
        name, ok = QInputDialog.getText(self, "New Preset", "Preset name:")
        if not ok or not name.strip():
            return
        name = name.strip()
        if name in self.preset_manager.list_presets():
            QMessageBox.warning(self, "Preset exists", "A preset with that name already exists.")
            return
        self.preset_manager.create_preset(name)
        self.main_window.switch_preset(name)

    def delete_preset(self):
        current = self.preset_manager.current_preset
        if not current:
            return
        presets = self.preset_manager.list_presets()
        if len(presets) <= 1:
            QMessageBox.warning(self, "Cannot delete", "You must have at least one preset.")
            return
        reply = QMessageBox.question(
            self,
            "Delete Preset",
            f"Delete preset '{current}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        self.preset_manager.delete_preset(current)
        new_current = self.preset_manager.list_presets()[0]
        self.main_window.switch_preset(new_current)

    def rename_preset(self):
        current = self.preset_manager.current_preset
        if not current:
            return
        new_name, ok = QInputDialog.getText(self, "Rename Preset", "New name:", text=current)
        if not ok or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == current:
            return
        if new_name in self.preset_manager.list_presets():
            QMessageBox.warning(self, "Preset exists", "A preset with that name already exists.")
            return
        self.preset_manager.rename_preset(current, new_name)
        self.main_window.switch_preset(new_name)

    def reload_all_pages(self):
        self.pages.removeWidget(self.keys_page)
        self.keys_page.deleteLater()
        self.keys_page = self.build_keys_page()
        self.pages.insertWidget(1, self.keys_page)

        self.pages.removeWidget(self.dashboard_page)
        self.dashboard_page.deleteLater()
        self.dashboard_page = self.build_dashboard_page()
        self.pages.insertWidget(0, self.dashboard_page)

        self.pages.removeWidget(self.presets_page)
        self.presets_page.deleteLater()
        self.presets_page = self.build_presets_page()
        self.pages.insertWidget(2, self.presets_page)

        self.pages.setCurrentWidget(self.keys_page)
        
        # FIX 1 (Part 2): Update sidebar state visually
        self.btn_dashboard.setChecked(False)
        self.btn_presets.setChecked(False)
        self.btn_keys.setChecked(True)

    def build_info_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("infoCard")
        frame.setFixedSize(200, 100)

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