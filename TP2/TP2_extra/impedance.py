import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import ltspice
import pandas as pd
#
fig = plt.figure()
mag, phase = fig.add_subplot(2,1,1), fig.add_subplot(2,1,2)

def plotImpedance (i):

    data = ltspice.Ltspice(f'C:/Users/alanv/Desktop/Caso{i}.raw')
    data.parse()

    Vin = data.getData('V(in)')
    Iin = data.getData('I(R1)')
    freq = data.getFrequency()

    num = 0
    while freq[num]<100: num+=1

    mag.plot(freq[num:], np.abs(Vin/Iin)[num:]/1000, label = f'Caso {i}')
    phase.plot(freq[num:], np.angle(-(Vin/Iin)[num:])*180/np.pi, label = f'Caso {i}')
plotImpedance(1)
plotImpedance(2)
plotImpedance(3)

mag.set_xscale('log'); phase.set_xscale('log')
mag.minorticks_on(); phase.minorticks_on()
mag.grid(which = 'both'); phase.grid(which = 'both')
phase.set_xlabel('Frequency [Hz]');
mag.set_ylabel('Impedance [k\u03A9]'); phase.set_ylabel('Phase [deg]')
mag.legend(); phase.legend()
plt.show()