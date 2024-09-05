import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from lib.mask_functions import find_closest_mean
import xarray as xr

file = '/home/jevz/swot_simulator/karin/2008/SWOT_L2_LR_SSH_Expert_001_011_20080101T083428_20080101T092554_DG10_01.nc'
ds =  xr.open_dataset(file)

lat = ds.latitude.data
lon = ds.longitude.data
zz = lon.copy()
padding = 5
razor = find_closest_mean(zz)
print(razor)
zz[:,:] = 1
for ii, idx in enumerate(razor):
    zz[ii, idx-padding:idx+padding] = np.nan

fig = plt.figure(figsize=(10.24,9.1), dpi=200)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
final = ax.pcolormesh(lon, lat, zz, cmap='Greys', vmin=0, vmax=1)
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(final)
plt.show()
