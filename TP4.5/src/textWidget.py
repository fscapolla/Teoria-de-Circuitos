from PyQt5.QtWidgets import QWidget, QVBoxLayout
class textWidget(QWidget):

    def __init__(self, figure, canvas, text = None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        # self.layout = QVBoxLayout(self)

        self.fig = figure
        self.canvas = canvas
        # self.layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        self.text = text

        if self.text: self.drawIt()

    def set_text(self, text): self.text = text

    def drawIt(self):
        self.fig.clear()
        t = self.fig.suptitle(self.text, size=20)
        self.canvas.draw()
        (x0, y0), (x1, y1) = t.get_window_extent().get_points()
        try:
            self.w = max(x1 - x0, self.w)
        except:
            self.w = x1 - x0

        try:
            self.h = max(y1 - y0, self.h)
        except:
            self.h = y1 - y0
        self.fig.set_size_inches(self.w / 80, self.h / 80)
