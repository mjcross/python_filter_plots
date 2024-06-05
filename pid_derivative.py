import numpy as np
import matplotlib.pyplot as plt

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def phase(h):
    return np.degrees(np.angle(h))

def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)
    np.phase = np.frompyfunc(phase, 1, 1)

    # 3dB point
    f_3db = 1000
    tau = 1/(2 * np.pi * f_3db)

    N = 1/tau
    Kd = 0.5

    # plot from 1Hz to 100kHz
    freq = np.logspace(1, 5)
    w = 2 * np.pi * freq
    s = 1j * w

    # high pass filter frequency response
    h_hpf = tau / (tau + 1/s)

    h_pid = N * Kd / (1 + N/s)



    # create axes
    fig, ax = plt.subplots(2, 1)
    ax[0].set_title('Frequency Domain')
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Gain (dB)')
    ax[0].grid()
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_ylim(-90, 0)
    ax[1].grid()



    # gain plot
    ax[0].semilogx(
        freq, np.gain_db(h_lpf), 'b-',
        freq, np.gain_db(h_pid), 'r-')

    # phase plot
    ax[1].semilogx(
        freq, np.phase(h_lpf), 'k-',
        freq, np.phase(h_pid), 'k-')
    
    plt.show()

if __name__ == '__main__':
    main()