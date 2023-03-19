import globalfonts
from gui.dials.AnalogGaugeWidget import AnalogGaugeWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


MAX_BLUR_RADIUS = 300

class VelocityDial(AnalogGaugeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setCustomGaugeTheme(
            color1="#242321",  # gray, end color, outer color
            color2="#757575",  # a lighter gray, just a shine
            color3="#000000"  # black, start color, center color
        )
        super().setNeedleColor(139, 225, 242, 255)
        super().setScaleValueColor(139, 225, 242, 255)
        super().setBigScaleColor(QColor(139, 225, 242, 255))
        super().setFineScaleColor(QColor(139, 225, 242, 255))
        super().setDisplayValueColor(206, 244, 255, 255)
        super().setMinValue(0.0)
        super().setMaxValue(80.0)
        super().setScalaCount(8)
        super().setScaleStartAngle(145)
        super().setTotalScaleAngleSize(150)
        super().setEnableValueText(True)
        super().setEnableCenterPoint(True)
        self.units = ""
        self.initial_scale_fontsize = globalfonts.scaled_dial_size(25)
        self.initial_value_fontsize = globalfonts.scaled_dial_size(50)

        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setOffset(0, 0)
        self.effect.setColor(QColor(139, 225, 242, 255))
        self.setGraphicsEffect(self.effect)

    def set_blur_effect(self, blur_ratio):
        self.effect.setBlurRadius(blur_ratio * MAX_BLUR_RADIUS)
