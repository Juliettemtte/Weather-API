from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CurrentWeather(BaseModel):
    temperature: float = Field(..., description="Température actuelle en °C")
    feels_like: float = Field(..., description="Température ressentie en °C")
    condition: str = Field(..., description="Condition météo (ex: Clear, Clouds, Rain)")
    condition_description: str = Field(..., description="Description détaillée")
    icon: str = Field(..., description="Code icône OpenWeather")
    humidity: int = Field(..., description="Humidité en %")
    wind_speed: float = Field(..., description="Vitesse du vent en km/h")
    precipitation_probability: int = Field(default=0, description="Probabilité de précipitations en %")
    timestamp: datetime = Field(..., description="Horodatage des données")

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
    cached: bool = Field(default=False, description="Données servies depuis le cache")
    cache_expires_at: Optional[datetime] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)