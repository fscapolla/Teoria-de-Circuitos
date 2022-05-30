from src.mywidget import MyWidget
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
