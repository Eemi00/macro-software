# ui/action_editor.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QHBoxLayout, QStackedWidget, QFileDialog, QWidget, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
import os
import qtawesome as qta

# Organized Icon Library by Categories
ICON_LIBRARY = {
    "Brands": {
        "Discord": "fa5b.discord",
        "GitHub": "fa5b.github",
        "Twitch": "fa5b.twitch",
        "YouTube": "fa5b.youtube",
        "Spotify": "fa5b.spotify",
        "Chrome": "fa5b.chrome",
        "Firefox": "fa5b.firefox",
        "Twitter": "fa5b.twitter",
        "Reddit": "fa5b.reddit",
        "Steam": "fa5b.steam",
    },
    "Media": {
        "Play": "fa5s.play",
        "Pause": "fa5s.pause",
        "Stop": "fa5s.stop",
        "Music": "fa5s.music",
        "Camera": "fa5s.video",
        "Screenshot": "fa5s.screenshot",
        "Volume Up": "fa5s.volume-up",
        "Volume Down": "fa5s.volume-down",
        "Mute": "fa5s.volume-mute",
        "Mic On": "fa5s.microphone",
        "Mic Off": "fa5s.microphone-slash",
    },
    "System": {
        "Home": "fa5s.home",
        "Settings": "fa5s.cog",
        "Power": "fa5s.power-off",
        "Terminal": "fa5s.terminal",
        "Folder": "fa5s.folder",
        "Trash": "fa5s.trash",
        "File": "fa5s.file",
        "Copy": "fa5s.copy",
        "Paste": "fa5s.paste",
        "Cut": "fa5s.cut",
        "Save": "fa5s.save",
        "Print": "fa5s.print",
    },
    "Navigation": {
        "Back": "fa5s.arrow-left",
        "Forward": "fa5s.arrow-right",
        "Refresh": "fa5s.sync",
        "Home": "fa5s.home",
        "Menu": "fa5s.bars",
        "Search": "fa5s.search",
        "Download": "fa5s.download",
        "Upload": "fa5s.upload",
    },
    "Development": {
        "Code": "fa5s.code",
        "Terminal": "fa5s.terminal",
        "GitHub": "fa5b.github",
        "Bug": "fa5s.bug",
        "Cogs": "fa5s.cogs",
        "Database": "fa5s.database",
    },
    "Communication": {
        "Chat": "fa5s.comments",
        "Mail": "fa5s.envelope",
        "Bell": "fa5s.bell",
        "Phone": "fa5s.phone",
        "User": "fa5s.user",
        "Users": "fa5s.users",
    },
    "Streaming": {
        "OBS": "fa5s.record-vinyl",
        "Twitch": "fa5b.twitch",
        "YouTube": "fa5b.youtube",
        "Broadcast": "fa5s.broadcast-tower",
        "Stream": "fa5s.stream",
    },
    "Gaming": {
        "Game": "fa5s.gamepad",
        "Dice": "fa5s.dice",
        "Joystick": "fa5s.gamepad",
        "Target": "fa5s.bullseye",
    },
    "UI": {
        "Minimize": "fa5s.window-minimize",
        "Maximize": "fa5s.window-maximize",
        "Close": "fa5s.window-close",
        "Expand": "fa5s.expand",
        "Compress": "fa5s.compress",
    },
    "Status": {
        "Lock": "fa5s.lock",
        "Unlock": "fa5s.unlock",
        "Heart": "fa5s.heart",
        "Star": "fa5s.star",
        "Check": "fa5s.check",
        "X": "fa5s.times",
        "Clock": "fa5s.clock",
        "Calendar": "fa5s.calendar",
    },
}

