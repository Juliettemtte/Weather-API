from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CurrentWeather(BaseModel):
    temperature: float = Field(..., description="Temperature in°C")
    feels_like: float = Field(..., description="Temperature feels like in °C")
    condition: str = Field(..., description="Weather condition (e.g., Clear, Clouds, Rain)")
    condition_description: str = Field(..., description="Detailed description")
    icon: str = Field(..., description="OpenWeather icon code")
    humidity: int = Field(..., description="Humidity in %")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    precipitation_probability: int = Field(default=0, description="Precipitation probability in %")
    timestamp: datetime = Field(..., description="Timestamp of the data")

class HourlyForecast(BaseModel):
    time: datetime
    temperature: float
    condition: str
    icon: str
    precipitation_probability: int
    wind_speed: float

class DailyForecast(BaseModel):
    date: datetime
    temp_min: float
    temp_max: float
    condition: str
    icon: str
    precipitation_probability: int
    humidity: int

class WeatherResponse(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    timezone: int
    current: CurrentWeather
    hourly: List[HourlyForecast] = Field(default_factory=list, max_length=12)
    daily: List[DailyForecast] = Field(default_factory=list, max_length=3)
    cached: bool = Field(default=False, description="Data served from cache")
    cache_expires_at: Optional[datetime] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)