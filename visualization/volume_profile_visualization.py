"""
Volume Profile Visualization Module - With Composite Heatmap and Classic Views
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
from matplotlib.ticker import FuncFormatter
import numpy as np

def plot_classic_composite_profile(profiles: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots multiple volume profiles side-by-side in the classic bar style.
    """
    if not profiles:
        return

    fig, ax = plt.subplots(figsize=(18, 10))

    # --- 1. Find global max volume for consistent scaling ---
    global_max_volume = 0
    for profile in profiles:
        max_vol = pd.DataFrame(profile['profile_data'])['volume'].max()
        if max_vol > global_max_volume:
            global_max_volume = max_vol

    # --- 2. Loop through each profile and plot its bars ---
    all_price_bins = set()
    for profile in profiles:
        for item in profile['profile_data']:
            all_price_bins.add(item['price_bin'])
    
    bin_size = pd.Series(list(all_price_bins)).sort_values().diff().median()
    if pd.isna(bin_size): bin_size = 10.0 # Default if only one price level

    for i, profile in enumerate(profiles):
        df = pd.DataFrame(profile['profile_data'])
        if df.empty:
            continue
            
        x_position = i
        # Normalize volume width for each profile relative to the available space (0.9 gives a small gap)
        normalized_width = (df['volume'] / global_max_volume) * 0.9
        
        # Plot the bars, starting from the x_position for that timeframe
        bars = ax.barh(
            y=df['price_bin'],
            width=normalized_width,
            left=x_position,
            height=bin_size,
            align='edge', # Align bars to the left edge of the price bin
            color='deepskyblue',
            alpha=0.6,
            edgecolor='gray',
            linewidth=0.5
        )

        # Highlight VA and POC for this specific profile
        poc_price = profile['poc']['price']
        va_low = profile['value_area']['low']
        va_high = profile['value_area']['high']

        for bar in bars:
            price_level = bar.get_y()
            if va_low <= price_level <= va_high:
                bar.set_color('royalblue')
                bar.set_alpha(0.7)
            if abs(price_level - poc_price) < 1e-6: # Exact match for POC
                bar.set_color('orangered')
                bar.set_alpha(0.9)

    # --- 3. Format axes ---
    ax.set_yticks(sorted(list(all_price_bins)))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'${y:,.0f}'))
    ax.set_ylabel("Price")

    ax.set_xticks([i + 0.45 for i in range(len(profiles))]) # Center ticks in the middle of each profile block
    ax.set_xticklabels([p['timestamp'].strftime('%H:%M') for p in profiles], rotation=45, ha='right')
    ax.set_xlabel(f"Time ({timeframe} intervals)")

    ax.set_title(title, fontsize=16, weight='bold')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    plt.show()


def plot_composite_profile(profiles: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots multiple volume profiles as a side-by-side heatmap in a single chart. (Heatmap version)
    """
    if not profiles:
        return
    # ... (کد هیت‌مپ بدون تغییر باقی می‌ماند) ...
    all_data = []
    for i, profile in enumerate(profiles):
        df = pd.DataFrame(profile['profile_data'])
        df['time_period'] = i
        df['timestamp'] = profile['timestamp']
        all_data.append(df)
    composite_df = pd.concat(all_data)
    heatmap_data = composite_df.pivot_table(index='price_bin', columns='time_period', values='volume', fill_value=0).sort_index(ascending=False)
    fig, ax = plt.subplots(figsize=(16, 10))
    im = ax.imshow(heatmap_data, aspect='auto', cmap='inferno', interpolation='none')
    poc_prices = [p['poc']['price'] for p in profiles]
    time_indices = list(range(len(profiles)))
    price_to_row_idx = {price: i for i, price in enumerate(heatmap_data.index)}
    poc_row_indices = [price_to_row_idx.get(p, -1) for p in poc_prices]
    ax.scatter(time_indices, poc_row_indices, color='white', s=50, marker='o', ec='black', label='Point of Control (POC)')
    ax.set_xticks(np.arange(len(profiles)))
    ax.set_xticklabels([p['timestamp'].strftime('%H:%M') for p in profiles], rotation=45, ha='right')
    ax.set_xlabel(f"Time ({timeframe} intervals)")
    ax.set_yticks(np.arange(len(heatmap_data.index)))
    ax.set_yticklabels([f"${price:,.0f}" for price in heatmap_data.index])
    ax.set_ylabel("Price")
    cbar = fig.colorbar(im, ax=ax, pad=0.01)
    cbar.set_label('Volume')
    ax.set_title(title, fontsize=16, weight='bold')
    ax.legend()
    fig.tight_layout()
    plt.show()