"""
Bid-Ask Profile aggregation example - Shows basic bid and ask volumes separately
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.data_reader import DataReader
from data_aggregator.bid_ask_profile_aggregator import BidAskProfileAggregator
from visualization.bid_ask_profile_visualization import plot_bid_ask_profiles, plot_bid_ask_volume_distribution

def run_bid_ask_profile_example():
    print("=== Generating Bid-Ask Profiles | Timeframe: 1H | Plot: both ===")
    
    data_reader = DataReader("data")
    bid_ask_agg = BidAskProfileAggregator("BTCUSDT", price_bin_size=10.0)
    
    print("Loading data (No Limit)...")

    for record_info in data_reader.iterate_records("2024-05-01", "2024-05-01", "*.csv", limit=None):
        bid_ask_agg.add_tick(record_info['tick_data'])
    
    print("Data loaded. Generating bid-ask profiles...")
    profiles = bid_ask_agg.generate_bid_ask_profiles_by_timeframe(timeframe='1H')
    
    if not profiles:
        print("No bid-ask profiles generated.")
        return

    print(f"Generated {len(profiles)} bid-ask profiles. Creating visualizations...")

    try:
        plot_title = "BTCUSDT Bid-Ask Profile Analysis (1H)"
        
        print("Creating bid-ask overview metrics...")
        plot_bid_ask_profiles(profiles, plot_title, '1H')
        
        print("Creating volume distribution heatmaps...")
        plot_bid_ask_volume_distribution(profiles, "BTCUSDT Bid-Ask Volume Distribution (1H)", '1H')
            
    except Exception as e:
        print(f"An error occurred during visualization: {e}")
        
    print("\nBid-ask profile analysis complete.")
    
    # Print summary statistics
    if profiles:
        print("\n=== Summary Statistics ===")
        
        # Calculate basic statistics from the profiles
        total_bid_volume = 0
        total_ask_volume = 0
        
        for profile in profiles:
            for bid_item in profile['bid_profile']:
                total_bid_volume += bid_item['volume']
            for ask_item in profile['ask_profile']:
                total_ask_volume += ask_item['volume']
        
        total_volume = total_bid_volume + total_ask_volume
        
        print(f"Total Bid Volume: {total_bid_volume:,.2f}")
        print(f"Total Ask Volume: {total_ask_volume:,.2f}")
        print(f"Total Volume: {total_volume:,.2f}")
        print(f"Periods Analyzed: {len(profiles)}")

if __name__ == "__main__":
    run_bid_ask_profile_example()
