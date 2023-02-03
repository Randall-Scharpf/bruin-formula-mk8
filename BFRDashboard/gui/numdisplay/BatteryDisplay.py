from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class BatteryDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__("gui/resources/battery.png", "V", True, parent)
