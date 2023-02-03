from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class CoolantDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__("gui/resources/coolant.png", "F", False, parent)

