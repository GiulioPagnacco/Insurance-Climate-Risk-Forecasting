"""
Download ECMWF SEAS5 seasonal forecasts and ERA5 observations
For Norwegian climate insurance forecasting project
"""

import cdsapi
import os
from datetime import datetime

# Geographic coordinates (9km x 9km areas)
BERGEN_COORDS = {
    'north': 60.5,
    'south': 60.3,
    'east': 5.5,
    'west': 5.1
}

OSLO_COORDS = {
    'north': 60.0,
    'south': 59.8,
    'east': 10.9,
    'west': 10.6
}

def check_credentials():
    """Check if CDS API credentials exist"""
    cdsapirc = os.path.expanduser('~/.cdsapirc')
    if not os.path.exists(cdsapirc):
        print("ERROR: CDS API credentials not found!")
        print("Please create ~/.cdsapirc with your credentials:")
        print("url: https://cds.climate.copernicus.eu/api/v2")
        print("key: {UID}:{API_KEY}")
        print("\nGet your credentials at: https://cds.climate.copernicus.eu/user")
        return False
    return True

def download_seas5_hindcasts(city, coords, output_dir):
    """
    Download SEAS5 seasonal hindcasts (retrospective forecasts)

    Parameters:
    - Quarterly initialization: Jan 1, Apr 1, Jul 1, Oct 1
    - Years: 2014-2021 (8 years × 4 quarters = 32 forecasts)
    - Lead time: 1-3 months ahead
    - All 51 ensemble members
    - Variable: Total precipitation
    """
    c = cdsapi.Client()

    print(f"\n{'='*60}")
    print(f"Downloading SEAS5 hindcasts for {city.upper()}")
    print(f"{'='*60}")

    # Quarterly initialization months
    quarters = {
        'Q1': '01',  # January initialization
        'Q2': '04',  # April initialization
        'Q3': '07',  # July initialization
        'Q4': '10'   # October initialization
    }

    years = [str(y) for y in range(2014, 2022)]

    output_file = f"{output_dir}/seas5_{city.lower()}_2014-2021.nc"

    # Check if file already exists
    if os.path.exists(output_file):
        print(f"✓ File already exists: {output_file}")
        print("  Skipping download. Delete file to re-download.")
        return output_file

    print(f"\nDownloading to: {output_file}")
    print("This may take 30-60 minutes...")
    print("Dataset: seasonal-monthly-single-levels (SEAS5)")

    try:
        c.retrieve(
            'seasonal-monthly-single-levels',
            {
                'format': 'netcdf',
                'originating_centre': 'ecmwf',
                'system': '5',  # SEAS5
                'variable': 'total_precipitation',
                'year': years,
                'month': list(quarters.values()),
                'leadtime_month': ['1', '2', '3'],  # 3-month lead time
                'area': [
                    coords['north'],
                    coords['west'],
                    coords['south'],
                    coords['east']
                ],
            },
            output_file
        )
        print(f"✓ Successfully downloaded: {output_file}")
        return output_file

    except Exception as e:
        print(f"✗ Error downloading SEAS5 data: {e}")
        print("\nTroubleshooting:")
        print("1. Check CDS credentials in ~/.cdsapirc")
        print("2. Verify you have accepted SEAS5 terms: https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-monthly-single-levels")
        print("3. Check CDS system status: https://cds.climate.copernicus.eu/live/status")
        return None

def download_era5_observations(city, coords, output_dir):
    """
    Download ERA5 observed precipitation for validation

    Parameters:
    - Daily data aggregated to monthly
    - Years: 2014-2021
    - Variable: Total precipitation
    """
    c = cdsapi.Client()

    print(f"\n{'='*60}")
    print(f"Downloading ERA5 observations for {city.upper()}")
    print(f"{'='*60}")

    output_file = f"{output_dir}/era5_{city.lower()}_2014-2021.nc"

    # Check if file already exists
    if os.path.exists(output_file):
        print(f"✓ File already exists: {output_file}")
        print("  Skipping download. Delete file to re-download.")
        return output_file

    print(f"\nDownloading to: {output_file}")
    print("This may take 10-20 minutes...")
    print("Dataset: reanalysis-era5-single-levels-monthly-means")

    years = [str(y) for y in range(2014, 2022)]
    months = [f"{m:02d}" for m in range(1, 13)]

    try:
        c.retrieve(
            'reanalysis-era5-single-levels-monthly-means',
            {
                'format': 'netcdf',
                'product_type': 'monthly_averaged_reanalysis',
                'variable': 'total_precipitation',
                'year': years,
                'month': months,
                'time': '00:00',
                'area': [
                    coords['north'],
                    coords['west'],
                    coords['south'],
                    coords['east']
                ],
            },
            output_file
        )
        print(f"✓ Successfully downloaded: {output_file}")
        return output_file

    except Exception as e:
        print(f"✗ Error downloading ERA5 data: {e}")
        print("\nTroubleshooting:")
        print("1. Check CDS credentials in ~/.cdsapirc")
        print("2. Verify you have accepted ERA5 terms: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means")
        print("3. Check CDS system status: https://cds.climate.copernicus.eu/live/status")
        return None

def download_all():
    """Download all required datasets"""
    output_dir = '/Users/giulio/portfolio1-norway/data/raw'

    # Check credentials first
    if not check_credentials():
        return False

    print("\n" + "="*60)
    print("ECMWF DATA DOWNLOAD")
    print("Portfolio 1: Norway Historical Insurance Claims")
    print("="*60)

    print("\nDatasets to download:")
    print("1. SEAS5 seasonal hindcasts (Bergen)")
    print("2. SEAS5 seasonal hindcasts (Oslo)")
    print("3. ERA5 observations (Bergen)")
    print("4. ERA5 observations (Oslo)")
    print("\nEstimated total download time: 1-2 hours")
    print("Estimated total size: ~1.5 GB")

    response = input("\nProceed with download? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Download cancelled.")
        return False

    # Download SEAS5 for Bergen
    seas5_bergen = download_seas5_hindcasts('bergen', BERGEN_COORDS, output_dir)

    # Download SEAS5 for Oslo
    seas5_oslo = download_seas5_hindcasts('oslo', OSLO_COORDS, output_dir)

    # Download ERA5 for Bergen
    era5_bergen = download_era5_observations('bergen', BERGEN_COORDS, output_dir)

    # Download ERA5 for Oslo
    era5_oslo = download_era5_observations('oslo', OSLO_COORDS, output_dir)

    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)

    success = all([seas5_bergen, seas5_oslo, era5_bergen, era5_oslo])

    if success:
        print("\n✓ All datasets downloaded successfully!")
        print("\nFiles created:")
        print(f"  - {seas5_bergen}")
        print(f"  - {seas5_oslo}")
        print(f"  - {era5_bergen}")
        print(f"  - {era5_oslo}")
        print("\n✓ PHASE 2 COMPLETE: ECMWF data downloaded")
    else:
        print("\n✗ Some downloads failed. Check errors above.")
        print("\nYou can re-run this script to retry failed downloads.")
        print("Successfully downloaded files will be skipped.")

    print("="*60)
    return success

def main():
    """Main execution"""
    download_all()

if __name__ == "__main__":
    main()
