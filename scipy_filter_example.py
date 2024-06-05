from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html#scipy.signal.lfilter
def main():
    # create a noisy signal
    rng = np.random.default_rng()
    t = np.linspace(-1, 1, 201)
    x = (np.sin(2*np.pi*0.75*t*(1-t) + 2.1) +
        0.1*np.sin(2*np.pi*1.25*t + 1) +
        0.18*np.cos(2*np.pi*3.85*t))
    xn = x + rng.standard_normal(len(t)) * 0.08

    # create a 3rd order Butterworth LPF
    b, a = signal.butter(3, 0.05)

    # apply the filter to the signal (with appropriate initial conditions)
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

    # apply the filter again, to get 6th order for comparison with signal.filtfilt()
    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

    # apply the filter forwards then backwards to get zero phase shift (at 6th order)
    y = signal.filtfilt(b, a, xn)

    # plot results
    fig, ax = plt.subplots(1, 1)
    ax.plot(t, xn, 'b', alpha=0.75)
    ax.plot(
        t, z, 'r--',
        t, z2, 'r', 
        t, y, 'k')
    ax.legend(('noisy signal', 'lfilter, once', 'lfilter, twice',
            'filtfilt'), loc='best')
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    main()