
all: densidades.dat fuerza.dat phi.dat serena.png

densidades.dat: densidades.py 
	densidades.py

phi.dat: antiFourier.py  densidades.dat
	python antiFourier.py

fuerza.dat:  fuerza.py  phi.dat 
	python fuerza.py

serena.png:  fuerza.dat  densidades.dat graph.py 
	python graph.py
