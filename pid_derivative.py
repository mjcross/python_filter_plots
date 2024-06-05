import numpy as np
import matplotlib.pyplot as plt

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def phase(h):
    return np.degrees(np.angle(h))

## From: https://www.scilab.org/discrete-time-pid-controller-implementation
##
## In the discrete approximation to a PID controller the derivative term
## is often approximated by a high-pass filter.
## 
## In the parallel form, the transfer function becomes H(s) = Kp + Ki (1/s) + N Kd / (1 + N / s)
## where `N` is the 3dB point of the high-pass filter in radians/sec.
##
def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)
    np.phase = np.frompyfunc(phase, 1, 1)

    # 3dB point
    f_3db = 1000
    tau = 1/(2 * np.pi * f_3db)

    w_3db = 2 * np.pi * f_3db   # equivalent of the 3db frequency for the HPF
    Kd = 1/w_3db                # this value of Kd gives unity gain at high frequency

    # plot from 1Hz to 100kHz
    freq = np.logspace(1, 5)
    w = 2 * np.pi * freq
    s = 1j * w

    # high pass filter frequency response
    h_hpf = tau / (tau + 1/s)           # conventional high-pass filter
    h_pid = Kd * w_3db / (1 + w_3db/s)  # high-pass transfer function used in the reference



    # create axes
    fig, ax = plt.subplots(2, 1)
    ax[0].set_title('Frequency Domain')
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Gain (dB)')
    ax[0].grid()
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_ylim(0, 90)
    ax[1].grid()



    # gain plot
    ax[0].semilogx(
        freq, np.gain_db(h_hpf), 'b-',
        freq, np.gain_db(h_pid), 'r-')

    # phase plot
    ax[1].semilogx(
        freq, np.phase(h_hpf), 'b-',
        freq, np.phase(h_pid), 'r-')
    
    plt.show()

if __name__ == '__main__':
    main()