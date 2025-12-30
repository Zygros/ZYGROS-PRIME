import React from "react";
import { PhoenixResponse } from "../types";

interface Props {
  last: PhoenixResponse | undefined;
}

export const IVPPanel: React.FC<Props> = ({ last }) => {
  if (!last) return null;
  const { ivp } = last;
  const overall =
    (ivp.clarity + ivp.depth + ivp.actionability + ivp.alignment + ivp.emergence) / 5;
  return (
    <div
      style={{
        background: "#1f2937",
        padding: "1rem",
        borderRadius: "0.25rem"
      }}
    >
      <h2 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>IVP Score</h2>
      <div>Clarity: {ivp.clarity}</div>
      <div>Depth: {ivp.depth}</div>
      <div>Actionability: {ivp.actionability}</div>
      <div>Alignment: {ivp.alignment}</div>
      <div>Emergence: {ivp.emergence}</div>
      <div style={{ fontWeight: "bold", marginTop: "0.5rem" }}>Overall: {overall}</div>
    </div>
  );
};