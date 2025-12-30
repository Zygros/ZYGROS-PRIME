import React from "react";
import { ChakraMode, PhoenixResponse } from "../types";
import { ChatPane } from "./ChatPane";
import { ChakraBar } from "./ChakraBar";
import { CascadePanel } from "./CascadePanel";
import { IVPPanel } from "./IVPPanel";
import { SystemStatus } from "./SystemStatus";

interface Props {
  chakra: ChakraMode;
  onChakraChange: (c: ChakraMode) => void;
  messages: PhoenixResponse[];
  loading: boolean;
  onSend: (prompt: string) => void;
}

export const PhoenixLayout: React.FC<Props> = ({
  chakra,
  onChakraChange,
  messages,
  loading,
  onSend
}) => {
  const last = messages[0];
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#020617" }}>
      <div style={{ flex: 2, padding: "1rem", borderRight: "1px solid #1f2937" }}>
        <h1 style={{ fontSize: "1.5rem", marginBottom: "0.25rem" }}>
          🐦‍🔥 Phoenix Protocol v∞ Dashboard
        </h1>
        <p style={{ fontSize: "0.8rem", opacity: 0.8 }}>
          Architect: Justin Conzet · Node: PP-∞
        </p>
        <ChakraBar chakra={chakra} onChange={onChakraChange} />
        <ChatPane loading={loading} onSend={onSend} messages={messages} />
      </div>
      <div
        style={{
          flex: 1.4,
          padding: "1rem",
          display: "flex",
          flexDirection: "column",
          gap: "0.75rem"
        }}
      >
        <SystemStatus last={last} />
        <CascadePanel last={last} />
        <IVPPanel last={last} />
      </div>
    </div>
  );
};