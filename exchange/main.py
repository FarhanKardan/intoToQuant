import asyncio
from exchange.bitmex_websocket import BitmexWebSocket

async def tick_example():
    ws = BitmexWebSocket(testnet=False)
    await ws.connect()
    
    try:
        while True:
            tick_list = await ws.ticks("XBTUSD")
            for tick in tick_list[:3]:
                print(f"{tick.symbol} {tick.side} {tick.size} @ ${tick.price:.2f}")
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if ws.websocket:
            await ws.websocket.close()

async def orderbook_example():
    ws = BitmexWebSocket(testnet=False)
    await ws.connect()
    
    try:
        while True:
            orderbook = await ws.orderbook_l2_25("XBTUSD")
            if orderbook:
                bids = orderbook.get('bids', [])
                asks = orderbook.get('asks', [])
                
                print(f"Bids: {bids[:3]}")
                print(f"Asks: {asks[:3]}")
                
                if bids and asks:
                    spread = asks[0]['price'] - bids[0]['price']
                    print(f"Spread: ${spread:.2f}")
            
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if ws.websocket:
            await ws.websocket.close()

def main():
    print("1. Tick data")
    print("2. Orderbook data")
    
    choice = input("Choice (1/2): ").strip()
    
    if choice == "2":
        asyncio.run(orderbook_example())
    else:
        asyncio.run(tick_example())

if __name__ == "__main__":
    main()
