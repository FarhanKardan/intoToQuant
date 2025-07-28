from dataclasses import dataclass
from datetime import datetime

@dataclass
class TickData:
    symbol: str
    side: str
    size: float
    price: float
    timestamp: datetime 