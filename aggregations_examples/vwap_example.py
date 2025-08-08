"""
VWAP aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from exchange.models import TickData
from data_aggregator.vwap_aggregator import VWAPAggregator
from datetime import datetime

def run_vwap_example():
    """Run VWAP aggregation on historical data"""
    print("=== VWAP Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    vwap_agg = VWAPAggregator("BTCUSDT")
    
    # Load data for a specific date
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data (limited to 10000 ticks)
    record_count = 0
    max_ticks = 10000
    
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv", limit=max_ticks):
        vwap_agg.add_tick(record_info['tick_data'])
        record_count += 1
    
    print(f"Loaded {record_count} records")
    
    # Generate VWAP data
    timeframe = '5min'
    vwap_data = vwap_agg.generate_vwap(timeframe)
    
    if vwap_data:
        print(f"Generated {len(vwap_data)} VWAP periods")
    else:
        print("No VWAP data generated")
    
    print("\nVWAP example completed!")
    
    # VWAP visualization
    try:
        from visualization.vwap_visualization import plot_vwap
        print("\nCreating VWAP visualization...")
        if vwap_data:
            plot_vwap(vwap_data, "BTCUSDT VWAP Analysis")
    except ImportError:
        print("Visualization module not available")

if __name__ == "__main__":
    run_vwap_example() 