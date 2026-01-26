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
        """Récupère les données météo depuis OpenWeatherMap"""
        
        # Appel API current weather
        current_data = self._fetch_current_weather(city, lat, lon)
        
        # Extraction des coordonnées pour les appels suivants
        coords_lat = current_data['coord']['lat']
        coords_lon = current_data['coord']['lon']
        
        # Appel API forecast (hourly + daily)
        forecast_data = self._fetch_forecast(coords_lat, coords_lon)
        
        # Normalisation des données
        normalized = normalize_weather_data(current_data, forecast_data)
        
        return WeatherResponse(**normalized)
    
    def _fetch_current_weather(self, city: Optional[str], lat: Optional[float], lon: Optional[float]) -> dict:
        """Appel API pour météo actuelle"""
        params = {
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'fr'
        }
        
        if city:
            params['q'] = city
        elif lat is not None and lon is not None:
            params['lat'] = lat
            params['lon'] = lon
        else:
            raise ValueError("City ou coordonnées requises")
        
        url = f"{self.base_url}/weather"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 404:
            raise ValueError(f"Ville '{city}' introuvable")
        elif response.status_code != 200:
            raise Exception(f"Erreur API OpenWeather: {response.status_code}")
        
        return response.json()
    
    def _fetch_forecast(self, lat: float, lon: float) -> dict:
        """Appel API pour prévisions horaires et quotidiennes"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'fr',
            'cnt': 40  # 5 jours de prévisions (on en gardera 3)
        }
        
        url = f"{self.base_url}/forecast"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code != 200:
            raise Exception(f"Erreur API Forecast: {response.status_code}")
        
        return response.json()
    
    def search_city(self, query: str, limit: int = 5) -> list:
        """Recherche de villes pour autocomplétion"""
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