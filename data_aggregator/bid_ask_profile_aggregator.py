"""
Bid-Ask Profile Aggregator - Tracks basic bid and ask volumes across price levels
"""

import pandas as pd
from typing import List, Dict, Any

from exchange.models import TickData

class BidAskProfileAggregator:
    """Aggregates tick data to create separate bid and ask volume profiles."""
    
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
        
        data = []
        for tick in self.ticks:
            data.append({
                'timestamp': tick.timestamp,
                'price': tick.price,
                'size': tick.size,
                'side': tick.side.lower(),
                'volume': tick.size * tick.price
            })
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        return df

    def _calculate_bid_ask_profile_for_period(self, period_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates basic bid and ask profiles for a given time period."""
        if period_df.empty:
            return {}

        # Separate bid and ask data
        bid_df = period_df[period_df['side'] == 'buy'].copy()
        ask_df = period_df[period_df['side'] == 'sell'].copy()
        
        # Bin prices for both bid and ask
        bid_df['price_bin'] = (bid_df['price'] // self.price_bin_size) * self.price_bin_size
        ask_df['price_bin'] = (ask_df['price'] // self.price_bin_size) * self.price_bin_size
        
        # Group by price bin and sum volumes for bids
        bid_profile = bid_df.groupby('price_bin')['volume'].sum().reset_index()
        bid_profile = bid_profile.sort_values('price_bin', ascending=False)
        
        # Group by price bin and sum volumes for asks
        ask_profile = ask_df.groupby('price_bin')['volume'].sum().reset_index()
        ask_profile = ask_profile.sort_values('price_bin', ascending=False)
        
        return {
            'timestamp': period_df.index.min(),
            'bid_profile': bid_profile.to_dict('records'),
            'ask_profile': ask_profile.to_dict('records')
        }

    def generate_bid_ask_profiles_by_timeframe(self, timeframe: str) -> List[Dict[str, Any]]:
        """
        Generates basic bid-ask profiles for specified timeframes.
        
        Args:
            timeframe (str): A pandas-compatible frequency string (e.g., '1H', '30min', '1D').
            
        Returns:
            A list of bid-ask profile dictionaries with timestamp, bid_profile, and ask_profile.
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
                profile = self._calculate_bid_ask_profile_for_period(period_df)
                if profile:
                    all_profiles.append(profile)
                    
        return all_profiles

    def clear_data(self):
        self.ticks.clear()
