import asyncio
import time


async def brew(name):
    print(f"Brewing {name} chai...")
    await asyncio.sleep(3)
    # time.sleep(3)
    print(f"{name} is ready.")


async def main():
    await asyncio.gather(
        brew("Masala"),
        brew("Green"),
        brew("Ginger"),
    )


asyncio.run(main())
