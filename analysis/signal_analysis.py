import numpy as np
from scipy.fft import fft, fftfreq

def oscillation_amp(signal):
    return np.max(signal) - np.min(signal)


def oscillation_freq(signal, dt ):

    yf = np.abs(fft(signal))
    xf = fftfreq(len(signal), dt)

    mask = (xf > 0)
    xf = xf[mask]
    yf = yf[mask]

    return xf[np.argmax(yf)], xf, yf