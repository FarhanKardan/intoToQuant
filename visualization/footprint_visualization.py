"""
Aesthetically Improved Footprint Chart Visualization Module
Features variable-width rectangles proportional to volume.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import MaxNLocator, FuncFormatter
from typing import List
from data_aggregator.footprint_aggregator import FootprintCandle
import numpy as np

def _format_volume(volume: float) -> str:
    """Formats volume numbers into a compact representation."""
    if volume >= 1000:
        return f"{volume / 1000:.1f}k"
    return f"{volume:,.0f}"

def plot_footprints(footprint_candles: List[FootprintCandle], title: str):
    """
    Plots a professional footprint chart with rectangle widths proportional to volume.
    """
    if not footprint_candles:
        print("No footprint candles to plot.")
        return

    fig, ax = plt.subplots(figsize=(18, 10))

    all_prices = [row.price for candle in footprint_candles for row in candle.footprint_data]
    if not all_prices: return
        
    min_price, max_price = min(c.low for c in footprint_candles), max(c.high for c in footprint_candles)
    ax.set_ylim(min_price * 0.999, max_price * 1.001)
    ax.set_xlim(-0.5, len(footprint_candles) - 0.5)

    bin_size = np.median(np.diff(sorted(list(set(all_prices))))) if len(all_prices) > 1 else 10.0

    for i, candle in enumerate(footprint_candles):
        if not candle.footprint_data: continue

        poc_row = max(candle.footprint_data, key=lambda row: row.bid_volume + row.ask_volume)
        poc_price_in_candle = poc_row.price
        
        # Normalize against the candle's POC volume to ensure the POC level has the max width.
        max_vol_in_candle = poc_row.bid_volume + poc_row.ask_volume

        for row_data in candle.footprint_data:
            font_weight = 'bold' if row_data.price == poc_price_in_candle else 'normal'

            # Calculate normalized width for each side (max width is 0.45 of the half-candle).
            ask_width = (row_data.ask_volume / max_vol_in_candle) * 0.45 if max_vol_in_candle > 0 else 0
            bid_width = (row_data.bid_volume / max_vol_in_candle) * 0.45 if max_vol_in_candle > 0 else 0
            
            # Draw Background Rectangles & Text
            # Bid background (Red), drawn from right-to-left.
            bid_rect = patches.Rectangle(
                (i - bid_width - 0.02, row_data.price - bin_size/2), bid_width, bin_size,
                facecolor='#E74C3C', alpha=0.6, lw=0
            )
            ax.add_patch(bid_rect)

            # Ask background (Green), drawn from left-to-right.
            ask_rect = patches.Rectangle(
                (i + 0.02, row_data.price - bin_size/2), ask_width, bin_size,
                facecolor='#2ECC71', alpha=0.6, lw=0
            )
            ax.add_patch(ask_rect)

            # Bid volume text.
            ax.text(i - 0.05, row_data.price, _format_volume(row_data.bid_volume), 
                    ha='right', va='center', fontsize=8, color='black', weight=font_weight)

            # Ask volume text.
            ax.text(i + 0.05, row_data.price, _format_volume(row_data.ask_volume), 
                    ha='left', va='center', fontsize=8, color='black', weight=font_weight)

    # Final Chart Formatting
    ax.set_title(title, fontsize=16)
    ax.set_ylabel("Price")
    ax.set_xlabel("Time")
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xticks(range(len(footprint_candles)))
    ax.set_xticklabels([c.timestamp.strftime('%H:%M') for c in footprint_candles], rotation=45, ha='right')
    
    ax.yaxis.set_major_locator(MaxNLocator(nbins=30, prune='both'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.show()