class KeyRecorder(QLineEdit):
    """A textbox that records key combinations in order and resets on release."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Press keys... (e.g., CTRL+ALT+I)")
        self.setReadOnly(True)
        self.active_keys = []
        self.keys_pressed_count = 0 

    def keyPressEvent(self, event):
        if event.isAutoRepeat(): return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.clearFocus()
            return

        self.keys_pressed_count += 1
        key_map = {
            Qt.Key_Control: "CTRL",
            Qt.Key_Shift: "SHIFT",
            Qt.Key_Alt: "ALT",
            Qt.Key_Meta: "WINDOWS",
        }
        
        key_text = key_map.get(event.key(), event.text().upper())
        if not key_text or key_text.isspace():
            key_text = event.key().name.upper()

        if key_text not in self.active_keys:
            self.active_keys.append(key_text)
        
        self.setText("+".join(self.active_keys))

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat(): return
        if self.keys_pressed_count > 0:
            self.keys_pressed_count -= 1
        if self.keys_pressed_count == 0:
            self.active_keys = []


class IconPickerDialog(QDialog):
    """Dialog for selecting icons from categorized library."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Icon")
        self.setMinimumSize(500, 400)
        self.selected_icon = None
        self.selected_icon_id = None
        
        layout = QVBoxLayout(self)
        
        # Category list on the left
        cat_layout = QHBoxLayout()
        
        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.on_category_selected)
        for category in ICON_LIBRARY.keys():
            self.category_list.addItem(category)
        self.category_list.setMaximumWidth(150)
        cat_layout.addWidget(self.category_list)
        
        # Icons grid on the right
        self.icon_list = QListWidget()
        self.icon_list.setSpacing(5)
        self.icon_list.itemDoubleClicked.connect(self.accept)
        self.icon_list.itemClicked.connect(self.on_icon_selected)
        cat_layout.addWidget(self.icon_list)
        
        layout.addLayout(cat_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("Select")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # Select first category by default
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
            self.on_category_selected(self.category_list.item(0))
    
    def on_category_selected(self, item):
        """Populate icon list when category is selected."""
        category = item.text()
        self.icon_list.clear()
        
        if category in ICON_LIBRARY:
            for icon_name, icon_id in ICON_LIBRARY[category].items():
                try:
                    icon = qta.icon(icon_id, color="#e0e0e0")
                    list_item = QListWidgetItem(icon, icon_name)
                    list_item.setData(Qt.UserRole, icon_id)
                    self.icon_list.addItem(list_item)
                except:
                    pass
        
        # Set icon size
        self.icon_list.setIconSize(QSize(32, 32))
    
    def on_icon_selected(self, item):
        """Store selected icon."""
        self.selected_icon = item.text()
        self.selected_icon_id = item.data(Qt.UserRole)


class ActionEditor(QDialog):
    def __init__(self, key_index, preset_manager):
        super().__init__()
        self.key_index = key_index
        self.preset_manager = preset_manager

        preset_name = str(self.preset_manager.current_preset).replace("_", " ").title()
        self.setWindowTitle(f"Config Key {key_index + 1}")
        self.setMinimumWidth(450)

        # Main Layout with cleaner spacing
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel(f"Editing Preset: {preset_name}")
        header.setStyleSheet("color: #10b981; font-weight: 800; font-size: 14px; border: none;")
        layout.addWidget(header)

        # 2. Display Name
        layout.addWidget(QLabel("Overlay Label:"))
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText("Enter custom text...")
        layout.addWidget(self.label_input)

        # 2.5 Icon Selection
        layout.addWidget(QLabel("Icon:"))
        icon_row = QHBoxLayout()
        
        self.icon_preview = QLabel("No Icon")
        self.icon_preview.setFixedSize(40, 40)
        self.icon_preview.setStyleSheet("border: 1px solid #444; background: #222; color: #888;")
        self.icon_preview.setAlignment(Qt.AlignCenter)
        icon_row.addWidget(self.icon_preview)

        self.icon_path = "" # Store the path
        self.icon_id = None  # Store the icon ID

        # Icon Library Button
        library_btn = QPushButton("From Library")
        library_btn.clicked.connect(self.select_library_icon)
        icon_row.addWidget(library_btn)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_icon_file)
        icon_row.addWidget(browse_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_icon)
        icon_row.addWidget(clear_btn)
        
        layout.addLayout(icon_row)

        # 3. Action Type
        layout.addWidget(QLabel("Action Type:"))
        self.type_box = QComboBox()
        self.type_box.addItems(["None", "Open Website", "Open App", "Run Command", "Key Combo", "Type Text"])
        layout.addWidget(self.type_box)

        # 4. Input Stack
        self.input_stack = QStackedWidget()
        layout.addWidget(self.input_stack)
        self.setup_inputs()
        self.type_box.currentIndexChanged.connect(self.input_stack.setCurrentIndex)

        # 5. Buttons
        btn_row = QHBoxLayout()
        
        remove_btn = QPushButton("Remove Config")
        remove_btn.setCursor(Qt.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #111;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 8px 16px;
                color: #ef4444;
                font-weight: 600;
            }
            QPushButton:hover {
                border: 1px solid #ef4444;
                background-color: #290a0a;
            }
            QPushButton:pressed {
                background-color: #ef4444;
                color: white;
            }
        """)
        remove_btn.clicked.connect(self.remove_config)
        btn_row.addWidget(remove_btn)
        
        btn_row.addStretch()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.load_data()

    def remove_config(self):
        keys = self.preset_manager.current_preset_data.get("keys", [])
        if self.key_index < len(keys):
            keys[self.key_index] = {
                "type": "none",
                "value": "",
                "label": "",
                "icon": ""
            }
            self.preset_manager.save_data(self.preset_manager.current_preset, self.preset_manager.current_preset_data)
        self.accept()

    def setup_inputs(self):
        # 0: None
        self.input_stack.addWidget(QLabel("No configuration needed."))
        # 1: Website
        self.web_in = QLineEdit(); self.web_in.setPlaceholderText("https://...")
        self.input_stack.addWidget(self.web_in)
        # 2: App
        app_w = QWidget(); app_l = QHBoxLayout(app_w); app_l.setContentsMargins(0,0,0,0)
        self.app_in = QLineEdit()
        btn = QPushButton("BROWSE"); btn.clicked.connect(self.browse_app)
        app_l.addWidget(self.app_in); app_l.addWidget(btn)
        self.input_stack.addWidget(app_w)
        # 3: Command
        self.cmd_in = QLineEdit()
        self.input_stack.addWidget(self.cmd_in)
        # 4: Key Combo
        self.recorder = KeyRecorder()
        self.input_stack.addWidget(self.recorder)
        # 5: Type Text
        self.text_in = QLineEdit()
        self.input_stack.addWidget(self.text_in)

    def browse_app(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select App", "", "Executable (*.exe)")
        if path: self.app_in.setText(path)

    def select_library_icon(self):
        """Open categorized icon picker dialog."""
        dialog = IconPickerDialog(self)
        if dialog.exec():
            if dialog.selected_icon_id:
                self.update_icon(dialog.selected_icon_id)

    def select_icon_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Images (*.png *.svg *.jpg *.ico)")
        if path:
            self.update_icon(path)

    def clear_icon(self):
        self.icon_path = ""
        self.icon_id = None
        self.icon_preview.setPixmap(QPixmap())
        self.icon_preview.setText("No Icon")

    def update_icon(self, icon_source):
        self.icon_path = icon_source
        
        # 1. Check for File Path
        if os.path.exists(icon_source):
            pix = QPixmap(icon_source)
            if not pix.isNull():
                self.icon_preview.setPixmap(pix.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.icon_preview.setText("")
                return
        
        # 2. Check for FontAwesome ID
        try:
            if icon_source:
                icon = qta.icon(icon_source, color="white")
                pix = icon.pixmap(32, 32)
                if not pix.isNull():
                    self.icon_preview.setPixmap(pix)
                    self.icon_preview.setText("")
                    return
        except:
            pass

        self.icon_preview.setText("Err")

    def load_data(self):
        keys = self.preset_manager.current_preset_data.get("keys", [])
        if self.key_index < len(keys):
            curr = keys[self.key_index]
            self.label_input.setText(curr.get("label", ""))
            
            icon = curr.get("icon", "")
            if icon:
                self.update_icon(icon)
                self.icon_id = icon  # Store the icon ID
            
            # Map saved snake_case to UI Display Names
            mapping = {"none": 0, "open_website": 1, "open_app": 2, "run_command": 3, "key_combo": 4, "type_text": 5}
            idx = mapping.get(curr.get("type", "none"), 0)
            self.type_box.setCurrentIndex(idx)
            
            val = curr.get("value", "")
            if idx == 1: self.web_in.setText(val)
            elif idx == 2: self.app_in.setText(val)
            elif idx == 3: self.cmd_in.setText(val)
            elif idx == 4: self.recorder.setText(val)
            elif idx == 5: self.text_in.setText(val)

    def save(self):
        idx = self.type_box.currentIndex()
        mapping = ["none", "open_website", "open_app", "run_command", "key_combo", "type_text"]
        vals = ["", self.web_in.text(), self.app_in.text(), self.cmd_in.text(), self.recorder.text(), self.text_in.text()]
        
        keys = self.preset_manager.current_preset_data.get("keys", [])
        while len(keys) <= self.key_index:
            keys.append({"type": "none", "value": "", "label": ""})
            
        keys[self.key_index] = {
            "type": mapping[idx],
            "value": vals[idx],
            "label": self.label_input.text(),
            "icon": self.icon_path
        }
        self.preset_manager.save_data(self.preset_manager.current_preset, self.preset_manager.current_preset_data)
        self.accept()