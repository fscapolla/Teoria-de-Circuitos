# Designer UI
from src.ui.tp1_tc import Ui_Form

# PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, Qt

# Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Extra libraries
import warnings
warnings.filterwarnings('ignore')

from src.CSV import csv_data, plot_csv
from src.LTSpice import ltspice_data, plot_ltspice
from src.TransferFunction import bode
from src.Callback_connection import connect_callback
from src.Toggles import toggle_csv_data, toggle_spice_data, toggle_transfer_data, \
    newPlot, toggle_signal_resp, toggle_freq_duty
from src.Clears import clear_csv, clear_spice, clear_transfer, clear
from src.signal_resp import plot_resp

class MyWidget(QWidget, Ui_Form):
    def __init__(self):

        # Constructor and setup.
        super().__init__()
        self.setupUi(self)

        # Title and size.
        self.setWindowTitle('TC - TP1')
        self.resize(QSize(1200, 700))

        # Matplotlib
        ################################################################################
        self.figure = Figure()
        self.canvas, self.axes = FigureCanvas(self.figure), self.figure.add_subplot()
        self.phase_axis = self.axes
        self.axes.minorticks_on()
        self.phase_axis.minorticks_on()
        self.Graphic.setCurrentIndex(self.Graphic.addWidget(self.canvas))
        self.x_axis, self.y_axis, self.y_phase = [], [], []
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setVisible(False)
        self.resetButton.hide()
        ################################################################################
        # Initial conditions.
        #############################
        self.showing_Hs = False
        self.showing_LT = False
        self.showing_CSV = False
        self.signal_response_showing = False
        self.transfer_data.hide()
        self.data_input_frame.hide()
        self.InputSpice.hide()
        self.CSV_input.hide()
        self.signal_response_frame.hide()
        self.duty_cycle.hide()
        #############################

        # Callback connection.
        connect_callback(self)

    # Toggles
    ############################################################
    def toggle_csv_data(self): toggle_csv_data(self)
    def toggle_transfer_data(self): toggle_transfer_data(self)
    def toggle_spice_data(self): toggle_spice_data(self)
    def newPlot(self): newPlot(self)
    def toggle_signal_resp(self): toggle_signal_resp(self)
    def toggle_freq_duty(self): toggle_freq_duty(self)
    ############################################################

    # Zoom and panning
    ##############################################################
    def zoom(self):
        if self.zoom_button.isChecked() or self.pan_button.isChecked(): self.resetButton.show()
        else: self.resetButton.hide()

        if self.zoom_button.isChecked(): self.pan_button.setChecked(False)
        self.toolbar.zoom()

    def reset(self): self.toolbar.home()

    def pan(self):
        if self.pan_button.isChecked() or self.zoom_button.isChecked(): self.resetButton.show()
        else: self.resetButton.hide()

        if self.pan_button.isChecked(): self.zoom_button.setChecked(False)
        self.toolbar.pan()
    ##############################################################

    # Get data
    #################################################################
    # Gets data from .csv and plots second column vs first column.
    def csv_data(self): return csv_data(self)

    # Gets data from LTSpice.
    def ltspice_data(self): return ltspice_data(self)
    #################################################################

    # Plot data
    ################################################################
    # Plots Bode.
    def bode(self): bode(self)

    # Plots CSV data.
    def plot_csv(self): plot_csv(self)

    # Plots LTSpice data.
    def plot_ltspice(self): plot_ltspice(self)

    # Plots y vs x with x_label and y_label.
    def plot(self):
        for i in range(len(self.x_axis)):
            self.axes.plot(self.x_axis[i][0], self.y_axis[i][0], label=f'Plot {i+1}')
            for j in range(len(self.y_phase)):
                if self.y_phase[j][0] == i: self.phase_axis.plot(self.x_axis[i][0], self.y_phase[j][1], label=f'Plot {i+1}')
        if len(self.y_phase): self.phase_axis.legend()
        self.axes.legend()
        self.canvas.draw()

    def plot_response(self): plot_resp(self)
    ################################################################

    # Clear data
    ###############################################################
    # Clears LTSpice data.
    def clear_spice(self): clear_spice(self)

    # Clears CSV data.
    def clear_csv(self): clear_csv(self)

    # Clears transfer function data.
    def clear_transfer(self): clear_transfer(self)

    # Clears plot.
    def clear(self): clear(self)
    ###############################################################

    # Exits with ESC.
    def keyPressEvent(self, key):
        if key.key() == Qt.Key_Escape: exit()
        else: super().keyPressEvent(key)


