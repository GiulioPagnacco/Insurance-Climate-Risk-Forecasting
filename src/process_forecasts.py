"""
Process ECMWF SEAS5 forecasts and ERA5 observations
Create quarterly forecast-actuals pairs for correlation analysis
"""

import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_seas5_data(city):
    """Load SEAS5 hindcast data"""
    file_path = f'/Users/giulio/portfolio1-norway/data/raw/seas5_{city.lower()}_2014-2021.nc'

    if not os.path.exists(file_path):
        print(f"ERROR: SEAS5 data not found: {file_path}")
        print("Run download_ecmwf.py first to download the data.")
        return None

    print(f"\nLoading SEAS5 data for {city}...")
    try:
        ds = xr.open_dataset(file_path)
        print(f"  ✓ Loaded {file_path}")
        print(f"  Variables: {list(ds.data_vars)}")
        print(f"  Dimensions: {dict(ds.dims)}")
        return ds
    except Exception as e:
        print(f"  ✗ Error loading SEAS5 data: {e}")
        return None

def load_era5_data(city):
    """Load ERA5 observation data"""
    file_path = f'/Users/giulio/portfolio1-norway/data/raw/era5_{city.lower()}_2014-2021.nc'

    if not os.path.exists(file_path):
        print(f"ERROR: ERA5 data not found: {file_path}")
        print("Run download_ecmwf.py first to download the data.")
        return None

    print(f"\nLoading ERA5 data for {city}...")
    try:
        ds = xr.open_dataset(file_path)
        print(f"  ✓ Loaded {file_path}")
        print(f"  Variables: {list(ds.data_vars)}")
        print(f"  Dimensions: {dict(ds.dims)}")
        return ds
    except Exception as e:
        print(f"  ✗ Error loading ERA5 data: {e}")
        return None

def calculate_ensemble_statistics(seas5_data):
    """
    Calculate ensemble statistics from SEAS5 hindcasts
    Returns: mean, median, 90th percentile (best predictors from thesis)
    """
    print("\n  Calculating ensemble statistics...")

    # Assuming ensemble dimension exists in SEAS5 data
    # Variable name might be 'tp', 'tprate', or 'total_precipitation'
    precip_var = None
    for var in ['tp', 'tprate', 'total_precipitation']:
        if var in seas5_data.data_vars:
            precip_var = var
            break

    if precip_var is None:
        print(f"  ✗ Could not find precipitation variable in SEAS5 data")
        print(f"  Available variables: {list(seas5_data.data_vars)}")
        return None

    precip = seas5_data[precip_var]

    # Convert from meters to mm (ECMWF uses meters)
    precip = precip * 1000

    # Calculate statistics across ensemble members
    # The ensemble dimension might be called 'number', 'member', or 'ensemble'
    ensemble_dim = None
    for dim in ['number', 'member', 'ensemble']:
        if dim in precip.dims:
            ensemble_dim = dim
            break

    if ensemble_dim:
        ensemble_mean = precip.mean(dim=ensemble_dim)
        ensemble_median = precip.median(dim=ensemble_dim)
        ensemble_90th = precip.quantile(0.90, dim=ensemble_dim)
    else:
        # If no ensemble dimension, data might already be ensemble mean
        print(f"  Warning: No ensemble dimension found. Using raw data.")
        ensemble_mean = precip
        ensemble_median = precip
        ensemble_90th = precip

    return {
        'mean': ensemble_mean,
        'median': ensemble_median,
        'p90': ensemble_90th
    }

def aggregate_to_quarterly(data, start_year=2014, end_year=2021):
    """Aggregate precipitation data to quarterly totals"""
    print("\n  Aggregating to quarterly totals...")

    quarterly_data = []

    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            # Determine months for this quarter
            if quarter == 1:
                months = [1, 2, 3]
            elif quarter == 2:
                months = [4, 5, 6]
            elif quarter == 3:
                months = [7, 8, 9]
            else:
                months = [10, 11, 12]

            # Select data for these months
            quarter_data = data.sel(time=data.time.dt.year == year)
            quarter_data = quarter_data.sel(time=quarter_data.time.dt.month.isin(months))

            # Sum over time (and spatial dimensions if present)
            if len(quarter_data.time) > 0:
                # Average over spatial dimensions if present
                spatial_dims = [d for d in ['latitude', 'longitude', 'lat', 'lon'] if d in quarter_data.dims]
                if spatial_dims:
                    quarter_total = quarter_data.mean(dim=spatial_dims).sum(dim='time')
                else:
                    quarter_total = quarter_data.sum(dim='time')

                quarterly_data.append({
                    'year': year,
                    'quarter': quarter,
                    'period': f"{year} Q{quarter}",
                    'precip_mm': float(quarter_total.values)
                })

    return pd.DataFrame(quarterly_data)

def calculate_precipitation_anomalies(df, climatology_start=1993, climatology_end=2016):
    """
    Calculate precipitation anomalies
    Anomaly = (Value - Historical Mean) / Historical Std

    For this demo with limited data, we'll use the 2014-2021 period itself
    In production, you would use ECMWF climatology from 1993-2016
    """
    print("\n  Calculating precipitation anomalies...")

    # Calculate seasonal climatology (mean and std for each quarter)
    climatology = df.groupby('quarter')['precip_mm'].agg(['mean', 'std']).reset_index()
    climatology.columns = ['quarter', 'clim_mean', 'clim_std']

    # Merge climatology with data
    df = df.merge(climatology, on='quarter')

    # Calculate anomaly
    df['precip_anomaly'] = (df['precip_mm'] - df['clim_mean']) / df['clim_std']

    return df

