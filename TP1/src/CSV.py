# Gets data from .csv and plots second column vs first column.
import pandas as pd
from src.FileHandling import __open_file

def csv_data(widg):
    if widg.showing_CSV: widg.toggle_csv_data()
    else:
        # widg.clear()
        file_name = __open_file('csv')
        if not len(file_name): return None
        widg.df = pd.read_csv(file_name)
        #widg.df = pd.read_csv(file_name, sep = ';')
        for key in widg.df.keys():
            widg.X_axis_input_csv.addItem(key)
            widg.Y_axis_input_csv.addItem(key)
        widg.toggle_csv_data()

def plot_csv(widg):
    widg.x_axis += [[widg.df[widg.X_axis_input_csv.currentText()], '' ]]
    widg.y_axis += [[widg.df[widg.Y_axis_input_csv.currentText()], '']]

    widg.figure.clear()
    widg.axes = widg.figure.add_subplot()
    widg.axes.grid(which='both')
    widg.plot()