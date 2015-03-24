# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from netCDF4 import Dataset
from scipy.interpolate import griddata
import numpy as np
file = 'air.mon.ltm .nc'
fh = Dataset(file, mode='r')
lons = fh.variables['lon'][:]
air = fh.variables['air'][:]
lats = fh.variables['lat'][:]
time = fh.variables['time'][:]
fh.close()

# <codecell>

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


grid_x, grid_y = np.mgrid[-90:90:200j, 0:360:200j]
points = []
values = []
for i in range(0,len(lats)):
    for j in range(0,len(lats)):
        points.append([lats[i],lons[j]])
        values.append(air[0,i,j])
points = np.asarray(points)   
values = np.asarray(values)   

    


# <codecell>


grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
plt.imshow(grid_z0.T, extent=(-90,90,0,360), origin='lower')
plt.title('Nearest')
plt.plot()
plt.show()

# <codecell>


nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
fig = plt.figure()
m = Basemap(projection='kav7',lon_0=0,resolution=None)

#topodat = m.transform_scalar(air[0],lons,lats,nx,ny)
plt.show()

# <codecell>


# <codecell>


