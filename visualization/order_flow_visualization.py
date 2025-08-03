"""
Simple Order Flow Visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List

def plot_order_flow(orderflow_data: List, title: str = "Order Flow Analysis"):
    """Simple order flow plot"""
    if not orderflow_data:
        print("No order flow data to plot")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'timestamp': flow.timestamp,
        'buy_volume': flow.buy_volume,
        'sell_volume': flow.sell_volume,
        'net_flow': flow.net_flow,
        'imbalance_ratio': flow.imbalance_ratio
    } for flow in orderflow_data])
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Net flow
    colors = ['green' if x >= 0 else 'red' for x in df['net_flow']]
    ax1.bar(df['timestamp'], df['net_flow'], color=colors, alpha=0.6)
    ax1.set_title(title)
    ax1.set_ylabel('Net Flow')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    
    # Imbalance ratio
    ax2.plot(df['timestamp'], df['imbalance_ratio'], 'purple', linewidth=2, label='Imbalance Ratio')
    ax2.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Neutral')
    ax2.set_ylabel('Imbalance Ratio')
    ax2.set_xlabel('Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show() 