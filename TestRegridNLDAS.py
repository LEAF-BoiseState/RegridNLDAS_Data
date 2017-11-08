import pygrib as pg
import numpy as np
from scipy import interpolate
from netCDF4 import Dataset
import matplotlib.pyplot as plt

##

# S
NLDAS_res = 0.125

# NLDAS file name
nldas_file = 'NLDAS_FORA0125_H.A20100603.0800.002.grb'

wrf_lat_file = 'xlat_d02.nc'
wrf_lon_file = 'xlong_d02.nc'

nc_wrf_lat_fid = Dataset(wrf_lat_file, 'r')
nc_wrf_lon_fid = Dataset(wrf_lon_file, 'r')

wrf_lats = nc_wrf_lat_fid.variables['XLAT'][0,:,:]
wrf_lons = nc_wrf_lon_fid.variables['XLONG'][0,:,:]

Sbnd = np.floor(wrf_lats.min()) + 2.0*NLDAS_res
Nbnd = np.ceil(wrf_lats.max()) + 2.0*NLDAS_res
Wbnd = np.floor(wrf_lons.min()) + 2.0*NLDAS_res
Ebnd = np.ceil(wrf_lons.max()) + 2.0*NLDAS_res

# Open the NLDAS grib file 
grbs = pg.open(nldas_file) # Open the file
grb = grbs[10] # Get the 10th variable, which is precipitation

data = grb.values
lat,lon = grb.latlons()

lat1d = lat[:,0]
lon1d = lon[0,:]

id_lat = np.ix_(np.logical_and(lat1d>=Sbnd,lat1d<=Nbnd))
id_lon = np.ix_(np.logical_and(np.abs(lon1d)>=np.abs(Ebnd),np.abs(lon1d)<=np.abs(Wbnd)))

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
NLDAS_wrfgrd = fNN(wrf_lons,wrf_lats)

plt.figure(1)
plt.subplot(211)
plt.pcolor(lon_ss,lat_ss,data_ss)
#plt.imshow(id_lat_lon)
plt.colorbar()

plt.subplot(212)
plt.pcolor(wrf_lons,wrf_lats,NLDAS_wrfgrd)
plt.colorbar()
plt.show()



