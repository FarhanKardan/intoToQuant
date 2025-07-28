"""
Exchange package for cryptocurrency trading data.

This package contains WebSocket clients for various cryptocurrency exchanges.
"""

from .bitmex_websocket import BitmexWebSocket
from .data_reader import DataReader
from .models import TickData

__all__ = ['BitmexWebSocket', 'DataReader', 'TickData']
__version__ = '1.0.0' 