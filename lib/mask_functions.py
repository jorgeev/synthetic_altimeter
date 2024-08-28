import xarray as xr
import numpy as np
import scipy as cp
from glob import glob
from os.path import join
from datetime import datetime

class altimetryMask():
    def __init__(self, lat, lon):
        self.lat = self.lat
        self.lon = self.lon
        #pass
    
    def getSwot(self, date):
        return 
    
    def getTrack(self, date):
        return
    
    def select_files(self):
        fmaps = np.zeros([self.lat.shape[0], self.lon.shape[0]], dtype=bool)
        
        return dd
    
    def read_files(self, date_files):
        return
        
        for file in date_files:
            ds = xr.open_dataset(file)
            scan_lat = ds.latitude.data.reshape(-1)
            scan_lon = ds.longitude.data.reshape(-1)-360
            mask = self.interp_data(scan_lon, scan_lat)
        return mask
    
    def interp_data(self, scan_lon, scan_lat):
        latx = scan_lat.reshape(-1)
        lonx = scan_lon.reshape(-1)
        zz = np.ones(scan_lat.reshape(-1).shape(-1))
        mask = cp.interpolate.griddata((lonx, latx), zz, (self.lon, self.lat), fill_value=0)
        
        return mask

def parsenames(path, date):
    YYYY =  date.astype('datetime64[Y]').astype(object).year
    MM = date.astype(object).month
    DD = date.astype('datetime64[D]').astype(object).day
    fpath = join(path, f'{YYYY}' , f'SWOT_L2_LR_SSH_Expert_001_*_{YYYY}{MM:02d}{DD:02d}*_DG10_01.nc')
    date_files = sorted(glob(fpath))
    return date_files

