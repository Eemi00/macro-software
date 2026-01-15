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
        layout = QGridLayout(self)
        layout.setSpacing(10)

        for i in range(16):
            row, col = divmod(i, 4)
            btn = QPushButton()
            btn.setFixedSize(100, 100)
            btn.setCursor(Qt.PointingHandCursor)

            if row == 3:
                labels = ["APP", "LAYER", "PREV", "NEXT"]
                btn.setText(labels[col])
                btn.setProperty("class", "fixed-key")
                if col == 0: btn.clicked.connect(self.main_window.show_interface)
                elif col == 1: btn.clicked.connect(self.main_window.show_overlay)
                elif col == 2: btn.clicked.connect(self.main_window.prev_preset)
                elif col == 3: btn.clicked.connect(self.main_window.next_preset)
            else:
                btn.setText(f"{i + 1:02d}")
                btn.setProperty("class", "macro-key")
                btn.clicked.connect(lambda _, x=i: self.on_click(x))
            layout.addWidget(btn, row, col)

    def on_click(self, index):
        if self.main_window.test_mode:
            keys = self.preset_manager.current_preset_data.get("keys", [])
            if index < len(keys): self.main_window.executor.execute(keys[index], force=True)
        else:
            if ActionEditor(index, self.preset_manager).exec():
                self.main_window.view.reload_all_pages()

