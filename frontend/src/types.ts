export interface AgronomicIndicator {
  indicator: string;
  severity: "info" | "warning" | "alert";
  message: string;
}

export interface WeatherSummary {
  latitude: number;
  longitude: number;
  timezone: string;
  current_temperature_c: number;
  current_precipitation_mm: number;
  daily_precipitation_sum_mm: number;
  daily_max_temp_c: number;
  daily_min_temp_c: number;
  observation_time?: string;
}

export interface AdvisoryPayload {
  crop: string;
  summary_date: string;
  weather: WeatherSummary;
  indicators: AgronomicIndicator[];
  advisory_text?: string | null;
}
