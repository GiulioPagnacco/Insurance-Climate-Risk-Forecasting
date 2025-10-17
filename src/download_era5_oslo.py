"""
Download ERA5 Precipitation for Oslo Area (2014-2021)
Uses monthly data for faster download
"""

import cdsapi
import xarray as xr
import pandas as pd
import numpy as np

# Oslo coordinates (9km x 9km grid per thesis)
oslo_area = {
    'north': 60.0,
    'south': 59.8,
    'east': 10.9,
    'west': 10.6
}

print("="*60)
print("DOWNLOADING ERA5 FOR OSLO (2014-2021)")
print("Monthly precipitation data")
print("="*60)

# Initialize CDS API
c = cdsapi.Client()

output_file = 'data/raw/era5_oslo_monthly_2014-2021.nc'

print(f"\nDownloading to: {output_file}")
print("This may take 10-20 minutes...")

try:
    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': 'total_precipitation',
            'year': [str(y) for y in range(2014, 2022)],
            'month': [f'{m:02d}' for m in range(1, 13)],
            'time': '00:00',
            'area': [
                oslo_area['north'],
                oslo_area['west'],
                oslo_area['south'],
                oslo_area['east']
            ],
            'format': 'netcdf'
        },
        output_file
    )
    print(f"\n✅ Downloaded: {output_file}")

except Exception as e:
    print(f"\n✗ Error downloading ERA5: {e}")
    print("\nTroubleshooting:")
    print("1. Check CDS credentials in ~/.cdsapirc")
    print("2. Accept ERA5 terms at: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means")
    exit(1)

# Process to quarterly aggregates
print("\n" + "="*60)
print("PROCESSING TO QUARTERLY AGGREGATES")
print("="*60)

# Load NetCDF
ds = xr.open_dataset(output_file)

print(f"\nDataset loaded:")
print(f"  Dimensions: {dict(ds.sizes)}")
print(f"  Variables: {list(ds.data_vars)}")

# Convert precipitation from meters to millimeters
ds['tp'] = ds['tp'] * 1000

# Spatial average (over Oslo area)
precip_mean = ds['tp'].mean(dim=['latitude', 'longitude'])

# Convert to pandas DataFrame
df = precip_mean.to_dataframe().reset_index()

# Handle different time coordinate names
time_coord = 'time' if 'time' in df.columns else 'valid_time'
df = df.rename(columns={'tp': 'precip_mm', time_coord: 'date'})

# Add year, quarter
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.quarter
df['period'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)

print(f"\nMonthly data:")
print(f"  Total months: {len(df)}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")

# Aggregate to quarterly
quarterly = df.groupby(['year', 'quarter', 'period']).agg({
    'precip_mm': 'sum',  # Total precipitation per quarter
    'date': 'min'
}).reset_index()

quarterly = quarterly.rename(columns={
    'precip_mm': 'total_precip_mm',
    'date': 'quarter_start_date'
})

# Calculate anomalies (vs. historical mean)
mean_precip = quarterly['total_precip_mm'].mean()
std_precip = quarterly['total_precip_mm'].std()

quarterly['precip_anomaly'] = (quarterly['total_precip_mm'] - mean_precip) / std_precip
quarterly['precip_anomaly_mm'] = quarterly['total_precip_mm'] - mean_precip

# Classify risk levels
def classify_risk(anomaly):
    if anomaly > 1.5:
        return 'EXTREME'
    elif anomaly > 1.0:
        return 'HIGH'
    elif anomaly > 0.5:
        return 'MEDIUM'
    elif anomaly > -0.5:
        return 'NORMAL'
    else:
        return 'LOW'

quarterly['risk_level'] = quarterly['precip_anomaly'].apply(classify_risk)

print(f"\n=== PRECIPITATION STATISTICS ===")
print(f"Mean quarterly precip: {mean_precip:.1f}mm")
print(f"Std dev: {std_precip:.1f}mm")
print(f"Min: {quarterly['total_precip_mm'].min():.1f}mm")
print(f"Max: {quarterly['total_precip_mm'].max():.1f}mm")

# Save
output_csv = 'data/processed/oslo_quarterly_precipitation_2014-2021.csv'
quarterly.to_csv(output_csv, index=False)
print(f"\n✅ Saved: {output_csv}")

# Show high precipitation quarters
print("\n=== HIGH PRECIPITATION QUARTERS ===")
high_precip = quarterly[quarterly['precip_anomaly'] > 1.0].sort_values('precip_anomaly', ascending=False)
if len(high_precip) > 0:
    print(high_precip[['period', 'total_precip_mm', 'precip_anomaly', 'risk_level']].to_string(index=False))
else:
    print("No quarters with anomaly > 1.0")

# Show all quarters
print("\n=== ALL QUARTERLY PRECIPITATION ===")
print(quarterly[['period', 'total_precip_mm', 'precip_anomaly']].to_string(index=False))

ds.close()

print("\n" + "="*60)
print("✓ PHASE 2 COMPLETE: ERA5 precipitation downloaded & processed")
print("="*60)
