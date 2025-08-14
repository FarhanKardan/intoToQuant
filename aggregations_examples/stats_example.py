"""
Statistics aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.stats_aggregator import StatsAggregator

def run_stats_example():
    """Run Statistics aggregation on historical data"""
    print("=== Statistics Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    stats_agg = StatsAggregator("BTCUSDT")
    
    # Load data for a specific date
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data (limited to 10000 ticks)
    record_count = 0
    max_ticks = 10000
    
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv", limit=max_ticks):
        stats_agg.add_tick(record_info['tick_data'])
        record_count += 1
    
    print(f"Loaded {record_count} records")
    
    # Generate summary statistics
    print("\nGenerating summary statistics...")
    stats = stats_agg.get_summary_stats()
    
    if stats:
        print("Summary Statistics:")
        print(f"  Total Ticks: {stats.get('total_ticks', 'N/A')}")
        print(f"  Total Volume: ${stats.get('total_volume', 0):,.2f}")
        print(f"  Average Price: ${stats.get('avg_price', 0):.2f}")
        print(f"  Time Span: {stats.get('time_span', 'N/A')}")
        
        # Volume statistics
        volume_stats = stats.get('volume_stats', {})
        print(f"\nVolume Statistics:")
        print(f"  Total Buy Volume: ${volume_stats.get('total_buy_volume', 0):,.2f}")
        print(f"  Total Sell Volume: ${volume_stats.get('total_sell_volume', 0):,.2f}")
        print(f"  Average Trade Size: ${volume_stats.get('avg_trade_size', 0):,.2f}")
        print(f"  Largest Trade: ${volume_stats.get('largest_trade', 0):,.2f}")
        
        
        # Trade distribution
        trade_dist = stats.get('trade_distribution', {})
        print(f"\nTrade Distribution:")
        print(f"  Buy Trades: {trade_dist.get('buy_trades', 0)}")
        print(f"  Sell Trades: {trade_dist.get('sell_trades', 0)}")
        
        # Large orders categorization (>100K USD)
        large_orders = stats.get('large_orders', {})
        print(f"\nLarge Orders (>$100K USD):")
        print(f"  Buy Orders: {large_orders.get('buy_orders_above_100k', 0)}")
        print(f"  Sell Orders: {large_orders.get('sell_orders_above_100k', 0)}")
        print(f"  Total Large Orders: {large_orders.get('total_large_orders', 0)}")
        print(f"  Large Buy Volume: ${large_orders.get('large_buy_volume', 0):,.2f}")
        print(f"  Large Sell Volume: ${large_orders.get('large_sell_volume', 0):,.2f}")
        
        # Simple visualization
        try:
            from visualization.stats_visualization import plot_summary_stats
            print("\nCreating statistics visualization...")
            plot_summary_stats(stats, "BTCUSDT Summary Statistics")
        except ImportError:
            print("Visualization module not available")
    else:
        print("No statistics generated")
    
    print("\nStatistics example completed!")

if __name__ == "__main__":
    run_stats_example() 