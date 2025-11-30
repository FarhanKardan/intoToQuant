import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exchange.data_reader import DataReader
from data_aggregator.delta_aggregator import DeltaAggregator
from data_aggregator.volume_profile_aggregator import VolumeProfileAggregator
from data_aggregator.volume_bucket_aggregator import VolumeBucketAggregator
from data_aggregator.ohlcv_aggregator import OHLCVAggregator

class AggregationSystem:
    def __init__(self, symbol: str = "BTCUSDT", start_date: str = "2024-05-01", end_date: str = "2024-05-04", limit: int = 10000000):
        self.symbol = symbol
        self.data_reader = DataReader("data")
        self.ticks = []
        
        for record_info in self.data_reader.iterate_records(start_date, end_date, "*.csv", limit=limit):
            self.ticks.append(record_info['tick_data'])
    
    def export_to_csv(self, df: pd.DataFrame, filename: str):
        if df is not None and not df.empty:
            output_path = os.path.join("output", filename)
            df.to_csv(output_path, index=False)
            return output_path
        return None
    
    def export_delta(self, timeframe: str = "1h", filename: str = "delta_results.csv"):
        delta_agg = DeltaAggregator(self.symbol)
        for tick_data in self.ticks:
            delta_agg.add_tick(tick_data)
        
        deltas = delta_agg.generate_delta_by_timeframe(timeframe)
        if deltas:
            df = pd.DataFrame([{'timestamp': d['timestamp'], 'delta': d['delta']} for d in deltas])
            return self.export_to_csv(df, filename)
        return None
    
    def export_volume_profile(self, timeframe: str = "1h", filename: str = "volume_profile_results.csv"):
        vp_agg = VolumeProfileAggregator(self.symbol, price_bin_size=10.0)
        for tick_data in self.ticks:
            vp_agg.add_tick(tick_data)
        
        vp_profiles = vp_agg.generate_profiles_by_timeframe(timeframe)
        if vp_profiles:
            df = pd.DataFrame([{'timestamp': p['timestamp'], 'total_volume': p['total_volume'], 'poc_price': p['poc']['price'], 'poc_volume': p['poc']['volume']} for p in vp_profiles])
            return self.export_to_csv(df, filename)
        return None
    
    def export_volume_buckets(self, bucket_size: float = 5000000.0, filename: str = "volume_buckets_results.csv"):
        vb_agg = VolumeBucketAggregator(self.symbol)
        for tick_data in self.ticks:
            vb_agg.add_tick(tick_data)
        
        buckets = vb_agg.generate_volume_buckets(bucket_size)
        if buckets:
            df = pd.DataFrame([{'timestamp': b.timestamp, 'open': b.open_price, 'high': b.high_price, 'low': b.low_price, 'close': b.close_price, 'total_volume': b.total_volume, 'net_flow': b.net_flow} for b in buckets])
            return self.export_to_csv(df, filename)
        return None
    
    def export_ohlcv(self, timeframe: str = "5min", filename: str = "ohlcv_results.csv"):
        ohlcv_agg = OHLCVAggregator(self.symbol)
        for tick_data in self.ticks:
            ohlcv_agg.add_tick(tick_data)
        
        ohlcv_data = ohlcv_agg.generate_ohlcv(timeframe)
        if ohlcv_data:
            df = pd.DataFrame([{'timestamp': o.timestamp, 'open': o.open, 'high': o.high, 'low': o.low, 'close': o.close, 'volume': o.volume, 'trade_count': o.trade_count} for o in ohlcv_data])
            return self.export_to_csv(df, filename)
        return None

def main():    
    agg_system = AggregationSystem("BTCUSDT")
    
    # agg_system.export_delta(timeframe="1h", filename="delta_results.csv")
    # agg_system.export_volume_profile(timeframe="1h", filename="volume_profile_results.csv")
    agg_system.export_volume_buckets(bucket_size=5000000.0, filename="volume_buckets_results.csv")
    # agg_system.export_ohlcv(timeframe="5min", filename="ohlcv_results.csv")
    
if __name__ == "__main__":
    main()
