from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class ExhaustDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(":/res/exhaust", "F", False, False, parent)
