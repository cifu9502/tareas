#Este programa grafica mi voz en mi_voz.png

#ya que estoy usando python2 necesito importar division 

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import wave
import sys

#se leen los datos de nombre.wav  y se guardan en signal
spf = wave.open('nombre.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
# Obtiene el framerate
fs = spf.getframerate()

#Convierte tiempo a segundos usando el framerate
t = np.linspace(0, len(signal)/fs, num=len(signal))
# Obtiene el framerate
plt.title('Voice Signal')
plt.plot( t,signal)
plt.ylabel('Sound wave')
plt.xlabel('Time(s)')
plt.savefig('mi_voz.png')
