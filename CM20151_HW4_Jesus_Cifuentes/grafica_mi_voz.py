from __future__ import division
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
plt.title('Voice Signal')
plt.plot( t,signal)
plt.ylabel('Sound wave')
plt.xlabel('Time(s)')
plt.savefig('mi_voz.png')
