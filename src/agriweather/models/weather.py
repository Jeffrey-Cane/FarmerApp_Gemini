"""Pydantic models representing weather data structures."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class WeatherSummary(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    current_temperature_c: float = Field(..., description="Current air temperature in Celsius.")
    current_precipitation_mm: float = Field(
        ..., description="Current precipitation rate in millimeters per hour."
    )
    daily_precipitation_sum_mm: float = Field(
        ..., description="Total expected precipitation for the day in millimeters."
    )
    daily_max_temp_c: float = Field(..., description="Daily maximum air temperature in Celsius.")
    daily_min_temp_c: float = Field(..., description="Daily minimum air temperature in Celsius.")
    observation_time: Optional[str] = Field(
        None, description="ISO timestamp of the latest observation from the API."
    )


class AgronomicIndicator(BaseModel):
    indicator: str
    severity: str
    message: str


class AdvisoryPayload(BaseModel):
    crop: str
    summary_date: date
    weather: WeatherSummary
    indicators: list[AgronomicIndicator]
    advisory_text: str | None = Field(
        default=None,
        description="Optional AI-generated advisory for the specified crop and conditions.",
    )
