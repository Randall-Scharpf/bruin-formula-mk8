from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class CoolantDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(":/res/coolant", "F", False, False, parent)

