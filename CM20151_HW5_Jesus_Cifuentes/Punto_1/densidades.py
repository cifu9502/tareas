from __future__ import division 
import numpy as np

#Creo que es un poco mas facil entender el codigo en el archivo de ipython que se encuentra en la misma carpeta.
#Debido a que vamos a escribir matrices tamano de 250**3 para poder pasar la informacion entre cada uno de los archivos del makefile quizas el proceso podria tardar demasido(cerca de 3 min y medio para todo el makefile), en este caso simplemente seria mejor cambiar en cada archivo part =250 por un numero mas pequeno como 150. Es un requisito
#que en todos los archivos el atributo part sea el mismo

#He conseguido crear un algoritmo lo suficientemente eficiente como para obtener una matriz de densidades de 250**3 en poco
#tiempo. Intentar crear una matriz de 1000**3 como se dice en el taller no tiene mucho sentido teniendo en cuenta el hecho
#de que python no permite tal alocacion de memoria. De hecho tambien hay que tener en cuenta que realizar la antitransformada de 
#fourier para mas valores no seria posible para un computador por lo que 250 es un limite aceptable
m =1
s = 'Serena-Venus.txt'
infile = open(s, 'r')
text = infile.readlines()
#Numero de partes en las que se divide cada lado
part = 250
#ro sera la matriz con las densidades
ro = np.zeros((part, part,part))

#En p se guardaran las columnas necesarias del texto
p1 = np.zeros((3,len(text)))
n = 0
for x in text:
    #parte el texto x segun ' '
    a = x.split(' ')
    p1[0,n] = float(a[1])
    p1[1,n] = float(a[2])
    p1[2,n] = float(a[3])
    n = n+1    
    
#p1[0] = np.fft.ifft(p1[0])    
#p1[1] = np.fft.ifft(p1[1])    
#p1[2] = np.fft.ifft(p1[2])    
#p1 = abs(p1)
    
    
#Se definen los valores de los deltas para cada dimension    
l0 = max(p1[0])-min(p1[0])   
delta0 = l0/part 
    
l1 = max(p1[1])-min(p1[1])   
delta1 = l1/part

l2 = max(p1[2])-min(p1[2])   
delta2 = l2/part 
#Se da la posicion de los centros de las casillas y se guardan en a
a = np.zeros((3, part))
a[0]= np.linspace(min(p1[0])+delta0/2,max(p1[0])-delta0/2,part)
a[1]= np.linspace(min(p1[1])+delta1/2,max(p1[1])-delta1/2,part)
a[2]= np.linspace(min(p1[2])+delta2/2,max(p1[2])-delta2/2,part)


#Esta funcion dira si el vector x esta dentro del cubo centrado en 0 y lado delta.
def W(x, delta):
    if (-delta < x) & (x <= 0):
        return 1+x/delta
    elif (delta > x) & (x > 0):
        return 1-x/delta
    else:
        return 0
    



#Se llena la matriz ro utilizando la funcion give ro, iterando sobre cada punto en la matriz p1 y anadiendo su contribucion
#a la densididad de los puntos cercanos a p0 unicamente

#Sera la matriz de densidades
ro = np.zeros((part, part,part))
t0 = a[0]
t1 = a[1]
t2 = a[2]
for i in range(0,len(p1[0])):
    #Se encuentran los limites inferiores en cada eje para los puntos en la matriz p1 de manera que podamos localizar las
    #matrices cercanas inferiores
    xa = t0[t0<p1[0,i]]
    ya = t1[t1<p1[1,i]]
    za = t2[t2<p1[2,i]]
    #La casilla dada por i1,i2,i3 sera la casilla con coordenadas inferiores en cada eje a p1[i], mas cercana a este. 
    #Dependiendo de donde se encuentre el punto p hay que tener en cuenta ciertas exepciones razon del los elif a continuacion
    if len(xa) == 0:
        i1 = 0
        j1 = 1
    elif len(xa) == len(t0):
        i1 = t0.tolist().index(max(xa))
        j1 = i1+1
    else:     
        i1 = t0.tolist().index(max(xa))
        j1 = i1+2
        
        
    if len(ya) == 0:
        i2 = 0
        j2 = 1
    elif len(ya) == len(t1):
        i2 = t1.tolist().index(max(ya))
        j2 = i2+1    
    else:     
        i2 = t1.tolist().index(max(ya))
        j2 = i2+2
        
        
    if len(za) == 0:
        i3 = 0
        j3 = 1
    elif len(za) == len(t2):
        i3 = t2.tolist().index(max(za))
        j3 = i3+1    
    else:     
        i3 = t2.tolist().index(max(za))
        j3 = i3+2
        
    k2=i2
    k3=i3
    #Se itera sobre las casillas mas cercanas al punto p, normalmente son 8 casillas las que son cercanas a un punto, pero
    #puede haber ciertas excepciones si entra en alguno de los casos restringidos anteriormente
    while(i1 < j1):
        i2=k2
        while(i2 < j2):
            i3 = k3
            while(i3 < j3):
                #Para cada una de estas casillas se anade la contribucion segun esta dado en la funcion de densidad
                ro[i1,i2,i3] = ro[i1,i2,i3] + (W(a[0,i1] - p1[0,i], delta0)*W(a[1,i2]  - p1[1,i],delta1)*W(a[2,i3]- p1[2,i],delta2))*m/(delta1*delta2*delta0)
                i3 = i3 +1
            i2 = i2 +1
        i1 = i1 +1    

#se transforma de fourier la densidad
ro2 = np.fft.fftn(ro)


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
