"""
Process NASK Oslo Insurance Claims Data (2014-2021)
Real data from Finance Norway's natural perils database
"""

import pandas as pd

# Oslo quarterly payouts from NASK (in 1000 NOK)
oslo_data = {
    "2014-Q1": 1854,
    "2014-Q2": 340,
    "2014-Q3": 337,
    "2014-Q4": 890,
    "2015-Q1": 3744,
    "2015-Q2": 74,
    "2015-Q3": 18761,  # Major flooding event!
    "2015-Q4": 1154,
    "2016-Q1": 768,
    "2016-Q2": 1110,
    "2016-Q3": 2335,   # Asker "200-year rain"
    "2016-Q4": 487,
    "2017-Q1": 435,
    "2017-Q2": 22,
    "2017-Q3": 1433,
    "2017-Q4": 2680,
    "2018-Q1": 491,
    "2018-Q2": 1968,
    "2018-Q3": 9086,   # Major event
    "2018-Q4": 3040,
    "2019-Q1": 1041,
    "2019-Q2": 2003,
    "2019-Q3": 2123,
    "2019-Q4": 415,
    "2020-Q1": 2228,
    "2020-Q2": 9375,   # Major event
    "2020-Q3": 1571,
    "2020-Q4": 2621,
    "2021-Q1": 1948,
    "2021-Q2": 378,
    "2021-Q3": 112,
    "2021-Q4": 3522
}

print("="*60)
print("PROCESSING NASK OSLO CLAIMS DATA (2014-2021)")
print("Real Insurance Data from Finance Norway")
print("="*60)

# Convert to DataFrame
df = pd.DataFrame([
    {
        'period': period,
        'year': int(period.split('-')[0]),
        'quarter': int(period.split('-Q')[1]),
        'payout_1000nok': amount,
        'payout_nok': amount * 1000,
        'payout_million_nok': amount / 1000
    }
    for period, amount in oslo_data.items()
])

# Sort by date
df = df.sort_values(['year', 'quarter']).reset_index(drop=True)

# Add date column (quarter start date)
df['date'] = pd.to_datetime(
    df['year'].astype(str) + '-' +
    ((df['quarter'] - 1) * 3 + 1).astype(str).str.zfill(2) + '-01'
)

# Flag extreme events
df['is_extreme'] = df['payout_1000nok'] > 5000
df['is_high'] = df['payout_1000nok'] > 3000

# Calculate statistics
print("\n=== OSLO CLAIMS STATISTICS ===")
print(f"Total payouts (8 years): {df['payout_million_nok'].sum():.1f}M NOK")
print(f"Average per quarter: {df['payout_million_nok'].mean():.1f}M NOK")
print(f"Median per quarter: {df['payout_million_nok'].median():.1f}M NOK")
print(f"Max quarter: {df['payout_million_nok'].max():.1f}M NOK ({df.loc[df['payout_million_nok'].idxmax(), 'period']})")
print(f"Min quarter: {df['payout_million_nok'].min():.1f}M NOK ({df.loc[df['payout_million_nok'].idxmin(), 'period']})")
print(f"\nExtreme quarters (>5M NOK): {df['is_extreme'].sum()}")
print(f"High quarters (>3M NOK): {df['is_high'].sum()}")

# Show extreme events
print("\n=== EXTREME EVENT QUARTERS ===")
extreme_df = df[df['is_extreme']][['period', 'payout_million_nok', 'payout_1000nok']]
print(extreme_df.to_string(index=False))

# Show all data
print("\n=== ALL QUARTERLY DATA ===")
print(df[['period', 'payout_million_nok']].to_string(index=False))

# Save to CSV
output_file = 'data/processed/oslo_quarterly_claims_2014-2021.csv'
df.to_csv(output_file, index=False)
print(f"\n✅ Saved: {output_file}")

print("\n" + "="*60)
print("✓ PHASE 1 COMPLETE: Oslo claims data processed")
print("="*60)
