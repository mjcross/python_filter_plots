import numpy as np
import matplotlib.pyplot as plt

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def phase(h):
    return np.degrees(np.angle(h))

def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)
    np.phase = np.frompyfunc(phase, 1, 1)

    # 3dB point of filter
    f_c = 1000
    w_c = 2 * np.pi * f_c
    tau = 1 / w_c

    # discrete time sampling frequency
    f_s = 20001
    T = 1 / f_s

    # sweep frequency from 100Hz - 10KHz
    freq = np.logspace(2, 4, num=512)
    w = 2 * np.pi * freq
    s = 1j * w              # equivalent of frequency in Laplace domain
    z = np.exp(1j * w * T)  # equivalent of frequency in Z domain

    # Laplace domain poles of 3rd order Butterworth
    s_poles = [-0.707+0.707j, -0.707-0.707j]

    # create axes
    fig, ax = plt.subplots(2, 1)
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Gain (dB)')
    ax[0].set_ylim(-60, 10)
    ax[0].grid()
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_ylim(-180, 180)
    ax[1].set_yticks([-180,-90,0,90,180])
    ax[1].grid()
    plt.tight_layout()


    # continuous time frequency response
    Gc = 1 / ((s * tau - s_poles[0]) * (s*tau - s_poles[1]))

    # discrete time frequency response
    Gd = 1 / (((2/T) * (z-1)/(z+1) * tau - s_poles[0]) * ((2/T) * (z-1)/(z+1) * tau - s_poles[1]))

    # gain plot
    ax[0].semilogx(freq, np.gain_db(Gc), 'b-', label=r'$G_c(j\omega)$')
    ax[0].semilogx(freq, np.gain_db(Gd), 'r-', label=r'$G_d(e^{j\omega T})$')
    ax[0].legend()

    # phase plot
    ax[1].semilogx(freq, np.phase(Gc), 'b-', label=r'$G_c(j\omega)$')
    ax[1].semilogx(freq, np.phase(Gd), 'r-', label=r'$G_d(e^{j\omega T})$')
    
    plt.show()

if __name__ == '__main__':
    main()