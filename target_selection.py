#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:32:57 2024

@author: jevz
"""

from lib.mask_functions import parse_names
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

path = '/home/jevz/swot_simulator/karin/'
date = np.datetime64("2024-09-01")
targets = parse_names(path, date)
print(targets)


for file in targets:
    ds2 = xr.open_dataset(file)
    latswot = ds2.latitude.data
    lonswot = ds2.longitude.data
    lonswot[lonswot > 180] -= 360.
    zz = ds2.simulated_error_karin.data
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    #ax.set_extent([-98.4,-73.5, 17.5, 33.5])
    ax.gridlines()
    final = ax.pcolormesh(lonswot, latswot, zz, cmap='Greys_r')
    ax.coastlines()
    plt.colorbar(final)
    plt.show()
    ax.cla()




