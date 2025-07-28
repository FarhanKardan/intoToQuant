
import asyncio
import json
import websockets
import ssl
from datetime import datetime
from exchange.models import TickData

class BitmexWebSocket:
    def __init__(self, testnet=False):
        if testnet:
            self.ws_url = "wss://testnet.bitmex.com/realtime"
        else:
            self.ws_url = "wss://ws.bitmex.com/realtime"
        self.websocket = None
        self.is_connected = False
    
    async def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        self.websocket = await asyncio.wait_for(
            websockets.connect(self.ws_url, ssl=ssl_context),
            timeout=10
        )
        self.is_connected = True
        print(f"Connected to BitMEX WebSocket: {self.ws_url}")
    
    async def orderbook_l2_25(self, symbol):
        subscribe_message = {
            "op": "subscribe",
            "args": [f"orderBook10:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            data = json.loads(message)
            if 'table' in data and data['table'] == 'orderBook10' and 'data' in data:
                raw_data = data['data']
                
                for orderbook in raw_data:
                    if orderbook.get('symbol') == symbol:
                        bids = orderbook.get('bids', [])
                        asks = orderbook.get('asks', [])
                        
                        formatted_bids = []
                        for bid in bids:
                            formatted_bids.append({
                                'price': float(bid[0]),
                                'size': float(bid[1])
                            })
                        
                        formatted_asks = []
                        for ask in asks:
                            formatted_asks.append({
                                'price': float(ask[0]),
                                'size': float(ask[1])
                            })
                        
                        full_orderbook = {
                            'symbol': symbol,
                            'timestamp': orderbook.get('timestamp', ''),
                            'bids': formatted_bids,
                            'asks': formatted_asks
                        }
                        
                        return full_orderbook
    
    async def ticks(self, symbol):
        subscribe_message = {
            "op": "subscribe",
            "args": [f"trade:{symbol}"]
        }
        await self.websocket.send(json.dumps(subscribe_message))
        
        async for message in self.websocket:
            data = json.loads(message)
            if 'table' in data and data['table'] == 'trade' and 'data' in data:
                raw_data = data['data']
                tick_list = []
                
                for trade in raw_data:
                    tick = TickData(
                        symbol=trade.get('symbol', ''),
                        side=trade.get('side', ''),
                        size=float(trade.get('size', 0)),
                        price=float(trade.get('price', 0)),
                        timestamp=datetime.strptime(trade.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                    tick_list.append(tick)
                
                return tick_list 