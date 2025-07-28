import asyncio
from tick_queue import TickQueue

async def tick_queue_example():
    tick_queue = TickQueue(symbol="XBTUSD", max_length=10, testnet=False)
    
    try:
        await tick_queue.connect()
        print(f"Connected to BitMEX WebSocket for {tick_queue.symbol}")
        print(f"Queue max length: {tick_queue.max_length}")
        
        streaming_task = asyncio.create_task(tick_queue.start_streaming())
        
        print("Starting tick data collection...")
        print("Press Ctrl+C to stop")
        
        while True:
            await asyncio.sleep(2)
            
            ticks = tick_queue.get_latest_ticks()
            queue_length = tick_queue.get_queue_length()
            
            print(f"\nQueue Status: {queue_length}/{tick_queue.max_length} items")
            
            if ticks:
                print("Full Queue Contents:")
                for i, tick in enumerate(ticks, 1):
                    print(f"  {i:2d}. {tick.symbol} {tick.side} {tick.size} @ ${tick.price:.2f}")
            else:
                print("No ticks received yet...")
            
            print("-" * 50)
    
    except KeyboardInterrupt:
        print("\nStopping tick queue...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await tick_queue.stop()
        print("Tick queue stopped")

def main():
    print("Tick Queue Example")
    print("==================")
    asyncio.run(tick_queue_example())

if __name__ == "__main__":
    main() 