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
    
    # Load historical data
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        vwap_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 100000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records")
    
    # Generate VWAP data with different timeframes
    timeframes = ['1min', '5min', '15min', '1H']
    
    for timeframe in timeframes:
        print(f"\nGenerating VWAP with {timeframe} timeframe...")
        vwap_data = vwap_agg.generate_vwap(timeframe)
        
        if vwap_data:
            print(f"Generated {len(vwap_data)} VWAP periods")
            
            # Show first and last periods
            first = vwap_data[0]
            last = vwap_data[-1]
            
            print(f"First period ({first.timestamp}):")
            print(f"  VWAP: ${first.vwap:.2f}")
            print(f"  Volume: {first.volume:.2f}")
            print(f"  Cumulative Volume: {first.cumulative_volume:.2f}")
            
            print(f"Last period ({last.timestamp}):")
            print(f"  VWAP: ${last.vwap:.2f}")
            print(f"  Volume: {last.volume:.2f}")
            print(f"  Cumulative Volume: {last.cumulative_volume:.2f}")
            
            # Calculate some statistics
            total_volume = sum(v.volume for v in vwap_data)
            avg_vwap = sum(v.vwap for v in vwap_data) / len(vwap_data)
            vwap_change = last.vwap - first.vwap
            vwap_change_pct = (vwap_change / first.vwap) * 100
            
            print(f"Summary:")
            print(f"  Total volume: {total_volume:.2f}")
            print(f"  Average VWAP: ${avg_vwap:.2f}")
            print(f"  VWAP change: ${vwap_change:.2f} ({vwap_change_pct:.2f}%)")
            
            # Show VWAP progression
            print(f"VWAP progression (first 5 periods):")
            for i, vwap in enumerate(vwap_data[:5]):
                print(f"  Period {i+1}: ${vwap.vwap:.2f} (Vol: {vwap.volume:.2f})")
        else:
            print("No VWAP data generated")
    
    print("\nVWAP example completed!")
    
    # Simple visualization
    try:
        from visualization.vwap_visualization import plot_vwap
        print("\nCreating VWAP visualization...")
        # Use 5min data for visualization
        vwap_data = vwap_agg.generate_vwap('5min')
        if vwap_data:
            plot_vwap(vwap_data, "BTCUSDT VWAP Analysis")
    except ImportError:
        print("Visualization module not available")

if __name__ == "__main__":
    run_vwap_example() 