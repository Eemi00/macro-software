import os

from PySide6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QStackedWidget, QFrame,
    QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, QUrl
from ui.action_editor import ActionEditor

class MacropadGrid(QWidget):
    """The 4x4 grid of buttons representing the physical macropad."""
    
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
        """Handle button click: Execute action in test mode or open editor."""
        if self.main_window.test_mode:
            keys = self.preset_manager.current_preset_data.get("keys", [])
            if index < len(keys): self.main_window.executor.execute(keys[index], force=True)
        else:
            if ActionEditor(index, self.preset_manager).exec():
                self.main_window.view.reload_all_pages()
                if self.main_window.overlay:
                     self.main_window.overlay.refresh()

class MainView(QWidget):
    """The main central widget containing sidebar and pages."""

    def __init__(self, preset_manager, main_window):
        super().__init__()
        self.preset_manager = preset_manager
        self.main_window = main_window
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Sidebar setup
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
        
        self.is_connected = False

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

    def build_model_view(self):
        model_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "macropad.glb")
        )
        return RotatingModelWidget(model_path)

    def build_dashboard(self):
        page = QFrame()
        page.setObjectName("dashboardPage")
        lyt = QVBoxLayout(page); lyt.setContentsMargins(50,50,50,50)
        title = QLabel("Command Center"); title.setObjectName("pageTitle"); lyt.addWidget(title)
        
        row = QHBoxLayout()
        row.addWidget(self.info_card("ACTIVE PROFILE", self.preset_manager.current_preset.upper()))
        
        # Mapped Keys Logic
        mapped_count = self.preset_manager.count_total_mapped_keys()
        row.addWidget(self.info_card("MAPPED KEYS", str(mapped_count)))
        
        status = "ACTIVE" if self.is_connected else "OFFLINE"
        color = "#10b981" if self.is_connected else "#ef4444"
        
        self.conn_card = self.info_card("CONNECTION", status)
        self.conn_card.value_label.setStyleSheet(f"color: {color};")
        row.addWidget(self.conn_card)

        lyt.addLayout(row)
        lyt.addSpacing(20)
        lyt.addWidget(self.build_model_view(), alignment=Qt.AlignCenter)
        lyt.addStretch()
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
        self.is_connected = connected
        status = "ACTIVE" if connected else "OFFLINE"
        color = "#10b981" if connected else "#ef4444"
        if hasattr(self, 'status_label'):
            self.status_label.setText(status); self.status_label.setStyleSheet(f"color: {color};")
        if hasattr(self, 'conn_card'):
            self.conn_card.value_label.setText(status); self.conn_card.value_label.setStyleSheet(f"color: {color};")


class RotatingModelWidget(QWidget):
    def __init__(self, model_path, parent=None):
        super().__init__(parent)
        self.setMinimumSize(520, 320)

        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWebEngineCore import QWebEngineSettings

        self.view = QWebEngineView()
        self.view.setAttribute(Qt.WA_TranslucentBackground, True)
        self.view.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.view.setFocusPolicy(Qt.NoFocus)
        self.view.setContextMenuPolicy(Qt.NoContextMenu)
        self.view.setStyleSheet("background: transparent;")
        self.view.page().setBackgroundColor(Qt.transparent)

        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        base_url = QUrl.fromLocalFile(os.path.dirname(model_path) + os.sep)
        self.view.setHtml(self._build_html(), base_url)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def _build_html(self):
        return """<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        html, body { margin: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }
        #wrap { position: relative; width: 100%; height: 100%; }
        #c { width: 100%; height: 100%; display: block; background: transparent; position: relative; z-index: 1; }
    
    </style>
</head>
<body>
    <div id="wrap">
        <canvas id="c"></canvas>
    </div>
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js"
            }
        }
    </script>
    <script type="module">
        import * as THREE from 'three';
        import { GLTFLoader } from 'https://unpkg.com/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';
        import { RoomEnvironment } from 'https://unpkg.com/three@0.160.0/examples/jsm/environments/RoomEnvironment.js';

        const canvas = document.getElementById('c');
        const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
        renderer.setPixelRatio(window.devicePixelRatio || 1);
        renderer.setClearColor(0x000000, 0);
        renderer.outputColorSpace = THREE.SRGBColorSpace;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 0.95;
        renderer.physicallyCorrectLights = true;
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        const scene = new THREE.Scene();
        scene.background = null;

        const pmrem = new THREE.PMREMGenerator(renderer);
        scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

        const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
        camera.position.set(0, 0, 5);

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.3);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.set(1024, 1024);
        keyLight.shadow.bias = -0.00015;
        scene.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0xffffff, 0.9);
        fillLight.position.set(-6, 3, 8);
        scene.add(fillLight);

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const rim = new THREE.DirectionalLight(0xffffff, 0.8);
        rim.position.set(-6, -2, -8);
        scene.add(rim);

        const loader = new GLTFLoader();
        let model = null;
        loader.load('macropad.glb', (gltf) => {
                        model = gltf.scene;
                        model.traverse((obj) => {
                            if (obj.isMesh && obj.material) {
                                const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
                                mats.forEach((m) => {
                                    if (m.isMeshStandardMaterial) {
                                        m.metalness = 0.0;
                                        m.roughness = 0.9;
                                        m.envMapIntensity = 0.0;
                                    }
                                    m.needsUpdate = true;
                                });
                                obj.castShadow = true;
                                obj.receiveShadow = true;
                            }
                        });
            scene.add(model);

            const box = new THREE.Box3().setFromObject(model);
            const size = box.getSize(new THREE.Vector3()).length();
            const center = box.getCenter(new THREE.Vector3());
            model.position.sub(center);
            model.position.y += size * 0.19;
            const scale = 140.0 / size;
            model.scale.setScalar(scale);

            const sphere = new THREE.Sphere();
            box.getBoundingSphere(sphere);
            camera.position.set(0, 0, sphere.radius * 1.8);
            camera.lookAt(0, 0, 0);
        }, undefined, (err) => {
            console.error('Failed to load GLB', err);
        });

        function resize() {
            const w = canvas.clientWidth;
            const h = canvas.clientHeight;
            renderer.setSize(w, h, false);
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
        }

        window.addEventListener('resize', resize);
        resize();

        function animate() {
            requestAnimationFrame(animate);
            if (model) model.rotation.y += 0.003;
            keyLight.position.copy(camera.position);
            keyLight.target.position.set(0, 0, 0);
            keyLight.target.updateMatrixWorld();
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>"""