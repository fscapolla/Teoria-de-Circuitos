import matplotlib.pyplot as plt
from scipy.signal import tf2zpk
from numpy import append

def plot_poles_zeros(b, a, fig : plt.figure = None, ax : plt.subplot = None, pos : int = 111,
                     color_zeros = 'blue', color_poles = 'red'):

    # Zeros, poles, gain
    zpk = tf2zpk(b,a)

    if not fig: fig = plt.figure()
    if not ax: ax = fig.add_subplot(pos)

    ax.minorticks_on()
    ax.grid(b = True, which = 'both')

    # First zero, with label.
    if len(zpk[0]): ax.scatter(zpk[0][0].real, zpk[0][0].imag, marker='o', color=color_zeros, label = 'Zeros')

    # Zeros
    for zero in zpk[0][1:]:
        ax.scatter(zero.real, zero.imag, marker = 'o', color = color_zeros)

    # First pole, with label.
    if len(zpk[1]): ax.scatter(zpk[1][0].real, zpk[1][0].imag, marker='x', color=color_poles, label = 'Poles')

    # Poles
    for pole in zpk[1][1:]:
        ax.scatter(pole.real, pole.imag, marker = 'x', color = color_poles)

    # Figure title and labels
    ax.set_title('Poles and Zeros')
    ax.set_xlabel(r'$\alpha$', fontsize = 15)
    ax.set_ylabel(r'j$\omega$', fontsize = 15)
    ax.legend()

    # X-Axis limits
    x = append(zpk[0].real, zpk[1].real)
    y = append(zpk[0].imag, zpk[1].imag)
    xmax = max(x)
    xmin = min(x)
    x_denorm = max(abs(xmax), abs(xmin)) * 1.1

    # Y-Axis limits
    ymax = max(y)
    ymin = min(y)
    y_denorm = max(abs(ymin), abs(ymax)) * 1.1

    ax.set_xlim(-y_denorm, y_denorm)
    ax.set_xlim(-x_denorm, x_denorm)

    # Lines at x = 0 (jw axis) and y = 0 (alpha axis)
    ax.axhline(0, lw = 1, color = 'black')
    ax.axvline(0, lw = 1, color = 'black')

    fig.tight_layout()
    return fig


if __name__ == '__main__':
    num = [1,1e2]
    denom = [1/1e3, 2, 1e3, 0.5, 4.23, 3, 2e4, 1]

    fig = plot_poles_zeros(num, denom)
    plt.show()