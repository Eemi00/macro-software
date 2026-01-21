# 🎹 Macropad Controller

<div align="center">

A powerful and customizable macropad system built with Raspberry Pi Pico and Python, featuring a modern GUI for managing keyboard shortcuts, application launchers, and automation commands.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
  - [Software Setup](#1-software-setup)
  - [Firmware Setup](#2-firmware-setup-raspberry-pi-pico)
  - [Hardware Connection](#3-hardware-connection)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🔍 Overview

This project provides a complete macropad solution consisting of:

- **Hardware**: Raspberry Pi Pico running MicroPython firmware
- **Software**: Python desktop application with PySide6 GUI
- **Communication**: Serial protocol (USB) for real-time key detection
- **Customization**: JSON-based preset system with visual editor

The macropad supports 16 physical keys that can be programmed to open websites, launch applications, execute commands, and more.

---

## ✨ Features

### 🎯 Core Functionality
- **16 Programmable Keys**: 12 customizable action keys + 4 function keys
- **Multiple Action Types**:
  - 🌐 Open websites in default browser
  - 🚀 Launch applications with custom paths
  - ⚙️ Execute shell commands
  - 📁 Open file explorer locations
- **Preset Management**: Create, save, and switch between different key configurations
- **Visual Editor**: Intuitive GUI for configuring key actions with icon support

### 🎨 User Interface
- **System Tray Integration**: Runs in background with quick access menu
- **Overlay Mode**: On-screen display showing current key mappings
- **Icon Support**: FontAwesome icons + custom image support (PNG, WEBP, JPG)
- **Single Instance**: Prevents multiple app instances from running simultaneously

### ⚡ Advanced Features
- **Auto-Start**: Batch file and VBS scripts for Windows startup
- **Serial Auto-Connect**: Automatically detects connected Raspberry Pi Pico
- **Low Latency**: Real-time key detection with 10ms polling rate

---

## 💻 System Requirements

### Software Requirements
- **Operating System**: Windows 10/11 (primary support)
- **Python**: 3.8 or higher
- **Git**: For cloning the repository

### Hardware Requirements
- **Microcontroller**: Raspberry Pi Pico (RP2040)
- **Buttons**: 16x momentary push buttons
- **Connection**: USB cable (for Pico)
- **Optional**: Custom PCB or breadboard for button matrix

---

## 📦 Installation

### 1. Software Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Eemi00/macro-software.git
cd macro-software
```

#### Step 2: Create Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

> **Note**: You should see `(.venv)` prefix in your terminal when activated.

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `PySide6` - Modern Qt6 GUI framework
- `pyserial` - Serial communication with Pico
- `qtawesome` - FontAwesome icon integration

#### Step 4: Verify Installation

Test that the application can start:

```bash
python app/main.py
```

The GUI should open. You can close it after verification.

---

### 2. Firmware Setup (Raspberry Pi Pico)

#### Step 1: Install MicroPython

1. Download the latest MicroPython firmware for Raspberry Pi Pico:
   - Visit: https://micropython.org/download/rp2-pico/
   - Download the `.uf2` file (e.g., `rp2-pico-latest.uf2`)

2. Enter bootloader mode:
   - Hold the **BOOTSEL** button on your Pico
   - While holding, plug the Pico into your computer via USB
   - Release the button after connecting
   - The Pico will appear as a USB mass storage device named `RPI-RP2`

3. Flash MicroPython:
   - Copy the downloaded `.uf2` file to the `RPI-RP2` drive
   - The Pico will automatically reboot with MicroPython installed

#### Step 2: Upload Firmware Code

1. The Pico should now be connected as a serial device (typically `COM3`, `COM4`, etc.)

2. Copy the firmware to the Pico:
   ```bash
   # Option A: Using a file explorer
   # Copy app/firmware/main.py to the Pico's drive as main.py
   
   # Option B: Using Thonny IDE (recommended)
   # 1. Install Thonny: https://thonny.org/
   # 2. Open Thonny and select "MicroPython (Raspberry Pi Pico)" interpreter
   # 3. Open app/firmware/main.py
   # 4. Click "File" > "Save as..." > "Raspberry Pi Pico"
   # 5. Save as "main.py" on the Pico
   ```

3. **Verify Firmware**:
   - Disconnect and reconnect the Pico
   - The firmware will auto-start on boot
   - Press any button - it should send `KEY:X` messages over serial

#### Firmware Pin Configuration

The default firmware is configured for GPIO pins:
```
Keys 1-12:  GPIO 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
Keys 13-16: GPIO 13, 14, 18, 22
```

> **Note**: Modify `app/firmware/main.py` if your button wiring differs.

---

### 3. Hardware Connection

1. **Connect Buttons to Pico**:
   - Connect one side of each button to the GPIO pins listed above
   - Connect the other side to GND
   - The firmware uses internal pull-up resistors (no external resistors needed)

2. **Connect Pico to Computer**:
   - Use a USB cable to connect the Pico to your computer
   - The application will auto-detect the Pico on the correct COM port

3. **Test Connection**:
   - Run the application: `python app/main.py`
   - Check the status bar for "Connected to COMX"
   - Press a button to verify it registers in the app

---

## 🚀 Usage

### Starting the Application

#### Manual Start
```bash
# Activate virtual environment (if not already active)
.venv\Scripts\activate

# Run the application
python app/main.py
```

#### Quick Start (Windows)
Double-click `macropad_start.vbs` to start the application silently in the background.

Or use `macropad_controller.bat` to start with a visible terminal window.

### Basic Operations

#### Configuring Keys
1. Open the Macropad Controller window
2. Click on any key slot (1-12)
3. Choose action type:
   - **Website**: Enter URL (e.g., `https://github.com`)
   - **Application**: Browse for `.exe` file
   - **Command**: Enter shell command
4. Set a label and select an icon
5. Click **Save Preset** to persist changes

#### Using Function Keys
- **Key 13 (F1)**: Toggle main window visibility
- **Key 14 (F2)**: Show/hide overlay with key labels
- **Key 15 (F3)**: Load previous preset
- **Key 16 (F4)**: Load next preset

#### Overlay Mode
Press Key 14 (F2) or use the system tray menu to toggle an on-screen overlay showing your current key configuration. Great for learning new layouts!

#### System Tray
The app runs in the system tray with these options:
- **Show/Hide**: Toggle main window
- **Test Mode**: Test actions without serial connection
- **Quit**: Exit application

---

## 📁 Project Structure

```
macro-software/
├── app/
│   ├── main.py                 # Main application entry point
│   ├── assets/
│   │   └── custom_icons/       # Custom icon images (PNG, WEBP, JPG)
│   ├── core/
│   │   ├── action_executor.py  # Executes key actions (launch apps, open URLs)
│   │   ├── preset_manager.py   # Manages JSON preset files
│   │   └── serial_manager.py   # Serial communication with Pico
│   ├── firmware/
│   │   └── main.py             # MicroPython firmware for Pico
│   ├── presets/
│   │   └── default.json        # Default key configuration
│   ├── styles/
│   │   └── main.css            # Application styling
│   └── ui/
│       ├── action_editor.py    # Key configuration dialog
│       ├── main_window.py      # Main GUI window
│       └── overlay.py          # On-screen overlay window
├── macropad_controller.bat     # Windows batch launcher
├── macropad_start.vbs          # Silent VBS launcher
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## ⚙️ Configuration

### Preset Files

Presets are stored as JSON files in `app/presets/`. Example structure:

```json
{
    "name": "default",
    "keys": [
        {
            "type": "open_website",
            "value": "https://github.com",
            "label": "GitHub",
            "icon": "fa5b.github"
        },
        {
            "type": "open_app",
            "value": "C:\\Program Files\\App\\app.exe",
            "label": "My App",
            "icon": "fa5s.rocket"
        }
    ]
}
```

### Action Types

- `open_website`: Opens URL in default browser
- `open_app`: Launches executable file
- `run_command`: Executes shell command
- `open_location`: Opens folder in File Explorer
- `none`: No action (empty key)

### Custom Icons

1. Place image files in `app/assets/custom_icons/`
2. In the action editor, browse and select your custom icon
3. Supported formats: PNG, WEBP, JPG, SVG

### Auto-Start Setup

To launch the app on Windows startup:

1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create a shortcut to `macropad_start.vbs` in the opened folder

---

## 🔧 Troubleshooting

### Application Won't Start

**Issue**: `ModuleNotFoundError: No module named 'PySide6'`

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

---

### Pico Not Detected

**Issue**: Status bar shows "Disconnected" or "No device found"

**Solutions**:
1. Check USB cable connection
2. Verify firmware is installed on Pico (should print `Macropad firmware started` on serial connection)
3. Check Device Manager for COM port conflicts
4. Try a different USB port
5. Restart the application

---

### Keys Not Responding

**Issue**: Pressing buttons doesn't trigger actions

**Solutions**:
1. Check button wiring (button → GPIO, other side → GND)
2. Verify GPIO pin numbers in firmware match your wiring
3. Test in serial monitor (Thonny) to see if `KEY:X` messages appear
4. Ensure Pico is connected to app (check status bar)

---

### Icons Not Displaying

**Issue**: Custom icons show as blank or missing

**Solutions**:
1. Use absolute paths for custom icons
2. Verify file format is supported (PNG, WEBP, JPG)
3. Check file permissions
4. For FontAwesome icons, use format: `fa5s.icon-name` or `fa5b.icon-name`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Describe your idea in a new issue
3. **Submit Pull Requests**: 
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a PR with clear description

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/macro-software.git
cd macro-software

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make changes and test
python app/main.py
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Raspberry Pi Foundation** - For the excellent Pico microcontroller
- **Qt Project** - For the PySide6 framework
- **FontAwesome** - For the icon library
- **MicroPython** - For making Python on microcontrollers possible

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search [existing issues](https://github.com/Eemi00/macro-software/issues)
3. Open a [new issue](https://github.com/Eemi00/macro-software/issues/new) with details

---

<div align="center">

**Made with ❤️ by [Eemi00](https://github.com/Eemi00)**

⭐ Star this repo if you find it helpful!

</div>