import globalfonts
from gui.dials.AnalogGaugeWidget import AnalogGaugeWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

MAX_RPM = 14.0
MAX_BLUR_RADIUS = 400

class RPMDial(AnalogGaugeWidget):
    def __init__(self, parent=None):
        super().__init__(parent, True)
        super().setCustomGaugeTheme(
            color1="#242321",  # gray, end color, outer color
            color2="#969696",  # a lighter gray, just a shine
            color3="#000000"  # black, start color, center color
        )
        super().setNeedleColor(139, 225, 242, 255)
        super().setScaleValueColor(139, 225, 242, 255)
        super().setBigScaleColor(QColor(139, 225, 242, 255))
        super().setFineScaleColor(QColor(139, 225, 242, 255))
        super().setDisplayValueColor(206, 244, 255, 255)
        super().setMinValue(0.0)
        super().setMaxValue(MAX_RPM)
        super().setScalaCount(7)
        super().setScaleStartAngle(155)
        super().setTotalScaleAngleSize(230)
        super().setEnableValueText(True)
        super().setEnableCenterPoint(True)
        self.units = ""
        self.initial_scale_fontsize = globalfonts.scaled_dial_size(35)
        self.initial_value_fontsize = globalfonts.scaled_dial_size(60)

        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setOffset(0, 0)
        self.effect.setColor(QColor(139, 225, 242, 255))
        self.setGraphicsEffect(self.effect)

    def set_blur_effect(self, blur_ratio):
        self.effect.setBlurRadius(blur_ratio * MAX_BLUR_RADIUS)
