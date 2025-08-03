"""
Order Flow aggregation example using historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from exchange.models import TickData
from data_aggregator.order_flow_aggregator import OrderFlowAggregator
from datetime import datetime

def run_order_flow_example():
    """Run Order Flow aggregation on historical data"""
    print("=== Order Flow Aggregation Example ===")
    
    # Initialize components
    data_reader = DataReader("data")
    flow_agg = OrderFlowAggregator("BTCUSDT")
    
    # Load data for a specific date
    start_date = "2024-05-01"
    end_date = "2024-05-01"
    
    print(f"Loading data from {start_date} to {end_date}...")
    
    # Load historical data
    record_count = 0
    for record_info in data_reader.iterate_records(start_date, end_date, "*.csv"):
        flow_agg.add_tick(record_info['tick_data'])
        record_count += 1
        
        # Progress indicator
        if record_count % 100000 == 0:
            print(f"Loaded {record_count} records...")
    
    print(f"Successfully loaded {record_count} records")
    
    # Generate order flow data with different timeframes
    timeframes = ['1min', '5min', '15min', '1H']
    
    for timeframe in timeframes:
        print(f"\nGenerating Order Flow with {timeframe} timeframe...")
        orderflow_data = flow_agg.generate_order_flow(timeframe)
        
        if orderflow_data:
            print(f"Generated {len(orderflow_data)} order flow periods")
            
            # Show first and last periods
            first = orderflow_data[0]
            last = orderflow_data[-1]
            
            print(f"First period ({first.timestamp}):")
            print(f"  Buy Volume: {first.buy_volume:.2f}")
            print(f"  Sell Volume: {first.sell_volume:.2f}")
            print(f"  Net Flow: {first.net_flow:.2f}")
            print(f"  Total Trades: {first.total_trades}")
            print(f"  Average Trade Size: {first.avg_trade_size:.2f}")
            print(f"  Large Trades: {first.large_trades}")
            print(f"  Imbalance Ratio: {first.imbalance_ratio:.2f}")
            
            print(f"Last period ({last.timestamp}):")
            print(f"  Buy Volume: {last.buy_volume:.2f}")
            print(f"  Sell Volume: {last.sell_volume:.2f}")
            print(f"  Net Flow: {last.net_flow:.2f}")
            print(f"  Total Trades: {last.total_trades}")
            print(f"  Average Trade Size: {last.avg_trade_size:.2f}")
            print(f"  Large Trades: {last.large_trades}")
            print(f"  Imbalance Ratio: {last.imbalance_ratio:.2f}")
            
            # Calculate some statistics
            total_buy_volume = sum(o.buy_volume for o in orderflow_data)
            total_sell_volume = sum(o.sell_volume for o in orderflow_data)
            total_net_flow = sum(o.net_flow for o in orderflow_data)
            total_trades = sum(o.total_trades for o in orderflow_data)
            avg_trade_size = sum(o.avg_trade_size for o in orderflow_data) / len(orderflow_data)
            total_large_trades = sum(o.large_trades for o in orderflow_data)
            
            print(f"Summary:")
            print(f"  Total buy volume: {total_buy_volume:.2f}")
            print(f"  Total sell volume: {total_sell_volume:.2f}")
            print(f"  Total net flow: {total_net_flow:.2f}")
            print(f"  Total trades: {total_trades}")
            print(f"  Average trade size: {avg_trade_size:.2f}")
            print(f"  Total large trades: {total_large_trades}")
            
            # Show order flow progression
            print(f"Order flow progression (first 5 periods):")
            for i, flow in enumerate(orderflow_data[:5]):
                print(f"  Period {i+1}: Buy={flow.buy_volume:.0f}, Sell={flow.sell_volume:.0f}, Net={flow.net_flow:.0f}")
        else:
            print("No order flow data generated")
    
    print("\nOrder Flow example completed!")

if __name__ == "__main__":
    run_order_flow_example() 