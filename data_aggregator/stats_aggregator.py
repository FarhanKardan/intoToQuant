"""
Statistics aggregator
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict
from exchange.models import TickData

class StatsAggregator:
    """Aggregates tick data into summary statistics"""
    
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
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        if not self.ticks:
            return {}
        
        df = self._prepare_dataframe()
        
        stats = {
            'total_ticks': len(df),
            'time_span': df['timestamp'].max() - df['timestamp'].min(),
            'total_volume': df['volume'].sum(),
            'avg_price': df['price'].mean(),
            'price_range': {
                'min': df['price'].min(),
                'max': df['price'].max(),
                'std': df['price'].std()
            },
            'volume_stats': {
                'total_buy_volume': df['buy_volume'].sum(),
                'total_sell_volume': df['sell_volume'].sum(),
                'avg_trade_size': df['volume'].mean(),
                'largest_trade': df['volume'].max()
            },
            'trade_distribution': {
                'buy_trades': len(df[df['side'].str.lower() == 'buy']),
                'sell_trades': len(df[df['side'].str.lower() == 'sell'])
            }
        }
        
        return stats
    
    def clear_data(self):
        """Clear stored data"""
        self.ticks.clear() 