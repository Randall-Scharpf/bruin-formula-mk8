from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


# widget's width = 140, height = 150
icon_size = 40


class NumberDisplayWidget(QWidget):
    def __init__(self, icon_filepath, unit, flipped, parent=None):
        super(NumberDisplayWidget, self).__init__(parent)

        pixmap = QPixmap(icon_filepath)
        pixmap = pixmap.scaledToWidth(icon_size)
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setStyleSheet("background-color : rgba(0, 0, 0, 0);")
        if flipped:
            icon.setGeometry(20, 70, icon_size, icon_size)
        else:
            icon.setGeometry(95, 70, icon_size, icon_size)

        self.numberLabel = QLabel(self)
        self.numberLabel.setText("N")
        self.numberLabel.setStyleSheet("color: white; font-size : 80pt; background-color : rgba(0, 0, 0, 0);")
        if flipped:
            self.numberLabel.setGeometry(50, 10, 100, 140)
        else:
            self.numberLabel.setGeometry(5, 10, 100, 140)
        self.numberLabel.setAlignment(Qt.AlignCenter)

        self.unitLabel = QLabel(self)
        self.unitLabel.setText(unit)
        self.unitLabel.setStyleSheet("color: white; font-size : 40pt; background-color : rgba(0, 0, 0, 0);")
        if flipped:
            self.unitLabel.setGeometry(20, 30, 40, 40)
        else:
            self.unitLabel.setGeometry(95, 30, 40, 40)
        self.unitLabel.setAlignment(Qt.AlignCenter)

    def _setNumberColor(self, r, g, b):
        color_str = "rgba(" + str(r) + "," + str(g) + "," + str(b) + ",255)"
        self.unitLabel.setStyleSheet("color: " + color_str + "; font-size : 40pt; background-color : rgba(0, 0, 0, 0);")
        self.numberLabel.setStyleSheet("color: " + color_str + "; font-size : 80pt; background-color : rgba(0, 0, 0, 0);")
