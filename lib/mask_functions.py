import xarray as xr
import numpy as np
from scipy.interpolate import griddata
from glob import glob
from os.path import join

class AltimetryMask:
    """
    A class to handle the generation of an altimetry mask using SWOT data.

    Attributes:
        lat (np.ndarray): Latitude grid.
        lon (np.ndarray): Longitude grid.
        path (str): Path to the directory containing SWOT data files.
    """

    def __init__(self, lat, lon, path: str = '/home/jevz/swot_simulator/karin/'):
        """
        Initializes the AltimetryMask class with latitude, longitude, and data path.

        Args:
            lat (np.ndarray): Array of latitude values.
            lon (np.ndarray): Array of longitude values.
            path (str): Directory path where SWOT data files are stored.
        """
        self.lat = lat
        self.lon = lon
        self.path = path

    def select_files(self, date):
        """
        Selects SWOT files based on the given date.

        Args:
            date (np.datetime64): Date for which files are to be selected.

        Returns:
            list: Sorted list of file paths matching the date.
        """
        # Extract year, month, and day from the date
        YYYY = date.astype('datetime64[Y]').astype(object).year
        MM = date.astype(object).month
        DD = date.astype('datetime64[D]').astype(object).day

        # Create the file path pattern to search for files
        fpath = join(self.path, f'{YYYY}',
                     f'SWOT_L2_LR_SSH_Expert_???_*_{YYYY}{MM:02d}{DD:02d}T*_*T*_DG10_01.nc')

        # Return sorted list of file paths
        return sorted(glob(fpath))

    def read_files(self, date_files):
        """
        Reads the selected files and generates the mask.

        Args:
            date_files (list): List of SWOT data file paths.

        Returns:
            np.ndarray: Mask generated from the data files.
        """
        # Create meshgrid of latitude and longitude
        Lonm, Latm = np.meshgrid(self.lon, self.lat)

        # Initialize the mask with zeros
        mask = np.zeros(Lonm.shape)

        # Check if any files were found
        if date_files:
            self.gg = []
            for file in date_files:
                print(f'Reading file: {file}')
                
                # Open the dataset
                ds = xr.open_dataset(file)
                
                self.middle = int(ds.latitude.shape[1]/2)
                # Extract and process latitude and longitude from the dataset
                scan_lat = ds.latitude.data.reshape(-1)
                scan_lon = ds.longitude.data.reshape(-1)
                scan_lon[scan_lon > 180] -= 360  # Convert longitudes to [-180, 180]

                # Interpolate and add the data to the mask
                mm = self.interp_data(scan_lon, scan_lat, Lonm, Latm)
                self.gg.append(mm)
                #mask += self.interp_data(scan_lon, scan_lat, Lonm, Latm)
                mask += mm

        return mask

    def interp_data(self, scan_lon, scan_lat, Lonm, Latm):
        """
        Interpolates SWOT scan data onto the grid.

        Args:
            scan_lon (np.ndarray): Flattened array of scan longitudes.
            scan_lat (np.ndarray): Flattened array of scan latitudes.
            Lonm (np.ndarray): Meshgrid of longitudes.
            Latm (np.ndarray): Meshgrid of latitudes.

        Returns:
            np.ndarray: Interpolated data.
        """
        zz = np.ones(scan_lon.shape)
        error = self.middle
        zz[:, error-5:error+5 ] = np.nan
        mask = griddata((scan_lon, scan_lat), zz, (Lonm, Latm), fill_value=0)
        return mask

    def get_swot(self, date):
        """
        Generates the SWOT mask for the given date.

        Args:
            date (np.datetime64): Date for which the SWOT mask is to be generated.

        Returns:
            np.ndarray: SWOT mask for the specified date.
        """
        date_files = self.select_files(date)
        print('Reading files...')
        final_mask = self.read_files(date_files)
        final_mask[final_mask != 0] = 1
        print('Done')
        return final_mask.astype(int)

    def get_track(self, date):
        """
        Placeholder for method to get the track data (currently not implemented).
        
        Args:
            date (np.datetime64): Date for which the track is to be retrieved.
        """
        pass

def parse_names(path, date):
    """
    Parses and retrieves the SWOT data file names based on the provided path and date.

    Args:
        path (str): Directory path where SWOT data files are stored.
        date (np.datetime64): Date for which files are to be selected.

    Returns:
        list: Sorted list of file paths matching the date.
    """
    YYYY = date.astype('datetime64[Y]').astype(object).year
    MM = date.astype(object).month
    DD = date.astype('datetime64[D]').astype(object).day

    fpath = join(path, f'_{YYYY}',
                 f'SWOT_L2_LR_SSH_Expert_001_*_{YYYY}{MM:02d}{DD:02d}T*_*T*_DG10_01.nc')

    return sorted(glob(fpath))

