"""Weather endpoints."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query

from ..config import Settings, get_settings
from ..models.weather import AdvisoryPayload
from ..services import agronomy, gemini_client, weather_client

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/summary", response_model=AdvisoryPayload)
async def get_weather_summary(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees."),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees."),
    crop: str | None = Query(None, max_length=32, description="Crop name (optional)."),
    settings: Settings = Depends(get_settings),
) -> AdvisoryPayload:
    """Return weather summary and agronomic indicators for a location."""

    weather_summary = await weather_client.fetch_weather_summary(
        latitude=latitude, longitude=longitude, settings=settings
    )

    indicators = agronomy.evaluate_indicators(
        weather=weather_summary,
        crop=crop or settings.default_crop,
        summary_date=date.today(),
    )

    gemini_client.configure_client(settings)
    advisory_text = await gemini_client.generate_advisory(
        crop=crop or settings.default_crop,
        summary_date=date.today(),
        weather=weather_summary,
        indicators=indicators,
        settings=settings,
    )

    return AdvisoryPayload(
        crop=crop or settings.default_crop,
        summary_date=date.today(),
        weather=weather_summary,
        indicators=indicators,
        advisory_text=advisory_text,
    )
