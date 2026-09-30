import os
from datetime import date, timedelta
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import httpx
API_KEY = os.getenv("WEATHERAPI_API_KEY")
from ..services.cache import get_cache, set_cache
from ..models import WeatherResponse

async def get_weather_forecast(destination: str, start_date: str, end_date: str) -> list[WeatherResponse]:

    cache_key = get_cache(f"weather_{destination}_{start_date}_{end_date}")
    if cache_key is not None:
        return cache_key


    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if start > end:
        raise ValueError("start_date must be on or before end_date")

    forecasts = []
    async with httpx.AsyncClient() as client:
        current = start
        while current <= end:
            response = await client.get(
                "https://api.weatherapi.com/v1/forecast.json",
                params={
                    "key": API_KEY,
                    "q": destination,
                    "dt": current.isoformat(),
                },
            )
            response.raise_for_status()
            data = response.json()

            for day in data["forecast"]["forecastday"]:
                forecasts.append(WeatherResponse(
                    date=day["date"],
                    condition=day["day"]["condition"]["text"],
                    temperature_high=day["day"]["maxtemp_c"],
                    temperature_low=day["day"]["mintemp_c"],
                    humidity=day["day"]["avghumidity"],
                    rain_chance=day["day"]["daily_chance_of_rain"],
                ))
            current += timedelta(days=1)


    set_cache(f"weather_{destination}_{start_date}_{end_date}", forecasts, ttl=3600)  # Cache for 1 hour
    return forecasts

    
        
