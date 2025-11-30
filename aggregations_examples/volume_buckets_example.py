"""
Volume Buckets aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.volume_bucket_aggregator import VolumeBucketAggregator

def run_volume_buckets_example():
    """Run Volume Buckets aggregation on historical data"""
    print("=== Volume Buckets Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    bucket_agg = VolumeBucketAggregator("BTCUSDT")
    
    # Load data for 3 days
    start_date = "2024-05-01"
    end_date = "2024-05-03"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data (limited to 100000 ticks)
    record_count = 0
    max_ticks = 100000
    
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv", limit=max_ticks):
        bucket_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 1000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records (limited to {max_ticks})")
    
    # Generate volume buckets with 5000 size
    bucket_size = 500000.0
    
    print(f"\nGenerating Volume Buckets with size {bucket_size:.0f}...")
    buckets = bucket_agg.generate_volume_buckets(bucket_size)
    
    if buckets:
        print(f"Generated {len(buckets)} volume buckets")
    else:
        print("No volume buckets generated")
    
    print("\nVolume Buckets example completed!")
    
    # Simple visualization
    try:
        from visualization.volume_buckets_visualization import plot_volume_buckets
        print("\nCreating volume buckets visualization...")
        buckets = bucket_agg.generate_volume_buckets(bucket_size=bucket_size)
        if buckets:
            plot_volume_buckets(buckets, "BTCUSDT Volume Buckets ($5000)")
    except ImportError:
        print("Visualization module not available")

if __name__ == "__main__":
    run_volume_buckets_example() 