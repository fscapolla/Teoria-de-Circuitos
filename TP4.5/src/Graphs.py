# Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np

from src.ui.tc_tp4_mainwindow_UI import Ui_Form
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import scipy.signal as ss


class plotter(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.figure1, self.figure2, self.figure3, self.figure4, self.figure5, self.figure6, self.figure7, self.figure8, self.figure9 = Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure()
        self.canvas1, self.axes1 = FigureCanvas(self.figure1), self.figure1.add_subplot()
        self.canvas2, self.axes2 = FigureCanvas(self.figure2), self.figure2.add_subplot()
        self.canvas3, self.axes3 = FigureCanvas(self.figure3), self.figure3.add_subplot()
        self.canvas4, self.axes4 = FigureCanvas(self.figure4), self.figure4.add_subplot()
        self.canvas5, self.axes5 = FigureCanvas(self.figure5), self.figure5.add_subplot()
        self.canvas6, self.axes6 = FigureCanvas(self.figure6), self.figure6.add_subplot()
        self.canvas7, self.axes7 = FigureCanvas(self.figure7), self.figure7.add_subplot()
        self.canvas8, self.axes8 = FigureCanvas(self.figure8), self.figure8.add_subplot()
        self.canvas9, self.axes9 = FigureCanvas(self.figure9), self.figure9.add_subplot()
        #self. figure = []
        #self.canvas = []
        #self.axes = []
        #for i in range(9) :
        #    self.figure.append(Figure())
        #    self.canvas.append(FigureCanvas(self.figure1))
        #    self. axes.append(self.figure1.add_subplot())
        #for i in range(9):
        #    self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas), i)
        #self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas))
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas1), 0)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas2), 1)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas3), 2)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas4), 3)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas5), 4)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas6), 5)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas7), 6)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas8), 7)
        self.graphic.setCurrentIndex(self.graphic.addWidget(self.canvas9), 8)

        self.axes1.minorticks_on()
        self.axes2.minorticks_on()
        self.axes3.minorticks_on()
        self.axes4.minorticks_on()
        self.axes5.minorticks_on()
        self.axes6.minorticks_on()
        self.axes7.minorticks_on()
        self.axes8.minorticks_on()
        self.axes9.minorticks_on()

    def denormalizedPlot(self, numerator, denominator):
        w = np.logspace(1, 8, num=10000) * 2 * np.pi
        w, mag, phase = ss.bode(ss.TransferFunction(numerator, denominator), w = w)
        self.axes1.plot(w, -mag, label = 'n =')
        self.axes1.set_xscale('log')

    def normalizedPlot(self, numeratorNorm, denominatorNorm):

    def phasePlot(self):

    def groupDelayPlot(self):

    def polesZeroesPlot(self):

    def impulsiveResponsePlot(self):

    def stepResponsePlot(self):

    def qualityFactorPlot(self):


