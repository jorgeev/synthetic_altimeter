import xarray as xr
from glob import glob
import numpy as np
import argparse
import os

def process_swot_masks(input_dir, output_file):
    # Get a sorted list of all .nc files in the input directory
    files = sorted(glob(os.path.join(input_dir, '*.nc')))
    nfiles = len(files)
    
    # Raise an error if no .nc files are found
    if nfiles == 0:
        raise ValueError(f"No .nc files found in {input_dir}")

    # Open the first file to get lat and lon coordinates
    ds = xr.open_dataset(files[0])
    lat = ds.lat
    lon = ds.lon
    
    # Initialize an empty 3D array for masks and a list for dates
    mask = np.zeros((nfiles, lat.size, lon.size))
    final_dates = []

    # Process each file
    for ii, file in enumerate(files):
        aux = xr.open_dataset(file)
        # Extract date from filename
        name = os.path.basename(file).split('_')[1]
        YYYY, MM, DD = name[:4], name[4:6], name[6:8]
        print(f"Processing: {YYYY}-{MM}-{DD}")
        date = np.datetime64(f"{YYYY}-{MM}-{DD}")
        # Store mask data and date
        mask[ii] = aux.mask.data
        final_dates.append(date)

    # Create a new dataset with the processed data
    ds = xr.Dataset(data_vars={'mask': (('date', 'lat', 'lon'), mask)}, 
                    coords={'date': final_dates, 'lat': lat, 'lon': lon})

    # Add attributes to the mask variable
    ds['mask'].attrs['description'] = 'SWOT mask for the Gulf of Mexico'
    ds['mask'].attrs['units'] = '1'
    ds['mask'].attrs['long_name'] = 'SWOT mask'
    ds['mask'].attrs['coordinates'] = 'lat lon'
    ds['mask'].attrs['grid_mapping'] = 'crs'
    ds['mask'].attrs['crs'] = 'EPSG:4326'
    ds['mask'].attrs['crs_wkt'] = 'EPSG:4326'
    ds['mask'].attrs['valid_range'] = (0, 1)

    # Add attributes to the latitude variable
    ds['lat'].attrs['units'] = 'degrees_north'
    ds['lat'].attrs['long_name'] = 'Latitude'
    ds['lat'].attrs['standard_name'] = 'latitude'
    ds['lat'].attrs['axis'] = 'Y'
    ds['lat'].attrs['valid_min'] = -90.0
    ds['lat'].attrs['valid_max'] = 90.0
    ds['lat'].attrs['bounds'] = 'lat_bounds'
    ds['lat'].attrs['crs'] = 'EPSG:4326'
    ds['lat'].attrs['crs_wkt'] = 'EPSG:4326'

    # Add attributes to the longitude variable
    ds['lon'].attrs['units'] = 'degrees_east'
    ds['lon'].attrs['long_name'] = 'Longitude'
    ds['lon'].attrs['standard_name'] = 'longitude'
    ds['lon'].attrs['axis'] = 'X'
    ds['lon'].attrs['valid_min'] = -180.0
    ds['lon'].attrs['valid_max'] = 180.0
    ds['lon'].attrs['bounds'] = 'lon_bounds'
    ds['lon'].attrs['crs'] = 'EPSG:4326'
    ds['lon'].attrs['crs_wkt'] = 'EPSG:4326'

    # Add global attributes to the dataset
    ds.attrs['title'] = 'Synthetic SWOT mask for the Gulf of Mexico'
    ds.attrs['institution'] = 'Florida State University, Deparment of Scientific Computing'
    ds.attrs['source'] = 'SWOT Simulator + synthetic SWOT tracks'
    ds.attrs['history'] = 'Created on ' + str(np.datetime64('now', 'D'))
    ds.attrs['Conventions'] = 'CF-1.7'
    ds.attrs['comment'] = 'SWOT mask for the Gulf of Mexico'
    ds.attrs['author'] = 'Jorge Eduardo Velasco Zavala'
    ds.attrs['author_email'] = 'jv24b@fsu.edu'

    # Save the dataset to a netCDF file
    ds.to_netcdf(output_file, format='NETCDF4')
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process SWOT mask files")
    parser.add_argument("input_dir", help="Directory containing input .nc files")
    parser.add_argument("output_file", help="Path for the output .nc file")
    args = parser.parse_args()

    # Call the main processing function
    process_swot_masks(args.input_dir, args.output_file)