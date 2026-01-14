# Macropad Controller

A 4x4 macropad built with a Raspberry Pi Pico and a desktop application.

## Structure

- `app/` – Desktop application (Python, PySide6)
- `firmware/` – MicroPython code for Raspberry Pi Pico
- `presets/` – JSON files defining key mappings and presets

## Setup

```bash
git clone https://github.com/eemi00/macro-software.git
cd macro-software

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

pip install -r requirements.txt
python app/main.py