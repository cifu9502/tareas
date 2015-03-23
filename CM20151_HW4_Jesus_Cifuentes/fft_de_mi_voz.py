from __future__ import division
from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import wave
import sys


spf = wave.open('nombre.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()


t = np.linspace(0, len(signal)/fs, num=len(signal))

n = len(signal)
signalf = fft(signal)/n
absf = np.abs(signalf)
n = len(signal)
freq = fftfreq(n, (1/fs)) # Recuperamos las frecuencias

absf[np.abs(freq) < 20] = 0
 
a = freq[(absf ==  max(absf)) & (freq > 0)] 
print("El armonico fundamental es: %f\n"% a)

plt.plot(freq, absf)
plt.title('Voice Fourier Transform')
plt.ylabel('Sound Wave')
plt.xlabel('Frequency(hz)')
plt.savefig('mi_voz_fft.png')
