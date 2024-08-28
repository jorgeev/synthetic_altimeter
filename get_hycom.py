#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 08:46:08 2024

@author: jevz
"""

from glob import glob
import numpy as np
import xarray as xr

experiment = "http://tds.hycom.org/thredds/dodsC/GOMu0.04/expt_50.1/data/netcdf/1993"

ds = xr.open_dataset(experiment, decode_times=False)['surf_el']
print(ds['time'])
print(ds['lon'])
ds.close()