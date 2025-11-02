"""Beginner-friendly agronomic indicators based on simple thresholds."""

from __future__ import annotations

from datetime import date

from ..models.weather import AgronomicIndicator, WeatherSummary


def evaluate_indicators(
    weather: WeatherSummary, crop: str, summary_date: date
) -> list[AgronomicIndicator]:
    """Generate a minimal set of agronomic indicators for the frontend."""

    indicators: list[AgronomicIndicator] = []

    if weather.daily_precipitation_sum_mm < 2:
        indicators.append(
            AgronomicIndicator(
                indicator="low_rainfall",
                severity="warning",
                message="Low rainfall expected today. Consider light irrigation if soil is dry.",
            )
        )

    if weather.current_precipitation_mm > 5:
        indicators.append(
            AgronomicIndicator(
                indicator="heavy_rain",
                severity="alert",
                message="Heavy rain right now. Delay field operations to avoid soil compaction.",
            )
        )

    if weather.daily_max_temp_c > 32:
        indicators.append(
            AgronomicIndicator(
                indicator="heat_stress",
                severity="alert",
                message="High temperatures today. Check for wilting and ensure crops have enough moisture.",
            )
        )

    if weather.daily_min_temp_c < 12:
        indicators.append(
            AgronomicIndicator(
                indicator="cool_night",
                severity="info",
                message="Cool night forecast. Young seedlings may grow slower; monitor for pests.",
            )
        )

    if not indicators:
        indicators.append(
            AgronomicIndicator(
                indicator="favorable",
                severity="info",
                message="Weather looks favorable for routine field work today.",
            )
        )

    return indicators
