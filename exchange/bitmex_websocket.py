
import asyncio
import json
import websockets
import ssl
from datetime import datetime
from exchange.models import TickData

class BitmexWebSocket:
    def __init__(self, testnet=False):
        self.ws_url = "wss://testnet.bitmex.com/realtime" if testnet else "wss://ws.bitmex.com/realtime"
        self.websocket = None
    
    async def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        self.websocket = await asyncio.wait_for(
            websockets.connect(self.ws_url, ssl=ssl_context),
            timeout=10
        )
    
    async def orderbook_l2_25(self, symbol):
        subscribe_message = {
            "op": "subscribe",
            "args": [f"orderBook10:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            data = json.loads(message)
            if 'table' in data and data['table'] == 'orderBook10' and 'data' in data:
                orderbook = data['data'][0]
                if orderbook.get('symbol') == symbol:
                    return {
                        'bids': [{'price': float(bid[0]), 'size': float(bid[1])} for bid in orderbook.get('bids', [])],
                        'asks': [{'price': float(ask[0]), 'size': float(ask[1])} for ask in orderbook.get('asks', [])]
                    }
    
    async def ticks(self, symbol):
        subscribe_message = {
            "op": "subscribe",
            "args": [f"trade:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            data = json.loads(message)
            if 'table' in data and data['table'] == 'trade' and 'data' in data:
                return [
                    TickData(
                        symbol=trade.get('symbol', ''),
                        side=trade.get('side', ''),
                        size=float(trade.get('size', 0)),
                        price=float(trade.get('price', 0)),
                        timestamp=datetime.strptime(trade.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                    for trade in data['data']
                ] 