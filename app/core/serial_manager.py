# core/serial_manager.py

import serial
import threading
import time
from PySide6.QtCore import QObject, Signal  # <--- NEW IMPORT

# Inherit from QObject
class SerialManager(QObject):
    # Create a signal that carries a True/False value
    connection_status = Signal(bool)

    def __init__(self, port, callback, baudrate=115200):
        super().__init__()  # Initialize QObject
        self.port = port
        self.callback = callback
        self.baudrate = baudrate
        self.running = False
        self.ser = None

    def start(self):
        print(f"[SerialManager] Starting on port {self.port}")
        
        # Run the connection attempt in a separate thread so UI doesn't freeze
        threading.Thread(target=self._connect_loop, daemon=True).start()

    def _connect_loop(self):
        # Notify UI we are searching (False initially)
        self.connection_status.emit(False)

        for attempt in range(10):
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
                self.running = True
                
                # SUCCESS! Tell the UI we are connected
                self.connection_status.emit(True)
                print("[SerialManager] Connected")

                # Start reading
                self.read_loop()
                return
            except Exception as e:
                print(f"[SerialManager] Failed attempt {attempt+1}:", e)
                time.sleep(1)
        
        print("[SerialManager] Could not open serial port")
        self.connection_status.emit(False)

    def read_loop(self):
        print("[SerialManager] read_loop started")
        while self.running:
            try:
                if self.ser:
                    line = self.ser.readline().decode().strip()
                    if line:
                        print("[SerialManager] RAW:", line)

                    if line.startswith("KEY:") or line.startswith("BTN:"):
                        _, value = line.split(":", 1)
                        self.callback(int(value))
            except Exception as e:
                print("[SerialManager] read_loop error (Device disconnected?):", e)
                self.running = False
                self.connection_status.emit(False) # Tell UI we lost connection
                break

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()