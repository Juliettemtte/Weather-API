# 🌤️ Weather API - Backend MVP

API météo centralisée avec cache intelligent Redis et normalisation des données OpenWeatherMap.

## 🚀 Installation rapide

### Prérequis
- Python 3.11+
- Redis Server
- Clé API OpenWeatherMap (gratuite)

### Étapes

```bash
# 1. Cloner le projet
git clone <your-repo>
cd weather-api

# 2. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre OPENWEATHER_API_KEY

# 5. Démarrer Redis
redis-server

# 6. Lancer l'API
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

## 📡 Endpoints

### `GET /api/weather`
Récupère les données météo

**Paramètres:**
- `city` (string, optionnel): Nom de la ville
- `lat` (float, optionnel): Latitude
- `lon` (float, optionnel): Longitude

**Exemple:**
```bash
curl "http://localhost:8000/api/weather?city=Paris"
curl "http://localhost:8000/api/weather?lat=48.8566&lon=2.3522"
```

### `GET /api/search`
Autocomplétion de villes

**Paramètres:**
- `q` (string, requis): Terme de recherche (min 2 caractères)
- `limit` (int, optionnel): Nombre de résultats (1-10, défaut 5)

**Exemple:**
```bash
curl "http://localhost:8000/api/search?q=Par&limit=5"
```

### `GET /health`
Vérification de santé

### `DELETE /api/cache`
Supprime une entrée du cache

## 🏗️ Architecture

```
Frontend (Angular)
    ↓ HTTP Request
FastAPI Backend
    ↓ Cache Check
Redis Cache (TTL: 30min)
    ↓ Cache Miss
OpenWeatherMap API
```

## ⚡ Performances

- **Cache HIT:** < 50ms
- **Cache MISS:** 200-500ms (selon API externe)
- **TTL Cache:** 30 minutes (configurable)

## 🔧 Configuration

Fichier `.env`:
- `OPENWEATHER_API_KEY`: Votre clé API
- `REDIS_HOST`: Hôte Redis (défaut: localhost)
- `CACHE_TTL`: Durée du cache en secondes (défaut: 1800)
- `CORS_ORIGINS`: Origines autorisées (séparées par virgules)

## 📊 Format de réponse

```json
{
  "city": "Paris",
  "country": "FR",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "current": {
    "temperature": 15.2,
    "feels_like": 14.1,
    "condition": "Clear",
    "humidity": 65,
    "wind_speed": 12.5
  },
  "hourly": [...],
  "daily": [...],
  "cached": true
}
```

## 🧪 Tests

```bash
# Test endpoint principal
curl "http://localhost:8000/api/weather?city=Paris"

# Vérifier la santé
curl "http://localhost:8000/health"
```

## 📝 Obtenir une clé API OpenWeatherMap

1. Créer un compte sur https://openweathermap.org/
2. Aller dans API Keys
3. Copier la clé et l'ajouter dans `.env`

## 🐳 Docker (optionnel)

```bash
# Démarrer Redis avec Docker
docker run -d -p 6379:6379 redis:alpine
```

## 🛠️ Développement

```bash
# Mode développement avec rechargement auto
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Documentation interactive
# Ouvrir http://localhost:8000/docs
```

## 📈 Prochaines étapes (post-MVP)

- [ ] Rate limiting par IP
- [ ] Métriques et monitoring (Prometheus)
- [ ] Tests unitaires (pytest)
- [ ] Support multi-sources météo
- [ ] Compression des réponses
- [ ] Docker Compose pour déploiement

-> 3 windows
 - source venv/bin/activate -> redis-server 
 - source venv/bin/activate -> uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
 - source venv/bin/activate -> curl "http://localhost:8000/api/weather?city=Paris" | jq

-> quit redis / uvicorn = CTRL - C
-> quit venv = deactivate