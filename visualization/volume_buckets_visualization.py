"""
Simple Volume Buckets Visualization
"""

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from typing import List

def plot_volume_buckets(bucket_data: List, title: str = "Volume Buckets"):
    """Plot volume buckets with OHLCV candles using mplfinance"""
    if not bucket_data:
        print("No volume bucket data to plot")
        return
    
    # Convert to DataFrame with OHLCV format for mplfinance
    df = pd.DataFrame([{
        'Open': bucket.open_price,
        'High': bucket.high_price,
        'Low': bucket.low_price,
        'Close': bucket.close_price,
        'Volume': bucket.total_volume
    } for bucket in bucket_data])
    
    # Set timestamp as index
    df.index = pd.to_datetime([bucket.timestamp for bucket in bucket_data])
    
    # Create candlestick chart
    mpf.plot(df, 
             type='candle',
             title=title,
             volume=True,
             style='charles',
             figsize=(12, 8),
             panel_ratios=(3, 1)) 