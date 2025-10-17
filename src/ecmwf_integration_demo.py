"""
ECMWF Integration Demonstration
Shows how real ERA5 data integrates with synthetic claims
"""

import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def load_era5_data(filepath):
    """Load ERA5 precipitation data"""
    print(f"\nLoading ERA5 data from: {filepath}")
    ds = xr.open_dataset(filepath)
    print(f"✓ Loaded ERA5 data")
    print(f"  Time range: {ds.valid_time.values[0]} to {ds.valid_time.values[-1]}")
    print(f"  Shape: {ds.tp.shape}")
    return ds

def process_era5_to_quarterly(ds):
    """Process ERA5 monthly data to quarterly totals"""
    print("\nProcessing ERA5 to quarterly totals...")

    # Extract precipitation (convert m to mm)
    precip = ds.tp.values.squeeze() * 1000
    times = pd.DatetimeIndex(ds.valid_time.values)

    # Create DataFrame
    df = pd.DataFrame({
        'date': times,
        'precip_mm': precip.mean(axis=-1) if len(precip.shape) > 1 else precip
    })

    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter

    # Aggregate to quarterly
    quarterly = df.groupby(['year', 'quarter']).agg({
        'precip_mm': 'sum'
    }).reset_index()

    quarterly['period'] = quarterly['year'].astype(str) + ' Q' + quarterly['quarter'].astype(str)

    print(f"✓ Created quarterly aggregations: {len(quarterly)} quarters")
    return quarterly

def merge_with_claims(era5_quarterly, claims_file, city):
    """Merge ERA5 data with claims data"""
    print(f"\nMerging ERA5 data with {city} claims...")

    # Load claims
    claims = pd.read_csv(claims_file)

    # Merge on year and quarter
    merged = era5_quarterly.merge(
        claims[['year', 'quarter', 'total_claims', 'natural_perils', 'rain_associated']],
        on=['year', 'quarter'],
        how='inner'
    )

    print(f"✓ Merged data: {len(merged)} quarters")
    return merged

def calculate_correlation(df, city):
    """Calculate correlation between ERA5 precipitation and claims"""
    print(f"\n{'='*60}")
    print(f"CORRELATION ANALYSIS: {city.upper()} (ERA5 Real Data)")
    print(f"{'='*60}\n")

    if len(df) < 3:
        print("⚠ Not enough data points for correlation analysis")
        return None

    r, p = stats.pearsonr(df['precip_mm'], df['total_claims'])
    r_nat, p_nat = stats.pearsonr(df['precip_mm'], df['natural_perils'])

    print(f"ERA5 Precipitation vs Claims:")
    print(f"  Pearson r = {r:.3f} (p = {p:.4f})")
    print(f"  {'Significant' if p < 0.05 else 'Not significant'} at p < 0.05")

    print(f"\nERA5 Precipitation vs Natural Perils:")
    print(f"  Pearson r = {r_nat:.3f} (p = {p_nat:.4f})")

    return {'r': r, 'p': p, 'r_nat': r_nat, 'p_nat': p_nat}

def create_visualization(df, city, output_path):
    """Create visualization of ERA5 vs claims"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Scatter plot
    axes[0].scatter(df['precip_mm'], df['total_claims'], alpha=0.7, s=100)
    axes[0].set_xlabel('ERA5 Quarterly Precipitation (mm)', fontsize=12)
    axes[0].set_ylabel('Quarterly Claims', fontsize=12)
    axes[0].set_title(f'{city}: ERA5 Real Data vs Claims', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    # Add trend line
    if len(df) > 1:
        z = np.polyfit(df['precip_mm'], df['total_claims'], 1)
        p = np.poly1d(z)
        axes[0].plot(df['precip_mm'], p(df['precip_mm']), 'r--', alpha=0.8, linewidth=2)

    # Time series
    axes[1].plot(df['period'], df['total_claims'], marker='o', label='Claims', linewidth=2)
    axes[1].set_xlabel('Quarter', fontsize=12)
    axes[1].set_ylabel('Total Claims', fontsize=12)
    axes[1].set_title(f'{city}: Quarterly Claims (ERA5 Period)', fontsize=14, fontweight='bold')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved visualization: {output_path}")

def main():
    """Main execution"""
    print("="*60)
    print("ECMWF INTEGRATION DEMONSTRATION")
    print("Real ERA5 Data + Synthetic Claims")
    print("="*60)

    # Load ERA5 data
    era5_file = '/Users/giulio/portfolio1-norway/data/raw/era5_bergen_sample_2020-2021.nc'
    ds = load_era5_data(era5_file)

    # Process to quarterly
    era5_quarterly = process_era5_to_quarterly(ds)
    print("\nERA5 Quarterly Data:")
    print(era5_quarterly)

    # Merge with Bergen claims
    bergen_claims = '/Users/giulio/portfolio1-norway/data/synthetic/bergen_quarterly_2014-2021.csv'
    bergen_merged = merge_with_claims(era5_quarterly, bergen_claims, 'Bergen')

    print("\nMerged Bergen Data:")
    print(bergen_merged[['period', 'precip_mm', 'total_claims', 'natural_perils']])

    # Calculate correlation
    bergen_corr = calculate_correlation(bergen_merged, 'Bergen')

    # Create visualization
    output_fig = '/Users/giulio/portfolio1-norway/outputs/figures/era5_integration_demo.png'
    create_visualization(bergen_merged, 'Bergen', output_fig)

    # Save merged data
    output_csv = '/Users/giulio/portfolio1-norway/data/processed/bergen_era5_demo.csv'
    bergen_merged.to_csv(output_csv, index=False)
    print(f"✓ Saved merged data: {output_csv}")

    print("\n" + "="*60)
    print("✓ ECMWF INTEGRATION DEMO COMPLETE")
    print("="*60)
    print("\nThis demonstrates:")
    print("  1. ✓ Real ERA5 precipitation data downloaded from CDS")
    print("  2. ✓ NetCDF data processing with xarray")
    print("  3. ✓ Quarterly aggregation from monthly data")
    print("  4. ✓ Correlation with insurance claims")
    print("  5. ✓ Visualization of real climate data vs claims")
    print("\nFor full 8-year analysis:")
    print("  - Download ERA5 for 2014-2021 (all months)")
    print("  - Download SEAS5 hindcasts (seasonal forecasts)")
    print("  - Run full correlation analysis")
    print("="*60)

    ds.close()

if __name__ == "__main__":
    main()
