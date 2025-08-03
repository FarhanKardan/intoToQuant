"""
OHLCV (Open, High, Low, Close, Volume) aggregator
"""

import pandas as pd
from datetime import datetime
from typing import List
from dataclasses import dataclass
from exchange.models import TickData

@dataclass
class OHLCV:
    """OHLCV candlestick data"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: int

class OHLCVAggregator:
    """Aggregates tick data into OHLCV candlesticks"""
    
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
        
        return df
    
    def generate_ohlcv(self, timeframe: str = '1min') -> List[OHLCV]:
        """Generate OHLCV candlesticks"""
        df = self._prepare_dataframe()
        
        # Resample to timeframe
        resampled = df.set_index('timestamp').resample(timeframe).agg({
            'price': ['first', 'max', 'min', 'last'],
            'volume': 'sum',
            'side': 'count'
        })
        
        resampled.columns = ['open', 'high', 'low', 'close', 'volume', 'trade_count']
        resampled = resampled.dropna()
        
        ohlcv_data = []
        for timestamp, row in resampled.iterrows():
            ohlcv = OHLCV(
                timestamp=timestamp,
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                trade_count=row['trade_count']
            )
            ohlcv_data.append(ohlcv)
        
        return ohlcv_data
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 