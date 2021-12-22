import scipy.signal as ss
from numpy import pi, logspace,float
from sympy import sympify

def bode(widg):
    num = [float(sympify(i).evalf()) for i in widg.numerator_text.text().split(',')]
    denom = [float(sympify(i).evalf()) for i in widg.denom_text.text().split(',')]
    w = logspace(1, 8, num = 10000) * 2 * pi
    Bode = ss.bode(ss.TransferFunction(num, denom), w = w)
    widg.figure.clear()
    for i in range(len(widg.x_axis)):
        if widg.x_axis[i][1] == 'TIME': del(widg.x_axis[i])
        if widg.y_axis[i][1] == 'TIME': del(widg.y_axis[i])
    widg.x_axis.append([Bode[0] / (2 * pi), 'BODE'])
    widg.y_axis.append([Bode[1], 'BODE'])
    widg.y_phase.append([len(widg.x_axis) - 1, Bode[2]])
    widg.axes, widg.phase_axis = widg.figure.add_subplot(2, 1, 2), widg.figure.add_subplot(2, 1, 1)
    __bodeAxis(widg.axes, ylabel='Amp [dB]', xlabel=True)
    __bodeAxis(widg.phase_axis, ylabel='Phase [deg]')
    widg.plot()

def __bodeAxis(axis, ylabel, xlabel=False):
    axis.set_ylabel(ylabel)
    if xlabel: axis.set_xlabel('Frequency [Hz]')
    axis.grid(which='both')
    axis.set_xscale('log')
