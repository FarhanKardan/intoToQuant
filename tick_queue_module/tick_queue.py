import asyncio
import json
import websockets
import ssl
from collections import deque
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchange.bitmex_websocket import BitmexWebSocket
from exchange.models import TickData

class TickQueue:
    def __init__(self, symbol="XBTUSD", max_length=10, testnet=False):
        self.symbol = symbol
        self.max_length = max_length
        self.testnet = testnet
        self.queue = deque(maxlen=max_length)
        self.websocket = None
        self.is_running = False
        self.bitmex_ws = BitmexWebSocket(testnet=testnet)
    
    async def connect(self):
        await self.bitmex_ws.connect()
        self.websocket = self.bitmex_ws.websocket
    
    async def start_streaming(self):
        self.is_running = True
        
        subscribe_message = {
            "op": "subscribe",
            "args": [f"trade:{self.symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            if not self.is_running:
                break
                
            data = json.loads(message)
            if 'table' in data and data['table'] == 'trade' and 'data' in data:
                for trade in data['data']:
                    tick = TickData(
                        symbol=trade.get('symbol', ''),
                        side=trade.get('side', ''),
                        size=float(trade.get('size', 0)),
                        price=float(trade.get('price', 0)),
                        timestamp=datetime.strptime(trade.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                    self.queue.append(tick)
    
    def get_latest_ticks(self):
        return list(self.queue)
    
    def get_queue_length(self):
        return len(self.queue)
    
    def is_full(self):
        return len(self.queue) == self.max_length
    
    async def stop(self):
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
    
    def clear(self):
        self.queue.clear() 