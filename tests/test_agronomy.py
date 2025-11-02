"""Tests for agronomy indicator evaluation."""

from __future__ import annotations

from datetime import date

from agriweather.models.weather import WeatherSummary
from agriweather.services import agronomy


def make_weather(**overrides):
    base = WeatherSummary(
        latitude=0.021,
        longitude=37.906,
        timezone="UTC",
        current_temperature_c=25.0,
        current_precipitation_mm=0.0,
        daily_precipitation_sum_mm=5.0,
        daily_max_temp_c=28.0,
        daily_min_temp_c=18.0,
        observation_time="2025-05-20T12:00",
    )
    return base.copy(update=overrides)


def test_evaluate_indicators_warns_on_low_rainfall() -> None:
    weather = make_weather(daily_precipitation_sum_mm=0.5)
    indicators = agronomy.evaluate_indicators(weather, "maize", date.today())
    assert any(ind.indicator == "low_rainfall" for ind in indicators)


def test_evaluate_indicators_alerts_on_heat_and_rain() -> None:
    weather = make_weather(current_precipitation_mm=6.5, daily_max_temp_c=34.0)
    indicators = agronomy.evaluate_indicators(weather, "maize", date.today())
    indicator_names = {ind.indicator for ind in indicators}
    assert {"heavy_rain", "heat_stress"}.issubset(indicator_names)


def test_evaluate_indicators_favorable_when_none_triggered() -> None:
    weather = make_weather()
    indicators = agronomy.evaluate_indicators(weather, "maize", date.today())
    assert indicators == [
        agronomy.AgronomicIndicator(
            indicator="favorable",
            severity="info",
            message="Weather looks favorable for routine field work today.",
        )
    ]
