"""
Footprint Chart example - Supports both Time-based and Range-based aggregation.
"""
import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.footprint_aggregator import FootprintAggregator
from visualization.footprint_visualization import plot_footprints

def run_footprint_example():
    parser = argparse.ArgumentParser(description="Generate and visualize Footprint charts.")
    parser.add_argument('--mode', type=str, default='time', choices=['time', 'range'], help="Aggregation mode: time-based or range-based.")
    parser.add_argument('--timeframe', type=str, default='5min', help="Timeframe for 'time' mode (e.g., '1min', '5min').")
    parser.add_argument('--range_levels', type=int, default=8, help="Number of price levels for a candle in 'range' mode.")
    parser.add_argument('--limit', type=int, default=50000, help="Limit the number of records to process.")
    parser.add_argument('--bin_size', type=float, default=10.0, help="The size to group price levels by.")
    
    args = parser.parse_args()
    
    print(f"=== Generating Footprint Chart | Mode: {args.mode} ===")
    
    footprint_agg = FootprintAggregator("BTCUSDT", price_bin_size=args.bin_size)
    data_reader = DataReader("data")
    
    print(f"Loading data (Limit: {args.limit:,})...")
    for record_info in data_reader.iterate_records("2024-05-01", "2024-05-01", "*.csv", limit=args.limit):
        footprint_agg.add_tick(record_info['tick_data'])
    
    print("Data loaded. Generating footprints...")
    
    if args.mode == 'time':
        footprint_candles = footprint_agg.generate_footprints(timeframe=args.timeframe)
        plot_title = f"Footprint Chart ({args.timeframe} | ${args.bin_size} Bins)"
    elif args.mode == 'range':
        footprint_candles = footprint_agg.generate_range_footprints(range_levels=args.range_levels)
        plot_title = f"Footprint Chart ({args.range_levels} Price Levels | ${args.bin_size} Bins)"
    else:
        footprint_candles = []
        plot_title = "Unknown Mode"

    if not footprint_candles:
        print("No footprint data generated.")
        return

    print(f"Generated {len(footprint_candles)} footprint candles. Visualizing...")

    try:
        plot_footprints(footprint_candles, plot_title)
    except Exception as e:
        print(f"An error occurred during visualization: {e}")

if __name__ == "__main__":
    run_footprint_example()