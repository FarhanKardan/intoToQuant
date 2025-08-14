"""
Delta Visualization Module - Shows basic delta (ask - bid) over time
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
import numpy as np

def plot_delta_metrics(deltas: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots basic delta over time showing buying vs selling pressure.
    """
    if not deltas:
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract data
    timestamps = [d['timestamp'] for d in deltas]
    delta_values = [d['delta'] for d in deltas]
    
    # Plot delta over time
    ax.plot(timestamps, delta_values, 'b-', linewidth=2, marker='o')
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    ax.fill_between(timestamps, delta_values, 0, 
                     where=[d > 0 for d in delta_values], alpha=0.3, color='green', label='Buying Pressure')
    ax.fill_between(timestamps, delta_values, 0, 
                     where=[d < 0 for d in delta_values], alpha=0.3, color='red', label='Selling Pressure')
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel('Delta (Buy - Sell)')
    ax.set_xlabel('Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.set_xticklabels([t.strftime('%H:%M') for t in timestamps], rotation=45)
    
    plt.tight_layout()
    plt.show()

def plot_cumulative_delta_series(deltas: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots the cumulative delta over time.
    """
    if not deltas:
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract data
    timestamps = [d['timestamp'] for d in deltas]
    delta_values = [d['delta'] for d in deltas]
    
    # Calculate cumulative delta
    cumulative_delta = np.cumsum(delta_values)
    
    # Plot cumulative delta
    ax.plot(timestamps, cumulative_delta, 'purple', linewidth=2, marker='o')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.7)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Cumulative Delta')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.set_xticklabels([t.strftime('%H:%M') for t in timestamps], rotation=45)
    
    plt.tight_layout()
    plt.show()
