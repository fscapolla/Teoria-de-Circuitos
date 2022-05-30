# # Project modules
from src.TC_TP4_mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
#
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
