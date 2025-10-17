"""
Generate synthetic Norwegian insurance claims data (2014-2021)
Based on: Gorji & Rødal (2021) - Norwegian School of Economics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

def create_date_range():
    """Create daily date range for 2014-2021 (2920 days)"""
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2021, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    return dates

def generate_bergen_claims():
    """
    Generate synthetic Bergen claims matching thesis statistics:
    - 80.5% zero-claim days
    - 15.4% one-claim days
    - 4.1% two+ claim days
    - Natural perils: 55% of all claims
    - Known extreme events
    """
    dates = create_date_range()
    n_days = len(dates)

    # Initialize daily claims array
    daily_claims = np.zeros(n_days, dtype=int)

    # Distribute days according to thesis statistics (adjusted for 2922 days)
    zero_claim_days = int(n_days * 0.805)
    one_claim_days = int(n_days * 0.154)
    two_plus_claim_days = n_days - zero_claim_days - one_claim_days

    # Create indices for each category
    all_indices = np.arange(n_days)
    np.random.shuffle(all_indices)

    one_claim_indices = all_indices[:one_claim_days]
    two_plus_indices = all_indices[one_claim_days:one_claim_days + two_plus_claim_days]

    # Assign one claim to designated days
    daily_claims[one_claim_indices] = 1

    # For 2+ claim days, use power law distribution (typical for extreme events)
    # Most days get 2-3 claims, few get many more
    two_plus_claims = np.random.choice([2, 3, 4, 5], size=two_plus_claim_days-8, p=[0.6, 0.25, 0.10, 0.05])

    # Reserve 8 days for 10+ claims (from thesis)
    high_claim_days = np.random.choice(range(10, 30), size=8)

    daily_claims[two_plus_indices[:len(two_plus_claims)]] = two_plus_claims
    daily_claims[two_plus_indices[len(two_plus_claims):]] = high_claim_days

    # Insert known extreme events at specific dates
    extreme_events = {
        '2015-01-10': 291,  # Storm Nina
        '2019-09-19': 29,   # Flood
        '2016-01-29': 25    # Hurricane Tor
    }

    for date_str, claims in extreme_events.items():
        idx = dates.get_loc(pd.Timestamp(date_str))
        daily_claims[idx] = claims

    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'total_claims': daily_claims
    })

    # Calculate natural perils (55% of all claims)
    # Higher probability on high-claim days
    natural_perils = []
    for claims in daily_claims:
        if claims == 0:
            nat_perils = 0
        else:
            # Binomial distribution: each claim has 55% chance of being natural peril
            nat_perils = np.random.binomial(claims, 0.55)
        natural_perils.append(nat_perils)

    df['natural_perils'] = natural_perils

    # Rain-associated claims (subset of natural perils + some non-natural)
    # Assume 80% of natural perils are rain-associated, plus 10% of other claims
    df['rain_associated'] = df.apply(
        lambda row: min(
            row['total_claims'],
            np.random.binomial(row['natural_perils'], 0.80) +
            np.random.binomial(row['total_claims'] - row['natural_perils'], 0.10)
        ),
        axis=1
    )

    # Add time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter

    return df

def generate_oslo_claims():
    """
    Generate synthetic Oslo claims matching thesis statistics:
    - 76.2% zero-claim days
    - 17.8% one-claim days
    - 6.0% two+ claim days
    - Natural perils: 14% of all claims
    - Known extreme events
    """
    dates = create_date_range()
    n_days = len(dates)

    # Initialize daily claims array
    daily_claims = np.zeros(n_days, dtype=int)

    # Distribute days according to thesis statistics (adjusted for 2922 days)
    zero_claim_days = int(n_days * 0.762)
    one_claim_days = int(n_days * 0.178)
    two_plus_claim_days = n_days - zero_claim_days - one_claim_days

    # Create indices for each category
    all_indices = np.arange(n_days)
    np.random.shuffle(all_indices)

    one_claim_indices = all_indices[:one_claim_days]
    two_plus_indices = all_indices[one_claim_days:one_claim_days + two_plus_claim_days]

    # Assign one claim to designated days
    daily_claims[one_claim_indices] = 1

    # For 2+ claim days, use power law distribution
    two_plus_claims = np.random.choice([2, 3, 4, 5, 6], size=two_plus_claim_days-8, p=[0.5, 0.25, 0.15, 0.05, 0.05])

    # Reserve 8 days for 10+ claims
    high_claim_days = np.random.choice(range(10, 45), size=8)

    daily_claims[two_plus_indices[:len(two_plus_claims)]] = two_plus_claims
    daily_claims[two_plus_indices[len(two_plus_claims):]] = high_claim_days

    # Insert known extreme events at specific dates
    extreme_events = {
        '2016-08-06': 220,  # "200-year rain" Asker
        '2015-09-03': 45,   # Flooding period
        '2015-09-04': 40,
        '2015-09-05': 40
    }

    for date_str, claims in extreme_events.items():
        idx = dates.get_loc(pd.Timestamp(date_str))
        daily_claims[idx] = claims

    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'total_claims': daily_claims
    })

    # Calculate natural perils (14% of all claims)
    natural_perils = []
    for claims in daily_claims:
        if claims == 0:
            nat_perils = 0
        else:
            nat_perils = np.random.binomial(claims, 0.14)
        natural_perils.append(nat_perils)

    df['natural_perils'] = natural_perils

    # For Oslo extreme events, set natural perils from thesis
    df.loc[df['date'] == '2016-08-06', 'natural_perils'] = 36
    df.loc[df['date'] == '2015-09-03', 'natural_perils'] = 4
    df.loc[df['date'] == '2015-09-04', 'natural_perils'] = 4
    df.loc[df['date'] == '2015-09-05', 'natural_perils'] = 4

    # Rain-associated claims
    df['rain_associated'] = df.apply(
        lambda row: min(
            row['total_claims'],
            np.random.binomial(row['natural_perils'], 0.85) +
            np.random.binomial(row['total_claims'] - row['natural_perils'], 0.08)
        ),
        axis=1
    )

    # Add time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter

    return df

def create_quarterly_aggregations(df, city):
    """Aggregate daily claims to quarterly totals"""
    quarterly = df.groupby(['year', 'quarter']).agg({
        'total_claims': 'sum',
        'natural_perils': 'sum',
        'rain_associated': 'sum',
        'date': 'count'  # Days in quarter
    }).reset_index()

    # Add days with claims
    days_with_claims = df[df['total_claims'] > 0].groupby(['year', 'quarter']).size()
    quarterly = quarterly.merge(
        days_with_claims.reset_index(name='days_with_claims'),
        on=['year', 'quarter'],
        how='left'
    )
    quarterly['days_with_claims'].fillna(0, inplace=True)

    # Add max daily claims per quarter
    max_daily = df.groupby(['year', 'quarter'])['total_claims'].max()
    quarterly = quarterly.merge(
        max_daily.reset_index(name='max_daily_claims'),
        on=['year', 'quarter']
    )

    # Rename and create period column
    quarterly.rename(columns={'date': 'days_in_quarter'}, inplace=True)
    quarterly['period'] = quarterly['year'].astype(str) + ' Q' + quarterly['quarter'].astype(str)

    # Reorder columns
    quarterly = quarterly[['period', 'year', 'quarter', 'total_claims', 'natural_perils',
                          'rain_associated', 'days_with_claims', 'max_daily_claims']]

    return quarterly

def validate_data(df, city, quarterly):
    """Validate synthetic data against thesis specifications"""
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT: {city.upper()}")
    print(f"{'='*60}\n")

    # Check total days (2014-2021 inclusive is 2922 days due to leap years)
    print(f"Total days: {len(df)} (expected: 2922)")
    assert len(df) == 2922, "Incorrect number of days"

    # Check distribution of claim days
    zero_claims = (df['total_claims'] == 0).sum()
    one_claim = (df['total_claims'] == 1).sum()
    two_plus = (df['total_claims'] >= 2).sum()

    total_days = zero_claims + one_claim + two_plus

    print(f"\nDaily Claim Distribution:")
    print(f"  Zero-claim days: {zero_claims} ({zero_claims/total_days*100:.1f}%)")
    print(f"  One-claim days: {one_claim} ({one_claim/total_days*100:.1f}%)")
    print(f"  2+ claim days: {two_plus} ({two_plus/total_days*100:.1f}%)")

    if city == 'Bergen':
        assert 79 <= zero_claims/total_days*100 <= 82, "Bergen zero-claim days mismatch"
        assert 14 <= one_claim/total_days*100 <= 17, "Bergen one-claim days mismatch"
        assert 3 <= two_plus/total_days*100 <= 6, "Bergen 2+ claim days mismatch"
    else:
        assert 75 <= zero_claims/total_days*100 <= 78, "Oslo zero-claim days mismatch"
        assert 16 <= one_claim/total_days*100 <= 19, "Oslo one-claim days mismatch"
        assert 5 <= two_plus/total_days*100 <= 7, "Oslo 2+ claim days mismatch"

    # Check natural perils percentage
    total_claims = df['total_claims'].sum()
    total_nat_perils = df['natural_perils'].sum()
    nat_peril_pct = (total_nat_perils / total_claims * 100) if total_claims > 0 else 0

    print(f"\nNatural Perils:")
    print(f"  Total claims: {total_claims}")
    print(f"  Natural peril claims: {total_nat_perils} ({nat_peril_pct:.1f}%)")

    if city == 'Bergen':
        assert 50 <= nat_peril_pct <= 60, f"Bergen natural perils should be ~55%, got {nat_peril_pct:.1f}%"
    else:
        assert 10 <= nat_peril_pct <= 18, f"Oslo natural perils should be ~14%, got {nat_peril_pct:.1f}%"

    # Check extreme events
    print(f"\nExtreme Events:")
    high_claim_days = df[df['total_claims'] >= 10].sort_values('total_claims', ascending=False)
    print(f"  Days with 10+ claims: {len(high_claim_days)}")
    print(f"\n  Top 5 claim days:")
    for _, row in high_claim_days.head(5).iterrows():
        print(f"    {row['date'].strftime('%Y-%m-%d')}: {row['total_claims']} claims ({row['natural_perils']} natural perils)")

    # Check weekly average
    weeks = len(df) / 7
    avg_per_week = total_claims / weeks
    print(f"\nAverage claims per week: {avg_per_week:.1f} (expected: ~3)")

    # Check quarterly data
    print(f"\nQuarterly Aggregations:")
    print(f"  Total quarters: {len(quarterly)} (expected: 32)")
    assert len(quarterly) == 32, "Should have 32 quarters (8 years × 4)"

    print(f"\n  Top 5 loss quarters:")
    top_quarters = quarterly.nlargest(5, 'total_claims')[['period', 'total_claims', 'natural_perils', 'max_daily_claims']]
    print(top_quarters.to_string(index=False))

    print(f"\n{'='*60}")
    print(f"✓ {city} validation PASSED")
    print(f"{'='*60}\n")

def create_validation_plots(df_bergen, df_oslo, quarterly_bergen, quarterly_oslo):
    """Create validation visualizations"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Plot 1: Daily claims distribution - Bergen
    axes[0, 0].hist(df_bergen['total_claims'], bins=50, alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Bergen: Daily Claims Distribution', fontweight='bold')
    axes[0, 0].set_xlabel('Claims per day')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_yscale('log')

    # Plot 2: Daily claims distribution - Oslo
    axes[0, 1].hist(df_oslo['total_claims'], bins=50, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].set_title('Oslo: Daily Claims Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Claims per day')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_yscale('log')

    # Plot 3: Natural perils percentage
    nat_peril_data = pd.DataFrame({
        'City': ['Bergen', 'Oslo'],
        'Natural Perils %': [
            df_bergen['natural_perils'].sum() / df_bergen['total_claims'].sum() * 100,
            df_oslo['natural_perils'].sum() / df_oslo['total_claims'].sum() * 100
        ],
        'Expected %': [55, 14]
    })
    x = np.arange(len(nat_peril_data))
    width = 0.35
    axes[0, 2].bar(x - width/2, nat_peril_data['Natural Perils %'], width, label='Generated', alpha=0.8)
    axes[0, 2].bar(x + width/2, nat_peril_data['Expected %'], width, label='Expected', alpha=0.8)
    axes[0, 2].set_ylabel('Percentage')
    axes[0, 2].set_title('Natural Perils % Validation', fontweight='bold')
    axes[0, 2].set_xticks(x)
    axes[0, 2].set_xticklabels(nat_peril_data['City'])
    axes[0, 2].legend()

    # Plot 4: Quarterly claims - Bergen
    axes[1, 0].plot(range(len(quarterly_bergen)), quarterly_bergen['total_claims'], marker='o')
    axes[1, 0].set_title('Bergen: Quarterly Claims (2014-2021)', fontweight='bold')
    axes[1, 0].set_xlabel('Quarter')
    axes[1, 0].set_ylabel('Total claims')
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 5: Quarterly claims - Oslo
    axes[1, 1].plot(range(len(quarterly_oslo)), quarterly_oslo['total_claims'], marker='o', color='green')
    axes[1, 1].set_title('Oslo: Quarterly Claims (2014-2021)', fontweight='bold')
    axes[1, 1].set_xlabel('Quarter')
    axes[1, 1].set_ylabel('Total claims')
    axes[1, 1].grid(True, alpha=0.3)

    # Plot 6: Time series comparison
    axes[1, 2].plot(df_bergen['date'], df_bergen['total_claims'].rolling(30).mean(),
                    label='Bergen (30-day avg)', alpha=0.7)
    axes[1, 2].plot(df_oslo['date'], df_oslo['total_claims'].rolling(30).mean(),
                    label='Oslo (30-day avg)', alpha=0.7, color='green')
    axes[1, 2].set_title('Daily Claims: 30-Day Moving Average', fontweight='bold')
    axes[1, 2].set_xlabel('Date')
    axes[1, 2].set_ylabel('Claims (30-day avg)')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/giulio/portfolio1-norway/outputs/figures/synthetic_data_validation.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Validation plots saved to outputs/figures/synthetic_data_validation.png")

def main():
    """Main execution function"""
    print("="*60)
    print("GENERATING SYNTHETIC NORWEGIAN INSURANCE CLAIMS DATA")
    print("Based on: Gorji & Rødal (2021)")
    print("="*60)

    # Generate Bergen data
    print("\nGenerating Bergen claims data...")
    df_bergen = generate_bergen_claims()

    # Generate Oslo data
    print("Generating Oslo claims data...")
    df_oslo = generate_oslo_claims()

    # Create quarterly aggregations
    print("\nCreating quarterly aggregations...")
    quarterly_bergen = create_quarterly_aggregations(df_bergen, 'Bergen')
    quarterly_oslo = create_quarterly_aggregations(df_oslo, 'Oslo')

    # Save to CSV
    print("\nSaving data files...")
    df_bergen.to_csv('/Users/giulio/portfolio1-norway/data/synthetic/bergen_daily_claims_2014-2021.csv', index=False)
    df_oslo.to_csv('/Users/giulio/portfolio1-norway/data/synthetic/oslo_daily_claims_2014-2021.csv', index=False)
    quarterly_bergen.to_csv('/Users/giulio/portfolio1-norway/data/synthetic/bergen_quarterly_2014-2021.csv', index=False)
    quarterly_oslo.to_csv('/Users/giulio/portfolio1-norway/data/synthetic/oslo_quarterly_2014-2021.csv', index=False)

    print("  ✓ bergen_daily_claims_2014-2021.csv")
    print("  ✓ oslo_daily_claims_2014-2021.csv")
    print("  ✓ bergen_quarterly_2014-2021.csv")
    print("  ✓ oslo_quarterly_2014-2021.csv")

    # Validate data
    validate_data(df_bergen, 'Bergen', quarterly_bergen)
    validate_data(df_oslo, 'Oslo', quarterly_oslo)

    # Create validation plots
    print("\nGenerating validation plots...")
    create_validation_plots(df_bergen, df_oslo, quarterly_bergen, quarterly_oslo)

    print("\n" + "="*60)
    print("✓ PHASE 1 COMPLETE: Synthetic claims data generated")
    print("="*60)

if __name__ == "__main__":
    main()
