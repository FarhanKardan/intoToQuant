"""
Simple Stats Visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

def plot_summary_stats(stats: Dict, title: str = "Summary Statistics"):
    """Simple summary stats plot"""
    if not stats:
        print("No stats data to plot")
        return
    
    # Create bar chart of key metrics
    metrics = ['total_ticks', 'total_volume', 'avg_price', 'price_volatility']
    values = [stats.get(metric, 0) for metric in metrics]
    
    # Clean up metric names for display
    labels = ['Total Ticks', 'Total Volume', 'Avg Price', 'Price Volatility']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'], alpha=0.7)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                f'{value:.2f}', ha='center', va='bottom')
    
    plt.title(title)
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show() 