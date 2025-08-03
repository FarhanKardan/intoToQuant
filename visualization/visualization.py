"""
Simple data visualization for trading data aggregations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def plot_ohlcv(ohlcv_data: List, title: str = "OHLCV Candlesticks"):
    """Plot OHLCV candlestick data"""
    if not ohlcv_data:
        print("No OHLCV data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'timestamp': o.timestamp,
            'open': o.open,
            'high': o.high,
            'low': o.low,
            'close': o.close,
            'volume': o.volume
        } for o in ohlcv_data
    ])
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
    
    # Plot candlesticks
    for i, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        alpha = 0.7
        
        # Body
        ax1.bar(i, row['close'] - row['open'], bottom=row['open'], 
                color=color, alpha=alpha, width=0.8)
        
        # Wicks
        ax1.plot([i, i], [row['low'], row['high']], color='black', linewidth=1)
    
    ax1.set_title(title)
    ax1.set_ylabel('Price')
    ax1.grid(True, alpha=0.3)
    
    # Plot volume
    ax2.bar(range(len(df)), df['volume'], color='blue', alpha=0.6)
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Time Period')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_vwap(vwap_data: List, title: str = "VWAP Analysis"):
    """Plot VWAP data"""
    if not vwap_data:
        print("No VWAP data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'timestamp': v.timestamp,
            'vwap': v.vwap,
            'volume': v.volume,
            'cumulative_volume': v.cumulative_volume
        } for v in vwap_data
    ])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot VWAP
    ax1.plot(df.index, df['vwap'], 'b-', linewidth=2, label='VWAP')
    ax1.set_title(title)
    ax1.set_ylabel('VWAP Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot cumulative volume
    ax2.plot(df.index, df['cumulative_volume'], 'g-', linewidth=2)
    ax2.set_ylabel('Cumulative Volume')
    ax2.set_xlabel('Time Period')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_volume_buckets(buckets: List, title: str = "Volume Bucket Analysis"):
    """Plot volume bucket data"""
    if not buckets:
        print("No volume bucket data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'bucket': b.bucket_count,
            'total_volume': b.total_volume,
            'avg_price': b.avg_price,
            'buy_volume': b.buy_volume,
            'sell_volume': b.sell_volume,
            'net_flow': b.net_flow
        } for b in buckets
    ])
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Volume per bucket
    ax1.bar(df['bucket'], df['total_volume'], color='skyblue', alpha=0.7)
    ax1.set_title('Volume per Bucket')
    ax1.set_ylabel('Volume')
    ax1.grid(True, alpha=0.3)
    
    # Average price per bucket
    ax2.plot(df['bucket'], df['avg_price'], 'r-o', linewidth=2)
    ax2.set_title('Average Price per Bucket')
    ax2.set_ylabel('Price')
    ax2.grid(True, alpha=0.3)
    
    # Buy vs Sell volume
    x = np.arange(len(df))
    width = 0.35
    ax3.bar(x - width/2, df['buy_volume'], width, label='Buy Volume', color='green', alpha=0.7)
    ax3.bar(x + width/2, df['sell_volume'], width, label='Sell Volume', color='red', alpha=0.7)
    ax3.set_title('Buy vs Sell Volume')
    ax3.set_ylabel('Volume')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Net flow
    colors = ['green' if x >= 0 else 'red' for x in df['net_flow']]
    ax4.bar(df['bucket'], df['net_flow'], color=colors, alpha=0.7)
    ax4.set_title('Net Flow (Buy - Sell)')
    ax4.set_ylabel('Net Flow')
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_order_flow(orderflow_data: List, title: str = "Order Flow Analysis"):
    """Plot order flow data"""
    if not orderflow_data:
        print("No order flow data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'timestamp': o.timestamp,
            'buy_volume': o.buy_volume,
            'sell_volume': o.sell_volume,
            'net_flow': o.net_flow,
            'total_trades': o.total_trades,
            'avg_trade_size': o.avg_trade_size,
            'imbalance_ratio': o.imbalance_ratio,
            'large_trades': o.large_trades
        } for o in orderflow_data
    ])
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Buy vs Sell volume over time
    ax1.plot(df.index, df['buy_volume'], 'g-', label='Buy Volume', linewidth=2)
    ax1.plot(df.index, df['sell_volume'], 'r-', label='Sell Volume', linewidth=2)
    ax1.set_title('Buy vs Sell Volume Over Time')
    ax1.set_ylabel('Volume')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Net flow
    colors = ['green' if x >= 0 else 'red' for x in df['net_flow']]
    ax2.bar(df.index, df['net_flow'], color=colors, alpha=0.7)
    ax2.set_title('Net Flow Over Time')
    ax2.set_ylabel('Net Flow')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # Trade count
    ax3.plot(df.index, df['total_trades'], 'b-o', linewidth=2)
    ax3.set_title('Total Trades Over Time')
    ax3.set_ylabel('Number of Trades')
    ax3.grid(True, alpha=0.3)
    
    # Imbalance ratio
    ax4.plot(df.index, df['imbalance_ratio'], 'purple', linewidth=2)
    ax4.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Neutral')
    ax4.set_title('Buy/Sell Imbalance Ratio')
    ax4.set_ylabel('Ratio (Buy/Sell)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_summary_stats(stats: Dict, title: str = "Summary Statistics"):
    """Plot summary statistics"""
    if not stats:
        print("No statistics to plot")
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Price distribution
    price_range = stats['price_range']
    ax1.bar(['Min', 'Max', 'Avg'], 
            [price_range['min'], price_range['max'], stats['avg_price']], 
            color=['red', 'green', 'blue'], alpha=0.7)
    ax1.set_title('Price Statistics')
    ax1.set_ylabel('Price')
    ax1.grid(True, alpha=0.3)
    
    # Volume statistics
    volume_stats = stats['volume_stats']
    ax2.bar(['Buy Vol', 'Sell Vol', 'Avg Trade'], 
            [volume_stats['total_buy_volume'], volume_stats['total_sell_volume'], volume_stats['avg_trade_size']], 
            color=['green', 'red', 'orange'], alpha=0.7)
    ax2.set_title('Volume Statistics')
    ax2.set_ylabel('Volume')
    ax2.grid(True, alpha=0.3)
    
    # Trade distribution
    trade_dist = stats['trade_distribution']
    ax3.pie([trade_dist['buy_trades'], trade_dist['sell_trades']], 
            labels=['Buy Trades', 'Sell Trades'], 
            colors=['green', 'red'], autopct='%1.1f%%')
    ax3.set_title('Trade Distribution')
    
    # Key metrics
    metrics = ['Total Ticks', 'Total Volume', 'Largest Trade']
    values = [stats['total_ticks'], stats['total_volume'], volume_stats['largest_trade']]
    ax4.bar(metrics, values, color=['blue', 'orange', 'purple'], alpha=0.7)
    ax4.set_title('Key Metrics')
    ax4.set_ylabel('Value')
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def create_sample_visualizations():
    """Create sample visualizations with mock data"""
    print("Creating sample visualizations...")
    
    # Sample OHLCV data
    sample_ohlcv = []
    for i in range(20):
        sample_ohlcv.append(type('OHLCV', (), {
            'timestamp': datetime.now() + timedelta(minutes=i),
            'open': 50000 + i * 10,
            'high': 50000 + i * 15,
            'low': 50000 + i * 5,
            'close': 50000 + i * 12,
            'volume': 100 + i * 20
        })())
    
    # Sample VWAP data
    sample_vwap = []
    for i in range(20):
        sample_vwap.append(type('VWAPData', (), {
            'timestamp': datetime.now() + timedelta(minutes=i),
            'vwap': 50000 + i * 8,
            'volume': 100 + i * 15,
            'cumulative_volume': (100 + i * 15) * (i + 1),
            'cumulative_pv': 0
        })())
    
    # Sample volume buckets
    sample_buckets = []
    for i in range(10):
        sample_buckets.append(type('VolumeBucket', (), {
            'timestamp': datetime.now() + timedelta(minutes=i),
            'bucket_size': 1000,
            'bucket_count': i,
            'total_volume': 1000 + i * 100,
            'avg_price': 50000 + i * 5,
            'buy_volume': 600 + i * 50,
            'sell_volume': 400 + i * 50,
            'net_flow': 200 + i * 10
        })())
    
    # Sample order flow
    sample_orderflow = []
    for i in range(20):
        sample_orderflow.append(type('OrderFlow', (), {
            'timestamp': datetime.now() + timedelta(minutes=i),
            'buy_volume': 800 + i * 20,
            'sell_volume': 600 + i * 15,
            'net_flow': 200 + i * 5,
            'buy_trades': 0,
            'sell_trades': 0,
            'total_trades': 50 + i * 5,
            'avg_trade_size': 20 + i,
            'large_trades': 2 + i % 3,
            'imbalance_ratio': 1.2 + i * 0.1
        })())
    
    # Sample stats
    sample_stats = {
        'total_ticks': 1000,
        'time_span': timedelta(hours=1),
        'total_volume': 50000,
        'avg_price': 50000,
        'price_range': {'min': 49500, 'max': 50500, 'std': 200},
        'volume_stats': {
            'total_buy_volume': 30000,
            'total_sell_volume': 20000,
            'avg_trade_size': 50,
            'largest_trade': 500
        },
        'trade_distribution': {
            'buy_trades': 600,
            'sell_trades': 400
        }
    }
    
    # Create plots
    plot_ohlcv(sample_ohlcv, "Sample OHLCV Data")
    plot_vwap(sample_vwap, "Sample VWAP Data")
    plot_volume_buckets(sample_buckets, "Sample Volume Buckets")
    plot_order_flow(sample_orderflow, "Sample Order Flow")
    plot_summary_stats(sample_stats, "Sample Summary Statistics")

def main():
    """Main function to run visualizations"""
    print("Trading Data Visualization Examples")
    print("=" * 40)
    
    # Create sample visualizations
    create_sample_visualizations()
    
    print("Visualization examples completed!")

if __name__ == "__main__":
    main() 