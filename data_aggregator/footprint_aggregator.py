"""
Footprint Chart data aggregator - Supports both Time-based and corrected Range-based aggregation.
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, field
from exchange.models import TickData
import numpy as np

@dataclass
class FootprintRow:
    price: float
    bid_volume: float = 0.0
    ask_volume: float = 0.0

@dataclass
class FootprintCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    total_volume: float
    delta: float
    footprint_data: List[FootprintRow] = field(default_factory=list)

class FootprintAggregator:
    def __init__(self, symbol: str = "XBTUSD", price_bin_size: float = 1.0):
        self.symbol = symbol
        self.price_bin_size = price_bin_size
        self.ticks: List[TickData] = []

    def add_tick(self, tick: TickData):
        self.ticks.append(tick)

    def _process_ticks_into_candle(self, ticks_for_candle: List[TickData]) -> FootprintCandle:
        if not ticks_for_candle: return None
        period_df = pd.DataFrame([{'price': t.price, 'volume': t.size * t.price, 'side': t.side.lower()} for t in ticks_for_candle])
        open_price, high_price, low_price, close_price = period_df['price'].iloc[0], period_df['price'].max(), period_df['price'].min(), period_df['price'].iloc[-1]
        
        period_df['price_bin'] = (period_df['price'] // self.price_bin_size) * self.price_bin_size
        price_groups = period_df.groupby('price_bin')
        footprint_rows_dict: Dict[float, FootprintRow] = {}
        for price_bin, group in price_groups:
            ask_volume = group[group['side'] == 'buy']['volume'].sum()
            bid_volume = group[group['side'] == 'sell']['volume'].sum()
            footprint_rows_dict[price_bin] = FootprintRow(price=price_bin, bid_volume=bid_volume, ask_volume=ask_volume)

        binned_low = (low_price // self.price_bin_size) * self.price_bin_size
        binned_high = (high_price // self.price_bin_size) * self.price_bin_size
        all_expected_bins = np.arange(binned_low, binned_high + self.price_bin_size, self.price_bin_size)
        
        complete_footprint_data = []
        for price_level in all_expected_bins:
            price_level = round(price_level, 8)
            complete_footprint_data.append(footprint_rows_dict.get(price_level, FootprintRow(price=price_level)))

        sorted_footprint_data = sorted(complete_footprint_data, key=lambda r: r.price)
        total_ask_volume = sum(row.ask_volume for row in sorted_footprint_data)
        total_bid_volume = sum(row.bid_volume for row in sorted_footprint_data)
        
        return FootprintCandle(
            timestamp=ticks_for_candle[-1].timestamp, open=open_price, high=high_price, low=low_price, close=close_price,
            total_volume=total_ask_volume + total_bid_volume, delta=total_ask_volume - total_bid_volume,
            footprint_data=sorted_footprint_data
        )

    def _process_df_into_candle(self, period_df: pd.DataFrame) -> FootprintCandle:
        dummy_ticks = [TickData(timestamp=idx, price=row['price'], size=row['volume']/row['price'] if row['price'] > 0 else 0, side=row['side'], symbol=self.symbol) for idx, row in period_df.iterrows()]
        return self._process_ticks_into_candle(dummy_ticks)

    def generate_footprints(self, timeframe: str = '5min') -> List[FootprintCandle]:
        if not self.ticks: return []
        df = pd.DataFrame([{'timestamp': t.timestamp, 'price': t.price, 'volume': t.size*t.price, 'side': t.side.lower(), 'symbol':t.symbol} for t in self.ticks])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        resampled_groups = df.resample(timeframe)
        all_candles = []
        for _, period_df in resampled_groups:
            if period_df.empty: continue
            candle = self._process_df_into_candle(period_df)
            if candle:
                all_candles.append(candle)
        return all_candles

    def generate_range_footprints(self, range_levels: int) -> List[FootprintCandle]:
        """Generates range-based footprint candles with corrected logic."""
        if not self.ticks or range_levels <= 1:
            return []
        all_candles, current_ticks = [], []
        for tick in self.ticks:
            potential_ticks = current_ticks + [tick]
            binned_prices = { (t.price // self.price_bin_size) * self.price_bin_size for t in potential_ticks }
            if len(binned_prices) < 2:
                current_ticks.append(tick)
                continue
            
            price_span = max(binned_prices) - min(binned_prices)
            levels_spanned = int(round(price_span / self.price_bin_size)) + 1
            
            if levels_spanned > range_levels:
                if current_ticks:
                    candle = self._process_ticks_into_candle(current_ticks)
                    if candle: all_candles.append(candle)
                current_ticks = [tick]
            else:
                current_ticks.append(tick)
        if current_ticks:
            candle = self._process_ticks_into_candle(current_ticks)
            if candle: all_candles.append(candle)
        return all_candles

    def clear_data(self):
        self.ticks.clear()