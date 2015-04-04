#Este archivo realizara la antitransformada de fourier del potencial y la guardara en phi.dat

from __future__ import division 
import numpy as np

part = 150

#recupera la informacion de la matriz  Matrix guardada en filename
#inputs fileName-- nombre del archivo donde se guarda
#       dim-- dimension de la matriz

def cargar(fileName,dim):
    infile = open(fileName, 'r')
    
    #load the full text by lines
    text = infile.readlines()
    
    ro1 = np.zeros((dim, dim,dim))
    num = 1
    for i in range(0,dim):
        for j in range(0,dim):
             g = text[num].split(',')
             g = np.array(g[:-1])
             ro1[i,j,:]= g.astype(np.float)
             num = num+1
    return ro1            


#guarda la matriz de densidades ro en el archivo densidades.dat. Ya que es una matriz de 150*150*150 las escribre de tal 
# manera que escribe 150 matrices de dimension 2 cada una con una posicion diferente en x

#inputs fileName-- nombre del archivo donde se guarda
#       matrix--  matriz a guaradar
#       dim-- dimension de la matriz

def guardar(fileName,matrix,dim):  
    fh = open(fileName, 'w')
    for i in range(0,dim):
        for j in range(0,dim):
            fh.write('\n')
            for k in range(0,dim):
                fh.write(repr(matrix[i,j,k])+',')
                
    fh.close()



#se carga ro 
ro = cargar('densidades.dat', part)

#Se hace la antitrasformada de fourier de las densidades para obtener phi
phi = np.fft.ifftn(-ro)
phi = abs(phi)

#Se guarda en phi.dat la matriz phi
guardar('phi.dat', phi,part)
