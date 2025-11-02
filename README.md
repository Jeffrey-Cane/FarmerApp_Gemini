# AgriWeather AI

Weather-aware crop advisory system that combines free Open-Meteo data with Google Gemini insights to help farmers make informed planting and irrigation decisions.

## Quick Start

### Backend (FastAPI)
1. Create and populate an environment file:
   ```bash
   cp .env.example .env
   ```
   Update values as needed (e.g., `GEMINI_API_KEY`).
2. Install dependencies in editable mode (Python 3.10+):
   ```bash
   pip install -e .
   ```
3. Run the API locally:
   ```bash
   uvicorn agriweather.main:create_app --reload
   ```
   The API is available at `http://127.0.0.1:8000` with docs at `/docs`.

### Frontend (React + Vite)
1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   Vite proxies `/api` calls to `http://127.0.0.1:8000`.

## Project Structure
- `src/agriweather/` — FastAPI app, routes, and services.
- `frontend/` — React client with advisory dashboard.
- `docs/architecture.md` — Detailed architecture notes and MVP scope.

## Environment Variables
| Variable            | Description                                                         |
|--------------------|---------------------------------------------------------------------|
| `GEMINI_API_KEY`    | Optional key enabling Gemini-generated advisories.                  |
| `DEFAULT_LATITUDE`  | Latitude used for the beginner-friendly advisory endpoint.         |
| `DEFAULT_LONGITUDE` | Longitude used for the beginner-friendly advisory endpoint.        |
| `DEFAULT_CROP`      | Default crop when none is provided.                                |

## Testing & Linting
- Backend tests: `pytest`
- Backend linting: `ruff`
- Frontend linting: `npm run lint`
- Frontend tests: `npm run test -- --run`
