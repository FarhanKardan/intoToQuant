import asyncio
from exchange.bitmex_websocket import BitmexWebSocket
from exchange.models import TickData

async def tick_example():
    ws = BitmexWebSocket(testnet=False)
    await ws.connect()
    
    symbol = "XBTUSD"
    
    try:
        while True:
            tick_list = await ws.ticks(symbol)
            
            for i, tick in enumerate(tick_list[:3]):
                print(f"Trade: {tick.symbol} {tick.side} {tick.size} @ ${tick.price:.2f}")
            
            print("-" * 40)
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping tick stream...")
    except Exception as e:
        print(f"Error getting tick data: {e}")
    finally:
        if ws.websocket:
            await ws.websocket.close()

async def orderbook_example():
    ws = BitmexWebSocket(testnet=False)
    await ws.connect()
    
    symbol = "XBTUSD"
    
    try:
        while True:
            full_orderbook = await ws.orderbook_l2_25(symbol)
            
            if full_orderbook:
                bids = full_orderbook.get('bids', [])
                print(f"Top 5 Bids:")
                for i, bid in enumerate(bids[:5]):
                    print(f"  {i+1}. ${bid['price']:.2f} (Size: {bid['size']:.0f})")
                
                asks = full_orderbook.get('asks', [])
                print(f"Top 5 Asks:")
                for i, ask in enumerate(asks[:5]):
                    print(f"  {i+1}. ${ask['price']:.2f} (Size: {ask['size']:.0f})")
                
                if bids and asks:
                    best_bid = bids[0]['price']
                    best_ask = asks[0]['price']
                    spread = best_ask - best_bid
                    print(f"Spread: ${spread:.2f}")
                    
                    total_bid_size = sum(bid['size'] for bid in bids)
                    total_ask_size = sum(ask['size'] for ask in asks)
                    ask_bid_ratio = total_ask_size / total_bid_size if total_bid_size > 0 else 0
                    print(f"Ask/Bid Size Ratio: {ask_bid_ratio:.3f} (Total Ask: {total_ask_size:.0f}, Total Bid: {total_bid_size:.0f})")
            
            print("-" * 40)
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping orderbook stream...")
    except Exception as e:
        print(f"Error getting orderbook data: {e}")
    finally:
        if ws.websocket:
            await ws.websocket.close()

def main():
    print("Choose an example:")
    print("1. Tick data streaming")
    print("2. Orderbook L10 data streaming")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(tick_example())
    elif choice == "2":
        asyncio.run(orderbook_example())
    else:
        print("Invalid choice. Running tick example by default.")
        asyncio.run(tick_example())

if __name__ == "__main__":
    main() 