import redis
import json
from typing import Optional
from datetime import datetime, timedelta
from app.config import settings

class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password if settings.redis_password else None,
            decode_responses=True
        )
    
    def _generate_key(self, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> str:
        """Génère une clé de cache unique"""
        if city:
            return f"weather:city:{city.lower()}"
        elif lat is not None and lon is not None:
            return f"weather:coords:{lat:.2f},{lon:.2f}"
        raise ValueError("City ou coordonnées requises")
    
    def get(self, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> Optional[dict]:
        """Récupère les données du cache"""
        try:
            key = self._generate_key(city, lat, lon)
            data = self.client.get(key)
            if data:
                cached_data = json.loads(data)
                cached_data['cached'] = True
                cached_data['cache_expires_at'] = cached_data.get('cache_expires_at')
                return cached_data
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, data: dict, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None):
        """Enregistre les données dans le cache"""
        try:
            key = self._generate_key(city, lat, lon)
            expires_at = datetime.utcnow() + timedelta(seconds=settings.cache_ttl)
            data['cache_expires_at'] = expires_at.isoformat()
            self.client.setex(
                key,
                settings.cache_ttl,
                json.dumps(data, default=str)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def delete(self, city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None):
        """Supprime une entrée du cache"""
        try:
            key = self._generate_key(city, lat, lon)
            self.client.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
    
    def health_check(self) -> bool:
        """Vérifie la connexion Redis"""
        try:
            return self.client.ping()
        except:
            return False

cache_service = CacheService()