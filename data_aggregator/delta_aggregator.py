"""
Delta Aggregator - Tracks basic delta (ask - bid) over time
"""

import pandas as pd
from typing import List, Dict, Any
from exchange.models import TickData

class DeltaAggregator:
    """Aggregates tick data to track basic delta (buying vs selling pressure) over time."""
    
    def __init__(self, symbol: str = "XBTUSD"):
        self.symbol = symbol
        self.ticks: List[TickData] = []
    
    def add_tick(self, tick: TickData):
        self.ticks.append(tick)
    
    def add_ticks(self, ticks: List[TickData]):
        self.ticks.extend(ticks)
    
    def _prepare_dataframe(self) -> pd.DataFrame:
        if not self.ticks:
            return pd.DataFrame()
        
        data = []
        for tick in self.ticks:
            # Calculate delta: positive for buys, negative for sells
            delta = tick.size if tick.side.lower() == 'buy' else -tick.size
            data.append({
                'timestamp': tick.timestamp,
                'price': tick.price,
                'size': tick.size,
                'side': tick.side,
                'delta': delta
            })
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        return df

    def _calculate_delta_for_period(self, period_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates basic delta for a given time period."""
        if period_df.empty:
            return {}

        # Calculate basic delta
        total_delta = period_df['delta'].sum()
        
        return {
            'timestamp': period_df.index.min(),
            'delta': total_delta
        }

    def generate_delta_by_timeframe(self, timeframe: str) -> List[Dict[str, Any]]:
        """
        Generates basic delta for specified timeframes.
        
        Args:
            timeframe (str): A pandas-compatible frequency string (e.g., '1H', '30min', '1D').
            
        Returns:
            A list of delta dictionaries with timestamp and delta value.
        """
        if not self.ticks:
            return []
            
        df = self._prepare_dataframe()
        if df.empty:
            return []
            
        # Use pandas resample to group data by clock-based timeframes
        resampled_groups = df.resample(timeframe)
        
        all_deltas = []
        for period_timestamp, period_df in resampled_groups:
            if not period_df.empty:
                delta_metrics = self._calculate_delta_for_period(period_df)
                if delta_metrics:
                    all_deltas.append(delta_metrics)
                    
        return all_deltas

    def clear_data(self):
        self.ticks.clear()
