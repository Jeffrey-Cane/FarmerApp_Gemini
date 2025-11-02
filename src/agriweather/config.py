"""Configuration management for AgriWeather backend."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AgriWeather AI"
    api_v1_prefix: str = "/api/v1"
    weather_api_base_url: str = Field(
        "https://api.open-meteo.com/v1",
        description="Base URL for the free Open-Meteo weather API.",
    )
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Optional Google Gemini API key for advisory generation.",
    )
    gemini_model: str = Field(
        "gemini-1.5-flash",
        description="Default Gemini model used for advisory generation.",
    )
    default_latitude: float = Field(
        0.021,
        description="Fallback latitude when none is provided.",
    )
    default_longitude: float = Field(
        37.906,
        description="Fallback longitude when none is provided.",
    )
    default_crop: str = Field(
        "maize",
        description="Default crop used when a crop is not specified in requests.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
