"""
OHLCV Visualization Module
"""

import matplotlib.pyplot as plt
import mplfinance as mpf
from typing import List
import pandas as pd

def plot_ohlcv(ohlcv_data: List, title: str = "OHLCV Candlesticks"):
    """Plot OHLCV candlestick chart using mplfinance"""
    if not ohlcv_data:
        print("No OHLCV data to plot")
        return
    
    # Convert to DataFrame with proper format for mplfinance
    df = pd.DataFrame([{
        'Open': ohlcv.open,
        'High': ohlcv.high,
        'Low': ohlcv.low,
        'Close': ohlcv.close,
        'Volume': ohlcv.volume
    } for ohlcv in ohlcv_data])
    
    # Set timestamp as index
    df.index = pd.to_datetime([ohlcv.timestamp for ohlcv in ohlcv_data])
    
    # Create candlestick chart
    mpf.plot(df, 
             type='candle',
             title=title,
             volume=True,
             style='charles',
             figsize=(12, 8),
             panel_ratios=(3, 1))

 