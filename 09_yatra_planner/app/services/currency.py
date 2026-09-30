import httpx
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
from ..services.cache import get_cache, set_cache

EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
async def fetch_exchange_rate(base_currency: str) -> dict[str, float]:
    '''Fetches the exchange rate for the given base currency from the ExchangeRate API.'''
    cache_data = get_cache(f"exchange_rate_{base_currency}")

    if cache_data is not None:
        return cache_data

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}"
        )
        response.raise_for_status()
        data = response.json()

        rates = data.get("conversion_rates", {})
        set_cache(f"exchange_rate_{base_currency}", rates, ttl=3600)  # Cache for 1 hour
        return rates

    