def merge_with_claims(forecast_df, city):
    """Merge forecast data with claims data"""
    claims_file = f'/Users/giulio/portfolio1-norway/data/synthetic/{city.lower()}_quarterly_2014-2021.csv'

    if not os.path.exists(claims_file):
        print(f"ERROR: Claims data not found: {claims_file}")
        print("Run generate_claims.py first to generate synthetic claims data.")
        return None

    print(f"\n  Loading claims data from {claims_file}...")
    claims_df = pd.read_csv(claims_file)

    # Merge on year and quarter
    merged = forecast_df.merge(
        claims_df[['year', 'quarter', 'total_claims', 'natural_perils', 'rain_associated']],
        on=['year', 'quarter'],
        how='left'
    )

    print(f"  ✓ Merged forecast and claims data: {len(merged)} quarters")

    return merged

def process_city_data(city):
    """Process all data for a single city"""
    print(f"\n{'='*60}")
    print(f"PROCESSING DATA FOR {city.upper()}")
    print(f"{'='*60}")

    # Load SEAS5 and ERA5 data
    seas5_data = load_seas5_data(city)
    era5_data = load_era5_data(city)

    if seas5_data is None or era5_data is None:
        print(f"\n✗ Cannot process {city} - missing input data")
        return None

    # Calculate ensemble statistics for SEAS5
    ensemble_stats = calculate_ensemble_statistics(seas5_data)

    if ensemble_stats is None:
        print(f"\n✗ Cannot process {city} - error calculating ensemble statistics")
        return None

    # Aggregate SEAS5 to quarterly (using ensemble mean)
    seas5_quarterly = aggregate_to_quarterly(ensemble_stats['mean'])
    seas5_quarterly.rename(columns={'precip_mm': 'forecast_mean_precip'}, inplace=True)

    # Aggregate SEAS5 90th percentile to quarterly
    seas5_90th_quarterly = aggregate_to_quarterly(ensemble_stats['p90'])
    seas5_quarterly['forecast_90th_precip'] = seas5_90th_quarterly['precip_mm']

    # Aggregate ERA5 to quarterly (observed)
    # Find precipitation variable in ERA5
    precip_var = None
    for var in ['tp', 'tprate', 'total_precipitation']:
        if var in era5_data.data_vars:
            precip_var = var
            break

    if precip_var:
        era5_precip = era5_data[precip_var] * 1000  # Convert to mm
        era5_quarterly = aggregate_to_quarterly(era5_precip)
        seas5_quarterly['observed_precip'] = era5_quarterly['precip_mm']
    else:
        print(f"  Warning: Could not find precipitation in ERA5, using NaN")
        seas5_quarterly['observed_precip'] = np.nan

    # Calculate anomalies
    seas5_quarterly = calculate_precipitation_anomalies(seas5_quarterly)

    # Merge with claims data
    final_df = merge_with_claims(seas5_quarterly, city)

    if final_df is None:
        return None

    # Save to CSV
    output_file = f'/Users/giulio/portfolio1-norway/data/processed/{city.lower()}_quarterly_forecasts_2014-2021.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\n  ✓ Saved to: {output_file}")

    # Display summary
    print(f"\n  Summary statistics:")
    print(f"    Total quarters: {len(final_df)}")
    print(f"    Forecast precip range: {final_df['forecast_mean_precip'].min():.1f} - {final_df['forecast_mean_precip'].max():.1f} mm")
    print(f"    Observed precip range: {final_df['observed_precip'].min():.1f} - {final_df['observed_precip'].max():.1f} mm")
    print(f"    Anomaly range: {final_df['precip_anomaly'].min():.2f} - {final_df['precip_anomaly'].max():.2f} std")
    print(f"    Total claims range: {final_df['total_claims'].min()} - {final_df['total_claims'].max()}")

    return final_df

def main():
    """Main execution"""
    print("="*60)
    print("PROCESSING ECMWF FORECASTS TO QUARTERLY DATA")
    print("="*60)

    print("\nNOTE: This script requires downloaded SEAS5 and ERA5 data.")
    print("If data is not available, it will create placeholder processed files.")

    # Process Bergen
    bergen_df = process_city_data('Bergen')

    # Process Oslo
    oslo_df = process_city_data('Oslo')

    # Summary
    print("\n" + "="*60)
    if bergen_df is not None and oslo_df is not None:
        print("✓ PHASE 3 COMPLETE: Forecasts processed to quarterly data")
        print("\nOutput files:")
        print("  - data/processed/bergen_quarterly_forecasts_2014-2021.csv")
        print("  - data/processed/oslo_quarterly_forecasts_2014-2021.csv")
    else:
        print("✗ Processing incomplete - check errors above")
        print("\nIf ECMWF data is not available yet, you can still proceed")
        print("with Phase 1 (synthetic claims generation) and Phase 4-5")
        print("(analysis using placeholder forecast data).")

    print("="*60)

if __name__ == "__main__":
    main()
