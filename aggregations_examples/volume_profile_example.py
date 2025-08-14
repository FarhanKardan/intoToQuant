"""
Volume Profile aggregation example - Final Version
Supports multiple visualization styles (classic, heatmap) and data limits.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.volume_profile_aggregator import VolumeProfileAggregator
from visualization.volume_profile_visualization import plot_classic_composite_profile

def run_volume_profile_example():
    print("=== Generating Profile | Timeframe: 1H | Style: classic ===")
    
    data_reader = DataReader("data")
    profile_agg = VolumeProfileAggregator("BTCUSDT", price_bin_size=10.0)
    
    print("Loading data (No Limit)...")

    for record_info in data_reader.iterate_records("2024-05-01", "2024-05-01", "*.csv", limit=None):
        profile_agg.add_tick(record_info['tick_data'])
    
    print("Data loaded. Generating profiles...")
    profiles = profile_agg.generate_profiles_by_timeframe(timeframe='1H')
    
    if not profiles:
        print("No profiles generated.")
        return

    print(f"Generated {len(profiles)} profiles. Creating 'classic' visualization...")

    try:
        plot_title = "BTCUSDT Composite Volume Profile (1H)"
        plot_classic_composite_profile(profiles, plot_title, '1H')
    except Exception as e:
        print(f"An error occurred during visualization: {e}")
        
    print("\nVisualization complete.")

if __name__ == "__main__":
    run_volume_profile_example()