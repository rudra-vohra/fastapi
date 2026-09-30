from fastapi import APIRouter, HTTPException
from ..models import travelRequest
from ..services.weather import get_weather_forecast
from ..services.places import get_places
from ..services.currency import fetch_exchange_rate
import asyncio

router = APIRouter(
    prefix="/plan",
    tags=["Travel Plan"],
)

@router.post("/", summary="Create a travel plan (Aggregated)")
async def create_travel_plan(
    travel_request: travelRequest
):
     
    """
    Create a travel plan by aggregating data from multiple sources.
    """
    # Logic to create a travel plan goes here
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")

    travel_days = (travel_request.end_date - travel_request.start_date).days

    if travel_days < 1:
        raise HTTPException(status_code=400, detail="Travel duration must be at least 1 day.")

    weather_data, places_data, currency_rates = await asyncio.gather(
        get_weather_forecast(
            destination=travel_request.destination,
            start_date=travel_request.start_date.isoformat(),
            end_date=travel_request.end_date.isoformat()
        ),
        get_places(destination=travel_request.destination),
        fetch_exchange_rate(base_currency=travel_request.base_currency)
    )

    return {
        "message": "Travel plan created successfully.",
        "weather_forecast": weather_data,
        "places": places_data,
        "currency_rates": currency_rates
    }



