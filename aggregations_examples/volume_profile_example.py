"""
Volume Profile aggregation example - Final Version
Supports multiple visualization styles (classic, heatmap) and data limits.
"""
import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.volume_profile_aggregator import VolumeProfileAggregator
# Import both visualization functions
from visualization.volume_profile_visualization import plot_composite_profile, plot_classic_composite_profile

def run_volume_profile_example():
    parser = argparse.ArgumentParser(description="Generate and visualize a composite Volume Profile.")
    parser.add_argument('--timeframe', type=str, required=True, choices=['1H', '30min', '5min'], help="Timeframe for aggregation.")
    parser.add_argument('--limit', type=int, default=None, help="Limit number of records to process.")
    parser.add_argument(
        '--style',
        type=str,
        default='classic',
        choices=['classic', 'heatmap'],
        help="Visualization style: 'classic' for bars, 'heatmap' for colors."
    )
    args = parser.parse_args()

    print(f"=== Generating Profile | Timeframe: {args.timeframe} | Style: {args.style} ===")
    
    data_reader = DataReader("data")
    profile_agg = VolumeProfileAggregator("BTCUSDT", price_bin_size=10.0)
    
    limit_str = f"(Limit: {args.limit:,})" if args.limit else "(No Limit)"
    print(f"Loading data {limit_str}...")

    for record_info in data_reader.iterate_records("2024-05-01", "2024-05-01", "*.csv", limit=args.limit):
        profile_agg.add_tick(record_info['tick_data'])
    
    print("Data loaded. Generating profiles...")
    profiles = profile_agg.generate_profiles_by_timeframe(timeframe=args.timeframe)
    
    if not profiles:
        print("No profiles generated.")
        return

    print(f"Generated {len(profiles)} profiles. Creating '{args.style}' visualization...")

    try:
        plot_title = f"BTCUSDT Composite Volume Profile ({args.timeframe})"
        if args.style == 'classic':
            plot_classic_composite_profile(profiles, plot_title, args.timeframe)
        elif args.style == 'heatmap':
            plot_composite_profile(profiles, plot_title, args.timeframe)
    except Exception as e:
        print(f"An error occurred during visualization: {e}")
        
    print("\nVisualization complete.")

if __name__ == "__main__":
    run_volume_profile_example()