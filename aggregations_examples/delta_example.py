"""
Delta aggregation example - Shows basic delta (ask - bid) over time
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.delta_aggregator import DeltaAggregator
from visualization.delta_visualization import plot_delta_metrics, plot_cumulative_delta_series

def run_delta_example():
    print("=== Generating Delta Metrics | Timeframe: 1H | Plot: both ===")
    
    data_reader = DataReader("data")
    delta_agg = DeltaAggregator("BTCUSDT")
    
    print("Loading data (No Limit)...")

    for record_info in data_reader.iterate_records("2024-05-01", "2024-05-01", "*.csv", limit=None):
        delta_agg.add_tick(record_info['tick_data'])
    
    print("Data loaded. Generating delta metrics...")
    deltas = delta_agg.generate_delta_by_timeframe(timeframe='1H')
    
    if not deltas:
        print("No delta metrics generated.")
        return

    try:
        plot_title = "BTCUSDT Delta Metrics (1H)"
        
        print("Creating delta metrics overview...")
        plot_delta_metrics(deltas, plot_title, '1H')
        
        print("Creating cumulative delta series...")
        plot_cumulative_delta_series(deltas, "BTCUSDT Cumulative Delta Series (1H)", '1H')
            
    except Exception as e:
        print(f"An error occurred during visualization: {e}")
        
    print("\nDelta analysis complete.")

if __name__ == "__main__":
    run_delta_example()
