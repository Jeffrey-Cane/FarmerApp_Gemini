"""Gemini advisory service stub for local development."""

from __future__ import annotations

import logging
from datetime import date

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None  # type: ignore

from ..config import Settings
from ..models.weather import AgronomicIndicator, WeatherSummary

logger = logging.getLogger(__name__)


def configure_client(settings: Settings) -> None:
    """Configure Gemini client if dependency and key are available."""

    if not genai or not settings.gemini_api_key:
        logger.warning(
            "Gemini client not fully configured. Set GEMINI_API_KEY and install optional 'ai' dependencies."
        )
        return
    genai.configure(api_key=settings.gemini_api_key)


async def generate_advisory(
    *,
    crop: str,
    summary_date: date,
    weather: WeatherSummary,
    indicators: list[AgronomicIndicator],
    settings: Settings,
) -> str:
    """Generate advisory text using Gemini or fallback message."""

    if not genai or not settings.gemini_api_key:
        return _fallback_advisory(crop=crop, indicators=indicators)

    prompt = _build_prompt(crop=crop, summary_date=summary_date, weather=weather, indicators=indicators)

    try:
        model = genai.GenerativeModel(settings.gemini_model)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else _fallback_advisory(crop, indicators)
    except Exception as exc:  # pragma: no cover - external API errors
        logger.error("Gemini advisory generation failed: %s", exc)
        return _fallback_advisory(crop=crop, indicators=indicators)


def _fallback_advisory(crop: str, indicators: list[AgronomicIndicator]) -> str:
    bullet_points = "\n".join(f"- {indicator.message}" for indicator in indicators)
    return (
        f"Summary for {crop.capitalize()} fields:\n"
        f"{bullet_points or '- Weather looks stable. Continue regular crop care.'}"
    )


def _build_prompt(
    *, crop: str, summary_date: date, weather: WeatherSummary, indicators: list[AgronomicIndicator]
) -> str:
    indicator_section = "\n".join(
        f"- {indicator.indicator} ({indicator.severity}): {indicator.message}" for indicator in indicators
    )
    return f"""
You are an agronomy assistant helping smallholder farmers. Using the weather snapshot and indicators, craft a simple, friendly advisory.

Date: {summary_date.isoformat()}
Crop: {crop}
Location: lat {weather.latitude:.3f}, lon {weather.longitude:.3f} ({weather.timezone})
Current temperature: {weather.current_temperature_c}°C
Current precipitation: {weather.current_precipitation_mm} mm/hr
Daily low/high: {weather.daily_min_temp_c}°C / {weather.daily_max_temp_c}°C
Expected precipitation today: {weather.daily_precipitation_sum_mm} mm

Indicators:
{indicator_section}

Keep the message under 150 words, use plain language, and include practical next steps.
"""
