import type { FC } from "react";

import type { WeatherSummary } from "../types";

interface WeatherVisualsProps {
  weather: WeatherSummary;
}

const clamp = (value: number, min: number, max: number) => {
  if (Number.isNaN(value)) {
    return min;
  }
  return Math.min(Math.max(value, min), max);
};

export const WeatherVisuals: FC<WeatherVisualsProps> = ({ weather }) => {
  const { daily_min_temp_c, daily_max_temp_c, current_temperature_c, daily_precipitation_sum_mm } = weather;

  const temperatureRange = daily_max_temp_c - daily_min_temp_c || 1;
  const normalizedTemp = clamp(((current_temperature_c - daily_min_temp_c) / temperatureRange) * 100, 0, 100);

  const precipitationTarget = 10; // simple agronomic benchmark for rain-rich day
  const normalizedPrecip = clamp((daily_precipitation_sum_mm / precipitationTarget) * 100, 0, 100);

  return (
    <div className="visual-grid">
      <div className="visual-card">
        <header>
          <span className="visual-title">Temperature Trend</span>
          <span className="visual-subtitle">Current vs. daily low/high</span>
        </header>
        <div className="visual-body">
          <div className="temp-scale">
            <span>{daily_min_temp_c}°C</span>
            <div className="temp-bar">
              <div className="temp-indicator" style={{ left: `${normalizedTemp}%` }} />
            </div>
            <span>{daily_max_temp_c}°C</span>
          </div>
          <p className="visual-footnote">Current: {current_temperature_c}°C</p>
        </div>
      </div>

      <div className="visual-card">
        <header>
          <span className="visual-title">Rain Outlook</span>
          <span className="visual-subtitle">Total today vs. 10 mm target</span>
        </header>
        <div className="visual-body">
          <div className="precip-gauge">
            <div className="precip-fill" style={{ width: `${normalizedPrecip}%` }} />
          </div>
          <p className="visual-footnote">Expected rainfall: {daily_precipitation_sum_mm} mm</p>
        </div>
      </div>
    </div>
  );
};
