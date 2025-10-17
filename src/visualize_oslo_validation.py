"""
Create Visualizations for Oslo Validation
Real claims vs. real precipitation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr

# Load merged data
df = pd.read_csv('data/processed/oslo_merged_claims_precip_2014-2021.csv')

# Set style
sns.set_style('whitegrid')

print("="*60)
print("GENERATING OSLO VALIDATION VISUALIZATIONS")
print("="*60)

# === CHART 1: Scatter Plot (Claims vs Precipitation) ===
print("\nGenerating Chart 1: Scatter plot...")

fig, ax = plt.subplots(figsize=(11, 7))

# Calculate correlation
r, p = pearsonr(df['total_precip_mm'], df['payout_million_nok'])

# Scatter plot with color by year
scatter = ax.scatter(
    df['total_precip_mm'],
    df['payout_million_nok'],
    c=df['year'],
    s=df['payout_million_nok'] * 30,  # Size by claim amount
    alpha=0.6,
    cmap='viridis',
    edgecolors='black',
    linewidth=0.5
)

# Trend line
z = np.polyfit(df['total_precip_mm'], df['payout_million_nok'], 1)
p_line = np.poly1d(z)
ax.plot(
    df['total_precip_mm'],
    p_line(df['total_precip_mm']),
    "r--",
    alpha=0.8,
    linewidth=2,
    label=f'Trend line (r={r:+.3f}, p={p:.3f})'
)

# Highlight extreme events
extreme = df[df['is_extreme']]
if len(extreme) > 0:
    ax.scatter(
        extreme['total_precip_mm'],
        extreme['payout_million_nok'],
        s=600,
        facecolors='none',
        edgecolors='red',
        linewidths=3,
        label=f'Extreme events (>5M NOK)'
    )

    # Label extreme events
    for _, row in extreme.iterrows():
        ax.annotate(
            row['period'],
            (row['total_precip_mm'], row['payout_million_nok']),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=9,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
        )

ax.set_xlabel('Quarterly Precipitation (mm)', fontsize=13, fontweight='bold')
ax.set_ylabel('Insurance Claims Payout (M NOK)', fontsize=13, fontweight='bold')
ax.set_title(
    'Oslo: Quarterly Precipitation vs. Insurance Claims (2014-2021)\n' +
    f'Real NASK Data - Pearson r = {r:+.3f}, p = {p:.4f}',
    fontsize=14,
    fontweight='bold',
    pad=20
)

plt.colorbar(scatter, label='Year', ax=ax)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/figures/oslo_scatter_precip_vs_claims.png', dpi=300, bbox_inches='tight')
print("✅ Saved: outputs/figures/oslo_scatter_precip_vs_claims.png")
plt.close()

# === CHART 2: Time Series (Both Variables) ===
print("Generating Chart 2: Time series...")

fig, ax1 = plt.subplots(figsize=(15, 7))

# Claims on left axis
bars = ax1.bar(
    range(len(df)),
    df['payout_million_nok'],
    color='steelblue',
    alpha=0.7,
    label='Claims Payout'
)

# Color extreme quarters in red
for i, (idx, row) in enumerate(df.iterrows()):
    if row['is_extreme']:
        bars[i].set_color('darkred')
        bars[i].set_alpha(0.8)

ax1.set_xlabel('Quarter', fontsize=13, fontweight='bold')
ax1.set_ylabel('Claims Payout (M NOK)', fontsize=13, fontweight='bold', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

# Precipitation on right axis
ax2 = ax1.twinx()
ax2.plot(
    range(len(df)),
    df['total_precip_mm'],
    color='darkgreen',
    marker='o',
    linewidth=2.5,
    markersize=7,
    label='Precipitation',
    alpha=0.8
)
ax2.set_ylabel('Quarterly Precipitation (mm)', fontsize=13, fontweight='bold', color='darkgreen')
ax2.tick_params(axis='y', labelcolor='darkgreen')

# Highlight extreme quarters with vertical lines
for idx, row in df[df['is_extreme']].iterrows():
    pos = df.index.get_loc(idx)
    ax1.axvline(x=pos, color='red', linestyle='--', alpha=0.4, linewidth=2)

# X-axis labels
ax1.set_xticks(range(len(df)))
ax1.set_xticklabels(df['period'], rotation=45, ha='right', fontsize=9)

ax1.set_title(
    'Oslo: Claims and Precipitation Time Series (2014-2021)\n' +
    'Real NASK Data - Red bars/lines indicate extreme claim quarters',
    fontsize=14,
    fontweight='bold',
    pad=20
)

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

ax1.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('outputs/figures/oslo_timeseries_claims_precip.png', dpi=300, bbox_inches='tight')
print("✅ Saved: outputs/figures/oslo_timeseries_claims_precip.png")
plt.close()

# === CHART 3: Event Detection Scorecard ===
print("Generating Chart 3: Event detection scorecard...")

fig, ax = plt.subplots(figsize=(12, 5))

extreme_quarters = df[df['is_extreme']].copy()
extreme_quarters['detected'] = extreme_quarters['precip_anomaly'] > 1.0

# Create table data
table_data = []
for _, row in extreme_quarters.iterrows():
    detected_str = "✅ YES" if row['detected'] else "❌ MISSED"
    table_data.append([
        row['period'],
        f"{row['payout_million_nok']:.1f}M NOK",
        f"{row['total_precip_mm']:.1f}mm",
        f"{row['precip_anomaly']:+.2f} σ",
        row['risk_level'],
        detected_str
    ])

# Create table
ax.axis('tight')
ax.axis('off')

if len(table_data) > 0:
    table = ax.table(
        cellText=table_data,
        colLabels=['Quarter', 'Claims Payout', 'Precipitation', 'Anomaly', 'Risk Level', 'Detected?'],
        cellLoc='center',
        loc='center',
        colWidths=[0.12, 0.18, 0.15, 0.13, 0.15, 0.15]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.8)

    # Color code detection column
    for i in range(len(table_data)):
        if "✅" in table_data[i][5]:
            table[(i+1, 5)].set_facecolor('#90EE90')  # Light green
        else:
            table[(i+1, 5)].set_facecolor('#FFB6C1')  # Light red

    # Header formatting
    for i in range(6):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')

    detection_rate = (extreme_quarters['detected'].sum() / len(extreme_quarters) * 100)

    title_text = (
        f'Oslo: Extreme Event Detection Scorecard (2014-2021)\n' +
        f'Real NASK Data - Detection Rate: {detection_rate:.0f}% ' +
        f'({extreme_quarters["detected"].sum()}/{len(extreme_quarters)} extreme quarters correctly flagged)'
    )
else:
    title_text = 'Oslo: No Extreme Events to Display'

ax.set_title(title_text, fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('outputs/figures/oslo_event_detection_scorecard.png', dpi=300, bbox_inches='tight')
print("✅ Saved: outputs/figures/oslo_event_detection_scorecard.png")
plt.close()

print("\n" + "="*60)
print("✓ PHASE 4 COMPLETE: All visualizations generated")
print("="*60)
print("\nGenerated files:")
print("  - oslo_scatter_precip_vs_claims.png")
print("  - oslo_timeseries_claims_precip.png")
print("  - oslo_event_detection_scorecard.png")
