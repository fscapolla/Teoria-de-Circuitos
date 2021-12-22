import numpy as np
from src.constants import *
from scipy.signal import ellip

def wb_cauer(widg, n):
    filt, wp, ws, Ap, As, lims, denorm_range = widg.data.values()
    num, denom = ellip(n, Ap, As, wp, filt, analog=True)[:2]

    widg.wb = wp

    if filt == LP:
        mini, maxi = wp, ws
    elif filt == HP:
        mini, maxi = ws, wp
    elif filt == BP:
        mini, maxi = wp[1], ws[1]
    else:
        mini, maxi = ws[1], wp[1]
    polynum, polydenom = np.poly1d(num), np.poly1d(denom)

    transfer = lambda w: polynum(1j * w) / polydenom(1j * w)
    mod = lambda w: 20 * np.log10(np.abs(transfer(w)))
    w = np.linspace(mini, maxi, num=np.int(maxi / mini) * 10000)
    m = w[np.abs(mod(w) + As) < 0.05]

    if filt in [LP, HP]:
        mul = 1 + (ws / m[0] - 1) * denorm_range if len(m) else 1
    else:
        mul = 1 + (ws[1] / m[0] - 1) * denorm_range if len(m) else 1

    # mul = (ws - m[0])*denorm_range

    newN = n
    if widg.nmin_checkbox.isChecked() and n < widg.n_min_value.value(): newN = widg.n_min_value.value()
    if widg.nmax_checkbox.isChecked() and n > widg.n_max_value.value(): newN = widg.n_max_value.value()

    num, denom = ellip(newN, Ap, As, wp*mul, filt, analog=True)[:2]
    polynum, polydenom = np.poly1d(num), np.poly1d(denom)
    transfer = lambda w: polynum(1j * w) / polydenom(1j * w)

    if filt in [LP, HP]:
        return wp * mul
    else:
        return [wp[0]/mul, wp[1]*mul]
