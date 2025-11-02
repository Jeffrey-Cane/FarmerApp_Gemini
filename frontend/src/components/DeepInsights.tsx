import type { FC } from "react";

interface DeepInsightsProps {
  text?: string | null;
}

const normalizeInsights = (text?: string | null): string[] => {
  if (!text) {
    return [];
  }

  const cleaned = text.replace(/Upgrade with a Gemini API key.*$/i, "").trim();
  if (!cleaned) {
    return [];
  }

  const byLine = cleaned
    .split(/\r?\n+/)
    .map((line) => line.replace(/^[-•\s]+/, "").trim())
    .filter((line) => line.length > 0);

  if (byLine.length > 0) {
    return byLine;
  }

  // fallback: split by sentence
  return cleaned
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter((sentence) => sentence.length > 0);
};

export const DeepInsights: FC<DeepInsightsProps> = ({ text }) => {
  const insights = normalizeInsights(text);

  if (!insights.length) {
    return (
      <div className="panel insights-panel">
        <h2>AI Guidance</h2>
        <p className="muted">Provide a Gemini API key to receive detailed, crop-specific recommendations.</p>
      </div>
    );
  }

  return (
    <div className="panel insights-panel">
      <h2>AI Guidance</h2>
      <ul>
        {insights.map((insight, index) => (
          <li key={index}>{insight}</li>
        ))}
      </ul>
    </div>
  );
};
