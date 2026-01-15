from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve


class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(120)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        g = self.geometry()
        self._anim.stop()
        self._anim.setStartValue(g)
        self._anim.setEndValue(g.adjusted(-2, -2, 2, 2))
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        g = self.geometry()
        self._anim.stop()
        self._anim.setStartValue(g)
        self._anim.setEndValue(g.adjusted(2, 2, -2, -2))
        self._anim.start()
        super().leaveEvent(event)