from __future__ import division 
import numpy as np

from scipy import meshgrid
import matplotlib.pyplot as plt

part = 250 

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

#Se fijan los valores minimos y maximos en x,y y z de la posicion, estos se obtienen de los valores minimos y maximos en cada vector p[0] 
#p[1], p[2] definido en el archivo de ipython
minx = 33.85371
maxx = 36.568359999999998
miny = 33.923020000000001
maxy = 36.650640000000003
minz = 33.495959999999997
maxz = 36.909080000000003

#Se dan los deltas en cada eje
l0 = maxx-minx   
delta0 = l0/part     
l1 = maxy-miny   
delta1 = l1/part
l2 = maxz-minz   
delta2 = l2/part 
 

#Se da la posicion de los centros de las casillas y se guardan en a
a = np.zeros((3, part))
a[0]= np.linspace(minx+delta0/2,maxx-delta0/2,part)
a[1]= np.linspace(miny+delta1/2,maxy-delta1/2,part)
a[2]= np.linspace(minz+delta2/2,maxz-delta2/2,part)




#Da la posicision en 3D del elemento con valor num en la matriz F2 de fuerzas
def darPosicion(num):
#Se obtiene la posicion de num
    m1 = np.where(F2==num)
    Min = []
#Se convierte la posicion a nuestras coordenadas
    Min.append( m1[0]*delta0 + a[0][1])
    Min.append( m1[1]*delta1 + a[1][1])
    Min.append( m1[2]*delta2 + a[2][1])
    return (map(float, Min))       
            
                     
mi = darPosicion(mini)           
maxi = darPosicion(Max)

print "El punto de minima fuerza es " + repr(mi)
print "El punto de maxima fuerza es " + repr(maxi)


#Proyectamos al plano x-z  para graficar (Esto es, sumamos sobre cada punto en el plano x-z las fuerzas para cada posicion en y)
F12 = F2[:,0,:]
for k in range(1, part-2):
    F12 = F12 + F2[:,k,:]

#Da la posicision en 3D del elemento con valor num en la matriz F12 de fuerzas proyectadas al plano x-z
def darPosicion2(num):
#Se obtiene la posicion de num
    m1 = np.where(F12==num)
    Min = []
#Se convierte la posicion a nuestras coordenadas
    Min.append( m1[0]*delta0 + a[0][1])
    Min.append( m1[1]*delta2 + a[2][1])
    return (map(float, Min)) 


mini = F12.min()
Max = F12.max()

#Se encuentra la posicion de los puntos de minima y maxima fuerza en el plano x-z utilizando la funcion darPosicion2
mi2 = darPosicion2(mini)           
maxi2 = darPosicion2(Max) 

print "Cuando proyectamos al plano x-z el punto de minima fuerza es " + repr(mi2)
print "Y el punto de maxima fuerza es " + repr(maxi2)   

#Se encuentra la posicion de los puntos de minima y maxima fuerza en el plano x-z utilizando la funcion darPosicion2
mi2 = darPosicion2(mini)           
maxi2 = darPosicion2(Max)   


#Se anaden fig y axs 
fig, axs = plt.subplots(1,1)

#Se grafican los puntos de minima y maxima fuerza
axs.plot([mi2[0]], [mi2[1]], 'ro')
axs.text(mi2[0],mi2[1],'Minimo')
axs.plot([maxi2[0]], [maxi2[1]], 'ro')
axs.text(maxi2[0],maxi2[1],'Maximo')

#Debido a la forma de la funcion contourf es necesario trasponer la matriz
F12 = F12.transpose()
#Se define el numero de niveles que va a tener el contorno. Para nuestro caso elegimos 15
levels = np.linspace(mini, Max, 15)

#Se hace el mapeo por el contorno dado
cs = axs.contourf(a[0][1:-1], a[2][1:-1], F12, levels=levels)
#Se anade barra de color
fig.colorbar(cs, ax=axs, format="%.3g")

#Se grafica la matriz F12 de fuerzas proyectadas al plano x-z. Note que el resultado es muy parecido a la imagen dada, fue por eso que se escogio este plano
#Se esta extendiendo entre los valores  minimos y maximos en x y en z en el archivo de ipython que  correponden justamente a los valores minimos y maximos de la posicion

plt.imshow(F12.T, extent=(minx, maxx,minz,maxz), origin='lower')
plt.title('Fuerzas en Serena Venus (plano x-z)')
plt.ylabel('Z')
plt.xlabel('X')
plt.savefig('serena.png')
plt.show()
