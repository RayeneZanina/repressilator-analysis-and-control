import numpy as np
import matplotlib.pyplot as plt

def time_series(t, X, p_eq = None):

    plt.plot(t, X[:, 0], label = 'P1')
    plt.plot(t, X[:, 1], label = 'P2')
    plt.plot(t, X[:, 2], label = 'P3')

    if p_eq is not None:
        plt.plot(t, p_eq, label = 'Equilibrium', alpha = 0.6)

    plt.xlabel('Time steps')
    plt.ylabel('Protein Concentration')

    plt.legend()
    plt.grid()
    plt.title('Time Series')

    plt.show()

def phase_portrait(X):

    plt.figure(figsize = (30, 10))

    plt.subplot(1, 3, 1)
    plt.plot(X[:, 0], X[:, 1])
    plt.xlabel('P1')
    plt.ylabel('P2')
    plt.title('Phase Portrait')
    plt.grid()

    plt.subplot(1, 3, 2)
    plt.plot(X[:, 1], X[:, 2])
    plt.xlabel('P2')
    plt.ylabel('P3')
    plt.title('Phase Portrait')
    plt.grid()

    plt.subplot(1, 3, 3)
    plt.plot(X[:, 0], X[:, 2])
    plt.xlabel('P1')
    plt.ylabel('P3')
    plt.title('Phase Portrait')
    plt.grid()

    plt.show()

def phase_portrait_3d(X):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(X[:, 0], X[:, 1], X[:, 2])
    ax.set_xlabel('P1')
    ax.set_ylabel('P2')
    ax.set_zlabel('P3')
    ax.set_title('3 Dimensional Phase Portrait')

    plt.show()

def control_signal(t, u):

    plt.plot(t, u)
    
    plt.xlabel('Time steps')
    plt.ylabel('Control Signal')

    plt.grid()
    plt.title('Control Signal')

    plt.show()

def regime_indicator(t, r):

    plt.plot(t, r)

    plt.xlabel('Time steps')
    plt.ylabel('Regime Indicator')

    plt.grid()
    plt.title('Regime Indicator')

    plt.show()

def fft_plot(freqs, spectrum):

    plt.plot(freqs, spectrum)

    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')

    plt.grid()
    plt.title('Fast Fourier Transform Frequency spectrum')

    plt.show()

def target_oscillation_plot(target_values, dom_freqs, amps):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)
    ax.plot(target_values, dom_freqs, color = 'blue', label = 'Dominant Frequency')
    plt.legend(bbox_to_anchor = (0.8, 1))
    ax.set_xlabel("Target Regime")
    ax.set_ylabel("Dominant Frequency")
    ax.grid()
    ax2 = ax.twinx()
    ax2.plot(target_values, amps, color = 'red', label = 'Oscillation Amplitude')
    plt.legend(loc = 'upper right', bbox_to_anchor = (0.8, 0.94))
    ax2.set_ylabel("Oscillation Amplitude")
    ax.set_title("Target Regime vs Dominant Frequency and Oscillation Amplitude")
    plt.show()

def hopf_comparison(model, states, u_values):
    gamma = model.gamma

    real_num = []
    real_theoretical = []
    for i in range(len(u_values)):
        state = states[i, :]
        u = u_values[i]

        eigs = model.eigenvalues(state, u)

        real_num.append(np.real(eigs[np.argmax(np.imag(eigs))]))

        beta = model.beta(u)
        real_theoretical.append(-gamma + beta / 2)
    
    real_num = np.array(real_num)
    real_theoretical = np.array(real_theoretical)

    plt.plot(real_num, label = 'Numerical real part')
    plt.plot(real_theoretical, label = 'Analytical real part', alpha=0.5)
    plt.xlabel('Time step')
    plt.ylabel('Real part')
    plt.legend()
    plt.grid()
    plt.title('Analytical vs numerical eigenvalue real part')

