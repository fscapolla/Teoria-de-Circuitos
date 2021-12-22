import numpy as np
from scipy.signal import zpk2tf
import sympy as sp
from src.Legendre import get_index, get_mapper
from src.constants import *

x = sp.symbols('x', real = True)
NMAX_GAUSS = 50

def get_roots(poly, widg):
    roots_ok = poly.roots[np.real(poly.roots) < 0]

    gain = 1/np.sqrt(poly(0))
    for pole in roots_ok: gain *= pole

    widg.poleNorm = roots_ok

    return zpk2tf([], roots_ok, gain)

def to_eval_square(pol: np.array):
    if not len(pol): return []
    res = np.zeros(2 * len(pol) - 1)
    res[-1] = pol[-1]
    for i in range(len(res)):
        if not i % 2: res[i] = pol[np.int(i / 2)]
    return res
fact = lambda num: num * fact(num - 1) if num > 1 else 1 if num >= 0 else None

def transfer(n, Ap, widg):
    multiplier = 1
    gn = (10 ** (Ap / 10))
    a = -np.log(gn) * multiplier
    res = np.zeros(n + 1)
    for k in range(1, n + 1): res[len(res) - k - 1] = a ** k / fact(k)
    rr = np.poly1d(to_eval_square(res))
    # return 10 * np.log10(gn ** (multiplier - 1) / (1 + rr(w)))
    return get_roots(1+rr, widg)

def trans_to_poly (n, Ap, widg):
    trans = transfer(n, Ap, widg)
    return np.poly1d(trans[0]), np.poly1d(trans[1])


checkap = lambda w, A, H: H(w) < -A and np.abs(H(w) + A) > 0.01
checkas = lambda w, A, H: H(w) > -A and np.abs(H(w) + A) > 0.01


def get_H(widg):
    n = 1
    if widg.nmin_checkbox.isChecked():
        n = widg.n_min_value.value()
    filt, wp, ws, Ap, As, lims,denorm_range = widg.data.values()

    wpx, wsx = wp, ws
    if filt == GD: wpx = widg.omega_gd_value.value() * 1000

    polynum, polydenom = trans_to_poly(n, Ap, widg)
    if filt in [BP, BS]:
        mapB = get_mapper(wp, ws, filt, widg)
        lim = get_index(filt, wp, ws, widg)
        wpx, wsx = np.abs(mapB(wp[lim])), np.abs(mapB(ws[lim]))

    H_full = lambda w: polynum(1j * w) / polydenom(1j * w)
    H = lambda w: 20 * np.log10(np.abs(H_full(w)))

    if filt != 'groupdelay':
        while checkap(1, Ap, H) or checkas(max(wpx, wsx) / min(wpx, wsx), As, H):
            n += 1
            polynum, polydenom = trans_to_poly(n,Ap, widg)
            if n == NMAX_GAUSS: break
            if widg.nmax_checkbox.isChecked() and n == widg.n_max_value.value(): break

    else:
        # gd = sp.lambdify(x,-sp.atan2(sp.im(H_full(x)), sp.re(H_full(x))).diff(x), modules = ['numpy', 'sympy'])
        wr = np.logspace(widg.lims[0], widg.lims[1], num = 10000)
        idx =  len(wr) - len(wr[wr>=wpx])
        g = -np.diff(np.angle(H_full(wr/wpx))) / np.diff(wr)
        # while gd(1)/gd(0) < 1-widg.to_var:
        while g[idx]/g[0] < 1-widg.to_var:
            n+=1
            polynum, polydenom = trans_to_poly(n,Ap, widg)
            # gd = sp.lambdify(x, -sp.atan2(sp.im(H_full(x)), sp.re(H_full(x))).diff(x), modules=['numpy', 'sympy'])
            g = -np.diff(np.angle(H_full(wr / wpx))) / np.diff(wr)
            if widg.nmax_checkbox.isChecked() and n == widg.n_max_value.value(): break

    print(n)

    widg.num, widg.denom = polynum.coeffs, polydenom.coeffs

    if filt != 'groupdelay': return H_full, H
    # else: return lambda w: gd(w/wpx)/gd(0) * widg.to
    else: return None

def gaussian(widg):
    filt, wp, ws, Ap, As, lims,denorm_range = widg.data.values()

    if filt != 'groupdelay':
        H_full, H = get_H(widg)
    else:
        gd = get_H(widg)
        widg.wn = widg.wb = widg.omega_gd_value.value() * 1000
        return gd

    # if filt in [LP, HP]:
    #     w = np.linspace(min(wp,ws)/10, max(wp,ws)*10, num=np.int(max(wp,ws) / min(wp,ws)) * 10000)
    #     tester = lambda w: H(w / wp) if filt == LP else H(wp / w)
    #     m = w[np.abs(tester(w) + As) < 0.01]
    #     mult = 1 + (ws / m[0] - 1) * denorm_range if len(m) else 1
    #     widg.wn = widg.wb = wp * mult
    #     return lambda w: H_full(w / (wp * mult)) if filt == LP else H_full(wp * mult / w)
    #
    # elif filt in [BP, BS]:
    #     if filt == BP:
    #         wedge, wcenter = ws, wp
    #     else:
    #         wedge, wcenter = ws,wp
    #
    #     mapB = get_mapper(wp, ws, filt, widg)
    #     lim = get_index(filt, wp, ws, widg)
    #     if not lim:
    #         mini, maxi = wedge, wcenter
    #     else:
    #         mini, maxi = wcenter, wedge
    #
    #     w = np.linspace(mini[lim], maxi[lim], num=np.int(maxi[lim] / mini[lim]) * 10000)
    #     tester = lambda w: H(mapB(w))
    #     m = w[np.abs(tester(w) + As) < 0.01]
    #
    #     mult = 1 + (ws[lim] / m[0] - 1) * denorm_range if len(m) else 1
    #
    #     if not lim: mult = 1 / mult
    #
    #     move = lambda w: [wi / mult if wi > np.sqrt(wp[0]*wp[1]) else wi * mult for wi in w]
    #
    #     return lambda w: H_full(mapB(move(w)))
    #
    # else:
