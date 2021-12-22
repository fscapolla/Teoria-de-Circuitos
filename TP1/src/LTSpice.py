from src.FileHandling import __open_file
import ltspice
from numpy import log10, angle,pi

def ltspice_data(widg):
    if widg.showing_LT:
        widg.toggle_spice_data()
    else:
        # widg.clear()
        file_name = __open_file('raw')
        if not len(file_name): return None
        widg.data = ltspice.Ltspice(file_name)
        widg.data.parse()

        for variable in widg.data.getVariableNames():
            widg.X_axis_input_spice.addItem(variable)
            widg.Y_axis_input_spice.addItem(variable)
        widg.toggle_spice_data()

# Manejo y grafico de variables
def plot_ltspice(widg):
    trans_x = lambda name: [widg.data.getTime(), 'TIME'] if name == 'time' else [widg.data.getFrequency(), 'BODE'] if name == 'frequency' else [widg.data.getData(name), 'TIME']
    trans_y = lambda name_x, name_y: [20 * log10(abs(widg.data.getData(name_y))), 'BODE'] if name_x == 'frequency' else [widg.data.getData(name_y), 'TIME']
    widg.x_axis.append(trans_x(widg.X_axis_input_spice.currentText()))
    widg.y_axis.append(trans_y(widg.X_axis_input_spice.currentText(), widg.Y_axis_input_spice.currentText()))
    widg.axes.cla()
    widg.phase_axis.cla()

    if widg.X_axis_input_spice.currentText() == 'frequency':
        widg.y_phase.append([len(widg.x_axis) - 1, 180 / pi * angle(widg.data.getData(widg.Y_axis_input_spice.currentText()))])
        widg.figure.clear()
        widg.axes, widg.phase_axis = widg.figure.add_subplot(2,1,2), widg.figure.add_subplot(2,1,1)
        widg.axes.set_xlabel('Frequency [Hz]')
        widg.axes.set_ylabel('Amp [dB]')
        widg.phase_axis.set_ylabel('Phase [deg]')
        widg.phase_axis.grid(which = 'both')
        widg.phase_axis.set_xscale('log')
        widg.axes.set_xscale('log')
        for i in range(len(widg.x_axis)):
            if widg.x_axis[i][1] == 'TIME': widg.x_axis.erase(i)
            if widg.y_axis[i][1] == 'TIME': widg.y_axis.erase(i)
    widg.axes.grid(which = 'both')

    # widg.axes.grid(which = 'both')
    widg.plot()