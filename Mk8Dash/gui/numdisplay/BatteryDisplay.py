from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class BatteryDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(":/res/battery", "V", True, True, parent)
