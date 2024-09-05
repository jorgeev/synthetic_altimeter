import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

file = '/home/jevz/swot_simulator/karin/2008/SWOT_L2_LR_SSH_Expert_001_011_20080101T083428_20080101T092554_DG10_01.nc'
ds =  xr.open_dataset(file)

lon_sw = ds['longitude'].data.copy()
lon_nadir = ds['longitude_nadir'].data.copy()
lat_sw = ds['latitude'].data.copy()
lat_nadir = ds['latitude_nadir'].data.copy()
zz = lon_sw.copy()
print(lon_sw.shape[0], lon_nadir.shape[0])
assert lon_sw.shape[0] == lon_nadir.shape[0]
assert lat_sw.shape[0] == lat_nadir.shape[0]

def find_nearest_index(lon, nadir):
    central_index = []
    for ii, idx in enumerate(nadir):
        central_index.append(np.abs(lon[ii, : ] - idx).argmin())
    
    return central_index


middle_line = find_nearest_index(zz, lon_nadir)

padding = 5
zz[:,:] = 1
for ii, idx in enumerate(middle_line):
    zz[ii, idx-padding:idx+padding] = 0

fig = plt.figure(figsize=(10.24,9.1), dpi=200)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
final = ax.pcolormesh(lon_sw, lat_sw, zz, cmap='Greys', vmin=0, vmax=1)
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(final)
plt.show()



