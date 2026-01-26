from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # OpenWeatherMap
    openweather_api_key: str
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    cache_ttl: int = 1800  # 30 minutes
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:4200"
    
    # Environment
    env: str = "development"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()