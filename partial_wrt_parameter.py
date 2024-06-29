import numpy as np
import matplotlib.pyplot as plt

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def phase(h):
    deg = np.degrees(np.angle(h))
    return np.degrees(np.angle(h))

def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)
    np.phase = np.frompyfunc(phase, 1, 1)

    # 3dB point
    f_3db = 1000
    tau = 1/(2 * np.pi * f_3db)

    # plot from 1Hz to 100kHz
    freq = np.logspace(1, 5, num=256)
    w = 2 * np.pi * freq
    s = 1j * w

    # low pass filter frequency response
    h_lpf = 1 / (1 + s * tau)

    # partial derivative of h_lpf with respect to tau
    h_deriv = -s / (1 + s * tau) ** 2

    # create axes
    fig, ax = plt.subplots(2, 1)
    ax[0].set_title('Gain')
    ax[0].set_ylabel('Gain (dB)')
    ax[0].grid()

    ax[1].set_title('Phase')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_ylim(-180, 180)
    ax[1].grid()

    # gain plot
    ax[0].semilogx(freq, np.gain_db(h_lpf), 'b-', label=r'$\frac{1}{1+s\tau}$')
    ax[0].semilogx(freq, np.gain_db(h_deriv), 'r-', label=r'$\frac{\partial}{\partial\tau}\left(\frac{1}{1+s\tau}\right)$')
    ax[0].legend()

    # phase plot
    ax[1].semilogx(
        freq, np.phase(h_lpf), 'b-',
        freq, np.phase(h_deriv), 'r-'
    )
    
    plt.show()

if __name__ == '__main__':
    main()