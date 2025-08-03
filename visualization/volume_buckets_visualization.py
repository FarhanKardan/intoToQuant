"""
Simple Volume Buckets Visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List

def plot_volume_buckets(bucket_data: List, title: str = "Volume Buckets"):
    """Simple volume buckets plot"""
    if not bucket_data:
        print("No volume bucket data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'timestamp': bucket.timestamp,
        'total_volume': bucket.total_volume,
        'avg_price': bucket.avg_price,
        'buy_volume': bucket.buy_volume,
        'sell_volume': bucket.sell_volume,
        'net_flow': bucket.net_flow
    } for bucket in bucket_data])
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Average price
    ax1.plot(df['timestamp'], df['avg_price'], 'r-', linewidth=2, label='Avg Price')
    ax1.set_title(title)
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Buy vs Sell volume
    ax2.bar(df['timestamp'], df['buy_volume'], color='green', alpha=0.6, label='Buy Volume')
    ax2.bar(df['timestamp'], -df['sell_volume'], color='red', alpha=0.6, label='Sell Volume')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show() 