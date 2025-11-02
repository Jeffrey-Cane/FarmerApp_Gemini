import { FormEvent, useEffect, useState } from "react";
import { fetchLatestAdvisory, fetchWeatherSummary } from "./api/agriweather";
import type { AdvisoryPayload } from "./types";
import { IndicatorCard } from "./components/IndicatorCard";
import { WeatherVisuals } from "./components/WeatherVisuals";
import { DeepInsights } from "./components/DeepInsights";

const defaultCoordinates = {
  latitude: 0.021,
  longitude: 37.906,
  crop: "maize"
};

export default function App() {
  const [form, setForm] = useState(defaultCoordinates);
  const [advisory, setAdvisory] = useState<AdvisoryPayload | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void loadLatest();
  }, []);

  const loadLatest = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchLatestAdvisory();
      setAdvisory(data);
      setForm({
        latitude: Number(data.weather.latitude.toFixed(3)),
        longitude: Number(data.weather.longitude.toFixed(3)),
        crop: data.crop
      });
    } catch {
      setError("Unable to reach AgriWeather backend. Ensure the FastAPI server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      setLoading(true);
      setError(null);
      const data = await fetchWeatherSummary({
        latitude: form.latitude,
        longitude: form.longitude,
        crop: form.crop
      });
      setAdvisory(data);
    } catch {
      setError("Failed to fetch weather summary. Check your internet connection and inputs.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: "latitude" | "longitude" | "crop", value: string) => {
    setForm((prev) => ({
      ...prev,
      [field]: field === "crop" ? value : Number(value)
    }));
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>AgriWeather Advisor</h1>
        <p>
          Local weather insights and friendly crop guidance powered by Open-Meteo data and Google Gemini
          (optional).
        </p>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Check your field</h2>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Latitude
              <input
                type="number"
                step="0.001"
                value={form.latitude}
                onChange={(event) => handleInputChange("latitude", event.target.value)}
                required
              />
            </label>
            <label>
              Longitude
              <input
                type="number"
                step="0.001"
                value={form.longitude}
                onChange={(event) => handleInputChange("longitude", event.target.value)}
                required
              />
            </label>
            <label>
              Crop
              <input
                type="text"
                value={form.crop}
                onChange={(event) => handleInputChange("crop", event.target.value)}
                placeholder="e.g. maize"
                required
              />
            </label>

            <div className="form-actions">
              <button type="submit" disabled={loading}>
                {loading ? "Loading..." : "Get Advisory"}
              </button>
              <button type="button" onClick={() => void loadLatest()} disabled={loading}>
                Use Default Location
              </button>
            </div>
          </form>

          {error ? <p className="error">{error}</p> : null}
        </section>

        <section className="panel">
          <h2>Today&apos;s Snapshot</h2>
          {advisory ? (
            <div className="snapshot">
              <div className="stat-grid">
                <div>
                  <span className="label">Crop</span>
                  <span className="value">{advisory.crop}</span>
                </div>
                <div>
                  <span className="label">Summary Date</span>
                  <span className="value">{new Date(advisory.summary_date).toLocaleDateString()}</span>
                </div>
                <div>
                  <span className="label">Current Temp</span>
                  <span className="value">{advisory.weather.current_temperature_c}°C</span>
                </div>
                <div>
                  <span className="label">Rain now</span>
                  <span className="value">{advisory.weather.current_precipitation_mm} mm/hr</span>
                </div>
                <div>
                  <span className="label">Today&apos;s Rain</span>
                  <span className="value">{advisory.weather.daily_precipitation_sum_mm} mm</span>
                </div>
                <div>
                  <span className="label">Low / High</span>
                  <span className="value">
                    {advisory.weather.daily_min_temp_c}°C / {advisory.weather.daily_max_temp_c}°C
                  </span>
                </div>
              </div>

              <WeatherVisuals weather={advisory.weather} />

              <div className="advisory">
                <h3>Actionable Advice</h3>
                <p>{advisory.advisory_text ?? "Weather looks stable. Continue regular crop care."}</p>
              </div>

              <div className="indicator-stack">
                <h3>Indicators</h3>
                <div className="indicator-grid">
                  {advisory.indicators.map((indicator) => (
                    <IndicatorCard key={indicator.indicator} indicator={indicator} />
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p>No advisory yet. Submit your location to get started.</p>
          )}
        </section>

        <DeepInsights text={advisory?.advisory_text} />
      </main>

      <footer className="footer">
        <small>
          Built for local testing. Start the FastAPI server on <code>http://127.0.0.1:8000</code> and the React
          dev server on <code>http://127.0.0.1:5173</code>.
        </small>
      </footer>
    </div>
  );
}
