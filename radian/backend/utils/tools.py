import asyncio
import os


async def delay_remove_file(file, delay):
    await asyncio.sleep(delay)
    os.remove(file)