import pygrib as pg
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

Elon = -110.0
Wlon = -120.0
Slat = 42.0
Nlat = 48.0

nldas_file = 'NLDAS_FORA0125_H.A20100603.0800.002.grb'
#wrf_lat_file = 
#wrf_lon_file = 

# Open the NLDAS grib file 
grbs = pg.open(nldas_file) # Open the file
grb = grbs[10] # Get the 10th variable, which is precipitation

data = grb.values
lat,lon = grb.latlons()

lat1d = lat[:,0]
lon1d = lon[0,:]

id_lat = np.ix_(np.logical_and(lat1d>=Slat,lat1d<=Nlat))
id_lon = np.ix_(np.logical_and(np.abs(lon1d)>=np.abs(Elon),np.abs(lon1d)<=np.abs(Wlon)))

id_lat_beg = np.min(id_lat)
id_lat_end = np.max(id_lat)

id_lon_beg = np.min(id_lon)
id_lon_end = np.max(id_lon)

lat_ss = lat[id_lat_beg:id_lat_end,id_lon_beg:id_lon_end]
lon_ss = lon[id_lat_beg:id_lat_end,id_lon_beg:id_lon_end]
data_ss = data[id_lat_beg:id_lat_end,id_lon_beg:id_lon_end]

# Create nearest neighbor interpolator for NLDAS data
# 1. Concatenate longitude (lon_ss = x) and latitude (lat_ss = y) vectors
lat_ss_1d = lat_ss.flatten()
lon_ss_1d = lon_ss.flatten()
points = np.stack((lon_ss_1d,lat_ss_1d),axis=-1)

# 2. invoke interpolator
fNN = interpolate.NearestNDInterpolator(points, data_ss.flatten())

# 3. Interpolate to lon and lat arrays from WRF

plt.pcolor(lon_ss,lat_ss,data_ss)
#plt.imshow(id_lat_lon)
plt.colorbar()
plt.show()



