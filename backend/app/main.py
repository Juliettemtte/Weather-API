from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time
from datetime import datetime

from app.config import settings
from app.models import WeatherResponse, ErrorResponse
from app.services.cache_service import cache_service
from app.services.weather_service import weather_service

# Initialisation FastAPI
app = FastAPI(
    title="Weather API",
    description="API météo centralisée avec cache intelligent et normalisation des données",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Endpoint de santé"""
    return {
        "service": "Weather API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    """Vérification de santé complète"""
    redis_status = cache_service.health_check()
    return {
        "status": "healthy" if redis_status else "degraded",
        "redis": "connected" if redis_status else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/weather", response_model=WeatherResponse)
def get_weather(
    city: Optional[str] = Query(None, description="Nom de la ville"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    """
    Récupère les données météo pour une ville ou des coordonnées.
    
    - **city**: Nom de la ville (ex: Paris, London)
    - **lat**: Latitude (ex: 48.8566)
    - **lon**: Longitude (ex: 2.3522)
    
    Retourne les données actuelles, prévisions horaires (12h) et quotidiennes (3 jours).
    """
    start_time = time.time()
    
    # Validation des paramètres
    if not city and (lat is None or lon is None):
        raise HTTPException(
            status_code=400,
            detail="Vous devez fournir soit 'city', soit 'lat' et 'lon'"
        )
    
    try:
        # Vérification du cache
        cached_data = cache_service.get(city=city, lat=lat, lon=lon)
        
        if cached_data:
            print(f"✅ Cache HIT - Temps: {(time.time() - start_time) * 1000:.0f}ms")
            return WeatherResponse(**cached_data)
        
        # Cache MISS - Appel API
        print(f"⚠️  Cache MISS - Appel API externe...")
        weather_data = weather_service.get_weather(city=city, lat=lat, lon=lon)
        
        # Sauvegarde dans le cache
        cache_service.set(
            weather_data.model_dump(mode='json'),
            city=weather_data.city if city else None,
            lat=lat,
            lon=lon
        )
        
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ Données récupérées et mises en cache - Temps: {elapsed:.0f}ms")
        
        return weather_data
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"❌ Erreur: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/search")
def search_cities(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    limit: int = Query(5, ge=1, le=10, description="Nombre de résultats")
):
    """
    Recherche de villes pour autocomplétion.
    
    - **q**: Terme de recherche (minimum 2 caractères)
    - **limit**: Nombre maximum de résultats (1-10)
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
    Supprime une entrée du cache (utile pour forcer le rafraîchissement).
    """
    if not city and (lat is None or lon is None):
        raise HTTPException(
            status_code=400,
            detail="Vous devez fournir soit 'city', soit 'lat' et 'lon'"
        )
    
    try:
        cache_service.delete(city=city, lat=lat, lon=lon)
        return {
            "status": "success",
            "message": "Cache supprimé avec succès"
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