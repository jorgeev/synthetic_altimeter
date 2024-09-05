#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:02:18 2024

@author: jevz
"""

#from lib.mask_functions import altimetryMask
import numpy as np
import xarray as xr

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

target = '~/swot_simulator/karin/2000/SWOT_L2_LR_SSH_Expert_002_220_20000129T163148_20000129T172314_DG10_01.nc'
ds = xr.open_dataset(target)
ds

latitude = ds.latitude.data
longitude = ds.longitude.data

ssh = ds.longitude.data

fig = plt.figure(figsize=(10.24,9.1), dpi=200)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
final = ax.pcolormesh(longitude, latitude, longitude, cmap='Greys_r')#, vmin=0, vmax=1)
ax.coastlines(color='yellow', linewidth=2)
ax.coastlines(color='k', linewidth=0.8)
plt.colorbar(final)
plt.show()
