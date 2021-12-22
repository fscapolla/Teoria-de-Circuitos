import numpy as np
from cmath import sqrt
import scipy.signal as ss
from src.constants import *

def denormZP(widg, poleNorm, which2, wn = None, B = None, wo = None):

       widg.num, widg.denom = widg.num.real, widg.denom.real

       if (which2 in [LP, GD]):
           poleDenorm = np.roots(widg.denom) * wn
           k = 1
           for pole in poleDenorm: k*=pole
           return ss.zpk2tf([], poleDenorm, np.abs(k))
       elif (which2 == HP):
           zeroDenorm = np.zeros(len(poleNorm))
           poleDenorm = wn / np.roots(widg.denom)
           return ss.zpk2tf(zeroDenorm, poleDenorm, np.abs(1))

       elif (which2 == BP):
           return ss.lp2bp(widg.num, widg.denom, wo, B)
       elif (which2 == BS):
           return ss.lp2bs(widg.num, widg.denom, wo, B)
       else:
           print("Error")
