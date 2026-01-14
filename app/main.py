import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from ui.main_window import MacropadGrid


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Macropad Controller")

        self.grid = MacropadGrid()
        self.setCentralWidget(self.grid)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(500, 600)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()