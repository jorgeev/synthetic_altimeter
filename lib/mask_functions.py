import xarray as xr
import numpy as np
from scipy.interpolate import griddata
import scipy as cp
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
                
                # Swot_like mask
                zz = ds.longitude.data.copy()
                lon_nadir = ds.longitude_nadir.data.copy()

                middle_line = self.find_nearest_index(zz, lon_nadir)
                padding = 1
                zz[:,:] = 1
                for ii, idx in enumerate(middle_line):
                    zz[ii, idx-padding:idx+padding] = 0
                
                # Extract and process latitude and longitude from the dataset
                scan_lat = ds.latitude.data
                scan_lon = ds.longitude.data
                ref_lon = scan_lon.copy()
                zz, scan_lon, scan_lat = mask_borders(zz, scan_lon, scan_lat)
                print('Lon data range')
                print(np.max(scan_lon))
                print(np.min(scan_lon))
                scan_lon[scan_lon > 180] -= 360  # Convert longitudes to [-180, 180]
                ref_lon [ref_lon > 180] -= 360   # Convert longitudes to [-180, 180]

                # Interpolate and add the data to the mask
                #mm = self.interp_data(scan_lon.reshape(-1), scan_lat.reshape(-1), Lonm, Latm, zz.reshape(-1))
                mm = self.interp_data(scan_lon, scan_lat, Lonm, Latm, zz.reshape(-1))
                print('')
                print(np.nanmax(mm))
                print(np.nanmin(mm))
                self.gg.append(mm)
                #mm[mm != 0] = 1
                #mask += self.interp_data(scan_lon, scan_lat, Lonm, Latm)
                mask += mm

        return mask

    def interp_data(self, scan_lon, scan_lat, Lonm, Latm, zz):
        """
        Interpolates SWOT scan data onto the grid.

        Args:
            scan_lon (np.ndarray): Flattened array of scan longitudes.
            scan_lat (np.ndarray): Flattened array of scan latitudes.
            Lonm (np.ndarray): Meshgrid of longitudes.
            Latm (np.ndarray): Meshgrid of latitudes.
            zz (np.ndarray)): lattened array of masking data
        Returns:
            np.ndarray: Interpolated data.
        """
        
        mask = griddata((scan_lon, scan_lat), zz, (Lonm, Latm), fill_value=0, method='linear')
        return mask
    
    def interp_data_method2(self, scan_lon, scan_lat, Lonm, Latm, zz):
        """
        Interpolates SWOT scan data onto the grid.

        Args:
            scan_lon (np.ndarray): Flattened array of scan longitudes.
            scan_lat (np.ndarray): Flattened array of scan latitudes.
            Lonm (np.ndarray): Meshgrid of longitudes.
            Latm (np.ndarray): Meshgrid of latitudes.
            zz (np.ndarray)): lattened array of masking data
        Returns:
            np.ndarray: Interpolated data.
        """
        points = np.vstack((scan_lon, scan_lat)).T
        tree = cp.spatial.KDTree(points)
        new_points = np.vstack((Lonm.flatten(), Latm.flatten())).T
        _, idx = tree.query(new_points)
        mask = zz[idx].reshape(Lonm.shape)

        return mask
    
    def find_closest_mean(self, A):
        closest_indices = []
        
        for row in A:
            mean_value = np.mean(row)  # Calculate the mean of the row
            # Find the index of the value closest to the mean
            closest_index = np.abs(row - mean_value).argmin()
            closest_indices.append(closest_index)
        
        return closest_indices
    
    def find_nearest_index(self, lon, nadir):
        central_index = []
        for ii, idx in enumerate(nadir):
            central_index.append(np.abs(lon[ii, : ] - idx).argmin())    
        return central_index

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



def mask_borders(data, lon, lat):
    l = data.shape
    lateral = np.nanmax((lon[:,1:] - lon[:,:-1]), axis=1)

    print(F'First lon, lat: {lon[0,0]},{lat[0,0]}')
    print(F'Last lon, lat: {lon[-1,0]},{lat[-1,0]}')

    lon2 = np.zeros([l[0], l[1]+4])
    lon2[:, 2:-2] = lon
    if lat[0, 0] > lat[-1, 0]:
        lon2[:, 0] = lon2[:, 2] + 1.5 * np.absolute(lateral)
        lon2[:, 1] = lon2[:, 2] + np.absolute(lateral)
        lon2[:, -1] = lon2[:, -3] - np.absolute(lateral)
        lon2[:, -2] = lon2[:, -3] - 1.5* np.absolute(lateral)
    else:
        lon2[:, 0] = lon2[:, 2] - 1.5 * np.absolute(lateral)
        lon2[:, 1] = lon2[:, 2] - np.absolute(lateral)
        lon2[:, -1] = lon2[:, -3] + np.absolute(lateral)
        lon2[:, -2] = lon2[:, -3] + 1.5 * np.absolute(lateral)


    lat2 = np.zeros([l[0], l[1]+4])
    lat2[:, 2:-2] = lat
    lat2[:, 0] = lat2[:, 2]
    lat2[:, 1] = lat2[:, 2]
    lat2[:, -1] = lat2[:, -3]
    lat2[:, -2] = lat2[:, -3]

    data2 = np.zeros([l[0], l[1]+4])
    data2[:, 2:-2] = data
    return data2.reshape(-1), lon2.reshape(-1), lat2.reshape(-1)
