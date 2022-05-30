import numpy as np
import scipy.signal as ss
from src.constants import *
import sympy as sp
from src.poles_zeros import plot_poles_zeros
from src.func2zpk import denormZP
from src.textWidget import textWidget
from cmath import sqrt

x = sp.symbols('x', real = True)

def plotAll(widg, which = 'numDenum'):
    if (widg.count == 0):

        widg.w = np.logspace(widg.lims[0], widg.lims[1], num=10000)
        if which != 'numDenum':
            if widg.data['filt'] in [BP, BS]:
                widg.num, widg.denom = denormZP(widg, np.roots(widg.denom), widg.data['filt'], B = widg.B, wo = widg.wo)
            else:
                widg.num, widg.denom = denormZP(widg, np.roots(widg.denom), widg.data['filt'], wn = widg.wn)

        widg.w1, widg.mag, widg.phase = ss.bode(ss.TransferFunction(widg.num, widg.denom), w=widg.w)

        # Llamado a funciones
        funcCall(widg, widg.w)
        for ax in widg.axes:
            ax.minorticks_on(); ax.grid(b = True, which = 'both')

    else:
        pageChange(widg)


def funcCall(widg, w):
    try: maxQPlot(widg)
    except: pass
    try: denormalizedPlot(widg)
    except: pass
    try: normalizedPlot(widg)
    except: pass
    try: jointTranferPlot(widg)
    except: pass
    try: phasePlot(widg)
    except: pass
    try: phaseDelayPlot(widg, w)
    except: pass
    try: ZeroesPolesPlot(widg)
    except: pass
    try: impulsiveResponse(widg)
    except: pass
    try: stepResponse(widg)
    except: pass
    try: sosPlot(widg)
    except: pass

    for fig in widg.figure: fig.tight_layout()
    for ax in widg.axes: ax.legend()
    for canvas in widg.canvas: canvas.draw()

from copy import deepcopy
def denormalizedPlot(widg):
    w = deepcopy(widg.w)
    w_t = deepcopy(widg.w)
    mag = deepcopy(widg.mag)
    mag_t = deepcopy(widg.mag)
    if widg.data['filt'] == BP and widg.approxType.currentText() in ['Legendre', 'Cauer']:
        w = widg.w[widg.w < widg.wo] / widg.mult
        w_t = np.append(w, widg.w[widg.w > widg.wo] * widg.mult)
    elif widg.data['filt'] == BS and widg.approxType.currentText() in ['Legendre', 'Cauer']:
        lim1 = lim2 = 0
        for i in w:
            if i < widg.wo*widg.mult: lim1 += 1
            if i < widg.wo/widg.mult: lim2 += 1

        w_t = w[: lim1]
        w_t = np.append(w_t, w[lim2:])
        w_x = w_t[w_t < widg.wo] / widg.mult
        w_t = np.append(w_x, w_t[w_t > widg.wo]*widg.mult)
        mag_t = mag[: lim1]
        mag_t = np.append(mag_t, mag[lim2:])


    widg.wok = w_t
    widg.magok = mag_t
    widg.axes[0].plot(w_t, -mag_t, label="Atenuación desnormalizada")
    widg.axes[0].set_xscale('log')
    widg.axes[0].set_xlabel(r'$\omega$ [$\frac{rad}{seg}$]',  fontsize = 15)
    widg.axes[0].set_ylabel(r'Atenuation [dB]',  fontsize = 12)

def normalizedPlot(widg):
    if widg.filt in [LP,HP, GD]:
        widg.axes[1].plot(widg.w / widg.wb, -widg.mag, label="Atenuación normalizada")
    else:
        mapB = lambda w: (1 / widg.B * (w / widg.wo - widg.wo / w)) ** ((-1) ** (widg.filt == BS))
        length = len(widg.w[widg.w <= widg.wo])
        mult = widg.wo
        if widg.filt == BS: mult = 1 / mult
        widg.axes[1].plot(mapB(widg.w[length:]) * mult, -widg.mag[length:], label="Atenuación normalizada")

    widg.axes[1].set_xscale('log')
    widg.axes[1].set_xlabel(r'$\omega$ [$\frac{rad}{seg}$]',  fontsize = 15)
    widg.axes[1].set_ylabel(r'Atenuation [dB]',  fontsize = 12)

