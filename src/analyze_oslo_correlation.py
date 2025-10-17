"""
Correlation Analysis: Oslo Claims vs ERA5 Precipitation
Real NASK data validation
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

print("="*60)
print("OSLO CORRELATION ANALYSIS")
print("Real Claims vs. Real Precipitation")
print("="*60)

# Load data
claims = pd.read_csv('data/processed/oslo_quarterly_claims_2014-2021.csv')
precip = pd.read_csv('data/processed/oslo_quarterly_precipitation_2014-2021.csv')

print(f"\nLoaded data:")
print(f"  Claims: {len(claims)} quarters")
print(f"  Precipitation: {len(precip)} quarters")

# Merge on period
merged = pd.merge(claims, precip, on=['year', 'quarter', 'period'], how='inner')

print(f"  Merged: {len(merged)} quarters")

# Calculate correlations
pearson_r, pearson_p = pearsonr(merged['total_precip_mm'], merged['payout_million_nok'])
spearman_r, spearman_p = spearmanr(merged['total_precip_mm'], merged['payout_million_nok'])

print(f"\n{'='*60}")
print("CORRELATION RESULTS")
print(f"{'='*60}")
print(f"\nPearson r:  {pearson_r:+.3f}, p-value: {pearson_p:.4f}")
print(f"Spearman r: {spearman_r:+.3f}, p-value: {spearman_p:.4f}")

# Statistical significance
if pearson_p < 0.001:
    significance = "HIGHLY SIGNIFICANT (p<0.001) ***"
elif pearson_p < 0.01:
    significance = "VERY SIGNIFICANT (p<0.01) **"
elif pearson_p < 0.05:
    significance = "SIGNIFICANT (p<0.05) *"
else:
    significance = "NOT SIGNIFICANT (p>0.05)"

print(f"\nStatistical significance: {significance}")

# Interpretation
print(f"\n{'='*60}")
print("INTERPRETATION")
print(f"{'='*60}")

if pearson_r > 0.5:
    print("✅ STRONG POSITIVE CORRELATION")
    print(f"   More precipitation → More insurance claims")
elif pearson_r > 0.3:
    print("✅ MODERATE POSITIVE CORRELATION")
    print(f"   Precipitation shows predictive value")
elif pearson_r > 0:
    print("⚠️ WEAK POSITIVE CORRELATION")
    print(f"   Some relationship but not strong")
else:
    print("❌ NEGATIVE OR NO CORRELATION")
    print(f"   Unexpected result - check data")

# Compare to thesis findings
print(f"\n{'='*60}")
print("COMPARISON TO THESIS")
print(f"{'='*60}")
print(f"\nGorji & Rødal (2021) Thesis:")
print(f"  Oslo daily prediction: AUC = 0.67 (moderate skill)")
print(f"  Method: Machine learning (XGBoost, Neural Nets)")
print(f"\nOur Result:")
print(f"  Oslo quarterly: r = {pearson_r:+.3f}")
print(f"  Method: Direct correlation (ERA5 observations)")

# Rule of thumb: r ~ 0.5-0.7 equivalent to AUC ~ 0.65-0.75
if abs(pearson_r) > 0.4:
    print(f"\n✅ Result aligns with thesis expectations!")
    print(f"   Quarterly correlation {pearson_r:.2f} consistent with daily AUC 0.67")
else:
    print(f"\n⚠️ Weaker than thesis findings")
    print(f"   Possible reasons: Quarterly vs daily, different time periods")

# Event detection analysis
print(f"\n{'='*60}")
print("EXTREME EVENT ANALYSIS")
print(f"{'='*60}")

extreme_claims = merged[merged['is_extreme']].copy()
print(f"\nExtreme claim quarters (>5M NOK): {len(extreme_claims)}")

if len(extreme_claims) > 0:
    print("\nDetailed analysis of extreme quarters:")
    for _, row in extreme_claims.iterrows():
        print(f"\n{row['period']}:")
        print(f"  Claims payout: {row['payout_million_nok']:.1f}M NOK")
        print(f"  Precipitation: {row['total_precip_mm']:.1f}mm")
        print(f"  Precip anomaly: {row['precip_anomaly']:+.2f} std deviations")
        print(f"  Risk level: {row['risk_level']}")

        if row['precip_anomaly'] > 1.0:
            print(f"  ✅ HIGH precipitation correctly identified")
        else:
            print(f"  ⚠️ Precipitation not elevated")

# Calculate event detection metrics
print(f"\n{'='*60}")
print("EVENT DETECTION METRICS")
print(f"{'='*60}")

# Define thresholds (top 25% of each)
high_precip_threshold = merged['precip_anomaly'].quantile(0.75)
high_claims_threshold = merged['payout_million_nok'].quantile(0.75)

print(f"\nThresholds:")
print(f"  High precipitation: {high_precip_threshold:+.2f} std dev")
print(f"  High claims: {high_claims_threshold:.1f}M NOK")

merged['forecast_high'] = merged['precip_anomaly'] > high_precip_threshold
merged['actual_high'] = merged['payout_million_nok'] > high_claims_threshold

# Confusion matrix
tp = ((merged['forecast_high']) & (merged['actual_high'])).sum()
tn = ((~merged['forecast_high']) & (~merged['actual_high'])).sum()
fp = ((merged['forecast_high']) & (~merged['actual_high'])).sum()
fn = ((~merged['forecast_high']) & (merged['actual_high'])).sum()

accuracy = (tp + tn) / len(merged)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"\nPredicting top 25% claims quarters:")
print(f"  Accuracy:  {accuracy:.2%} (overall correct predictions)")
print(f"  Precision: {precision:.2%} (when forecast high, claims are high)")
print(f"  Recall:    {recall:.2%} (of high claim quarters, % correctly flagged)")
print(f"  F1 Score:  {f1:.3f} (harmonic mean)")

print(f"\nConfusion Matrix:")
print(f"  True Positives:  {tp:2d} (correctly forecast high-loss)")
print(f"  False Positives: {fp:2d} (false alarms)")
print(f"  False Negatives: {fn:2d} (missed events)")
print(f"  True Negatives:  {tn:2d} (correctly forecast low-loss)")

# Save merged data
output_file = 'data/processed/oslo_merged_claims_precip_2014-2021.csv'
merged.to_csv(output_file, index=False)
print(f"\n✅ Saved: {output_file}")

# Summary statistics
print(f"\n{'='*60}")
print("SUMMARY STATISTICS")
print(f"{'='*60}")

print(f"\nClaims (8 years):")
print(f"  Total payouts: {merged['payout_million_nok'].sum():.1f}M NOK")
print(f"  Average/quarter: {merged['payout_million_nok'].mean():.1f}M NOK")
print(f"  Std dev: {merged['payout_million_nok'].std():.1f}M NOK")

print(f"\nPrecipitation (8 years):")
print(f"  Average/quarter: {merged['total_precip_mm'].mean():.1f}mm")
print(f"  Std dev: {merged['total_precip_mm'].std():.1f}mm")
print(f"  Range: {merged['total_precip_mm'].min():.1f} - {merged['total_precip_mm'].max():.1f}mm")

print("\n" + "="*60)
print("✓ PHASE 3 COMPLETE: Correlation analysis")
print("="*60)
