import requests
from typing import Optional
from datetime import datetime
from app.config import settings
from app.models import WeatherResponse, CurrentWeather, HourlyForecast, DailyForecast
from app.utils.normalizer import normalize_weather_data

class WeatherService:
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.base_url = settings.openweather_base_url
    
    def get_weather(self, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> WeatherResponse:
        """Retrieves weather data from OpenWeatherMap"""
        
        # Call API current weather
        current_data = self._fetch_current_weather(city, lat, lon)
        
        # Extract coordinates for subsequent calls
        coords_lat = current_data['coord']['lat']
        coords_lon = current_data['coord']['lon']
        
        # Call API forecast (hourly + daily)
        forecast_data = self._fetch_forecast(coords_lat, coords_lon)
        
        # Normalize data
        normalized = normalize_weather_data(current_data, forecast_data)
        
        return WeatherResponse(**normalized)
    
    def _fetch_current_weather(self, city: Optional[str], lat: Optional[float], lon: Optional[float]) -> dict:
        """Call API for current weather"""
        params = {
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'en'
        }
        
        if city:
            params['q'] = city
        elif lat is not None and lon is not None:
            params['lat'] = lat
            params['lon'] = lon
        else:
            raise ValueError("City or coordinates required")
        
        url = f"{self.base_url}/weather"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 404:
            raise ValueError(f"City '{city}' not found")
        elif response.status_code != 200:
            raise Exception(f"OpenWeather API error: {response.status_code}")
        
        return response.json()
    
    def _fetch_forecast(self, lat: float, lon: float) -> dict:
        """Call API for hourly and daily forecasts"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'en',
            'cnt': 40  # 5 days of forecasts (we will keep 3)
        }
        
        url = f"{self.base_url}/forecast"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code != 200:
            raise Exception(f"Forecast API error: {response.status_code}")
        
        return response.json()
    
    def search_city(self, query: str, limit: int = 5) -> list:
        """City search for autocomplete"""
        params = {
            'q': query,
            'limit': limit,
            'appid': self.api_key
        }
        
        url = "http://api.openweathermap.org/geo/1.0/direct"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code != 200:
            return []
        
        cities = response.json()
        return [
            {
                'name': city.get('name'),
                'country': city.get('country'),
                'state': city.get('state', ''),
                'lat': city.get('lat'),
                'lon': city.get('lon')
            }
            for city in cities
        ]

weather_service = WeatherService()