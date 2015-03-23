#Este programa realiza la transformada de fourier de mi voz y la grafica en mi_voz_fft.png

#ya que estoy usando python2 necesito importar division 
from __future__ import division

from scipy.fftpack import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import wave
import sys

#se leen los datos de nombre.wav  y se guardan en signal. Vamos a omitir los datos en fecuencias no audibles ( Menores a 20 Hz)
spf = wave.open('nombre.wav','r')
#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
# Obtiene el framerate
fs = spf.getframerate()

#Convierte tiempo a segundos
t = np.linspace(0, len(signal)/fs, num=len(signal))

#realiza la transf de fourier
n = len(signal)
signalf = fft(signal)/n
absf = np.abs(signalf)
n = len(signal)
freq = fftfreq(n, (1/fs)) # Recuperamos las frecuencias

#Se anulan los datos en frecuencias menores a 20 Hz
absf[np.abs(freq) < 20] = 0

#Se obtiene el maximo de frecuencia positivo 
a = freq[(absf ==  max(absf)) & (freq > 0)] 
print("El armonico fundamental es: %f\n"% a)

#grafica
plt.plot(freq, absf)
plt.title('Voice Fourier Transform')
plt.ylabel('Sound Wave')
plt.xlabel('Frequency(hz)')
plt.savefig('mi_voz_fft.png')
