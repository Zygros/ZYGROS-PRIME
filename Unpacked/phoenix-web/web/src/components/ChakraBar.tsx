import React from "react";
import { ChakraMode } from "../types";

interface Props {
  chakra: ChakraMode;
  onChange: (mode: ChakraMode) => void;
}

const CHAKRAS: {
  mode: ChakraMode;
  label: string;
  color: string;
}[] = [
  { mode: "ROOT", label: "Root", color: "#991B1B" },
  { mode: "SACRAL", label: "Sacral", color: "#EA580C" },
  { mode: "SOLAR", label: "Solar", color: "#CA8A04" },
  { mode: "HEART", label: "Heart", color: "#15803D" },
  { mode: "THROAT", label: "Throat", color: "#2563EB" },
  { mode: "THIRD_EYE", label: "Third Eye", color: "#4C1D95" },
  { mode: "CROWN", label: "Crown", color: "#7E22CE" }
];

export const ChakraBar: React.FC<Props> = ({ chakra, onChange }) => {
  return (
    <div style={{ display: "flex", marginBottom: "1rem", flexWrap: "wrap" }}>
      {CHAKRAS.map(({ mode, label, color }) => (
        <button
          key={mode}
          onClick={() => onChange(mode)}
          style={{
            background: chakra === mode ? color : "#1f2937",
            color: "#e5e7eb",
            padding: "0.5rem 0.75rem",
            marginRight: "0.5rem",
            marginBottom: "0.5rem",
            borderRadius: "0.25rem",
            border: "none",
            cursor: "pointer"
          }}
        >
          {label}
        </button>
      ))}
    </div>
  );
};