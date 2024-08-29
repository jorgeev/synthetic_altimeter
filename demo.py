#from lib.mask_functions import altimetryMask
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from lib.mask_functions import AltimetryMask

#lat = np.linspace(17.5, 33.5, 1000)
lat = np.linspace(17.5, 50.5, 1000)
lon = np.linspace(-98.4, -73.5, 1000)
LL, NN = np.meshgrid(lon, lat)
date = np.datetime64('2024-09-01')

gen =  AltimetryMask(lat, lon)
gulfMask = gen.get_swot(date)

ax = plt.axes(projection=ccrs.PlateCarree())
#ax.set_extent
ax.gridlines()
final = ax.pcolormesh(lon, lat, gulfMask, cmap='Greys_r')#, vmin=0, vmax=1)
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(final)
plt.show()

individual_masks = gen.gg

for mm in individual_masks:
    fig = plt.figure(figsize=(10.24,9.1), dpi=200)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    final = ax.pcolormesh(lon, lat, mm, cmap='Greys_r', vmin=0, vmax=1)
    ax.coastlines(color='yellow', linewidth=2)
    ax.coastlines(color='k', linewidth=0.8)
    plt.colorbar(final)
    plt.show()
    fig.clf()
    ax.cla()
    plt.close()
