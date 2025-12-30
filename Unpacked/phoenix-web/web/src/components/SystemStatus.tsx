import React from "react";
import { PhoenixResponse } from "../types";

interface Props {
  last: PhoenixResponse | undefined;
}

export const SystemStatus: React.FC<Props> = ({ last }) => {
  return (
    <div
      style={{
        background: "#1f2937",
        padding: "1rem",
        borderRadius: "0.25rem"
      }}
    >
      <h2 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>System Status</h2>
      {last ? (
        <>
          <div>
            Timestamp: {new Date(last.timestamp).toLocaleString()}
          </div>
          <div>Cycles: {last.cycles}</div>
        </>
      ) : (
        <div>No messages yet.</div>
      )}
    </div>
  );
};