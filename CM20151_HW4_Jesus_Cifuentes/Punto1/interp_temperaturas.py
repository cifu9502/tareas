# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# Este codigo lee el archivo temperaturas.csv creado en el punto anterior y hace la interpolación acordada
#ya que estamos usando python 2 es necesario importar division
from __future__ import division
import numpy as np
import string

from matplotlib import pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num
from scipy.interpolate import UnivariateSpline
from scipy import interpolate


s = 'temperaturas.csv'

#constante de camio en fecha, sera util mas tarde
k = (2015-1968)/(735630.0-718401.0)

#Se lee el archivo
infile = open(s, 'r')
text = infile.readlines()

#para una ciudad asignada se obtienen los datos de tal ciudad para hacer la interpolacion
def getData(ciudad):
    total = []
    a = []
    b = []
    for x in text:
        c = x.split(',')
        if(c[4] == ciudad):
#Se obtiene la fecha como un float de acuerdo al formato del csv
            t = datetime.strptime(c[3], "%Y-%m-%d")
            n = date2num(t)
            a.append((n-718401.0)*k +1968)
            b.append(float(c[5].split('\n')[0]))
    total.append(a) # Date
    total.append(b) # Temperature       
    return total   
             
        

# Se hace intepolacion  polinomial lineal y por splines grado 5 para cada ciudad. La interpolacion polinomial lineal se uso debido a que las interpolaciones cuadraticas y cubicas daban resultados muy alejados de la grafica, sin embargo esta imporlacion no resulta muy confiable debido al numero de datos. (Note que el problema principal para nuestra interpolacion es que tenemos datos  mensuales desde 1968 hasta 2015, se pudo haber utilizado la media anual, pero decidí no hacerlo debido a que no era especificado en el taller). Mientras tanto la aproximación por splines es mucho mas agradable, si bien no oscila tan fuerte como la aproximación lineal, describe muy bien el comportamiento en conjunto del sistema por lo que se cree que es la mas apropiada. 

a =getData('"Bogota"')
t = np.linspace(a[0][0],a[0][-1], 200)
spl = UnivariateSpline(a[0], a[1], k = 5)
f = interpolate.interp1d(a[0], a[1])

plt.figure(1)
plt.subplot(511)
plt.title('Temperature Interpolation')
plt.ylabel('Bogota (T) ')
plt.plot(a[0],a[1], 'r.', t, spl(t) ,'b', t, f(t) ,'y')



a =getData('"Cali"')
t = np.linspace(a[0][0],a[0][-1], 200)
spl = UnivariateSpline(a[0], a[1], k = 5)
f = interpolate.interp1d(a[0], a[1])

plt.subplot(512)
plt.ylabel('Cali')
plt.plot(a[0],a[1], 'r.', t, spl(t) ,'b', t, f(t) ,'y')



a =getData('"Barranquilla"')
t = np.linspace(a[0][0],a[0][-1], 200)
spl = UnivariateSpline(a[0], a[1], k = 5)
f = interpolate.interp1d(a[0], a[1])

plt.subplot(513)
plt.ylabel('Barranquilla (T) ')
plt.plot(a[0],a[1], 'r.', t, spl(t) ,'b', t, f(t) ,'y')


a =getData('"Bucaramanga"')
t = np.linspace(a[0][0],a[0][-1], 200)
spl = UnivariateSpline(a[0], a[1], k = 5)
f = interpolate.interp1d(a[0], a[1])

plt.subplot(514)
plt.ylabel('Bucaramanga (T) ')
plt.plot(a[0],a[1], 'r.', t, spl(t) ,'b', t, f(t) ,'y')



a =getData('"Ipiales"')
t = np.linspace(a[0][0],a[0][-1], 200)
spl = UnivariateSpline(a[0], a[1], k = 5)
f = interpolate.interp1d(a[0], a[1])

plt.subplot(515)
plt.ylabel('Ipiales (T) ')
plt.plot(a[0],a[1], 'r.', t, spl(t) ,'b', t, f(t) ,'y')
plt.xlabel('Date')


plt.savefig('temperature_interpolation.png')



plt.show()

