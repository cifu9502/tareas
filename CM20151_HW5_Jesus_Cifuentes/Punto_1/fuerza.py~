#Este archivo va a sacar el gradiente de phi para encontrar la fuerza en cada
#punto y luego halla la magnitud de esa fuerza

from __future__ import division 
import numpy as np

part = 150
l0 = 2.7146499999999989
l1 = 2.7276200000000017
l2 = 3.4131200000000064

#Se definen los valores de los deltas para cada dimension     
delta0 = l0/part  
delta1 = l1/part  
delta2 = l2/part 


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



#se carga phi
phi = cargar('phi.dat', part)

# Derivamos parcialmente en phi para obtener la matriz de fuerza en cada cordenada. Utilizamos la formula 
#f'(x) = f(x+h)-f(x-h)/2h
Fx = -(phi[2:,1:-1,1:-1]-phi[:-2,1:-1,1:-1])/(2*delta0)
Fy = -(phi[1:-1,2:,1:-1]-phi[1:-1,:-2,1:-1])/(2*delta1)
Fz = -(phi[1:-1,1:-1,2:]-phi[1:-1,1:-1,:-2])/(2*delta2)

#Magnitud  de la fuerza
F2 = (Fx**2+Fy**2 + Fz**2)**(0.5) 

#Guarda la matriz
guardar('fuerza.dat',F2,part-2)
