"""
Volume Bucket aggregator - Optimized
"""

import pandas as pd
from datetime import datetime
from typing import List
from dataclasses import dataclass
from exchange.models import TickData

@dataclass
class VolumeBucket:
    """Volume bucket data with OHLCV candles"""
    timestamp: datetime
    bucket_size: float
    bucket_count: int
    total_volume: float
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    avg_price: float
    buy_volume: float
    sell_volume: float
    net_flow: float

class VolumeBucketAggregator:
    """Aggregates tick data into volume buckets - Optimized version"""
    
    def __init__(self, symbol: str = "XBTUSD"):
        self.symbol = symbol
        self.ticks: List[TickData] = []
    
    def add_tick(self, tick: TickData):
        """Add single tick"""
        self.ticks.append(tick)
    
    def add_ticks(self, ticks: List[TickData]):
        """Add multiple ticks"""
        self.ticks.extend(ticks)
    
    def generate_volume_buckets(self, bucket_size: float = 1000.0) -> List[VolumeBucket]:
        """Generate volume buckets - Optimized implementation"""
        if not self.ticks:
            return []
        
        # Create DataFrame directly without intermediate steps
        df = pd.DataFrame([{
            'timestamp': tick.timestamp,
            'price': tick.price,
            'volume': tick.size * tick.price,  # USD volume
            'side': tick.side.lower()
        } for tick in self.ticks])
        
        # Optimize data types and sorting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Vectorized operations for better performance
        df['buy_volume'] = df['volume'].where(df['side'] == 'buy', 0)
        df['sell_volume'] = df['volume'].where(df['side'] == 'sell', 0)
        df['price_volume'] = df['price'] * df['volume']
        
        # Calculate cumulative volume and bucket numbers
        df['cumulative_volume'] = df['volume'].cumsum()
        df['bucket_number'] = (df['cumulative_volume'] // bucket_size).astype(int)
        
        # Group by bucket and aggregate efficiently
        bucket_groups = df.groupby('bucket_number')
        
        bucket_data = []
        for bucket_num, bucket_ticks in bucket_groups:
            if len(bucket_ticks) == 0:
                continue
            
            # Calculate all metrics in one pass
            total_volume = bucket_ticks['volume'].sum()
            price_volume_sum = bucket_ticks['price_volume'].sum()
            
            bucket = VolumeBucket(
                timestamp=bucket_ticks.iloc[-1]['timestamp'],
                bucket_size=bucket_size,
                bucket_count=bucket_num,
                total_volume=total_volume,
                open_price=bucket_ticks.iloc[0]['price'],
                high_price=bucket_ticks['price'].max(),
                low_price=bucket_ticks['price'].min(),
                close_price=bucket_ticks.iloc[-1]['price'],
                avg_price=price_volume_sum / total_volume if total_volume > 0 else 0,
                buy_volume=bucket_ticks['buy_volume'].sum(),
                sell_volume=bucket_ticks['sell_volume'].sum(),
                net_flow=bucket_ticks['buy_volume'].sum() - bucket_ticks['sell_volume'].sum()
            )
            bucket_data.append(bucket)
        
        return bucket_data
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 