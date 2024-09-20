import numpy as np
import xarray as xr
from lib.mask_functions import AltimetryMask, write_netcdf
from multiprocessing import Pool, cpu_count

lat = np.arange(17.5, 33.5, 2/60)
lon = np.arange(-98.4, -73.5, 2/60)
print("lat.shape, lon.shape\n", lat.shape, lon.shape)
LL, NN = np.meshgrid(lon, lat)

output_dir = '/home/jevz/swot_simulator/swot_pool'

dates = np.arange(np.datetime64('2016-01-01'), np.datetime64('2024-12-31'), np.timedelta64(1, 'D'))

def process_date(date):
    gen = AltimetryMask(lat, lon)
    gulfMask = gen.get_swot(date)
    write_netcdf(date, gulfMask, lon, lat, output_dir)

# Use all available CPU cores
# num_processes = cpu_count()

# Optionally, you could set a maximum number of processes
print("Number of cores: ", cpu_count())
num_processes = min(cpu_count(), 26)  # Example: Use up to 16 cores

# Create a pool of worker processes
with Pool(num_processes) as pool:
    # Map the process_date function to all dates
    pool.map(process_date, dates)
