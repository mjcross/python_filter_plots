import numpy as np
import matplotlib.pyplot as plt


"""
Bode plot of the IFT controller function from the "Application to a DC-Servo
with backlash" [1].

Ref: H. Hjalmarsson, M. Gevers, S. Gunnarsson and O. Lequin, "Iterative feedback 
tuning: theory and applications," in IEEE Control Systems Magazine, vol. 18, 
no. 4, pp. 26-41, Aug. 1998, doi: 10.1109/37.710876.
"""

def main():
    fs = 25                         # their sampling frequency is 25Hz
    T = 1 / fs

    w = np.logspace(0, 2, 128)      # NB: their Bode plot (Fig. 12) is in rad/sec 
    z = np.exp(1j * w * T)
    
    # "the controller has the structure C = p1 + p2 q^-1 + p3 q^-2 + p4 q^-4 
    #  followed by an integrator"
    z_1 = 1/z
    z_2 = 1/(z*z)
    z_3 = 1/(z*z*z)
    C0 = (4.89 - 7.28*z_1 + 2.66*z_2 + 1.96*z_3) / (1 - z_1)

    # Bode plot
    fig = plt.figure('Bode plot of Controller')
    ax = fig.subplots(2, 1)

    # gain
    ax[0].grid(which='both')
    ax[0].set_ylabel('Amplitude')
    ax[0].loglog(w, np.absolute(C0), 'b-')

    # phase
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_xlabel('Frequency (rad/s)')
    ax[1].grid(which='both')    
    ax[1].semilogx(w, np.degrees(np.unwrap(np.angle(C0))), 'b-')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()