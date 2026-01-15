# core/serial_manager.py

import serial
import threading
import time

class SerialManager:
    def __init__(self, port, callback, baudrate=115200):
        self.port = port
        self.callback = callback
        self.baudrate = baudrate
        self.running = False
        self.ser = None

    def start(self):
        print("[SerialManager] Starting on port", self.port)
        for attempt in range(10):
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
                self.running = True

                self.thread = threading.Thread(target=self.read_loop, daemon=True)
                self.thread.start()
                print("[SerialManager] Connected")
                return
            except Exception as e:
                print(f"[SerialManager] Failed attempt {attempt+1}:", e)
                time.sleep(1)

        print("[SerialManager] Could not open serial port")

    def read_loop(self):
        print("[SerialManager] read_loop started")
        while self.running:
            try:
                line = self.ser.readline().decode().strip()
                if line:
                    print("[SerialManager] RAW:", line)

                if line.startswith("KEY:") or line.startswith("BTN:"):
                    _, value = line.split(":", 1)
                    index = int(value)
                    print("[SerialManager] Parsed key index:", index)
                    self.callback(index)

            except Exception as e:
                print("[SerialManager] read_loop error:", e)
                time.sleep(0.1)
