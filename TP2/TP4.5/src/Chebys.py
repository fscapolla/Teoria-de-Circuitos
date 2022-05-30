import numpy as np
from src.constants import *
from src.Butter import transfer_BP_BS_aux

def wb_cheby1(widg, n):
    filt, wp, ws, Ap, As, lims, denorm_range = widg.data.values()

    w0min = np.cosh(1 / n * np.arccosh(np.sqrt(10 ** (As / 10) - 1) / (np.sqrt(10 ** (As / 10) - 1))))
    w0max = np.cosh(1 / n * np.arccosh(np.sqrt(10 ** (As / 10) - 1) / (np.sqrt(10 ** (Ap / 10) - 1))))

    wb = w0min + (w0max - w0min)*denorm_range
    w0 = w0max
    widg.wb = wp
    # wx = 1 / (10 ** (Ap/ 10) - 1)**(0.5/n)

    if filt == LP:
        wbmax = ws / w0
    elif filt == HP:
        wbmax = ws * w0
    else:
        # wb = transfer_BP_BS_aux(widg, 'Cheby 1', 1 / (wx + (w0-wx)*denorm_range))
        wb = transfer_BP_BS_aux(widg, 'Cheby 1', 1/wb)


    # else: wb = widg.transfer_BP_BS_aux(n, 'Cheby 1',1/w0 * (1-denorm_range))
    if filt in [HP, LP]:
        wb = min(wp, wbmax) + denorm_range * abs(wbmax - wp)

    return wb
