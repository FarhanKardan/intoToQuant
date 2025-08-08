from dataclasses import dataclass
from datetime import datetime

@dataclass
class TickData:
    symbol: str
    side: str
    size: float
    price: float
    timestamp: datetime 


@dataclass
class TopBookL1:
    symbol: str
    Bprice: float
    Aprice: float
    BSize: float
    ASize: float
    timestamp: datetime 




