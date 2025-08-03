"""
Run all aggregation examples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aggregations_examples.ohlcv_example import run_ohlcv_example
from aggregations_examples.vwap_example import run_vwap_example
from aggregations_examples.volume_buckets_example import run_volume_buckets_example
from aggregations_examples.order_flow_example import run_order_flow_example

def main():
    """Run all aggregation examples"""
    print("Running All Aggregation Examples")
    print("=" * 50)
    
    examples = [
        ("OHLCV Aggregation", run_ohlcv_example),
        ("VWAP Aggregation", run_vwap_example),
        ("Volume Buckets", run_volume_buckets_example),
        ("Order Flow", run_order_flow_example)
    ]
    
    for name, example_func in examples:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            example_func()
        except Exception as e:
            print(f"Error running {name}: {e}")
    
    print("\n" + "="*50)
    print("All examples completed!")

if __name__ == "__main__":
    main() 