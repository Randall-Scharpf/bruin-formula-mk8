from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF


class GearWidget(QWidget):
    def __init__(self, parent=None):
        super(GearWidget, self).__init__(parent)

        label = QLabel(self)
        label.setText("GEAR")
        label.setStyleSheet("color: white; font-size : 36pt; background-color : rgba(0, 0, 0, 0);")
        label.setGeometry(0, 30, 250, 30)
        label.setAlignment(Qt.AlignCenter)

        self.gear = QLabel(self)
        self.gear.setText("N")
        self.gear.setStyleSheet("color: white; font-size : 220pt; background-color : rgba(0, 0, 0, 0);")
        self.gear.setGeometry(0, 70, 260, 190)
        self.gear.setAlignment(Qt.AlignCenter)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(182, 182, 182, 255), 5, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, 250, 260), 40, 40)
