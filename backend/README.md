# 🌤️ Weather API - Backend MVP

Centralized weather API with intelligent Redis cache and OpenWeatherMap data normalization.

## 🚀 Quick Installation

### Prerequisites
- Python 3.11+
- Redis Server
- OpenWeatherMap API Key (free)

### Steps

```bash
# 1. Clone the project
git clone <your-repo>
cd weather-api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your OPENWEATHER_API_KEY

# 5. Start Redis
redis-server

# 6. Launch the API
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 Endpoints

### `GET /api/weather`
Get weather data

**Parameters:**
- `city` (string, optional): City name
- `lat` (float, optional): Latitude
- `lon` (float, optional): Longitude

**Example:**
```bash
curl "http://localhost:8000/api/weather?city=Paris"
curl "http://localhost:8000/api/weather?lat=48.8566&lon=2.3522"
```

### `GET /api/search`
City autocomplete

**Parameters:**
- `q` (string, required): Search term (min 2 characters)
- `limit` (int, optional): Number of results (1-10, default 5)

**Example:**
```bash
curl "http://localhost:8000/api/search?q=Par&limit=5"
```

### `GET /health`
Health check

### `DELETE /api/cache`
Delete cache entry

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

## ⚡ Performance

- **Cache HIT:** < 50ms
- **Cache MISS:** 200-500ms (depending on external API)
- **Cache TTL:** 30 minutes (configurable)

## 🔧 Configuration

`.env` file:
- `OPENWEATHER_API_KEY`: Your API key
- `REDIS_HOST`: Redis host (default: localhost)
- `CACHE_TTL`: Cache duration in seconds (default: 1800)
- `CORS_ORIGINS`: Allowed origins (comma-separated)

## 📊 Response Format

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

## 🧪 Testing

```bash
# Test main endpoint
curl "http://localhost:8000/api/weather?city=Paris"

# Check health
curl "http://localhost:8000/health"
```

## 📝 Get an OpenWeatherMap API Key

1. Create an account at https://openweathermap.org/
2. Go to API Keys
3. Copy the key and add it to `.env`

## 🐳 Docker (optional)

```bash
# Start Redis with Docker
docker run -d -p 6379:6379 redis:alpine
```

## 🛠️ Development

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Interactive documentation
# Open http://localhost:8000/docs
```

## 📈 Next Steps (post-MVP)

- [ ] Rate limiting per IP
- [ ] Metrics and monitoring (Prometheus)
- [ ] Unit tests (pytest)
- [ ] Multi-source weather support
- [ ] Response compression
- [ ] Docker Compose for deployment

## 💡 Development Workflow

-> 3 terminal windows:
 - `source venv/bin/activate` -> `redis-server`
 - `source venv/bin/activate` -> `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
 - `source venv/bin/activate` -> `curl "http://localhost:8000/api/weather?city=Paris" | jq`

-> quit redis / uvicorn = CTRL + C
-> quit venv = `deactivate`