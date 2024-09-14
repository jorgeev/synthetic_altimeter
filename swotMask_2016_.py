import numpy as np
import xarray as xr
from lib.mask_functions import AltimetryMask, write_netcdf


lat = np.arange(17.5, 33.5, 2/60)
lon = np.arange(-98.4, -73.5, 2/60)
print("lat.shape, lon.shape\n", lat.shape, lon.shape)
LL, NN = np.meshgrid(lon, lat)

output_dir = '/home/jevz/swot_simulator/swot_pool'

dates = np.arange(np.datetime64('2016-01-01'), np.datetime64('2024-12-31'), np.timedelta64(1, 'D'))

for date in dates:
    gen =  AltimetryMask(lat, lon,)
    gulfMask = gen.get_swot(date)
    write_netcdf(date, gulfMask, lon, lat, output_dir)
