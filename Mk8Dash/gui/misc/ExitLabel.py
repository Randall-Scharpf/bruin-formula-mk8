from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class ExitLabel(QLabel):
    exit = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.exit.emit()
        exit()
