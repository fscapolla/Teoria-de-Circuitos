from PyQt5.QtCore import pyqtSlot

from ui.QtTest import Ui_Form
import scipy.signal as signal
from numpy import linspace, logspace, cos, sin, heaviside, log10, floor, zeros, ones
from math import pi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtWidgets


class myWidget(QWidget, Ui_Form):
    def __init__(self):
        super(myWidget, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Electrotecnia - TP Final")

        # Init
        self.filter_flag = 'none'
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.char_value_input.hide()
        self.zero_value_input.hide()
        self.pole_label.hide()

        # Input Validators
        # First Pole Input
        self.first_pole_real.setValidator(QtGui.QDoubleValidator(-10e12, -10e-12, 8, self))
        self.first_pole_im.setValidator(QtGui.QDoubleValidator(-10e12, 10e12, 8, self))
        # First Zero Input
        self.first_zero_real.setValidator(QtGui.QDoubleValidator(-10e12, 10e12, 8, self))
        self.first_zero_im.setValidator(QtGui.QDoubleValidator(-10e12, 10e12, 8, self))
        # Second Order Pole w0, xi Input
        self.w0_input.setValidator(QtGui.QDoubleValidator(10e-12, 10e12, 8, self))
        self.xi_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        # Second Order Zero w0, xi Input
        self.wz_input.setValidator(QtGui.QDoubleValidator(10e-12, 10e12, 8, self))
        self.xiz_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        # Sine/Cosine Amplitude and Frequency Input
        self.amplitude_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        self.freq_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        # Square/Sawtooth Amplitude and Frequency Input
        self.square_amplitude_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        self.square_duty_input.setValidator(QtGui.QDoubleValidator(1e-12, 1, 8, self))
        # Step Amplitude
        self.ut_amplitude_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))
        # Transfer Function Gain Input
        self.gain_input.setValidator(QtGui.QDoubleValidator(0, 10e12, 8, self))

        # Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        canvas_index = self.plotter_container.addWidget(self.canvas)
        self.plotter_container.setCurrentIndex(canvas_index)

        # Filter buttons
        # First Order
        self.low_pass_1.clicked.connect(self.set_1st_lowpass)
        self.high_pass_1.clicked.connect(self.set_1st_highpass)
        #        self.high_all_pass_1.clicked.connect(self.set_1st_high_allpass)
        self.low_all_pass_1.clicked.connect(self.set_1st_low_allpass)
        self.arb_filter.clicked.connect(self.set_arb_filter)
        # Second Order
        self.high_pass_2.clicked.connect(self.set_2nd_highpass)
        self.low_pass_2.clicked.connect(self.set_2nd_lowpass)
        self.band_pass.clicked.connect(self.set_bandpass)
        self.notch.clicked.connect(self.set_notch)
        #        self.high_all_pass_2.clicked.connect(self.set_2nd_high_allpass)
        self.low_all_pass_2.clicked.connect(self.set_2nd_low_allpass)
        self.high_pass_notch.clicked.connect(self.set_high_pass_notch)
        self.low_pass_notch.clicked.connect(self.set_low_pass_notch)

        # Graph buttons
        self.bode_plot_button.clicked.connect(lambda: self.plot('bode'))
        self.phase_plot_button.clicked.connect(lambda: self.plot('phase'))
        self.pole_plot_button.clicked.connect(lambda: self.plot('pole'))
        self.sine_plot_button.clicked.connect(lambda: self.plot('sine'))
        self.cosine_plot_button.clicked.connect(lambda: self.plot('cosine'))
        self.u_plot_button.clicked.connect(lambda: self.plot('ut'))
        self.square_plot_button.clicked.connect(lambda: self.plot('square'))
        self.sawtooth_plot_button.clicked.connect(lambda: self.plot('sawtooth'))
        self.delta_plot_button.clicked.connect(lambda: self.plot('delta'))

        # Other
        self.first_pole_checkbox.clicked.connect(self.hide_show_responses)

    @pyqtSlot()
    # Transfer Function Button Setters
    def set_1st_lowpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.first_pole_checkbox.hide()
        self.char_value_input.hide()
        self.zero_value_input.hide()
        self.first_zero_input.hide()
        self.first_pole_input.show()
        self.first_pole_input.setTitle("First Order Pole")
        self.filter_flag = '1st low pass'
        self.filter_label.setText('1st Order Low Pass Filter')

    def set_1st_highpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.first_pole_checkbox.hide()
        self.char_value_input.hide()
        self.zero_value_input.hide()
        self.first_zero_input.hide()
        self.first_pole_input.show()
        self.first_pole_input.setTitle("First Order Pole")
        self.filter_flag = '1st high pass'
        self.filter_label.setText('1st Order High Pass Filter')

    #    def set_1st_high_allpass(self):
    #        self.first_pole_input.setTitle("First Order Zero")
    #        self.char_value_input.hide()
    #        self.first_pole_input.show()
    #        self.zero_value_input.hide()
    #        self.filter_flag = '1st high all pass'
    #        self.filter_label.setText('1st Order High All Pass Filter')

    def set_1st_low_allpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.first_pole_checkbox.hide()
        self.char_value_input.hide()
        self.first_pole_input.show()
        self.zero_value_input.hide()
        self.first_zero_input.hide()
        self.first_pole_input.setTitle("First Order Pole")
        self.filter_flag = '1st low all pass'
        self.filter_label.setText('1st Order All Pass Filter')

    def set_arb_filter(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.first_pole_checkbox.show()
        self.char_value_input.hide()
        self.first_pole_input.show()
        self.first_zero_input.show()
        self.zero_value_input.hide()
        self.first_pole_input.setTitle("First Order Pole")
        self.filter_flag = '1st arb filter'
        self.filter_label.setText('1st Order Arbitrary Pole/Zero Filter')

    def set_2nd_lowpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.zero_value_input.hide()
        self.filter_flag = '2nd low pass'
        self.filter_label.setText('2nd Order Low Pass Filter')

    def set_2nd_highpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.zero_value_input.hide()
        self.filter_flag = '2nd high pass'
        self.filter_label.setText('2nd Order High Pass Filter')

    def set_bandpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.zero_value_input.hide()
        self.filter_flag = 'band pass'
        self.filter_label.setText('2nd Order Band Pass Filter')

    def set_notch(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.zero_value_input.hide()
        self.filter_flag = 'notch'
        self.filter_label.setText('2nd Order Notch Filter')

    #    def set_2nd_high_allpass(self):
    #        self.char_value_input.show()
    #        self.first_pole_input.hide()
    #        self.zero_value_input.hide()
    #        self.filter_flag = '2nd high all pass'
    #        self.filter_label.setText('2nd Order High All Pass Filter')

    def set_2nd_low_allpass(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.zero_value_input.hide()
        self.first_zero_input.hide()
        self.filter_flag = '2nd low all pass'
        self.filter_label.setText('2nd Order All Pass Filter')

    def set_high_pass_notch(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.first_zero_input.hide()
        self.zero_value_input.show()
        self.filter_flag = 'high pass notch'
        self.filter_label.setText('2nd Order High Pass Notch Filter')

    def set_low_pass_notch(self):
        self.first_pole_checkbox.setChecked(False)
        self.hide_show_responses()
        self.char_value_input.show()
        self.first_pole_input.hide()
        self.zero_value_input.show()
        self.first_zero_input.hide()
        self.filter_flag = 'low pass notch'
        self.filter_label.setText('2nd Order Low Pass Notch Filter')

    # Other
    def hide_show_responses(self):
        if self.first_pole_checkbox.isChecked():
            self.sine_input_box.hide()
            self.step_input_box.hide()
            self.square_input_box.hide()
            self.delta_input_box.hide()
        else:
            self.sine_input_box.show()
            self.step_input_box.show()
            self.square_input_box.show()
            self.delta_input_box.show()

    # Plotter Function
    def plot(self, flag):

        # General Parameters
        order_of_magnitude = 1
        w0 = 1
        pole = 0 + 1j * 0
        zero = 0 + 1j * 0
        gain = 1

        # Transfer function Quotient Generator
        if self.filter_flag == '1st low pass':
            pole = (float(self.first_pole_real.text()) + 1j * float(self.first_pole_im.text()))
            w0 = abs(pole)
            P = [w0]
            Q = [1, w0]
        elif self.filter_flag == '1st high pass':
            pole = (float(self.first_pole_real.text()) + 1j * float(self.first_pole_im.text()))
            w0 = abs(pole)
            P = [1, 0]
            Q = [1, w0]
        #        elif self.filter_flag == '1st high all pass':
        #            pole = (-1 * float(self.first_pole_real.text()) + 1j* float(self.first_pole_im.text()))
        #            w0 = abs(pole)
        #            P = [1, w0]
        #            Q = [1, -1 * w0]
        elif self.filter_flag == '1st low all pass':
            pole = (float(self.first_pole_real.text()) + 1j * float(self.first_pole_im.text()))
            w0 = abs(pole)
            P = [1, -1 * w0]
            Q = [1, w0]
        elif self.filter_flag == '1st arb filter':
            pole = (float(self.first_pole_real.text()) + 1j * float(self.first_pole_im.text()))
            wp = abs(pole)
            zero = (float(self.first_zero_real.text()) + 1j * float(self.first_zero_im.text()))
            wz = abs(zero)
            # if wz == 0 => full high pass
            if self.first_pole_checkbox.isChecked() and wz != 0:
                P = [1/wz, 1]
                Q = [1]
                w0 = wz
            elif self.first_zero_checkbox.isChecked() and wp != 0:
                P = [wp]
                Q = [1, wp]
                w0 = wp
                self.filter_label.setText('1st Order Low Pass Filter')
            else:
                if wz == 0.0:
                    P = [1, 0]
                    Q = [1, wp]
                    self.filter_label.setText('1st Order High Pass Filter')
                else:
                    P = [1 / wz, 1]
                    Q = [1 / wp, 1]

                if wz > wp:
                    self.filter_label.setText('1st Order Arbitrary Pole/Zero Low Pass Filter')
                elif wp == wz:
                    # wp == wz => all pass
                    self.filter_flag = '1st low all pass'
                    self.filter_label.setText('1st Order All Pass Filter')
                    self.first_zero_input.hide()
                elif wz != 0:
                    gain = gain * (wz / wp)
                    self.filter_label.setText('1st Order Arbitrary Pole/Zero High Pass Filter')
                w0 = wp
        elif self.filter_flag == '2nd low pass':
            w0 = (float(self.w0_input.text()))
            xi = (float(self.xi_input.text()))
            P = [w0 ** 2]
            Q = [1, 2 * xi * w0, w0 ** 2]
        elif self.filter_flag == '2nd high pass':
            w0 = (float(self.w0_input.text()))
            xi = (float(self.xi_input.text()))
            P = [1, 0, 0]
            Q = [1, 2 * xi * w0, w0 ** 2]
        elif self.filter_flag == 'band pass':
            w0 = (float(self.w0_input.text()))
            xi = (float(self.xi_input.text()))
            P = [2 * xi * w0, 0]
            Q = [1, 2 * xi * w0, w0 ** 2]
        elif self.filter_flag == 'notch':
            w0 = (float(self.w0_input.text()))
            xi = (float(self.xi_input.text()))
            P = [1, 0, w0 ** 2]
            Q = [1, 2 * xi * w0, w0 ** 2]
        #        elif self.filter_flag == '2nd high all pass':
        #            w0 = (float(self.w0_input.text()))
        #            xi = (float(self.xi_input.text()))
        #            P = [1, 2 * xi * w0, w0 ** 2]
        #            Q = [1, -2 * xi * w0, w0 ** 2]
        elif self.filter_flag == '2nd low all pass':
            w0 = (float(self.w0_input.text()))
            xi = (float(self.xi_input.text()))
            P = [1, -2 * xi * w0, w0 ** 2]
            Q = [1, 2 * xi * w0, w0 ** 2]
        elif self.filter_flag == 'high pass notch':
            wp = (float(self.w0_input.text()))
            xip = (float(self.xi_input.text()))
            wz = (float(self.wz_input.text()))
            xiz = (float(self.xiz_input.text()))
            P = [1 / (wz ** 2), -2 * (xiz / wz), 1]
            Q = [1 / (wp ** 2), 2 * (xip / wp), 1]
            w0 = wp
            if wz > wp:
                self.filter_label.setText('2nd Order Low Pass Notch Filter')
                self.filter_flag = 'low pass notch'
            elif wz == wp and xip == xiz:
                self.filter_label.setText('2nd All Pass Filter')
                self.zero_value_input.hide()
                self.filter_flag = '2nd low all pass'
            else:
                gain = gain * (wz ** 2) / (wp ** 2)
        elif self.filter_flag == 'low pass notch':
            wp = (float(self.w0_input.text()))
            xip = (float(self.xi_input.text()))
            wz = (float(self.wz_input.text()))
            xiz = (float(self.xiz_input.text()))
            P = [1 / (wz ** 2), -2 * (xiz / wz), 1]
            Q = [1 / (wp ** 2), 2 * (xip / wp), 1]
            w0 = wp
            if wz < wp:
                self.filter_label.setText('2nd Order High Pass Notch Filter')
                self.filter_flag = 'high pass notch'
                gain = gain * (wz ** 2) / (wp ** 2)
            elif wz == wp and xip == xiz:
                self.filter_label.setText('2nd All Pass Filter')
                self.zero_value_input.hide()
                self.filter_flag = '2nd low all pass'
        elif self.filter_flag == 'none':
            self.filter_label.setText('No Filter Selected!')
            return

        # Graphing Scope (area where the Bode will be defined)
        order_of_magnitude = floor(log10(w0))
        left_limit = order_of_magnitude - 5
        right_limit = order_of_magnitude + 5

        # Applying gain
        gain = gain * float(self.gain_input.text())
        i = 0
        while i < len(P):
            P[i] = gain * P[i]
            i += 1

        # Creating the Transfer Function
        H = signal.TransferFunction(P, Q)

        x = logspace(left_limit, right_limit, num=1000)
        Bode = signal.bode(H, x)

        # Defining X axis
        if self.x_axis_mod.isChecked():
            freq = Bode[0]
        else:
            freq = Bode[0] / (2 * pi)

        self.axes.clear()

        # Graphing the Selected Plot
        if flag == 'bode':
            self.x_axis_mod.show()
            self.pole_label.hide()
            self.axes.set_title('Bode plot')
            if self.x_axis_mod.isChecked():
                self.axes.set_xlabel('w (log) [rad/s]')
            else:
                self.axes.set_xlabel('f (log) [Hz]')
            self.axes.set_xscale('log')
            self.axes.set_ylabel('|H(jw)| [dB]')
            if self.filter_flag == '1st low all pass' or self.filter_flag == '2nd low all pass':
                self.axes.plot(freq, 20 * log10(ones(len(freq)) * gain))
            else:
                self.axes.plot(freq, Bode[1])
        elif flag == 'phase':
            self.x_axis_mod.show()
            self.pole_label.hide()
            self.axes.set_title('Bode Phase plot')
            if self.x_axis_mod.isChecked():
                self.axes.set_xlabel('w (log) [rad/s]')
            else:
                self.axes.set_xlabel('f (log) [Hz]')
            self.axes.set_xscale('log')
            self.axes.set_ylabel('/_H(jw) [deg]')
            self.axes.plot(freq, Bode[2])
        elif flag == 'pole':
            self.x_axis_mod.hide()
            self.pole_label.show()
            self.axes.set_title('Zero/Pole plot')
            self.axes.set_xlabel('Re(Z)')
            self.axes.set_ylabel('Im(Z)')
            if self.filter_flag == '1st low pass' or self.filter_flag == '1st high pass' or self.filter_flag == '1st low all pass' or self.filter_flag == '1st arb filter' and self.first_pole_checkbox.isChecked() == False:
                transfer_poles = pole
            else:
                transfer_poles = H.poles
            if self.filter_flag == '1st low all pass':
                transfer_zeros = -1 * pole.real + 1j * pole.imag
            elif self.filter_flag == '1st arb filter':
                transfer_zeros = zero
            else:
                transfer_zeros = H.zeros
            self.axes.scatter(transfer_poles.real, transfer_poles.imag, marker='o', color='r')
            self.axes.scatter(transfer_zeros.real, transfer_zeros.imag, marker='^', color='b')
        elif flag == 'sine':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            A = float(self.amplitude_input.text())
            f = float(self.freq_input.text())
            x2 = linspace(0, 10 / f, num=1000)
            sinx = A * sin(2 * pi * f * x2)
            sine = signal.lsim(H, U=sinx, T=x2)

            self.axes.set_title('sin(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(sine[0], sine[1])
        elif flag == 'cosine':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            A = float(self.amplitude_input.text())
            f = float(self.freq_input.text())
            x2 = linspace(0, 10 / f, num=1000)
            cosx = A * cos(2 * pi * f * x2)
            cosine = signal.lsim(H, U=cosx, T=x2)

            self.axes.set_title('cos(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(cosine[0], cosine[1])
        elif flag == 'ut':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            A = float(self.ut_amplitude_input.text())
            x2 = linspace(0, 10, num=1000)
            ut = A * heaviside(x2, 0.5)
            step = signal.lsim(H, U=ut, T=x2)

            self.axes.set_title('u(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(step[0], step[1])
        elif flag == 'square':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            A = float(self.square_amplitude_input.text())
            dc = float(self.square_duty_input.text())
            x2 = linspace(0, 10 / dc, num=1000)
            sqx = A * signal.square(x2, dc)
            square = signal.lsim(H, U=sqx, T=x2)

            self.axes.set_title('Π(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(square[0], square[1])
        elif flag == 'sawtooth':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            A = float(self.square_amplitude_input.text())
            dc = float(self.square_duty_input.text())
            x2 = linspace(0, 10 / dc, num=1000)
            stx = A * signal.sawtooth(x2, dc)
            sawtooth = signal.lsim(H, U=stx, T=x2)

            self.axes.set_title('Λ(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(sawtooth[0], sawtooth[1])
        elif flag == 'delta':
            self.x_axis_mod.hide()
            self.pole_label.hide()
            x2 = linspace(0, 10, num=1000)
            delta = signal.impulse(H, T=x2)

            self.axes.set_title('δ(t) response')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('Amplitude')

            self.axes.plot(delta[0], delta[1])

        self.axes.grid(True, which='both')
        self.axes.minorticks_on()

        self.canvas.draw()
