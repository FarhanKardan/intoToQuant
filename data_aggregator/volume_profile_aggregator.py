"""
Volume Profile aggregator - Updated for time-based aggregation
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

from exchange.models import TickData

class VolumeProfileAggregator:
    """Aggregates tick data into Volume Profiles for specified timeframes."""
    
    def __init__(self, symbol: str = "XBTUSD", price_bin_size: float = 1.0):
        self.symbol = symbol
        self.price_bin_size = price_bin_size
        self.ticks: List[TickData] = []
    
    def add_tick(self, tick: TickData):
        self.ticks.append(tick)
    
    def add_ticks(self, ticks: List[TickData]):
        self.ticks.extend(ticks)
    
    def _prepare_dataframe(self) -> pd.DataFrame:
        if not self.ticks:
            return pd.DataFrame()
        
        data = [{'timestamp': tick.timestamp, 'price': tick.price, 'volume': tick.size * tick.price} for tick in self.ticks]
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        return df

    def _calculate_profile_for_period(self, period_df: pd.DataFrame, va_percentage: int) -> Dict[str, Any]:
        """Calculates a single volume profile for a given DataFrame (a period of time)."""
        if period_df.empty:
            return {}

        # 1. Bin prices
        period_df = period_df.copy()
        period_df['price_bin'] = (period_df['price'] // self.price_bin_size) * self.price_bin_size
        
        # 2. Group by price bin and sum volumes
        profile_data = period_df.groupby('price_bin')['volume'].sum().reset_index().sort_values('price_bin', ascending=False)
        
        if profile_data.empty:
            return {}
            
        total_volume = profile_data['volume'].sum()
        
        # 3. Find POC
        poc_row = profile_data.loc[profile_data['volume'].idxmax()]
        poc = {'price': poc_row['price_bin'], 'volume': poc_row['volume']}
        
        # 4. Calculate Value Area
        target_va_volume = total_volume * (va_percentage / 100)
        poc_index = poc_row.name
        
        va_rows = profile_data.loc[[poc_index]].copy()
        current_va_volume = poc['volume']
        
        rows_below = profile_data.loc[:poc_index-1].sort_index(ascending=False)
        rows_above = profile_data.loc[poc_index+1:].sort_index(ascending=True)
        
        below_idx, above_idx = 0, 0
        
        while current_va_volume < target_va_volume:
            vol_below = rows_below.iloc[below_idx]['volume'] if below_idx < len(rows_below) else -1
            vol_above = rows_above.iloc[above_idx]['volume'] if above_idx < len(rows_above) else -1
            
            if vol_below == -1 and vol_above == -1: break

            if vol_below > vol_above:
                current_va_volume += vol_below
                va_rows = pd.concat([va_rows, rows_below.iloc[[below_idx]]])
                below_idx += 1
            else:
                current_va_volume += vol_above
                va_rows = pd.concat([va_rows, rows_above.iloc[[above_idx]]])
                above_idx += 1

        return {
            'timestamp': period_df.index.min(),
            'profile_data': profile_data.to_dict('records'),
            'poc': poc,
            'value_area': {'high': va_rows['price_bin'].max(), 'low': va_rows['price_bin'].min(), 'percentage': va_percentage},
            'total_volume': total_volume,
        }

    def generate_profiles_by_timeframe(self, timeframe: str, va_percentage: int = 70) -> List[Dict[str, Any]]:
        """
        Generates a list of volume profiles, one for each period in the specified timeframe.
        
        Args:
            timeframe (str): A pandas-compatible frequency string (e.g., '1H', '30min', '1D').
            va_percentage (int): The percentage for the Value Area calculation.
            
        Returns:
            A list of profile dictionaries.
        """
        if not self.ticks:
            return []
            
        df = self._prepare_dataframe()
        if df.empty:
            return []
            
        # Use pandas resample to group data by clock-based timeframes
        resampled_groups = df.resample(timeframe)
        
        all_profiles = []
        for period_timestamp, period_df in resampled_groups:
            if not period_df.empty:
                profile = self._calculate_profile_for_period(period_df, va_percentage)
                if profile:
                    all_profiles.append(profile)
                    
        return all_profiles

    def clear_data(self):
        self.ticks.clear()