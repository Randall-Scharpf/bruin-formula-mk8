from gui.numdisplay.NumberDisplayWidget import NumberDisplayWidget


class BrakeDisplay(NumberDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(":/res/brake", "%", True, False, parent)
