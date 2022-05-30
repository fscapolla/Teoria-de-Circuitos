from PyQt5.QtWidgets import QWidget, QFileDialog

def __open_file(ext=''): return QFileDialog.getOpenFileName(filter='*.'+ext)[0]