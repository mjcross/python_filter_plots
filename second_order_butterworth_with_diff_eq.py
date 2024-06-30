import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial 

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
    freq = np.logspace(2, 4, num=128)
    w = 2 * np.pi * freq
    s = 1j * w              # equivalent of frequency in Laplace domain
    z = np.exp(1j * w * T)  # equivalent of frequency in Z domain

    # Laplace domain poles of 2nd order Butterworth
    s_poles = [
        -0.707+0.707j, 
        -0.707-0.707j
    ]

    # create axes
    fig, ax = plt.subplots(2, 1)
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Gain (dB)')
    ax[0].set_ylim(-60, 10)
    ax[1].set_xlabel('Time (ms)')
    
    # continuous time frequency response
    Gc = 1 / ((s * tau - s_poles[0]) * (s*tau - s_poles[1]))

    # Z domain approximation using bilinear transform
    k = 2/T
    Gd = 1 / ((k * (z-1)/(z+1) * tau - s_poles[0]) * (k * (z-1)/(z+1) * tau - s_poles[1]))

    # expanded to proper rational form
    a = Polynomial([
        (tau*k)**2 - np.sqrt(2)*tau*k + 1,  # a0
        -2*(tau*k)**2 + 2,                  # a1
        (tau*k)**2 + np.sqrt(2)*tau*k + 1   # a2
    ])
    b = Polynomial([
        1,  # b0
        2,  # b1
        1   # b2
    ])  
    Gd2 = b(z) / a(z)

    # time domain gain from difference equation
    gain_list = []
    for f in freq:
        w = 2 * np.pi * f
        x2 = x1 = 0     # initialise previous input samples
        y2 = y1 = 0     # initialise previous output samples

        # sum the square of the output signal over Ns samples
        sum_sq = 0
        Ns = 1000
        for n in range(Ns):
            t = n * T

            # input sample (sine wave)
            x0 = np.sin(w * t)

            # output sample from difference equation 
            y0 = (b.coef[2]*x0 + b.coef[1]*x1 + b.coef[0]*x2 - a.coef[1]*y1 - a.coef[0]*y2) / a.coef[2]
            sum_sq += y0**2

            # update previous samples
            x2 = x1
            x1 = x0
            y2 = y1
            y1 = y0

        # calculate gain from output power
        rms = np.sqrt(sum_sq / Ns)
        gain_list.append(rms * np.sqrt(2))

    gt = np.array(gain_list)

    # step response
    x2 = x1 = 0     # initialise previous input samples
    y2 = y1 = 0     # initialise previous output samples

    t_list = []
    step_resp_list = []
    Ns = 50
    for n in range(Ns):
        t = n * T

        # input sample (unit step)
        x0 = 1

        # output sample from difference equation        
        y0 = (b.coef[2]*x0 + b.coef[1]*x1 + b.coef[0]*x2 - a.coef[1]*y1 - a.coef[0]*y2) / a.coef[2]
        t_list.append(t)
        step_resp_list.append(y0)

        # update previous samples
        x2 = x1
        x1 = x0
        y2 = y1
        y1 = y0

    t = np.array(t_list)
    step_resp = np.array(step_resp_list)

    # plot gains versus frequency
    ax[0].semilogx(freq, np.gain_db(Gc), 'b-', label=r'CT response')
    ax[0].semilogx(freq, np.gain_db(Gd), 'r-', label=r'DT bilinear transform')
    #ax.semilogx(freq, np.gain_db(Gd2), 'k--', label=r'DT proper rational')
    ax[0].semilogx(freq, np.gain_db(gt), 'g-', label=r'DT difference eq')
    ax[0].legend()

    # plot step response
    ax[1].plot(1000*t, step_resp, 'g-', label='step response')
    ax[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()