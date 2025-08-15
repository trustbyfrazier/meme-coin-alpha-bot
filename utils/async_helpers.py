import asyncio
import random
from core.logger import log, error_log

async def async_retry(coro, retries=3, backoff_in_seconds=2):
    attempt = 0
    while attempt < retries:
        try:
            return await coro
        except Exception as e:
            attempt += 1
            wait_time = backoff_in_seconds * (2 ** (attempt - 1)) + random.uniform(0, 1)
            error_log(f"Attempt {attempt} failed with error: {e}. Retrying in {wait_time:.2f}s...")
            await asyncio.sleep(wait_time)
    error_log("All retry attempts failed.")
    return None

