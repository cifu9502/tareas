# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division
import numpy as np
import string


from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy import interpolate

#archivo a leer
s = 'coastal-stns-byVol-updated-oct2007.txt'


#Se lee el archivo
infile = open(s, 'r')
text = infile.readlines()
#En vec se guardaran las lineas del texto en una forma mucho mas leible
vec = []
#flux sera el vector de flujos
flux = []
for x in text:
    #parte el texto x segun ' '
    a = x.split(' ')
    n = 0
    for y in x.split(' '):
        #omite los residuos de la forma ''
        if(y == ''):
            a.pop(n)
            n = n-1
        if((n == 5) & (y != '')& (y != 'Vol(km3/yr)')):
            flux.append(float(y))
        n = n+1
    vec.append(a)    
titulos = vec.pop(0)

#rios contendra los 300 rios con mayor flujo
rios = []
f = []
for i in range(0,300):
    #se encuentra el maximo de los flujos y luego se busca la linea que contenga este flujo
    m = max(flux)
    i = 0
    for v in vec:
        if flux[i] == m:
            f.append(m)
            rios.append(v)
            flux.remove(m)
            vec.remove(v)
            break
        i = i +1

# <codecell>

import csv
#se escribe el csv con los rios encontrados anteriormente. El delimitador sera ','
with open('top_300_rios.csv', 'w' ) as fp:
    arch = csv.writer(fp, delimiter=',')
    for v in rios:
        v = v[:13]
        arch.writerow(v)
        
    

