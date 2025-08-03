"""
OHLCV Visualization Module
"""

import matplotlib.pyplot as plt
from typing import List
import pandas as pd

def plot_ohlcv(ohlcv_data: List, title: str = "OHLCV Candlesticks"):
    """Simple OHLCV plot"""
    if not ohlcv_data:
        print("No OHLCV data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'timestamp': ohlcv.timestamp,
        'open': ohlcv.open,
        'high': ohlcv.high,
        'low': ohlcv.low,
        'close': ohlcv.close,
        'volume': ohlcv.volume
    } for ohlcv in ohlcv_data])
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Close price line
    ax1.plot(df['timestamp'], df['close'], 'b-', linewidth=2, label='Close Price')
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

 