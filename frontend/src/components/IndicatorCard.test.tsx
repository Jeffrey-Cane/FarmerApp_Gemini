import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { IndicatorCard } from "./IndicatorCard";
import type { AgronomicIndicator } from "../types";

describe("IndicatorCard", () => {
  const baseIndicator: AgronomicIndicator = {
    indicator: "low_rainfall",
    severity: "warning",
    message: "Low rainfall expected today."
  };

  it("displays indicator title and message", () => {
    render(<IndicatorCard indicator={baseIndicator} />);
    expect(screen.getByText("Low Rainfall")).toBeInTheDocument();
    expect(screen.getByText(baseIndicator.message)).toBeInTheDocument();
  });

  it("applies severity styling", () => {
    render(<IndicatorCard indicator={baseIndicator} />);
    const card = screen.getByText("Low Rainfall").closest("div");
    expect(card).toHaveStyle({ borderLeft: "4px solid #f97316" });
  });
});
