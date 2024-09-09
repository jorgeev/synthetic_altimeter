import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

file = '/home/jevz/swot_simulator/karin/2000/SWOT_L2_LR_SSH_Expert_001_414_20000115T180733_20000115T185859_DG10_01.nc'
ds = xr.open_dataset(file)
lon = ds.longitude.data
lat = ds.latitude.data
mask = np.ones(lon.shape)

fig, ax = plt.subplots(1, 1, subplot_kw={'projection': ccrs.PlateCarree()}, )
ax.set_extent([-98.4, -73.5, 17.5, 33.5])
ax.pcolormesh(lon, lat, mask, cmap='Greys_r')
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)

plt.savefig('raw_swot.png', dpi=200, bbox_inches='tight')
