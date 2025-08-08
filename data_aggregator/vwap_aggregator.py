"""
VWAP (Volume Weighted Average Price) aggregator
"""

import pandas as pd
from datetime import datetime
from typing import List
from dataclasses import dataclass
from exchange.models import TickData

@dataclass
class VWAPData:
    """Volume Weighted Average Price data"""
    timestamp: datetime
    vwap: float
    volume: float
    cumulative_volume: float
    cumulative_pv: float

class VWAPAggregator:
    """Aggregates tick data into VWAP calculations"""
    
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
                'volume': tick.size * tick.price,  # USD volume (BTC size * price)
                'side': tick.side,
                'symbol': tick.symbol
            })
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Add price * volume column
        df['price_volume'] = df['price'] * df['volume']
        
        return df
    
    def generate_vwap(self, timeframe: str = '1min') -> List[VWAPData]:
        """Generate VWAP data"""
        df = self._prepare_dataframe()
        
        # Resample to timeframe
        resampled = df.set_index('timestamp').resample(timeframe).agg({
            'price_volume': 'sum',
            'volume': 'sum'
        })
        
        resampled = resampled.dropna()
        
        # Calculate cumulative values
        resampled['cumulative_pv'] = resampled['price_volume'].cumsum()
        resampled['cumulative_volume'] = resampled['volume'].cumsum()
        resampled['vwap'] = resampled['cumulative_pv'] / resampled['cumulative_volume']
        
        vwap_data = []
        for timestamp, row in resampled.iterrows():
            vwap = VWAPData(
                timestamp=timestamp,
                vwap=row['vwap'],
                volume=row['volume'],
                cumulative_volume=row['cumulative_volume'],
                cumulative_pv=row['cumulative_pv']
            )
            vwap_data.append(vwap)
        
        return vwap_data
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 