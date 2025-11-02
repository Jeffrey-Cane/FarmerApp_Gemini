import type { FC } from "react";

import type { AgronomicIndicator } from "../types";

interface IndicatorCardProps {
  indicator: AgronomicIndicator;
}

const severityColor: Record<AgronomicIndicator["severity"], string> = {
  info: "#0d9488",
  warning: "#f97316",
  alert: "#dc2626"
};

const prettyIndicatorName = (indicator: string): string =>
  indicator
    .split("_")
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1))
    .join(" ");

export const IndicatorCard: FC<IndicatorCardProps> = ({ indicator }) => (
  <div
    style={{
      borderLeft: `4px solid ${severityColor[indicator.severity]}`,
      padding: "0.75rem 1rem",
      background: "#fff",
      borderRadius: "0.5rem",
      boxShadow: "0 1px 2px rgba(15, 23, 42, 0.1)"
    }}
  >
    <p style={{ fontWeight: 600, marginBottom: "0.25rem" }}>{prettyIndicatorName(indicator.indicator)}</p>
    <p style={{ margin: 0 }}>{indicator.message}</p>
  </div>
);
