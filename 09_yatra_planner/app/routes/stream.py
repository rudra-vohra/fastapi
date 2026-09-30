from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models import travelRequest
from ..services.weather import get_weather_forecast
from ..services.places import get_places
from ..services.currency import fetch_exchange_rate
import json
from pydantic import BaseModel
from datetime import date,datetime

router = APIRouter(
    prefix="/stream",
    tags=["Streaming Response"]
)

def _jsonable(value):
     if isinstance(value,BaseModel):
        return _jsonable(value.model_dump())

     if isinstance(value,(date,datetime)):
            return value.isoformat()

     if isinstance(value,(list,tuple)):
            return [_jsonable(v) for v in value]
     if isinstance(value,dict):
          return {k:_jsonable(v) for k,v in value.items()}
     return value


def format_sse(data: str,event: str = None) -> str:
    json_data = json.dumps(_jsonable(data))
    return f"data: {json_data}\n\n" if event is None else f"event: {event}\ndata: {json_data}\n\n"


async def stream_travel_plan_generator(travel_request: travelRequest):
    yield format_sse({"message": "Starting to create travel plan..."}, event="start")
    yield format_sse({"message": "Fetching weather forecast..."}, event="weather")

    weather_data = await get_weather_forecast(
        destination=travel_request.destination,
        start_date=travel_request.start_date.isoformat(),
        end_date=travel_request.end_date.isoformat()
    )
    yield format_sse({"weather_data":weather_data}, event="weather")
    yield format_sse({"message": "Fetching places of interest..."}, event="places")
    places_data = await get_places(destination=travel_request.destination)
    yield format_sse({"places_data":places_data}, event="places")
    yield format_sse({"message": "Fetching currency exchange rates..."}, event="currency")
    currency_rates = await fetch_exchange_rate(base_currency=travel_request.base_currency)
    yield format_sse({"currency_rates":currency_rates}, event="currency")
    yield format_sse({"message": "Travel plan aggregation completed successfully."}, event="complete")

     
@router.post("/plan", summary="Stream a travel plan (Aggregated)")
async def stream_travel_plan(travel_request: travelRequest):
    if travel_request.start_date > travel_request.end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
    
    travel_days = (travel_request.end_date - travel_request.start_date).days
    
    if travel_days < 1:
        raise HTTPException(status_code=400, detail="Travel duration must be at least 1 day.")


    return StreamingResponse(
        content = stream_travel_plan_generator(travel_request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
    