# 🖥️ Macropad Software

A simple macropad system using:

- Raspberry Pi Pico (MicroPython firmware)
- Python desktop app (PySide6)
- Serial communication (BTN:1–16)
- Customizable key actions stored in JSON

---

## 🚀 Features

- 12 customizable keys  
- 4 function keys (Open App, Overlay, Prev/Next Preset)  
- GUI for editing actions  
- Supports:
  - Opening websites  
  - Launching applications  
  - Running commands  

---

## 📦 Installation (Windows)

### 1. Clone the repo
```bash
git clone https://github.com/Eemi00/macro-software.git
cd macro-software
```

## 2. Create & activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

🔌 Flash Firmware to Pico

Hold BOOTSEL
Plug in the Pico
Copy app/firmware/main.py to the Pico as main.py
Reconnect normally
The Pico will send messages like:

```bash
BTN:1
BTN:2
BTN:13
```

# Run the app
```bash
python app/main.py
```