class MainView(QWidget):
    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame(); self.sidebar.setObjectName("sidebar")
        side_lyt = QVBoxLayout(self.sidebar)
        
        title = QLabel("MACROPAD"); title.setObjectName("sidebarTitle")
        sub = QLabel("MK.III // GRID"); sub.setObjectName("sidebarSubtitle")
        side_lyt.addWidget(title); side_lyt.addWidget(sub); side_lyt.addSpacing(20)

        self.nav_btns = []
        for i, text in enumerate(["DASHBOARD", "KEY CONFIG", "PRESETS"]):
            btn = QPushButton(text); btn.setObjectName("navButton"); btn.setCheckable(True)
            btn.clicked.connect(lambda _, idx=i: self.switch_page(idx))
            side_lyt.addWidget(btn)
            self.nav_btns.append(btn)

        side_lyt.addStretch()
        self.status_label = QLabel("OFFLINE"); self.status_label.setObjectName("statusLabel")
        side_lyt.addWidget(self.status_label)

        self.pages = QStackedWidget()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        self.reload_all_pages()

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)

    def reload_all_pages(self):
        """Total refresh of all UI components to sync with JSON files."""
        cur_idx = self.pages.currentIndex() if self.pages.count() > 0 else 0
        while self.pages.count():
            w = self.pages.widget(0)
            self.pages.removeWidget(w)
            w.deleteLater()
        
        self.pages.addWidget(self.build_dashboard())
        self.pages.addWidget(self.build_keys())
        self.pages.addWidget(self.build_presets())
        self.switch_page(cur_idx)

    def build_dashboard(self):
        page = QFrame()
        lyt = QVBoxLayout(page); lyt.setContentsMargins(50,50,50,50)
        title = QLabel("Command Center"); title.setObjectName("pageTitle"); lyt.addWidget(title)
        
        row = QHBoxLayout()
        row.addWidget(self.info_card("ACTIVE PROFILE", self.preset_manager.current_preset.upper()))
        
        # Mapped Keys Logic
        mapped_count = self.preset_manager.count_total_mapped_keys()
        row.addWidget(self.info_card("MAPPED KEYS", str(mapped_count)))
        
        self.conn_card = self.info_card("CONNECTION", "OFFLINE")
        row.addWidget(self.conn_card)
        
        lyt.addLayout(row); lyt.addStretch()
        return page

    def info_card(self, t, v):
        f = QFrame(); f.setObjectName("infoCard"); f.setFixedSize(220, 100)
        l = QVBoxLayout(f); l.addWidget(QLabel(t))
        val = QLabel(v); val.setObjectName("infoCardValue"); l.addWidget(val)
        f.value_label = val
        return f

    def build_keys(self):
        page = QFrame()
        lyt = QVBoxLayout(page); lyt.setContentsMargins(50,50,50,50)
        
        hdr = QHBoxLayout()
        v_lyt = QVBoxLayout()
        title = QLabel("Grid Layout"); title.setObjectName("pageTitle")
        # CURRENT PRESET LABEL BACK IN CONFIG
        self.preset_lbl = QLabel(f"Current Preset: {self.preset_manager.current_preset}")
        self.preset_lbl.setStyleSheet("color: #10b981; font-weight: bold; font-size: 14px;")
        v_lyt.addWidget(title); v_lyt.addWidget(self.preset_lbl)
        
        hdr.addLayout(v_lyt); hdr.addStretch()
        
        tbtn = QPushButton("TEST MODE"); tbtn.setCheckable(True)
        tbtn.setChecked(self.main_window.test_mode)
        tbtn.clicked.connect(lambda: setattr(self.main_window, 'test_mode', tbtn.isChecked()))
        hdr.addWidget(tbtn)
        
        lyt.addLayout(hdr)
        lyt.addWidget(MacropadGrid(self.preset_manager, self.main_window), alignment=Qt.AlignCenter)
        lyt.addStretch()
        return page

    def build_presets(self):
        page = QFrame()
        lyt = QVBoxLayout(page)
        lyt.setContentsMargins(50, 50, 50, 50)
        
        # Header with Buttons
        hdr = QHBoxLayout()
        hdr.addWidget(QLabel("AVAILABLE PROFILES"))
        hdr.addStretch()
        
        btn_add = QPushButton("+ NEW")
        btn_ren = QPushButton("RENAME")
        btn_del = QPushButton("DELETE")
        
        # Link to the fixed functions
        btn_add.clicked.connect(self.add_preset)
        btn_ren.clicked.connect(self.rename_preset)
        btn_del.clicked.connect(self.delete_preset)
        
        hdr.addWidget(btn_add)
        hdr.addWidget(btn_ren)
        hdr.addWidget(btn_del)
        lyt.addLayout(hdr)

        # The List
        self.plist = QListWidget()
        self.plist.setObjectName("presetList")
        for p in self.preset_manager.list_presets():
            item = QListWidgetItem(p)
            self.plist.addItem(item)
            if p == self.preset_manager.current_preset:
                item.setSelected(True)
        
        self.plist.itemClicked.connect(self.on_preset_select)
        lyt.addWidget(self.plist)
        return page

    def on_preset_select(self, item):
        """Triggered when clicking a preset in the list."""
        self.main_window.switch_preset(item.text())
        self.switch_page(1) # Jump to key config automatically

    def add_preset(self):
        name, ok = QInputDialog.getText(self, "New Preset", "Enter preset name:")
        if ok and name:
            name = name.strip()
            if name in self.preset_manager.list_presets():
                QMessageBox.warning(self, "Error", "A preset with that name already exists!")
                return
            
            self.preset_manager.create_preset(name)
            self.main_window.switch_preset(name) # This reloads everything automatically
            self.switch_page(1) # Jump to Key Config

    def rename_preset(self):
        # Acts on the CURRENTLY ACTIVE preset
        old_name = self.preset_manager.current_preset
        
        if old_name == "default":
            QMessageBox.warning(self, "Protected", "The 'default' preset cannot be renamed.")
            return

        new_name, ok = QInputDialog.getText(
            self, "Rename Active Preset", 
            f"Enter new name for '{old_name}':", 
            text=old_name
        )
        
        if ok and new_name and new_name.strip() != old_name:
            new_name = new_name.strip()
            self.preset_manager.rename_preset(old_name, new_name)
            self.main_window.switch_preset(new_name)
            self.switch_page(1)

    def delete_preset(self):
        # Acts on the CURRENTLY ACTIVE preset
        target = self.preset_manager.current_preset
        
        if target == "default":
            QMessageBox.warning(self, "Protected", "The 'default' preset cannot be deleted.")
            return

        # --- CONFIRMATION DIALOG ---
        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to permanently delete the preset: '{target}'?\n\nThis cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.preset_manager.delete_preset(target)
            # Always switch back to default after a deletion
            self.main_window.switch_preset("default")
            self.switch_page(0) # Go to Dashboard to see updated count

    def update_connection_state(self, connected):
        status = "ACTIVE" if connected else "OFFLINE"
        color = "#10b981" if connected else "#ef4444"
        if hasattr(self, 'status_label'):
            self.status_label.setText(status); self.status_label.setStyleSheet(f"color: {color};")
        if hasattr(self, 'conn_card'):
            self.conn_card.value_label.setText(status); self.conn_card.value_label.setStyleSheet(f"color: {color};")