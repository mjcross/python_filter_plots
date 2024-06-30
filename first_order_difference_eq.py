import numpy as np
import matplotlib.pyplot as plt
import math

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)

    # 3dB point of filter
    f_c = 1000
    w_c = 2 * np.pi * f_c
    tau = 1 / w_c

    # discrete time sampling frequency
    f_s = 20000
    T = 1 / f_s
    k = 2 / T

    # sweep frequency from 100Hz - 10KHz
    freq = np.logspace(2, 4, num=128)

    gain_list = []
    for f in freq:

        # measure gain at frequency
        w = 2 * math.pi * f

        xn1 = 0
        yn1 = 0
        sum_sq = 0

        # generate 1000 samples at each freq
        Ns = 1000
        for n in range(0, Ns):
            t = n * T

            # time domain input signal sample 'n'
            xn = math.sin(w * t)

            # time domain output signal sample 'n'
            yn = (xn + xn1 - (1 - tau * k) * yn1) / (tau * k + 1)

            # signals delayed by one sample
            xn1 = xn
            yn1 = yn

            # accumulate sum of output amplitude squared
            sum_sq += yn ** 2

        # calculate RMS output and convert to sinewave amplitude
        rms = math.sqrt(sum_sq / Ns)
        gain_list.append(rms * math.sqrt(2))

    # plot gain
    gain = np.array(gain_list)

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Frequency Domain')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.set_ylim(-60, 10)
    ax.grid()

    ax.semilogx(freq, np.gain_db(gain), 'b-')
    plt.show()


if __name__ == '__main__':
    main()