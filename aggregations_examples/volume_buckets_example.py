"""
Volume Buckets aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from exchange.models import TickData
from data_aggregator.volume_bucket_aggregator import VolumeBucketAggregator
from datetime import datetime

def run_volume_buckets_example():
    """Run Volume Buckets aggregation on historical data"""
    print("=== Volume Buckets Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    bucket_agg = VolumeBucketAggregator("BTCUSDT")
    
    # Load data for a specific date
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        bucket_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 100000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records")
    
    # Generate volume buckets with different sizes
    bucket_sizes = [1000.0, 5000.0, 10000.0, 50000.0]
    
    for bucket_size in bucket_sizes:
        print(f"\nGenerating Volume Buckets with size {bucket_size:.0f}...")
        buckets = bucket_agg.generate_volume_buckets(bucket_size)
        
        if buckets:
            print(f"Generated {len(buckets)} volume buckets")
            
            # Show first and last buckets
            first = buckets[0]
            last = buckets[-1]
            
            print(f"First bucket:")
            print(f"  Total Volume: {first.total_volume:.2f}")
            print(f"  Average Price: ${first.avg_price:.2f}")
            print(f"  Buy Volume: {first.buy_volume:.2f}")
            print(f"  Sell Volume: {first.sell_volume:.2f}")
            print(f"  Net Flow: {first.net_flow:.2f}")
            
            print(f"Last bucket:")
            print(f"  Total Volume: {last.total_volume:.2f}")
            print(f"  Average Price: ${last.avg_price:.2f}")
            print(f"  Buy Volume: {last.buy_volume:.2f}")
            print(f"  Sell Volume: {last.sell_volume:.2f}")
            print(f"  Net Flow: {last.net_flow:.2f}")
            
            # Calculate some statistics
            total_volume = sum(b.total_volume for b in buckets)
            avg_price = sum(b.avg_price for b in buckets) / len(buckets)
            total_buy_volume = sum(b.buy_volume for b in buckets)
            total_sell_volume = sum(b.sell_volume for b in buckets)
            total_net_flow = sum(b.net_flow for b in buckets)
            
            print(f"Summary:")
            print(f"  Total volume across buckets: {total_volume:.2f}")
            print(f"  Average price: ${avg_price:.2f}")
            print(f"  Total buy volume: {total_buy_volume:.2f}")
            print(f"  Total sell volume: {total_sell_volume:.2f}")
            print(f"  Total net flow: {total_net_flow:.2f}")
            
            # Show bucket progression
            print(f"Bucket progression (first 5 buckets):")
            for i, bucket in enumerate(buckets[:5]):
                print(f"  Bucket {i+1}: Vol={bucket.total_volume:.0f}, Avg=${bucket.avg_price:.2f}, Net={bucket.net_flow:.0f}")
        else:
            print("No volume buckets generated")
    
    print("\nVolume Buckets example completed!")

if __name__ == "__main__":
    run_volume_buckets_example() 