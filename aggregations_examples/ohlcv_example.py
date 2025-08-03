"""
OHLCV aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from exchange.models import TickData
from data_aggregator.ohlcv_aggregator import OHLCVAggregator
from datetime import datetime

def run_ohlcv_example():
    """Run OHLCV aggregation on historical data"""
    print("=== OHLCV Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    ohlcv_agg = OHLCVAggregator("BTCUSDT")
    
    # Load data for a specific date
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        ohlcv_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 100000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records")
    
    # Generate OHLCV data with different timeframes
    timeframes = ['1min', '5min', '15min', '1H']
    
    for timeframe in timeframes:
        print(f"\nGenerating OHLCV with {timeframe} timeframe...")
        ohlcv_data = ohlcv_agg.generate_ohlcv(timeframe)
        
        if ohlcv_data:
            print(f"Generated {len(ohlcv_data)} OHLCV periods")
            
            # Show first and last periods
            first = ohlcv_data[0]
            last = ohlcv_data[-1]
            
            print(f"First period ({first.timestamp}):")
            print(f"  O: ${first.open:.2f} H: ${first.high:.2f} L: ${first.low:.2f} C: ${first.close:.2f}")
            print(f"  Volume: {first.volume:.2f} Trades: {first.trade_count}")
            
            print(f"Last period ({last.timestamp}):")
            print(f"  O: ${last.open:.2f} H: ${last.high:.2f} L: ${last.low:.2f} C: ${last.close:.2f}")
            print(f"  Volume: {last.volume:.2f} Trades: {last.trade_count}")
            
            # Calculate some statistics
            total_volume = sum(o.volume for o in ohlcv_data)
            avg_volume = total_volume / len(ohlcv_data)
            price_change = last.close - first.open
            price_change_pct = (price_change / first.open) * 100
            
            print(f"Summary:")
            print(f"  Total volume: {total_volume:.2f}")
            print(f"  Average volume per period: {avg_volume:.2f}")
            print(f"  Price change: ${price_change:.2f} ({price_change_pct:.2f}%)")
        else:
            print("No OHLCV data generated")
    
    print("\nOHLCV example completed!")
    
    # Simple visualization
    try:
        from visualization.ohlcv_visualization import plot_ohlcv
        print("\nCreating OHLCV visualization...")
        # Use 5min data for visualization
        ohlcv_data = ohlcv_agg.generate_ohlcv('5min')
        if ohlcv_data:
            plot_ohlcv(ohlcv_data, "BTCUSDT OHLCV Analysis")
    except ImportError:
        print("Visualization module not available")

if __name__ == "__main__":
    run_ohlcv_example() 