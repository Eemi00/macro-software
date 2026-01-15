# serial_manager.py
import serial
import threading
import time
from PySide6.QtCore import QObject, Signal

class SerialManager(QObject):
    connection_status = Signal(bool)
    key_pressed = Signal(int)  # NEW: Signal to safely send data to main thread

    def __init__(self, port, callback, baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.ser = None
        # Connect the signal to your callback so it executes on the main thread
        self.key_pressed.connect(callback)

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            try:
                if not self.ser:
                    self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
                    self.connection_status.emit(True)
                
                line = self.ser.readline().decode().strip()
                if line.startswith("KEY:"):
                    # EMIT signal instead of calling callback directly
                    self.key_pressed.emit(int(line.split(":")[1]))
            except:
                if self.ser:
                    self.ser.close()
                    self.ser = None
                self.connection_status.emit(False)
                time.sleep(2)