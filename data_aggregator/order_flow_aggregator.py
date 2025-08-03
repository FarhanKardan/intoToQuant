"""
Order Flow aggregator
"""

import pandas as pd
from datetime import datetime
from typing import List
from dataclasses import dataclass
from exchange.models import TickData

@dataclass
class OrderFlow:
    """Order flow analysis data"""
    timestamp: datetime
    buy_volume: float
    sell_volume: float
    net_flow: float
    buy_trades: int
    sell_trades: int
    total_trades: int
    avg_trade_size: float
    large_trades: int
    imbalance_ratio: float

class OrderFlowAggregator:
    """Aggregates tick data into order flow analysis"""
    
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
        
        return df
    
    def generate_order_flow(self, timeframe: str = '1min') -> List[OrderFlow]:
        """Generate order flow analysis"""
        df = self._prepare_dataframe()
        
        # Calculate average trade size
        avg_trade_size = df['volume'].mean()
        large_trade_threshold = avg_trade_size * 2
        
        # Resample to timeframe
        resampled = df.set_index('timestamp').resample(timeframe).agg({
            'buy_volume': 'sum',
            'sell_volume': 'sum',
            'volume': 'sum',
            'side': 'count'
        })
        
        # Calculate metrics
        resampled['net_flow'] = resampled['buy_volume'] - resampled['sell_volume']
        resampled['avg_trade_size'] = resampled['volume'] / resampled['side']
        resampled['imbalance_ratio'] = resampled['buy_volume'] / resampled['sell_volume'].replace(0, 1)
        
        # Count large trades
        large_trades = []
        for timestamp in resampled.index:
            period_ticks = df[
                (df['timestamp'] >= timestamp) & 
                (df['timestamp'] < timestamp + pd.Timedelta(timeframe))
            ]
            large_count = len(period_ticks[period_ticks['volume'] > large_trade_threshold])
            large_trades.append(large_count)
        
        resampled['large_trades'] = large_trades
        resampled = resampled.dropna()
        
        order_flow_data = []
        for timestamp, row in resampled.iterrows():
            flow = OrderFlow(
                timestamp=timestamp,
                buy_volume=row['buy_volume'],
                sell_volume=row['sell_volume'],
                net_flow=row['net_flow'],
                buy_trades=0,
                sell_trades=0,
                total_trades=row['side'],
                avg_trade_size=row['avg_trade_size'],
                large_trades=row['large_trades'],
                imbalance_ratio=row['imbalance_ratio']
            )
            order_flow_data.append(flow)
        
        return order_flow_data
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 