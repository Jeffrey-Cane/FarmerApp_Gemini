"""Advisory endpoints."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends

from ..config import Settings, get_settings
from ..models.weather import AdvisoryPayload
from ..services import agronomy, gemini_client, weather_client

router = APIRouter(prefix="/advisories", tags=["advisories"])


@router.get("/latest", response_model=AdvisoryPayload)
async def get_latest_advisory(settings: Settings = Depends(get_settings)) -> AdvisoryPayload:
    """Return advisory for default location and crop (beginner-friendly quick start)."""

    weather_summary = await weather_client.fetch_weather_summary(
        latitude=settings.default_latitude,
        longitude=settings.default_longitude,
        settings=settings,
    )

    indicators = agronomy.evaluate_indicators(
        weather=weather_summary,
        crop=settings.default_crop,
        summary_date=date.today(),
    )

    gemini_client.configure_client(settings)
    advisory_text = await gemini_client.generate_advisory(
        crop=settings.default_crop,
        summary_date=date.today(),
        weather=weather_summary,
        indicators=indicators,
        settings=settings,
    )

    return AdvisoryPayload(
        crop=settings.default_crop,
        summary_date=date.today(),
        weather=weather_summary,
        indicators=indicators,
        advisory_text=advisory_text,
    )
