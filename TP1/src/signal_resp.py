import numpy as np
import scipy.signal as ss

def get_transfer_function(widg):
    num = [float(i) for i in widg.numerator_text.text().split(',')]
    denom = [float(i) for i in widg.denom_text.text().split(',')]
    return ss.TransferFunction(num, denom)

def sine_resp(widg,freq):
    try:
        sys = get_transfer_function(widg)
        x = np.linspace(0, 5, num = 1000)
        t, yout, xout = ss.lsim(sys, T = x, U = np.sin(2*np.pi*freq*x))

        widg.figure.clear()
        widg.axes = widg.figure.add_subplot()
        widg.axes.grid(which='both')
        for i in range (len(widg.x_axis)):
            if widg.x_axis[i][1] == 'BODE': del(widg.x_axis[i])
            if widg.y_axis[i][1] == 'BODE': del(widg.y_axis[i])
        widg.y_phase.clear()
        widg.x_axis += [[t,'TIME'], [t,'TIME']]
        widg.y_axis += [[np.sin(2*np.pi*freq*t),'TIME'], [yout,'TIME']]
        widg.plot()
    except: pass

def impulse_resp(widg):
    try:
        sys = get_transfer_function(widg)
        t, yout = ss.impulse(sys)
        widg.figure.clear()
        widg.axes = widg.figure.add_subplot()
        widg.axes.grid(which='both')
        for i in range (len(widg.x_axis)):
            if widg.x_axis[i][1] == 'BODE': del(widg.x_axis[i])
            if widg.y_axis[i][1] == 'BODE': del(widg.y_axis[i])
        widg.x_axis += [[t,'TIME']]
        widg.y_axis += [[yout,'TIME']]
        widg.y_phase.clear()

        widg.plot()
    except: pass

def step_resp(widg):
    try:
        sys = get_transfer_function(widg)
        t, yout = ss.step(sys)
        widg.figure.clear()
        widg.axes = widg.figure.add_subplot()
        widg.axes.grid(which='both')
        for i in range (len(widg.x_axis)):
            if widg.x_axis[i][1] == 'BODE': del(widg.x_axis[i])
            if widg.y_axis[i][1] == 'BODE': del(widg.y_axis[i])
        widg.x_axis.append([t,'TIME'])
        widg.y_axis.append([yout,'TIME'])
        widg.y_phase.clear()

        widg.plot()
    except: pass
def square_resp(widg, freq, duty):
    try:
        sys = get_transfer_function(widg)
        t = np.linspace(0, 2, num = 1000)
        res = ss.lsim(sys, T = t, U = ss.square(t * 2 * np.pi * freq, duty = duty))
        widg.figure.clear()
        widg.axes = widg.figure.add_subplot()
        widg.axes.grid(which = 'both')
        for i in range (len(widg.x_axis)):
            if widg.x_axis[i][1] == 'BODE': del(widg.x_axis[i])
            if widg.y_axis[i][1] == 'BODE': del(widg.y_axis[i])
        widg.x_axis += [[res[0],'TIME'],[res[0],'TIME']]
        widg.y_axis += [[ss.square(t * 2 * np.pi * freq, duty = duty), 'TIME'], [res[1], 'TIME']]
        widg.y_phase.clear()

        widg.plot()
    except: pass

def plot_resp(widg):
    if widg.signal_type_box.currentText() == 'Sine': sine_resp(widg,widg.fr_box.value())
    elif widg.signal_type_box.currentText() == 'Square': square_resp(widg, widg.fr_box.value(), widg.duty_box.value())
    elif widg.signal_type_box.currentText() == 'Impulse': impulse_resp(widg)
    elif widg.signal_type_box.currentText() == 'Step': step_resp(widg)