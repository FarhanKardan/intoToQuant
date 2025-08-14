"""
Bid-Ask Profile Visualization Module - Shows basic bid and ask volumes separately
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
import numpy as np

def plot_bid_ask_profiles(profiles: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots basic bid and ask volume comparison over time.
    """
    if not profiles:
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract data and calculate total volumes for each period
    timestamps = [p['timestamp'] for p in profiles]
    total_bid_volumes = []
    total_ask_volumes = []
    
    for profile in profiles:
        bid_volume = sum(item['volume'] for item in profile['bid_profile'])
        ask_volume = sum(item['volume'] for item in profile['ask_profile'])
        total_bid_volumes.append(bid_volume)
        total_ask_volumes.append(ask_volume)
    
    # Plot bid vs ask volume over time
    x_pos = np.arange(len(timestamps))
    width = 0.35
    
    ax.bar([t - width/2 for t in x_pos], total_bid_volumes, width, label='Bid Volume', color='blue', alpha=0.7)
    ax.bar([t + width/2 for t in x_pos], total_ask_volumes, width, label='Ask Volume', color='red', alpha=0.7)
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel('Volume')
    ax.set_xlabel('Time')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([t.strftime('%H:%M') for t in timestamps], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_bid_ask_volume_distribution(profiles: List[Dict[str, Any]], title: str, timeframe: str):
    """
    Plots the volume distribution for bid and ask separately across price levels.
    """
    if not profiles:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Collect all price levels and volumes
    all_bid_prices = set()
    all_ask_prices = set()
    
    for profile in profiles:
        for item in profile['bid_profile']:
            all_bid_prices.add(item['price_bin'])
        for item in profile['ask_profile']:
            all_ask_prices.add(item['price_bin'])
    
    # Sort price levels
    sorted_bid_prices = sorted(list(all_bid_prices), reverse=True)
    sorted_ask_prices = sorted(list(all_ask_prices))
    
    # Create volume matrices
    bid_volume_matrix = np.zeros((len(sorted_bid_prices), len(profiles)))
    ask_volume_matrix = np.zeros((len(sorted_ask_prices), len(profiles)))
    
    # Fill matrices
    for i, profile in enumerate(profiles):
        for item in profile['bid_profile']:
            price_idx = sorted_bid_prices.index(item['price_bin'])
            bid_volume_matrix[price_idx, i] = item['volume']
        
        for item in profile['ask_profile']:
            price_idx = sorted_ask_prices.index(item['price_bin'])
            ask_volume_matrix[price_idx, i] = item['volume']
    
    # Plot bid volume distribution
    im1 = ax1.imshow(bid_volume_matrix, aspect='auto', cmap='Blues', interpolation='none')
    ax1.set_title('Bid Volume Distribution', fontweight='bold')
    ax1.set_xlabel('Time Period')
    ax1.set_ylabel('Price Level')
    ax1.set_xticks(range(len(profiles)))
    ax1.set_xticklabels([p['timestamp'].strftime('%H:%M') for p in profiles], rotation=45)
    ax1.set_yticks(range(len(sorted_bid_prices)))
    ax1.set_yticklabels([f"${price:,.0f}" for price in sorted_bid_prices])
    
    # Plot ask volume distribution
    im2 = ax2.imshow(ask_volume_matrix, aspect='auto', cmap='Reds', interpolation='none')
    ax2.set_title('Ask Volume Distribution', fontweight='bold')
    ax2.set_xlabel('Time Period')
    ax2.set_ylabel('Price Level')
    ax2.set_xticks(range(len(profiles)))
    ax2.set_xticklabels([p['timestamp'].strftime('%H:%M') for p in profiles], rotation=45)
    ax2.set_yticks(range(len(sorted_ask_prices)))
    ax2.set_yticklabels([f"${price:,.0f}" for price in sorted_ask_prices])
    
    # Add colorbars
    cbar1 = fig.colorbar(im1, ax=ax1, pad=0.01)
    cbar1.set_label('Bid Volume')
    cbar2 = fig.colorbar(im2, ax=ax2, pad=0.01)
    cbar2.set_label('Ask Volume')
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
