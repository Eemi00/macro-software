import serial
import threading
import time
from PySide6.QtCore import QObject, Signal

class SerialManager(QObject):
    connection_status = Signal(bool)

    def __init__(self, port, callback, baudrate=115200):
        super().__init__()
        self.port = port
        self.callback = callback
        self.baudrate = baudrate
        self.running = False
        self.ser = None

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
                    self.callback(int(line.split(":")[1]))
            except:
                if self.ser:
                    self.ser.close()
                    self.ser = None
                self.connection_status.emit(False)
                time.sleep(2)