#from lib.mask_functions import altimetryMask
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from glob import glob
import scipy as cp

lat = np.linspace(17.5, 33.5, 1000)
lon = np.linspace(-98.4, -73.5, 1000)
#grid_x, grid_y = np.mgrid[lon, lat]
LL, NN = np.meshgrid(lon, lat)

ff =  glob('/home/jevz/swot_simulator/karin/2024/*.nc')

ds = xr.open_dataset(ff[0])
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-98.4,-73.5, 17.5, 33.5])
ax.gridlines(label=True)
ds['cross_track_distance'].plot.pcolormesh(x='longitude', y='latitude', ax=ax, add_colorbar=False, add_labels=False, cmap='PuBu')
ax.coastlines()
plt.show()

ds2 = xr.open_dataset(ff[0])
latswot = ds2.latitude.data.reshape(-1)
lonswot = ds2.longitude.data.reshape(-1)-360
z =  np.ones(latswot.shape[0]).reshape(-1)

mm = cp.interpolate.griddata((lonswot, latswot), z, (LL, NN), fill_value=0)
mm[mm!=0]=1

ax = plt.axes(projection=ccrs.PlateCarree())
mymask = ax.pcolormesh(lon, lat, mm.astype(int), cmap='Greys_r')
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(mymask)
plt.show()