from __future__ import division 
import numpy as np

from scipy import meshgrid
import matplotlib.pyplot as plt

part = 150 

#recupera la informacion de la matriz  Matrix guardada en filename
#inputs fileName-- nombre del archivo donde se guarda
#       matix--  matriz a guaradar
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




#Grafica la imagen 


ro = cargar('densidades.dat',part)
F2 = cargar('fuerza.dat',part-2)

#Obtiene minimos y maximos
mini = F2.min()
Max = F2.max()

#Da la posicision en 3D del elemento senalado 
def darPosicion(num):
    for i in range(0,part-2):
        for j in range(0,part-2):
            for k in range(0,part-2):
                if F2[i,j,k] == num:
                    return [i,j,k]
                
mi = darPosicion(mini)           
            
maxi = darPosicion(Max)

print "El punto de minima fuerza es " + repr(mi)
print "El punto de maxima fuerza es " + repr(maxi)


#Proyectamos al plano x-z  para graficar 

F12 = ro[:,0,:]
for k in range(1, part):
    F12 = F12 + ro[:,k,:]



plt.imshow(F12.T, extent=(0,1,0,1), origin='lower')

plt.title('Serena Venus')
plt.ylabel('Y')
plt.xlabel('X')
plt.savefig('serena.png')
plt.show()

plt.show()
