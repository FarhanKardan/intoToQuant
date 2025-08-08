"""
VWAP Visualization using mplfinance
"""

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from typing import List

def plot_vwap(vwap_data: List, title: str = "VWAP Analysis"):
    """Plot VWAP using mplfinance"""
    if not vwap_data:
        print("No VWAP data to plot")
        return
    
    # Convert to DataFrame with proper format for mplfinance
    df = pd.DataFrame([{
        'Open': vwap.vwap,  # Use VWAP as both open and close for line chart
        'High': vwap.vwap,
        'Low': vwap.vwap,
        'Close': vwap.vwap,
        'Volume': vwap.volume
    } for vwap in vwap_data])
    
    # Set timestamp as index
    df.index = pd.to_datetime([vwap.timestamp for vwap in vwap_data])
    
    # Create VWAP chart with volume
    mpf.plot(df, 
             type='line',  # Use line chart for VWAP
             title=title,
             volume=True,
             style='charles',
             figsize=(12, 8),
             panel_ratios=(3, 1),
             ylabel='VWAP Price',
             ylabel_lower='Volume')

def plot_vwap_with_candles(vwap_data: List, ohlcv_data: List, title: str = "VWAP + Candlesticks"):
    """Plot VWAP line overlaid on OHLCV candlesticks"""
    if not vwap_data or not ohlcv_data:
        print("No data to plot")
        return
    
    # Convert VWAP to DataFrame
    vwap_df = pd.DataFrame([{
        'Open': vwap.vwap,
        'High': vwap.vwap,
        'Low': vwap.vwap,
        'Close': vwap.vwap,
        'Volume': vwap.volume
    } for vwap in vwap_data])
    vwap_df.index = pd.to_datetime([vwap.timestamp for vwap in vwap_data])
    
    # Convert OHLCV to DataFrame
    ohlcv_df = pd.DataFrame([{
        'Open': ohlcv.open,
        'High': ohlcv.high,
        'Low': ohlcv.low,
        'Close': ohlcv.close,
        'Volume': ohlcv.volume
    } for ohlcv in ohlcv_data])
    ohlcv_df.index = pd.to_datetime([ohlcv.timestamp for ohlcv in ohlcv_data])
    
    # Create custom style for VWAP line
    vwap_style = mpf.make_mpf_style(
        base_mpf_style='charles',
        marketcolors=mpf.make_marketcolors(
            up='green', down='red',
            edge='inherit',
            wick='inherit',
            volume='blue'
        ),
        gridstyle='',
        y_on_right=False
    )
    
    # Plot candlesticks with VWAP overlay
    mpf.plot(ohlcv_df,
             type='candle',
             title=title,
             volume=True,
             style=vwap_style,
             figsize=(15, 10),
             panel_ratios=(3, 1),
             addplot=[
                 mpf.make_addplot(vwap_df['Close'], color='orange', width=2, label='VWAP')
             ],
             savefig='vwap_candles.png') 