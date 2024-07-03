import numpy as np
import matplotlib.pyplot as plt

def gain_db(h):
    return 20 * np.log10(np.absolute(h))

def main():
    np.gain_db = np.frompyfunc(gain_db, 1, 1)
    
    fc = 1000
    tau = 1/(2*np.pi*fc)

    f = np.logspace(2, 4)
    s = 2*np.pi*1j*f

    p1 = -0.5+0.866j
    p2 = -1
    p3 = -0.5-0.866j

    # normal (series) form
    G1 = 1/((s*tau-p1)*(s*tau-p2)*(s*tau-p3))

    # partial fractions (parallel) form
    #   note that we can't realise this physically as three 'one pole'
    #   responses because the coefficients are complex, however because
    #   poles are either real or in conjugate pairs it's possible as a
    #   combination of first and second order stages.
    r1 = 1/((p1-p2)*(p1-p3))
    r2 = 1/((p2-p1)*(p2-p3))
    r3 = 1/((p3-p1)*(p3-p2))
    G2 = r1/(s*tau-p1) + r2/(s*tau-p2) + r3/(s*tau-p3)

    # plot results
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.semilogx(f, np.gain_db(G1), 'b-', label='series')
    ax.semilogx(f, np.gain_db(G2), 'r.', label='parallel')

    plt.show()


if __name__ == '__main__':
    main()