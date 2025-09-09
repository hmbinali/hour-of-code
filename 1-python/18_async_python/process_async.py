import asyncio
from concurrent.futures import ProcessPoolExecutor


def encrypt(data):
    return f"🔒 {data[::-1]}"


async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, encrypt, "credit_card_1234")
        print(result)


asyncio.run(main())
# if __name__ == "__name__":
