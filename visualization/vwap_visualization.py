"""
Simple VWAP Visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List

def plot_vwap(vwap_data: List, title: str = "VWAP Analysis"):
    """Simple VWAP plot"""
    if not vwap_data:
        print("No VWAP data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'timestamp': vwap.timestamp,
        'vwap': vwap.vwap,
        'volume': vwap.volume
    } for vwap in vwap_data])
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # VWAP line
    ax1.plot(df['timestamp'], df['vwap'], 'b-', linewidth=2, label='VWAP')
    ax1.set_title(title)
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Volume bars
    ax2.bar(df['timestamp'], df['volume'], color='green', alpha=0.6)
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Time')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show() 