from datetime import datetime
from typing import Dict, List

def normalize_weather_data(current_data: dict, forecast_data: dict) -> dict:
    """Normalize OpenWeatherMap data into our standardized format"""
    
    # Extract current weather data
    current = {
        'temperature': round(current_data['main']['temp'], 1),
        'feels_like': round(current_data['main']['feels_like'], 1),
        'condition': current_data['weather'][0]['main'],
        'condition_description': current_data['weather'][0]['description'].capitalize(),
        'icon': current_data['weather'][0]['icon'],
        'humidity': current_data['main']['humidity'],
        'wind_speed': round(current_data['wind']['speed'] * 3.6, 1),  # m/s -> km/h
        'precipitation_probability': 0,  # Not available in current weather
        'timestamp': datetime.utcnow()
    }
    
    # Hourly forecasts (next 12 hours)
    hourly = []
    for item in forecast_data['list'][:12]:
        hourly.append({
            'time': datetime.fromtimestamp(item['dt']),
            'temperature': round(item['main']['temp'], 1),
            'condition': item['weather'][0]['main'],
            'icon': item['weather'][0]['icon'],
            'precipitation_probability': int(item.get('pop', 0) * 100),
            'wind_speed': round(item['wind']['speed'] * 3.6, 1)
        })
    
    # Daily forecasts (3 days)
    daily = _aggregate_daily_forecasts(forecast_data['list'][:24])
    
    return {
        'city': current_data['name'],
        'country': current_data['sys']['country'],
        'latitude': current_data['coord']['lat'],
        'longitude': current_data['coord']['lon'],
        'timezone': forecast_data['city']['timezone'],
        'current': current,
        'hourly': hourly,
        'daily': daily[:3],
        'cached': False
    }

def _aggregate_daily_forecasts(forecast_list: List[dict]) -> List[dict]:
    """Aggregate 3-hour forecasts into daily forecasts"""
    daily_data = {}
    
    for item in forecast_list:
        dt = datetime.fromtimestamp(item['dt'])
        date_key = dt.date()
        
        if date_key not in daily_data:
            daily_data[date_key] = {
                'temps': [],
                'conditions': [],
                'icons': [],
                'precip_probs': [],
                'humidity': []
            }
        
        daily_data[date_key]['temps'].append(item['main']['temp'])
        daily_data[date_key]['conditions'].append(item['weather'][0]['main'])
        daily_data[date_key]['icons'].append(item['weather'][0]['icon'])
        daily_data[date_key]['precip_probs'].append(item.get('pop', 0) * 100)
        daily_data[date_key]['humidity'].append(item['main']['humidity'])
    
    # Transform into a list of daily forecasts
    daily_forecasts = []
    for date, data in sorted(daily_data.items())[:3]:
        # Dominant condition (most frequent)
        most_common_condition = max(set(data['conditions']), key=data['conditions'].count)
        # Corresponding icon (take the one at noon if possible)
        mid_idx = len(data['icons']) // 2
        icon = data['icons'][mid_idx] if data['icons'] else '01d'
        
        daily_forecasts.append({
            'date': datetime.combine(date, datetime.min.time()),
            'temp_min': round(min(data['temps']), 1),
            'temp_max': round(max(data['temps']), 1),
            'condition': most_common_condition,
            'icon': icon,
            'precipitation_probability': int(max(data['precip_probs'])),
            'humidity': int(sum(data['humidity']) / len(data['humidity']))
        })
    
    return daily_forecasts