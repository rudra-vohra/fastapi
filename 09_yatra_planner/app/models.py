from pydantic import BaseModel
from datetime import date

class travelRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date
    base_currency: str = "INR"

class WeatherResponse(BaseModel):
    date: date
    condition: str
    temperature_high: float
    temperature_low: float
    humidity: float
    rain_chance: float

class PlaceModel(BaseModel):
    name: str
    description: str
    category: str
    rating: float
    estimated_time_hours: int
    entry_fee: float | None = None
    