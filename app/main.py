import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Macropad Controller")

        label = QLabel("Macropad controller app (skeleton)")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()