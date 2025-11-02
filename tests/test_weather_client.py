"""Tests for the weather client integration."""

from __future__ import annotations

from datetime import date

import pytest
import respx
from httpx import Response

from agriweather.config import Settings
from agriweather.services.weather_client import fetch_weather_summary


@pytest.mark.asyncio
async def test_fetch_weather_summary_parses_response() -> None:
    settings = Settings()
    sample_response = {
        "latitude": 0.021,
        "longitude": 37.906,
        "timezone": "Africa/Nairobi",
        "current_weather": {
            "temperature": 28.4,
            "time": "2025-05-20T12:00",
        },
        "hourly": {
            "time": ["2025-05-20T11:00", "2025-05-20T12:00"],
            "precipitation": [0.1, 6.2],
        },
        "daily": {
            "time": ["2025-05-20"],
            "temperature_2m_max": [33.5],
            "temperature_2m_min": [18.3],
            "precipitation_sum": [1.5],
        },
    }

    with respx.mock(base_url=settings.weather_api_base_url) as router:
        router.get("/forecast").mock(return_value=Response(200, json=sample_response))

        summary = await fetch_weather_summary(
            latitude=0.021, longitude=37.906, settings=settings
        )

    assert summary.latitude == pytest.approx(sample_response["latitude"])
    assert summary.longitude == pytest.approx(sample_response["longitude"])
    assert summary.timezone == sample_response["timezone"]
    assert summary.current_temperature_c == sample_response["current_weather"]["temperature"]
    assert summary.current_precipitation_mm == pytest.approx(6.2)
    assert summary.daily_precipitation_sum_mm == pytest.approx(1.5)
    assert summary.daily_max_temp_c == pytest.approx(33.5)
    assert summary.daily_min_temp_c == pytest.approx(18.3)
    assert summary.observation_time == "2025-05-20T12:00"


@pytest.mark.asyncio
async def test_fetch_weather_summary_falls_back_to_last_precipitation() -> None:
    settings = Settings()
    sample_response = {
        "latitude": 0.021,
        "longitude": 37.906,
        "timezone": "Africa/Nairobi",
        "current_weather": {
            "temperature": 24.0,
            "time": "2025-05-20T14:00",
        },
        "hourly": {
            "time": ["2025-05-20T11:00", "2025-05-20T12:00"],
            "precipitation": [0.0, 1.2],
        },
        "daily": {
            "time": ["2025-05-20"],
            "temperature_2m_max": [30.0],
            "temperature_2m_min": [17.0],
            "precipitation_sum": [0.0],
        },
    }

    with respx.mock(base_url=settings.weather_api_base_url) as router:
        router.get("/forecast").mock(return_value=Response(200, json=sample_response))

        summary = await fetch_weather_summary(
            latitude=0.021, longitude=37.906, settings=settings
        )

    assert summary.current_precipitation_mm == pytest.approx(1.2)
