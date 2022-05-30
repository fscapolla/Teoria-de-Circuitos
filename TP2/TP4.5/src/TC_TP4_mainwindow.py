from src.ui.tc_tp4_mainwindow_UI import Ui_Form
import matplotlib.pyplot as plt
from src.textWidget import *
from sys import exit
import warnings
from src.Butter import wb_butter
from src.Legendre import transfer_legendre
from src.Chebys import wb_cheby1
from src.constants import *
from src.Cauer import wb_cauer
from src.Gauss import gaussian
warnings.filterwarnings('ignore')
from src.graphic import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt


class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialSetup()

        self.setWindowTitle('TC - TP 4.5')

        self.num, self.denom = np.array([]), np.array([])
        self.data = {}
        self.to_var = self.to = 1

        # self.ok_go.clicked.connect(lambda: plotAll(self))

        self.show()
        self.showFullScreen()

        self.figure, self.canvas, self.axes, self.toolbars = [], [], [], []
        self.count = 0
        self.totalPages = 10
        self.witch = 'numDenum'
        self.q_max_value.setMinimum(0.51)

        for i in range(self.totalPages):
            self.figure.append(plt.figure(i + 1))
            self.canvas.append(FigureCanvas(self.figure[i]))
            self.toolbars.append(NavigationToolbar(self.canvas[i], self))
            wdg = QWidget()
            lay = QVBoxLayout(wdg)
            lay.addWidget(self.toolbars[i])
            lay.addWidget(self.canvas[i])
            self.graphic.addWidget(wdg)
            self.axes.append(self.figure[i].add_subplot())
        self.callback_connection()

    def show_params(self):
        if self.filterType.currentText() not in ['Band Pass', 'Band Stop']:
            self.parameters_frame.show()
            self.parameters_BP_SB_frame.hide()
        else:
            self.parameters_BP_SB_frame.show()
            self.parameters_frame.hide()

    def show_restric(self):
        self.restric_frame.show()
        self.ok_restric_frame.show()

    @staticmethod
    def checkbox_connection(checkbox, value):
        checkbox.toggled.connect(lambda: value.show() if checkbox.isChecked() else value.hide())

    @staticmethod
    def limit_connection(value, limit, minus=False):
        if minus: func = min
        else: func = max
        value.valueChanged.connect(lambda: limit.setValue(func(value.value() + 0.1 * (-1) ** minus, limit.value())))

    def reset_limits(self):
        if self.filterType.currentText() == 'Low Pass': wmin, wmax = self.wp_value, self.ws_value
        elif self.filterType.currentText() == 'High Pass': wmin, wmax = self.ws_value, self.wp_value
        elif self.filterType.currentText() == 'Band Pass':
            wmin1_b, wmin2_b, wmin3_b, wmin4_b = self.wsmin_value, self.wpmin_value, self.wpmax_value, self.wsmax_value
        else:
            wmin1_b, wmin2_b, wmin3_b, wmin4_b = self.wpmin_value, self.wsmin_value, self.wsmax_value, self.wpmax_value

        if self.filterType.currentText() in ['High Pass', 'Low Pass']:
            wmin.disconnect(); wmax.disconnect()
            self.limit_connection(wmin, wmax, minus=False)
            self.limit_connection(wmax, wmin, minus=True)
            wmax.setValue(max(wmin.value() + 0.1, wmax.value()))
            wmin.setValue(min(wmax.value() - 0.1, wmin.value()))

        else:
            wmin1_b.disconnect(); wmin2_b.disconnect()
            wmin3_b.disconnect(); wmin4_b.disconnect()

            self.limit_connection(wmin1_b, wmin2_b, minus=False)
            self.limit_connection(wmin2_b, wmin3_b, minus=False)
            self.limit_connection(wmin3_b, wmin4_b, minus=False)
            self.limit_connection(wmin4_b, wmin3_b, minus=True)
            self.limit_connection(wmin3_b, wmin2_b, minus=True)
            self.limit_connection(wmin2_b, wmin1_b, minus=True)

            wmin2_b.setValue(max(wmin1_b.value() + 0.1, wmin2_b.value()))
            wmin3_b.setValue(max(wmin2_b.value() + 0.1, wmin3_b.value()))
            wmin4_b.setValue(max(wmin3_b.value() + 0.1, wmin4_b.value()))

            wmin3_b.setValue(min(wmin4_b.value() - 0.1, wmin3_b.value()))
            wmin2_b.setValue(min(wmin3_b.value() - 0.1, wmin2_b.value()))
            wmin1_b.setValue(min(wmin2_b.value() - 0.1, wmin1_b.value()))

    def initialSetup(self):
        self.parameters_BP_SB_frame.hide()
        # self.graphic.hide()
        self.q_max_value.hide()
        self.prev_next_frame.hide()
        self.n_min_value.hide()
        self.n_max_value.hide()
        self.range_value.hide()
        self.parameters_GD_frame_2.hide()
        self.n_max_value.setMaximum(25)
        self.n_min_value.setMaximum(25)
        self.as_value.setMinimum(10.1)
        self.as_bp_bs_value.setMinimum(10.1)

    def callback_connection(self):
        self.filterType.currentIndexChanged.connect(self.show_params)
        self.checkbox_connection(self.qmax_checkbox, self.q_max_value)
        self.checkbox_connection(self.nmin_checkbox, self.n_min_value)
        self.checkbox_connection(self.nmax_checkbox, self.n_max_value)
        self.checkbox_connection(self.denorm_range_checkbox, self.range_value)
        # self.denorm_range_checkbox.toggled.connect(lambda: self.denorm_range_checkbox.setCheckState(False) if self.approxType.currentText() == 'Cheby 2' else None)

        self.exit_button.clicked.connect(lambda: self.close() or exit())

        self.approxType.currentTextChanged.connect(lambda: [self.denorm_range_checkbox.setCheckState(False), self.range_frame.hide()]\
            if self.approxType.currentText() == 'Cheby 2' else self.range_frame.show())

        # self.filterType.currentTextChanged.connect(lambda: [self.denorm_range_checkbox.setCheckState(False), self.range_frame.hide()]\
        #     if self.filterType.currentText() not in ['Low Pass', 'High Pass'] else self.range_frame.show() if self.approxType.currentText() != 'Cheby 2' else None)

        self.denorm_range_checkbox.toggled.connect(lambda: self.denorm_range_checkbox.setText(f'Denormalization Range ({self.range_value.value()}%)') \
            if self.denorm_range_checkbox.isChecked() else self.denorm_range_checkbox.setText(f'Denormalization Range'))

        self.filterType.currentTextChanged.connect(self.rewrite_approx)
        self.filterType.currentIndexChanged.connect(self.reset_limits)
        self.reset_limits()

        self.filterType.currentTextChanged.connect(lambda: [self.parameters_GD_frame_2.show(), self.parameters_frame.hide(), self.parameters_BP_SB_frame.hide()] if self.filterType.currentText() == 'Group Delay'
                                                   else self.parameters_GD_frame_2.hide())
        self.ok_go.clicked.connect(self.create_transfer)
        self.range_value.valueChanged.connect(lambda: self.denorm_range_checkbox.setText(f'Denormalization Range ({self.range_value.value()}%)'))
        self.clear_button.clicked.connect(self.clear)

        self.next_button.clicked.connect(self.next)
        self.previous_button.clicked.connect(self.previous)

    def rewrite_approx(self):
        self.approxType.clear()
        if self.filterType.currentText() == 'Group Delay':
            self.approxType.addItem('Gauss')
        elif self.filterType.currentText() not in ['Band Pass', 'Band Stop']:
            self.approxType.addItems(['Butterworth', 'Cheby 1', 'Cheby 2', 'Cauer', 'Legendre'])
        else:
            self.approxType.addItems(['Butterworth', 'Cheby 1', 'Cheby 2', 'Legendre'])

    def clear(self):
        for ax in self.axes:
            ax.clear()
            ax.minorticks_on()
            ax.grid(which = 'both', b = True)
        for canvas in self.canvas: canvas.draw()
        self.count = 0
        self.graphic.setCurrentIndex(0)
        self.prev_next_frame.hide()

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key_Escape: self.close(), exit()
        elif a0.key() == Qt.Key_Return: self.ok_go.click()
        elif a0.key() == Qt.Key_Right: self.next_button.click()
        elif a0.key() == Qt.Key_Left: self.previous_button.click()
        else: super().keyPressEvent(a0)

    def create_transfer(self):

        self.count = 0
        self.graphic.setCurrentIndex(0)

        options = {
            'Butterworth' : (ss.buttord, ss.butter, 0),
            'Cheby 1' : (ss.cheb1ord, ss.cheby1, 1),
            'Cheby 2' : (ss.cheb2ord, ss.cheby2, 2),
            'Bessel' : (ss.bessel, None, 5),
            'Gauss' : (None, None, 6),
            'Legendre' : (None, None, 4),
            'Cauer' : (ss.ellipord, ss.ellip, 3)
        }

        approx = self.approxType.currentText()

        if approx not in options.keys(): return

        self.get_params()

        filt, wp, ws, Ap, As, lims, denorm_range = self.data.values()
        self.lims = lims

        plotter = 'numDenum'

        if options[approx][2] < 4:
            n, wn = options[approx][0](wp, ws, Ap, As, analog=True)
            if self.nmin_checkbox.isChecked() and n < self.n_min_value.value(): n = self.n_min_value.value()
            if self.nmax_checkbox.isChecked() and n > self.n_max_value.value(): n = self.n_max_value.value()
            if n > NMAX : n = NMAX
        if options[approx][2] == 0:
            wb = wb_butter(self, n)
            # if filt not in [BP, BS]:
            self.num, self.denom = options[approx][1](n, wb, filt, analog = True)[:2]
        elif options[approx][2] == 1:
            wb = wb_cheby1(self, n)
            self.num, self.denom = options[approx][1](n, Ap, wb, filt, analog = True)[:2]
        elif options[approx][2] == 2:
            wb = wn
            self.wb = wn
            if filt in [BP,BS]:
                n1, wn1 = options[approx][0](wp[0], ws[0], Ap, As, analog=True)
                n2, wn2 = options[approx][0](wp[1], ws[1], Ap, As, analog=True)
                if n1 > n2: self.index = 0
                else: self.index = 1
                if filt == BP:
                    self.wo = np.sqrt(wp[0] * wp[1])
                    self.B = wp[1] - wp[0]

                elif filt == BS:
                    self.wo = np.sqrt(ws[0] * ws[1])
                    self.B = wp[1] - wp[0]
            self.num, self.denom = options[approx][1](n, As, wb, filt, analog = True)[:2]

        elif options[approx][2] == 3:
            wb = wb_cauer(self, n)
            self.num, self.denom = options[approx][1](n, Ap, As, wb, filt, analog = True)[:2]
        elif options[approx][2] == 4:
            legN = transfer_legendre(self)
            plotter = 'func'

        elif options[approx][2] == 6:
            self.gd = gaussian(self)
            plotter = 'func'

        plotAll(self, plotter)
        # self.graphic.show()
        self.prev_next_frame.show()
        self.next()

    def get_params(self):
        filt = self.filterType.currentText().lower().replace(' ', '')
        self.filt = filt

        wp, ws =  self.wp_value.value()*1e3, self.ws_value.value()*1e3
        Ap, As = self.ap_value.value(), self.as_value.value()
        lims = np.log10(np.array([min(wp, ws) / 10, max(wp, ws) * 10]))
        if filt in [BP, BS]:
            wpmin, wpmax, wsmin, wsmax = self.wpmin_value.value(), self.wpmax_value.value(),\
                                         self.wsmin_value.value(), self.wsmax_value.value()
            wp, ws = np.array([wpmin, wpmax])*1e3, np.array([wsmin, wsmax])*1e3
            Ap, As = self.ap_bp_bs_value.value(), self.as_bp_bs_value.value()

            if filt == BP: lims = np.log10(np.array([wsmin * 1e3 / 10, wsmax *1e3 * 10]))
            else: lims = np.log10(np.array([wpmin * 1e3 / 10, wpmax * 1e3 * 10]))
        elif filt == 'groupdelay':
            self.to = self.t0_value.value()
            self.to_var = self.error_tau_value.value() / 100
            wx = self.omega_gd_value.value()
            lims = np.log10(1000 * np.array([wx/10 , wx * 10]))
        denorm_range = self.range_value.value() * self.denorm_range_checkbox.isChecked()

        self.data =\
            {
                'filt' : filt,
                'wp' : wp,
                'ws' : ws,
                'Ap' : Ap,
                'As' : As,
                'lims' : lims,
                'denorm_range' : denorm_range / 100
            }

    def previous(self):
        if self.count == 1: self.count = self.totalPages + 1
        self.count = max(1, self.count - 1)
        pageChange(self)
    def next(self):
        if self.count == self.totalPages: self.count = 0
        self.count = min(self.totalPages, self.count + 1)
        pageChange(self)
