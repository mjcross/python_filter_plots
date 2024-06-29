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
    f_max = 5000
    tau = 1/(2 * np.pi * f_3db)

    # plot from 1Hz to 100kHz
    freq = np.linspace(0, f_max, num=512)
    w = 2 * np.pi * freq
    s = 1j * w

    # low pass filter frequency response
    h_lpf = 1 / (1 + s * tau)

    # partial derivative of h_lpf with respect to tau
    h_deriv = -s / (1 + s * tau) ** 2


    # check dh/d_tau at the 3dB point
    dTau = tau * 0.0000001
    s = 1j * 2 * np.pi * f_3db
    dH = np.absolute(1/(1+s*tau)) - np.absolute(1/(1+s*(tau+dTau)))
    print('derivative at f_3db is approx', dH/dTau)

    dhh = 1/(1+s*tau) - 1/(1+s*(tau+dTau))
    print(np.absolute(dhh/dTau))


    # create axes
    fig, ax1 = plt.subplots()
    blue = 'tab:blue'
    ax1.set_title(r'$f_c = 1000$')
    ax1.set_ylabel('magnitude', color=blue)
    ax1.tick_params(axis='y', labelcolor=blue)
    ax1.set_ylim(0, 1)
    ax1.set_xlim(0, f_max)
    ax1.grid(axis='x')

    ax2 = ax1.twinx()
    ax1.set_xlabel('frequency')

    red = 'tab:red'
    ax2.set_ylabel(r'magnitude', color=red)
    ax2.tick_params(axis='y', labelcolor=red)
    ax2.set_ylim(0, 3500)

    # gain plot
    ax1.plot(freq, np.absolute(h_lpf), 'b-', label=r'$\frac{1}{1+s\tau}$')
    ax2.plot(freq, np.absolute(h_deriv), 'r-', label=r'$\frac{\partial}{\partial\tau}\left(\frac{1}{1+s\tau}\right)$')
    ax1.legend(loc=3)
    ax2.legend(loc=4)


    fig.tight_layout()    
    plt.show()

if __name__ == '__main__':
    main()