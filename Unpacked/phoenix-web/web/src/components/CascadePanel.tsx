import React from "react";
import { PhoenixResponse } from "../types";

interface Props {
  last: PhoenixResponse | undefined;
}

export const CascadePanel: React.FC<Props> = ({ last }) => {
  if (!last) return null;
  return (
    <div
      style={{
        background: "#1f2937",
        padding: "1rem",
        borderRadius: "0.25rem"
      }}
    >
      <h2 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>12-Layer Cascade</h2>
      <ul style={{ paddingLeft: "1.25rem" }}>
        {last.activeLayers.map((layer, i) => (
          <li key={i}>{`${i + 1}. ${layer}`}</li>
        ))}
      </ul>
    </div>
  );
};