def plot_limits(which, widg):
    if widg.data['filt'] in [BP, BS]:
        wp = widg.data['wp'][widg.index]
        ws = widg.data['ws'][widg.index]
    else:
        wp = widg.data['wp']
        ws = widg.data['ws']

    if which == HP:
        widg.axes[2].plot([10 ** widg.lims[0], ws], [widg.data['As'], widg.data['As']], color='black')
        widg.axes[2].plot([ws, ws], [widg.data['As'], 0], color='black')
        widg.axes[2].plot([wp, 10 ** widg.lims[1]], [widg.data['Ap'], widg.data['Ap']], color='black')
        widg.axes[2].plot([wp, wp], [widg.data['Ap'], widg.data['Ap'] + 40], color='black')
    else:
        widg.axes[2].plot([10 ** widg.lims[0], wp], [widg.data['Ap'], widg.data['Ap']], color='black')
        widg.axes[2].plot([wp, wp], [widg.data['Ap'], widg.data['Ap'] + 40], color='black')
        widg.axes[2].plot([ws, 10 ** widg.lims[1]], [widg.data['As'], widg.data['As']], color='black')
        widg.axes[2].plot([ws, ws], [0, widg.data['As']], color='black')

def jointTranferPlot(widg):

    widg.axes[2].plot(widg.wok, -widg.magok, label="Atenuación desnormalizada")

    if (widg.data['filt'] == HP): plot_limits(HP, widg)
    elif (widg.data['filt'] == BS):
        if (widg.index == 0): plot_limits(LP, widg)
        else: plot_limits(HP, widg)
    elif (widg.data['filt'] == BP):
        if (widg.index == 0): plot_limits(HP, widg)
        else: plot_limits(LP, widg)

    else: plot_limits(LP, widg)

    widg.axes[2].set_xscale('log')
    widg.axes[2].set_xlabel(r'$\omega$ [$\frac{rad}{seg}$]', fontsize=15)
    widg.axes[2].set_ylabel(r'Atenuation [dB]', fontsize=12)


def phasePlot(widg):
    for i in range(len(widg.phase)):
        if widg.phase[i] < -180: widg.phase[i]+=360
        elif widg.phase[i] > 180: widg.phase[i] -= 360
    widg.axes[3].plot(widg.w, widg.phase, label="Fase")
    widg.axes[3].set_xscale('log')
    widg.axes[3].set_xlabel(r'$\omega$ [$\frac{rad}{seg}$]',  fontsize = 15)
    widg.axes[3].set_ylabel(r'$\Phi$ [deg]',  fontsize = 15)


def phaseDelayPlot(widg, w):
    polynum, polydenom = np.poly1d(widg.num), np.poly1d(widg.denom)
    H = lambda w: polynum(1j * w) / polydenom(1j * w)
    hx = H(w)
    g = -np.diff(np.angle(hx)) / np.diff(w)
    g = g[np.abs(g) / g[0] * widg.to < 1e2]

    if widg.filt == 'groupdelay':
        widg.axes[4].plot(w[:len(g)], g / g[0] * widg.to, label='Retardo de grupo')
    else:
        widg.axes[4].plot(w[:len(g)], g, label='Retardo de grupo')

    widg.axes[4].set_xlabel(r'$\omega$ [$\frac{rad}{seg}$]',  fontsize = 15)
    widg.axes[4].set_ylabel(r'$\tau [s]$',  fontsize = 15)
    widg.axes[4].set_xscale('log')

def ZeroesPolesPlot(widg):
    widg.zeroes, widg.poles, gain = ss.tf2zpk(widg.num, widg.denom)
    plot_poles_zeros(widg.num, widg.denom, widg.figure[5], ax = widg.axes[5])


def impulsiveResponse(widg):
    if (widg.witch == 'numDenum'):
        widg.ti, widg.yImpulse = ss.impulse((widg.num, widg.denom), N = 10000)
    elif (widg.witch == 'function'):
        print("hola")
    widg.axes[6].plot(widg.ti, widg.yImpulse, label="Respuesta impulsiva")
    widg.axes[6].set_xlabel(r'Time [s]',  fontsize = 12)
    widg.axes[6].set_ylabel(r'Response [V]',  fontsize = 12)


def stepResponse(widg):
    widg.ts, widg.yStep = ss.step((widg.num, widg.denom), N = 10000)
    widg.axes[7].plot(widg.ts, widg.yStep, label="Respuesta al escalón")
    widg.axes[7].set_xlabel(r'Time [s]',  fontsize = 12)
    widg.axes[7].set_ylabel(r'Response [V]',  fontsize = 12)


def maxQPlot(widg):
    i = 1
    run = 0
    Q = lambda pole: -np.abs(pole) / (2 * np.real(pole))

    widg.zeroes, widg.poles, gain = ss.tf2zpk(widg.num, widg.denom)

    if (widg.qmax_checkbox.isChecked()):
        for j in range(len(widg.poles)):
            # print(widg.q_max_value.value())
            if  Q(widg.poles[j]) > widg.q_max_value.value() and widg.poles[j].real != 0\
                    and widg.poles[j].imag != 0:
                widg.poles[j] = setPoleQmax(widg, widg.poles[j])

        if len(widg.zeroes): widg.num = np.poly(widg.zeroes) * gain
        else: widg.num = [gain]
        widg.denom = np.poly(widg.poles)
        widg.w1, widg.mag, widg.phase = ss.bode(ss.TransferFunction(widg.num, widg.denom), w=widg.w)

    for pole in widg.poles[widg.poles.imag != 0]:
        if (np.real(pole) != 0):
            if (run == 0):
                widg.axes[8].scatter(i, Q(pole), label='Q poles')
                run += 1
            else:
                widg.axes[8].scatter(i, Q(pole))
        else:
            widg.axes[8].scatter(0, 0, label = fr'Q{i} = $\infty$')
            # widg.axes[8].text(r'Q en $\infty$')
        i += 1

