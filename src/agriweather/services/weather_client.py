"""Weather client integration using the free Open-Meteo API."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from fastapi import HTTPException, status

from ..config import Settings
from ..models.weather import WeatherSummary

logger = logging.getLogger(__name__)

FORECAST_PATH = "/forecast"


async def fetch_weather_summary(
    latitude: float, longitude: float, settings: Settings
) -> WeatherSummary:
    """Fetch and normalize a weather summary for the requested location."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto",
        "current_weather": "true",
        "hourly": "precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    }

    async with httpx.AsyncClient(
        base_url=settings.weather_api_base_url,
        timeout=httpx.Timeout(10.0, read=10.0),
    ) as client:
        try:
            response = await client.get(FORECAST_PATH, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:  # pragma: no cover - network failure path
            logger.error("Weather API request failed: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Weather service is temporarily unavailable.",
            ) from exc

    data: dict[str, Any] = response.json()

    try:
        current = data["current_weather"]
        daily = data["daily"]
    except KeyError as exc:  # pragma: no cover - defensive guard
        logger.error("Unexpected response schema from weather API: %s", data)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Weather data could not be parsed.",
        ) from exc

    current_precip = _extract_current_precipitation(data, current["time"])

    summary = WeatherSummary(
        latitude=data.get("latitude", latitude),
        longitude=data.get("longitude", longitude),
        timezone=data.get("timezone", "UTC"),
        current_temperature_c=current["temperature"],
        current_precipitation_mm=current_precip,
        daily_precipitation_sum_mm=_first_value(daily, "precipitation_sum"),
        daily_max_temp_c=_first_value(daily, "temperature_2m_max"),
        daily_min_temp_c=_first_value(daily, "temperature_2m_min"),
        observation_time=current.get("time"),
    )
    return summary


def _extract_current_precipitation(data: dict[str, Any], current_time: str) -> float:
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    precipitation = hourly.get("precipitation", [])

    if current_time in times:
        index = times.index(current_time)
        try:
            return float(precipitation[index])
        except (IndexError, ValueError, TypeError):
            pass

    if precipitation:
        try:
            return float(precipitation[-1])
        except (ValueError, TypeError):
            pass

    return 0.0


def _first_value(payload: dict[str, Any], key: str) -> float:
    values = payload.get(key)
    if not values:
        return 0.0
    try:
        return float(values[0])
    except (TypeError, ValueError):
        return 0.0
