import numpy as np
from src.constants import *
from scipy.special import legendre
from scipy.signal import zpk2tf, bode, TransferFunction

def get_minimaxi(filt, wp, ws, widg, norm = False):
    if filt == 'lowpass':
        mini, maxi = wp, ws
    elif filt == 'highpass':
        mini, maxi = ws, wp

    else:
        wx = wp if filt == BP else ws
        wb = ws if filt == BP else wp
        wo = np.sqrt(wp[0] * wp[1])
        mapB = get_mapper(wp, ws, filt, widg)
        if not get_index(filt, wp, ws, widg):
            mini, maxi = min(wx[1], wo**2/wb[0]), max(wx[1], wo**2/wb[0])
        else:
            mini, maxi = min(wx[1], wb[1]), max(wx[1], wb[1])

        if norm: mini, maxi = np.abs(mapB(mini)), np.abs(mapB(maxi))

    # return maxi,mini
    return min(mini, maxi), max(mini, maxi)
def get_roots(poly, widg):
    # roots_ok = poly.roots[np.logical_and(poly.roots.real < 0, np.abs(poly.roots.real) > 1e-10)]
    # print(roots_ok)

    roots_ok = np.array([complex(
        pole.real if abs(pole.real) > 1e-12 else 0,
        pole.imag if abs(pole.imag) > 1e-12 else 0
    ) for pole in 1j*poly.roots if pole.real < 0])

    # roots_ok = 1j * poly.roots[poly.roots.imag > 0]
    # print(roots_ok)
    gain = 1 / np.sqrt(poly(0))

    for pole in roots_ok: gain *= pole

    return zpk2tf([], roots_ok, gain)

def to_eval_square(pol: np.array):
    if not len(pol): return []
    res = np.zeros(2 * len(pol) - 1)
    res[-1] = pol[-1]
    for i in range(len(res)):
        if not i % 2: res[i] = pol[np.int(i / 2)]
    return res
def get_index(filt, wp, ws, widg):
    wd = ws if filt == BP else wp
    # wx = wp if filt == BP else ws
    mapB = get_mapper(wp,ws,filt, widg)
    # print('wp:',mapB(wp))
    # print('ws:',mapB(ws))
    res = int(np.abs(mapB(wd[0])) > np.abs(mapB(wd[1])))
    return 1 - res if filt == BS else res

def poly_legendre(wp, ws, Ap, As, filt, widg):
    n = 1
    if widg.nmin_checkbox.isChecked():
        n = widg.n_min_value.value()

    # eps = np.sqrt(10 ** (Ap / 10) - 1)
    eps = np.sqrt(10 ** (Ap / 10) - 1)
    # print('eps:',eps)
    poly_ok = legendre(n)
    transfer = lambda w: 10 * np.log10(np.abs(1 / (1 + eps ** 2 * poly_ok(w**2))))

    checkap = lambda w, A: transfer(w) < -A and np.abs(transfer(w) + A) > 0.05
    checkas = lambda w, A: transfer(w) > -A and np.abs(transfer(w) + A) > 0.05

    norm = (filt in [BP, BS])
    mini, maxi = get_minimaxi(filt, wp, ws, widg, norm)

    while checkap(1, Ap) or checkas(maxi/mini, As):
        # print(transfer(maxi/mini) > -As)
        # print(transfer(1) < -Ap)
        n += 1
        poly_ok = legendre(n)
        if widg.nmax_checkbox.isChecked() and n == widg.n_max_value.value(): break
        if n == NMAX : break

    return poly_ok * eps**2 + 1

