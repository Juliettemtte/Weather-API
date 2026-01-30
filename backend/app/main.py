from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time
from datetime import datetime

from app.config import settings
from app.models import WeatherResponse, ErrorResponse
from app.services.cache_service import cache_service
from app.services.weather_service import weather_service

# Initialization of the FastAPI application
app = FastAPI(
    title="Weather API",
    description="Centralized weather API with intelligent caching and data normalization",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Health endpoint"""
    return {
        "service": "Weather API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    """Comprehensive health check"""
    redis_status = cache_service.health_check()
    return {
        "status": "healthy" if redis_status else "degraded",
        "redis": "connected" if redis_status else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/weather", response_model=WeatherResponse)
def get_weather(
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    """
    Retrieves weather data for a city or coordinates.
    
    - **city**: City name (e.g., Paris, London)
    - **lat**: Latitude (e.g., 48.8566)
    - **lon**: Longitude (e.g., 2.3522)
    
    Returns current data, hourly forecasts (12h), and daily forecasts (3 days).
    """
    start_time = time.time()
    
    # Parameter validation
    if not city and (lat is None or lon is None):
        raise HTTPException(
            status_code=400,
            detail="You must provide either 'city' or both 'lat' and 'lon'"
        )
    
    try:
        # Cache check
        cached_data = cache_service.get(city=city, lat=lat, lon=lon)
        
        if cached_data:
            print(f"✅ Cache HIT - Time: {(time.time() - start_time) * 1000:.0f}ms")
            return WeatherResponse(**cached_data)
        
        # Cache MISS - External API call
        print(f"⚠️  Cache MISS - External API call...")
        weather_data = weather_service.get_weather(city=city, lat=lat, lon=lon)
        
        # Save to cache
        cache_service.set(
            weather_data.model_dump(mode='json'),
            city=weather_data.city if city else None,
            lat=lat,
            lon=lon
        )
        
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ Data retrieved and cached - Time: {elapsed:.0f}ms")
        
        return weather_data
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/api/search")
def search_cities(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(5, ge=1, le=10, description="Number of results")
):
    """
    City search for autocomplete.
    
    - **q**: Search term (minimum 2 characters)
    - **limit**: Maximum number of results (1-10)
    """
    try:
        cities = weather_service.search_city(q, limit)
        return {
            "query": q,
            "results": cities,
            "count": len(cities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cache")
def clear_cache(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None)
):
    """
    Deletes a cache entry (useful for forcing a refresh).
    """
    if not city and (lat is None or lon is None):
        raise HTTPException(
            status_code=400,
            detail="You must provide either 'city' or both 'lat' and 'lon'"
        )
    
    try:
        cache_service.delete(city=city, lat=lat, lon=lon)
        return {
            "status": "success",
            "message": "Cache successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.env == "development"
    )