import numpy as np
from src.constants import *
from scipy.signal import buttap, buttord, cheb1ap, cheb1ord

def wb_butter(widg, n):
    filt, wp, ws, Ap, As, lims, denorm_range = widg.data.values()
    wb = 1 / (10 ** ((Ap + (As - Ap) * denorm_range) / 10) - 1) ** (1 / (2 * n))

    widg.wb = wp / wb


    if filt == LP:
        wb *= (min(ws, wp) + (ws - wp) * denorm_range)
    elif filt == HP:
        wb = (max(ws, wp) + (ws - wp) * denorm_range) / wb
    elif filt in [BP, BS]:
        wb = transfer_BP_BS_aux(widg, 'Butter', wb)

    return wb


def transfer_BP_BS_aux(widg,approx, wb):
    filt, wp, ws, Ap, As, lims, denorm_range = widg.data.values()

    opt = {
        'Butter': (buttap, buttord),
        'Cheby 1': (cheb1ap, cheb1ord)
    }

    if approx not in opt.keys(): return

    # wb = 1 / (10 ** ((Ap + (As - Ap) * denorm_range) / 10) - 1) ** (1 / (2 * n))
    wx = wp + (ws - wp) * denorm_range
    # wx = wp

    if filt == BP:
        wo = np.sqrt(wp[0] * wp[1])
    else:
        wo = np.sqrt(ws[0] * ws[1])

    # wo = np.sqrt(wp[0] * wp[1])

    B = np.abs(wp[1] - wp[0]) / wo
    # if filt == BP:
    #     B *= wb
    # else:
    #     B /= wb
    map_B = lambda s: 1 / B * (s / wo + wo / s)
    n1, wn1 = opt[approx][1](np.abs(map_B(1j*wp[0])), np.abs(map_B(1j*ws[0])), Ap, As, analog=True)
    n2, wn2 = opt[approx][1](np.abs(map_B(1j*wp[1])), np.abs(map_B(1j*ws[1])), Ap, As, analog=True)

    if n1 > n2:
        denorm = wx[0]
        widg.index = 0
    else:
        denorm = wx[1]
        widg.index = 1
    # w_mul = wb * (filt == BP) + 1 / wb * (filt == BS)
    w_mul = wb * (filt == BP) + 1/wb * (filt == BS)

    widg.B = B
    widg.wo = wo
    widg.wb = wp / wb

    res = np.abs([
        -w_mul * (denorm - wo ** 2 / denorm) / 2 + np.sqrt(
            w_mul ** 2 * denorm ** 2 - 2 * w_mul ** 2 * wo ** 2 + w_mul ** 2 * wo ** 4 / denorm ** 2 + 4 * wo ** 2) / 2,
        -w_mul * (denorm - wo ** 2 / denorm) / 2 - np.sqrt(
            w_mul ** 2 * denorm ** 2 - 2 * w_mul ** 2 * wo ** 2 + w_mul ** 2 * wo ** 4 / denorm ** 2 + 4 * wo ** 2) / 2
    ])

    # if n1>n2:
    #     widg.mult = min(res) / wp[0]
    # else:
    #     widg.mult = max(res) / wp[1]
    #
    # if filt == BS: widg.mult = 1 / widg.mult


    return res
