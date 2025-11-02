"""FastAPI application factory for AgriWeather AI."""

from fastapi import FastAPI

from .config import get_settings
from .routes import advisories, weather


def create_app() -> FastAPI:
    """Create and configure FastAPI app."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.include_router(weather.router, prefix=settings.api_v1_prefix)
    app.include_router(advisories.router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["health"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app
