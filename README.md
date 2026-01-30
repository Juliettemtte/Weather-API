# Weather API — Full Project

This repository contains a complete weather application with a Python FastAPI backend and an Angular frontend. The project is configured to run with Docker Compose (Redis + backend + frontend).

## Demo
https://github.com/user-attachments/assets/4f7cca67-20d0-4ba3-9168-672a15edc0c6


## Overview
- Backend: REST API built with FastAPI and Uvicorn, using Redis for caching.
- Frontend: Angular application serving the user interface.
- Orchestration: `docker-compose.yml` to run all services locally.

## Project layout
- `backend/` — backend code (FastAPI app, services, normalizers, etc.)
- `frontend/` — frontend code (Angular)
- `docker-compose.yml` — Docker Compose configuration (redis, backend, frontend)

## Prerequisites
- Docker and Docker Compose installed
- (Optional) Node.js and Python if you prefer to run services locally without Docker

## Environment variables
- An example environment file for the backend is available at `backend/.env.example`. Copy it to `backend/.env` and update values as needed.
- The frontend expects an `API_URL` environment variable. When using Docker Compose, `API_URL` is set in the `frontend` service.

## Run (Docker Compose)
To start the complete application (Redis + backend + frontend):

```bash
docker-compose up --build
```

After startup:
- Backend API is available at `http://localhost:8000` (prefix `/api` if the app exposes it)
- Frontend is available at `http://localhost:4200`

Run in detached mode:

```bash
docker-compose up -d --build
```

Stop and remove containers:

```bash
docker-compose down
```

## Backend — Quick details
- Location: `backend/`
- Stack: Python, FastAPI, Uvicorn, Redis (cache), Pydantic, httpx
- Dependencies: listed in `backend/requirements.txt`
- Entry point: `backend/app/main.py`
- Configuration: `backend/config.py`

Local development (without Docker):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend — Quick details
- Location: `frontend/`
- Stack: Angular

Local development (without Docker):

```bash
cd frontend
npm install
npm run start
```

Ensure `API_URL` points to the running API.

## Tests & Quality
- If tests exist, run them according to the backend or frontend instructions.

## Deployment
- The project is container-ready; adapt Docker/CI configuration for your deployment target.
- Secure secrets and API keys via environment management in production.

## Contribution
- Fork the repo, create a feature branch, open a pull request with a clear description of changes.

## License
This repository includes a restrictive license file. See `LICENSE` for details.
