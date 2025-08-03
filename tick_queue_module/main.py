import asyncio
from tick_queue_module.tick_queue import TickQueue

async def tick_queue_example():
    queue = TickQueue(symbol="XBTUSD", max_length=10, testnet=False)
    
    await queue.connect()
    print(f"Connected to {queue.symbol}")
    print(f"Queue max length: {queue.max_length}")
    print("Starting... Press Ctrl+C to stop")
    
    try:
        while True:
            await asyncio.sleep(2)
            
            ticks = queue.get_latest_ticks()
            if ticks:
                print(f"Queue: {queue.get_queue_length()}/{queue.max_length}")
                for i, tick in enumerate(ticks[-3:], 1):
                    print(f"  {i}. {tick.symbol} {tick.side} {tick.size} @ ${tick.price:.2f}")
                print("-" * 40)
    
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        await queue.stop()

if __name__ == "__main__":
    asyncio.run(tick_queue_example()) 