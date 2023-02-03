from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF


border_color = QColor(182, 182, 182, 255)
border_width = 5
width = 150
height = 280


class BorderBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super(BorderBackgroundWidget, self).__init__(parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(border_color, border_width, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, width, height), 40, 40)
        painter.drawLine(0, height / 2, width, height / 2)
