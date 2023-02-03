from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class ExhaustDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__("gui/resources/exhaust.png", "F", False, parent)
