"""
Statistics aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from exchange.models import TickData
from data_aggregator.stats_aggregator import StatsAggregator
from datetime import datetime

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
    
    # Load historical data
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        stats_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 100000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records")
    
    # Generate summary statistics
    print("\nGenerating summary statistics...")
    stats = stats_agg.get_summary_stats()
    
    if stats:
        print("Summary Statistics:")
        print(f"  Total Ticks: {stats.total_ticks}")
        print(f"  Total Volume: {stats.total_volume:.2f}")
        print(f"  Average Price: ${stats.avg_price:.2f}")
        print(f"  Price Range: ${stats.min_price:.2f} - ${stats.max_price:.2f}")
        print(f"  Price Volatility: {stats.price_volatility:.4f}")
        print(f"  Buy Volume: {stats.buy_volume:.2f}")
        print(f"  Sell Volume: {stats.sell_volume:.2f}")
        print(f"  Net Flow: {stats.net_flow:.2f}")
        print(f"  Buy/Sell Ratio: {stats.buy_sell_ratio:.2f}")
        print(f"  Average Trade Size: {stats.avg_trade_size:.2f}")
        print(f"  Large Trades (>1000): {stats.large_trades}")
        print(f"  Time Span: {stats.time_span}")
        
        # Simple visualization
        try:
            from visualization.stats_visualization import plot_summary_stats
            print("\nCreating statistics visualization...")
            plot_summary_stats(stats.__dict__, "BTCUSDT Summary Statistics")
        except ImportError:
            print("Visualization module not available")
    else:
        print("No statistics generated")
    
    print("\nStatistics example completed!")

if __name__ == "__main__":
    run_stats_example() 