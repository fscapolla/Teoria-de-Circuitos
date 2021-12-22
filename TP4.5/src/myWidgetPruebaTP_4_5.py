# from Debugger_display_gui import Ui_MainWindow
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import Qt
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from cmath import sqrt


class myWidgetPrueba(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Constructor and setup.
        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.plotAll)

        self.figure, self.canvas, self.axes = [], [], []
        self.count = 0
        self.totalPages = 9
        self.witch = 'numDenum'

        for i in range(self.totalPages):
            self.figure.append(plt.figure(i + 1))
            self.canvas.append(FigureCanvas(self.figure[i]))
            self.Display.addWidget(self.canvas[i])
            self.axes.append(self.figure[i].add_subplot())



    def plotAll(self):
        if (self.count == 0):
            print("plotAll inicial")
            self.w0 = 2000
            self.wb = 2000
            self.w = np.logspace(1, 6, num=1000) * 2 * np.pi
            self.numerador = [1]
            self.denominador = [1/self.w0**2, 2/self.w0, 1]
            #self.tf = 1/((1j*self.w/self.w0)**2 + 2*1j*self.w/self.w0 + 1)
            if (self.witch == 'numDenum'):
                self.w1, self.mag, self.phase = ss.bode(ss.TransferFunction(self.numerador, self.denominador), w=self.w)
            #elif (self.witch == 'function'):
            #    self.mag = 20*np.log10(self.tf)
            #    self.phase = np.arctan(np.imag(tf)/np.real(tf))



            #Llamado a funciones
            self.funcCall()


            #self.zeroes, self.poles, self.gain = ss.tf2zpk(self.numerador, self.denominador)
            #self.denormZP(B=0.5, k=1, wn=self.wb, which2='LP', poleNorm=self.poles)
            #self.denormZP(B=0.5, k=1, wn=self.wb, which2='HP', poleNorm=self.poles)
            #self.denormZP(B=0.5, k=1, wn=self.wb, which2='BP', poleNorm=self.poles)
            #self.denormZP(B=0.5, k=1, wn=self.wb, which2='SP', poleNorm=self.poles)

            print(1)
            self.count += 1

        else:
            self.pageChange()



    def funcCall(self):
        self.denormalizedPlot()
        self.normalizedPlot()
        self.jointTranferPlot()
        self.phasePlot()
        self.phaseDelayPlot()
        self.ZeroesPolesPlot()
        self.impulsiveResponse()
        self.stepResponse()
        self.maxQPlot()

    def denormalizedPlot(self):
        self.axes[0].plot(self.w, -self.mag, label = "Atenuación desnormalizada")
        self.axes[0].set_xscale('log')
        self.axes[0].legend()
        self.canvas[0].draw()

    def normalizedPlot(self):
        self.axes[1].plot(self.w/self.wb, -self.mag, label="Atenuación normalizada")
        self.axes[1].set_xscale('log')
        self.axes[1].legend()
        self.canvas[1].draw()

    def jointTranferPlot(self):
        self.axes[2].plot(self.w, -self.mag, label="Atenuación desnormalizada")
        #self.axes[2].plot(self.w / self.wb, -self.mag, label="Atenuación normalizada")
        #self.axes[2].axhline(y= )
        self.axes[2].set_xscale('log')
        self.axes[2].legend()
        self.canvas[2].draw()

    def phasePlot(self):
        self.axes[3].plot(self.w, self.phase, label = "Fase")
        self.axes[3].set_xscale('log')
        self.axes[3].legend()
        self.canvas[3].draw()

    def phaseDelayPlot(self):
        w, groupDelay = ss.group_delay((self.numerador, self.denominador))
        self.axes[4].plot(2*np.pi*w, groupDelay, label = 'Retardo de grupo')
        self.axes[4].legend()
        self.canvas[4].draw()

    def ZeroesPolesPlot(self):
        if (self.witch == 'numDenum'):
            self.zeroes , self.poles, self.gain = ss.tf2zpk(self.numerador, self.denominador)
        elif (self.witch == 'function'):
            print("PEPE")
        magZero, magPole = [], []
        self.axes[5].axvline(0, color = '0.3')
        self.axes[5].axhline(0, color = '0.3')
        for zero in self.zeroes:
            self.axes[5].scatter(np.real(zero), np.imag(zero), marker = 'o', label = 'Ceros')
            magZero.append(np.abs(zero))
        for pole in self.poles:
            self.axes[5].scatter(np.real(pole), np.imag(pole), marker = 'x', label = 'Polos')
            magPole.append((np.abs(pole)))
        r = 1.5 * np.amax(np.concatenate((magZero, magPole), axis = None))
        self.axes[5].axis('scaled')
        #self.axes[5].axis([-r, r, -r, r])
        self.axes[5].set_xlim((-r, r))
        self.axes[5].set_ylim((-r, r))
        self.axes[5].minorticks_on()
        self.axes[5].grid(which = 'both')
        self.axes[5].legend()
        self.canvas[5].draw()

    def impulsiveResponse(self):
        if (self.witch == 'numDenum'):
            self.ti, self.yImpulse = ss.impulse((self.numerador, self.denominador))
        elif (self.witch == 'function'):
            print("hola")
        self.axes[6].plot(self.ti, self.yImpulse, label = "Respuesta impulsiva")
        self.axes[6].legend()
        self.canvas[6].draw()

    def stepResponse(self):
        self.ts, self.yStep = ss.step((self.numerador, self.denominador))
        self.axes[7].plot(self.ts, self.yStep, label = "Respuesta al escalón")
        self.axes[7].legend()
        self.canvas[7].draw()

    def maxQPlot(self):
        i = 1
        for pole in self.poles:
            if (np.real(pole)!=0):
                #self.axes[8].scatter(-np.abs(pole)/(2 * np.real(pole)), label = f'Q{i}')
                #self.axes[8].stem(-np.abs(pole)/(2 * np.real(pole)), label = f'Q{i}')
                print(f'Q{i} = ', -np.abs(pole)/(2 * np.real(pole)))
                i += 1
            else:
                #self.axes[8].scatter(label = f'Q{i} = infinito')
                print(f'Q{i} = infinito')
                i += 1
        self.axes[8].legend()
        self.canvas[8].draw()


    def pageChange(self):
        if (self.count <= self.totalPages):
            print(f'Page {self.count}')
            self.Display.setCurrentIndex(self.count)
            if (self.count == self.totalPages):
                self.count = 1
            else:
                self.count += 1
        else:
            print("Error")
