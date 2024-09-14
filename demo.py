#from lib.mask_functions import altimetryMask
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from lib.mask_functions import AltimetryMask, write_netcdf

output_dir = '/home/jevz/swot_simulator/swot_pool'

lat = np.arange(17.5, 33.5, 2/60)
lon = np.arange(-98.4, -73.5, 2/60)
LL, NN = np.meshgrid(lon, lat)

date = np.datetime64('2000-01-15')
#date = np.datetime64('2008-01-01')

gen =  AltimetryMask(lat, lon,)
gulfMask = gen.get_swot(date)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.gridlines()
final = ax.pcolormesh(lon, lat, gulfMask, cmap='Greys_r')#, vmin=0, vmax=1)
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(final)
plt.savefig('swot.png', dpi=300,)


'''
individual_masks = gen.gg
for ii, mm in enumerate(individual_masks):
    fig = plt.figure(figsize=(10.24,9.1), dpi=200)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    final = ax.pcolormesh(lon, lat, mm, cmap='Greys_r',)
    ax.coastlines(color='yellow', linewidth=2)
    ax.coastlines(color='k', linewidth=0.8)
    plt.colorbar(final)
    plt.savefig(F'swot_{ii}.png', dpi=300,)
    fig.clf()
    ax.cla()
    plt.close()
'''