def transfer_legendre(widg):
    filt, wp, ws, Ap, As, lims, denorm_range = widg.data.values()

    poly = poly_legendre(wp, ws, Ap, As, filt, widg)
    poly_ok = np.poly1d(to_eval_square(poly.coeffs))

    transfer = get_roots(poly_ok, widg)

    widg.num, widg.denom = transfer

    polynum, polydenom = np.poly1d(transfer[0]), np.poly1d(transfer[1])
    H = lambda w : polynum(1j*w) / polydenom(1j*w)
    print('H(1):', 20*np.log10(np.abs(H(1))))

    multS = get_mult_S(wp, ws, As, filt, H, denorm_range, widg) if denorm_range else 1
    # if filt == BS: multS = 1 / multS

    widg.mult = multS

    print('MULT: ',multS)
    # if filt in [BP, BS]:
    #     mapB = get_mapper(wp, ws, filt, widg)
    #     transform = lambda w: w / multS if w>np.sqrt(wp[0]*wp[1]) else w*multS
    #     w_trans = lambda w: np.array([transform(wi) for wi in w])
    #     w_res = lambda w: mapB(w_trans(w))

    if filt in [LP, HP]:
        widg.wn = widg.wb = wp * multS
        # return lambda w: H(w / (wp * multS)) if filt == LP else H(wp * multS / w)
    else:
        widg.index = get_index(filt, wp, ws,widg)
        # return lambda w: H(w_res(w)) if filt == BP else open_BS(wp, ws, Ap, As, lambda w: H(w_res(w)), w)
        # return lambda w: H(w_res(w))

def get_mapper(wp, ws, filt, widg):
    wx = wp if filt == BP else wp
    wo = np.sqrt(wx[0] * wx[1])
    B  = np.abs(wx[1] - wx[0])/ wo
    widg.wo = wo
    # if filt == BS: widg.wo = np.sqrt(ws[0] * ws[1])
    widg.B = B*wo
    # if filt == BS: widg.B = ws[1] - ws[0]
    return lambda w: (1/B * (w/wo-wo/w)) ** ((-1)**(filt == BS))

def get_mapper2(wp, ws, filt):
    wx = wp if filt == BP else ws
    # wo = np.sqrt(wp[0] * wp[1])
    wo = np.sqrt(wx[0] * wx[1])
    B = np.abs(wp[1] - wp[0]) / wo
    return lambda w: (1 / B * (w / wo - wo / w)) ** ((-1) ** (filt == BS))


def get_mult_S(wp, ws, As, filt, H, denorm_range, widg):
    mini, maxi = get_minimaxi(filt, wp, ws, widg, norm=True)

    if filt in [BP, BS]:
        lim = get_index(filt,wp,ws, widg)
        wo = np.sqrt(wp[0]*wp[1])
        wx = wp if filt == BP else ws
        wb = ws if filt == BP else wp
        w = np.linspace(min(wo, wb[lim]), max(wo, wb[lim]), num=int(max(wo, wb[lim]) / min(wo, wb[lim])) * 100000)
        mapB = get_mapper(wp, ws, filt, widg)
    else:
        w = np.linspace(mini, maxi, num=int(maxi/mini) * 10000)

    mag = lambda w: 20 * np.log10(np.abs(H(w)))


    test = lambda w: mag(w / wp) if filt == LP else mag(wp / w) if filt == HP \
        else mag(mapB(w)) if filt in [BP, BS] else None

    m = w[np.abs(test(w) + As) < 0.01]
    print('m0: ', m[0])

    if filt in [HP, LP]:
        return 1 + (ws / m[0] - 1) * denorm_range if len (m) else 1
    else:
        lim = get_index(filt,wp,ws, widg)

        wo = np.sqrt(wp[0] * wp[1])
        if not lim:
            # return (1 + (wo**2/wb[0] / wx[1] / m[0] - 1) * denorm_range) if len (m) else 1
            return (1 + (m[0]/ws[0] - 1) * denorm_range) if len(m) else 1

        else:
            # return 1 + (wb[1] / wx[1] / m[0] - 1) * denorm_range if len (m) else 1
            return 1 + (ws[1] / m[0] - 1) * denorm_range if len (m) else 1


def open_BS(wp, ws, Ap, As, H, w):
    return H(w)
    # m = w[np.abs(20 * np.log10(np.abs(H(w))) + As) < 0.05]
    # wo = np.sqrt(ws[0] * ws[1])
    #
    # lim = get_index('bandstop', wp, ws, widg)
    #
    # if not lim: m = m[m < wo]
    # else: m = m[m > wo]
    #
    # mult = m[0] / ws[lim] if len(m) else 1
    # if lim: mult = 1/mult
    # return H(w / mult)
