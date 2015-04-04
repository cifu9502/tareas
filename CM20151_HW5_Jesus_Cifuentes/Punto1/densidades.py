from __future__ import division 
import numpy as np

#Creo que es un poco mas facil entender el codigo en el archivo de ipython que se encuentra en la misma carpeta.


#He conseguido crear un algoritmo lo suficientemente eficiente como para obtener una matriz de densidades de 150**3 en poco
#tiempo(menos de un minuto). Intentar crear una matriz de 1000**3 como se dice en el taller no tiene mucho sentido teniendo en cuenta el hecho
#de que python no permite tal alocacion de memoria en un array de numpy. Por lo que nos conformaremos con 150. 

m =1

#Se lee el archivo
s = 'Serena-Venus.txt'
infile = open(s, 'r')
text = infile.readlines()
#Numero de partes en las que se divide cada lado
part = 150
#ro sera la matriz con las densidades
ro = np.zeros((part, part,part))

#En p1 se guardaran las columnas necesarias del texto
p1 = np.zeros((3,len(text)))
n = 0
for x in text:
    #parte el texto x segun ' '
    a = x.split(' ')
    p1[0,n] = float(a[1])
    p1[1,n] = float(a[2])
    p1[2,n] = float(a[3])
    n = n+1    

#Se definen los valores de los deltas para cada dimension    
l0 = max(p1[0])-min(p1[0])   
delta0 = l0/part 
    
l1 = max(p1[1])-min(p1[1])   
delta1 = l1/part

l2 = max(p1[2])-min(p1[2])   
delta2 = l2/part 
    



#Se ordena la matriz p de acuerdo a la fila 1

#inputs: points: matriz de 3 columnas; i: numero de la columna+
#return p: la matriz points ordenada segun los datos de la columna i-esima
def ordenar(points,i):
    ord = points[i]
    ord = np.argsort(ord)
    
    p = np.zeros((3,len(points[0])))
    n = 0
    for i in ord:
        p[0,n] = points[0,i]
        p[1,n] = points[1,i]
        p[2,n] = points[2,i]
        n = n+1
    return p

#Con el fin de aumentar la efectividad del algoritmo se crea este metodo. Basicamente se le insertan dos vectores (en 
# general seran p[0] y a[0]). Ya que a[0] contiene la ubicacion en x de los centros de cada casilla, este metodo permite 
#saber que puntos estan fuera del alcance de a[0] y por lo tanto en el momento de encontrar la densidad solo se itera sobre
#los puntos necesarios

#Para que esta funcion tenga sentido es necesario primero haber invocado la funcion ordenar sobre v

#Encuentra los limites de alcance en v para cada vector en A
#inputs v,a, Vectores con v ordenado anteriormente
#return lims lista con los limites de efectividad para cada casilla

def getLims(v,A):
    lims = [0]
    i = 0
    #Hay que evitar el caso en que v = Null
    if len(v)== 0:
        for j in range(0, len(A)):
            lims.append(0)
        lims.append(0)    
    else:
        x = v[0]
        #Par cada casilla (j) vamos tomando uno por uno los elementos de v y vemos hasta donde se pasa del limite de A[j]
        for j in range(0, len(A)):
            while (x <= A[j]) & (i<(len(v)-1)):
                i = i+1 
                x = v[i]
            lims.append(i)
        lims.append(len(v))
    return lims


p = ordenar(p1,0)

#Se da la posicion de los centros de las casillas y se guardan en a
a = np.zeros((3, part))
a[0]= np.linspace(min(p[0])+delta0/2,max(p[0])-delta0/2,part)
a[1]= np.linspace(min(p[1])+delta1/2,max(p[1])-delta1/2,part)
a[2]= np.linspace(min(p[2])+delta2/2,max(p[2])-delta2/2,part)
len(a[0])



#Esta funcion dira si el vector x esta dentro del cubo centrado en 0 y lado delta.
def W(x, delta):
    if (-delta < x) & (x <= 0):
        return 1+x/delta
    elif (delta > x) & (x > 0):
        return 1-x/delta
    else:
        return 0
    

#Dado una celda en la posicion x,y,z da la matriz de densidades
#inputs x,y,z posicion de la celda
#       q , lim numero de celda en el eje dado y limite usado para restringir la sumatoria
#       pk matriz de puntos usada
def giveRo(x,y,z,q,pk,lim):    
    s = 0
    #Se suma sobre todas las particulas representadas por la matriz pk, y  tales que las particulas esten entre los 
    #limites dados que se van a limitar por la funcion getLim
    for i in range(lim[q],lim[q+2]):
        s = s + W(x - pk[0,i], delta0)*W(y - pk[1,i],delta1)*W(z - pk[2,i],delta2)
    return s*m/(delta1*delta2*delta0)    


#Se llena la matriz ro utilizando la fucion give ro. Solo se itera sobre aquellos lugares limitados por la funcion getLims

p = ordenar(p1,0)
lims = getLims(p[0],a[0])


for i in range(0,part):
    #Sobre cada posicion i de las casillas en la coordenada x se crea una nueva matriz que contenga solo aquellos puntos
    #definidos por la funcion getLims. Esta matriz se vuelve a ordenar y se le aplica la funcion getLims sobre a[1] de 
    #manera que ahora obtenemos los limites sobre el eje y para iterar sobre menos numeros
    n = lims[i+2]-lims[i]
    p2 = np.zeros((3,n))
    p2[0] = p[0][lims[i]:lims[i+2]]
    p2[1] = p[1][lims[i]:lims[i+2]]
    p2[2] = p[2][lims[i]:lims[i+2]]
    
    p2 = ordenar(p2,1)
    lims2 = getLims(p2[1],a[1])
    
    for j in range(0,part):
        for k in range(0,part):
           ro[i,j,k] =  giveRo(a[0,i],a[1,j],a[2,k],j,p2,lims2) 


#guarda la matriz de densidades en el archivo densidades.dat. Ya que es una matriz en 3 dimensiones las escribre de tal 
# manera que escribe todas las matrices de dimension 2 cada una con una posicion diferente en x
#inputs fileNeme-- nombre del archivo donde se guarda
#       matix--  matriz a guaradar
#       dim-- dimension de la matriz
def guardar(fileName,matrix,dim):  
    fh = open(fileName, 'w')
    for i in range(0,dim):
        for j in range(0,dim):
            fh.write('\n')
            for k in range(0,dim):
                fh.write(repr(matrix[i,j,k])+',')
                
    fh.close()        


guardar('densidades.dat', ro,part)