def setPoleQmax(widg, oldPole):
    A = np.array([[1, 2 * widg.q_max_value.value()], [1, 0]])
    B = np.array([0, np.abs(oldPole)])
    X = np.linalg.solve(A, B)
    return X[1] + 1j*np.sqrt(X[0]**2-X[1]**2) * ((-1) ** (oldPole.imag < 0))

def pageChange(widg):
    if (widg.count <= widg.totalPages): widg.graphic.setCurrentIndex(widg.count-1)
    else: print("Error")

def sosPlot(widg):
    sos = np.round(ss.tf2sos(widg.num, widg.denom, pairing='keep_odd'), 2)
    sos = sosPlotMinFirst(sos)

    pairs, k = get_pairs(widg.zeroes)
    r = 0
    done = False
    string = ''
    for i in range(len(sos)):
        string += r'$T_{'
        string += f'{i}'
        string += r'}$ = $\frac'
        if sos[i][2]==sos[i][5]==0: down = [sos[i][3],sos[i][4]]
        else: down = sos[i][3:]

        up = np.poly1d(widg.num).coeffs[0] if not done else 1
        done = True
        up *= (np.real(np.poly(pairs[r])) if len(pairs) > r else np.array([1]))
        r += 1

        for u in range(len(up)):
            up[u] = np.round(float(up[u]), 2)
            if np.abs(up[u]) < 1e-10: up[u] = 0
        upstring, downstring = r'', r''

        for n in range (len(up)):
            upstring += f'{up[n]} \cdot s^{len(up) - 1 - n}' if n < len(up)-1 and up[n] != 0 and len(up)-1-n != 1 else f'{up[n]} \cdot s' if len(up) - 1 - n == 1 and up[n] != 0  else f'{up[n]}' if up[n]!=0 else ''
            if n != len(up)-1 and up[n+1]!=0: upstring += '+'
        for n in range(len(down)):
            downstring += f'{down[n]} \cdot s^{len(down) - 1 - n}' if n < len(down) - 1 and down[n] != 0 and len(down)-1-n != 1  else f'{down[n]} \cdot s' if len(down) - 1 - n == 1 and down[n] != 0 else f'{down[n]}' if down[n]!=0 else ''
            if n != len(down)-1 and down[n+1]!=0: downstring += '+'

        stringtemp = '{'
        stringtemp += f'{upstring}'
        stringtemp += '}'
        string += f'{stringtemp}'
        stringtemp = '{'
        stringtemp += f'{downstring}'
        stringtemp += '}'
        string += f'{stringtemp}'
        string += '$'

        string += '\n'

    string = rf'{string}'
    # tWidg = textWidget(widg.figure[9], widg.canvas[9], string)

    if not 'tw' in sosPlot.__dict__.keys():
        sosPlot.__dict__['tw'] = textWidget(widg.figure[9], widg.canvas[9], string)
    else:
        sosPlot.__dict__['tw'].set_text(string)

    sosPlot.__dict__['tw'].drawIt()

def get_pairs(roots):
    tot = deepcopy(roots)
    res = []
    k = 0
    for i in range (len(roots)):
        if np.abs(tot[i].imag) < 1e-12 and tot[i] != 1234:
            re = [roots[i].real]
            for j in range(i+1, len(tot)):
                if tot[j] == tot[i]:
                    re.append(roots[j])
                    tot[j] = 1234
                    break

            res.append(re)
            k+=1
    for i in range(len(roots)):
        for j in range(i+1,len(roots)):
            if roots[i] != 1234 and roots[i]!=0 and roots[j]!=0 and np.abs(roots[i].real - roots[j].real) < 1e-12 and np.abs(roots[i].imag + roots[j].imag) < 1e-12:
                res.append([roots[i], roots[j]])



    return np.sort(res), k

def swap(poly, i, j):
    aux = deepcopy(poly[i])
    poly[i] = deepcopy(poly[j])
    poly[j] = aux

def sosPlotMinFirst(sos):
    k = 0
    for i in range(len(sos)):
        if sos[i][2] == sos[i][5] == 0:
            swap(sos,k,i)
            k+=1

    return sos

