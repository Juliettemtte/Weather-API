export interface CurrentWeather {
  temperature: number;
  feels_like: number;
  condition: string;
  condition_description: string;
  icon: string;
  humidity: number;
  wind_speed: number;
  precipitation_probability: number;
  timestamp: string;
}

export interface HourlyForecast {
  time: string;
  temperature: number;
  condition: string;
  icon: string;
  precipitation_probability: number;
  wind_speed: number;
}

export interface DailyForecast {
  date: string;
  temp_min: number;
  temp_max: number;
  condition: string;
  icon: string;
  precipitation_probability: number;
  humidity: number;
}

export interface WeatherResponse {
  city: string;
  country: string;
  latitude: number;
  longitude: number;
  timezone: string;
  current: CurrentWeather;
  hourly: HourlyForecast[];
  daily: DailyForecast[];
  cached: boolean;
  cache_expires_at?: string;
}

export interface CitySearchResult {
  name: string;
  country: string;
  state?: string;
  lat: number;
  lon: number;
}

export interface FavoriteCity {
  name: string;
  country: string;
  savedAt: string;
}