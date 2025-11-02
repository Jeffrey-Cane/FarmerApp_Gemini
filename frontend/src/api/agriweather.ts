import client from "./client";
import type { AdvisoryPayload } from "../types";

export interface SummaryRequest {
  latitude: number;
  longitude: number;
  crop?: string;
}

export const fetchWeatherSummary = async (
  params: SummaryRequest
): Promise<AdvisoryPayload> => {
  const response = await client.get<AdvisoryPayload>('/weather/summary', {
    params
  });
  return response.data;
};

export const fetchLatestAdvisory = async (): Promise<AdvisoryPayload> => {
  const response = await client.get<AdvisoryPayload>('/advisories/latest');
  return response.data;
};
