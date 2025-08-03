"""
Volume Bucket aggregator
"""

import pandas as pd
from datetime import datetime
from typing import List
from dataclasses import dataclass
from exchange.models import TickData

@dataclass
class VolumeBucket:
    """Volume bucket data"""
    timestamp: datetime
    bucket_size: float
    bucket_count: int
    total_volume: float
    avg_price: float
    buy_volume: float
    sell_volume: float
    net_flow: float

class VolumeBucketAggregator:
    """Aggregates tick data into volume buckets"""
    
    def __init__(self, symbol: str = "XBTUSD"):
        self.symbol = symbol
        self.ticks: List[TickData] = []
    
    def add_tick(self, tick: TickData):
        """Add single tick"""
        self.ticks.append(tick)
    
    def add_ticks(self, ticks: List[TickData]):
        """Add multiple ticks"""
        self.ticks.extend(ticks)
    
    def _prepare_dataframe(self) -> pd.DataFrame:
        """Convert ticks to DataFrame"""
        if not self.ticks:
            raise ValueError("No tick data available")
        
        data = []
        for tick in self.ticks:
            data.append({
                'timestamp': tick.timestamp,
                'price': tick.price,
                'volume': tick.size,
                'side': tick.side,
                'symbol': tick.symbol
            })
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Add derived columns
        df['buy_volume'] = df.apply(lambda x: x['volume'] if x['side'].lower() == 'buy' else 0, axis=1)
        df['sell_volume'] = df.apply(lambda x: x['volume'] if x['side'].lower() == 'sell' else 0, axis=1)
        df['price_volume'] = df['price'] * df['volume']
        
        return df
    
    def generate_volume_buckets(self, bucket_size: float = 1000.0) -> List[VolumeBucket]:
        """Generate volume buckets"""
        df = self._prepare_dataframe()
        
        # Calculate cumulative volume
        df['cumulative_volume'] = df['volume'].cumsum()
        df['bucket_number'] = (df['cumulative_volume'] // bucket_size).astype(int)
        
        bucket_data = []
        for bucket_num in df['bucket_number'].unique():
            bucket_ticks = df[df['bucket_number'] == bucket_num]
            
            if len(bucket_ticks) == 0:
                continue
            
            bucket = VolumeBucket(
                timestamp=bucket_ticks.iloc[-1]['timestamp'],
                bucket_size=bucket_size,
                bucket_count=bucket_num,
                total_volume=bucket_ticks['volume'].sum(),
                avg_price=(bucket_ticks['price_volume'].sum() / bucket_ticks['volume'].sum()),
                buy_volume=bucket_ticks['buy_volume'].sum(),
                sell_volume=bucket_ticks['sell_volume'].sum(),
                net_flow=bucket_ticks['buy_volume'].sum() - bucket_ticks['sell_volume'].sum()
            )
            bucket_data.append(bucket)
        
        return bucket_data
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 