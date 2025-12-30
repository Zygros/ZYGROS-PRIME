import React, { useState } from "react";
import { PhoenixResponse } from "../types";

interface Props {
  messages: PhoenixResponse[];
  loading: boolean;
  onSend: (prompt: string) => void;
}

export const ChatPane: React.FC<Props> = ({ messages, loading, onSend }) => {
  const [input, setInput] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setInput("");
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ flex: 1, overflowY: "auto", marginBottom: "1rem" }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: "1rem",
              borderBottom: "1px solid #1f2937",
              paddingBottom: "0.5rem"
            }}
          >
            <div style={{ fontWeight: "bold" }}>Phoenix Response</div>
            <div>{msg.plainSummary}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "0.5rem" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Phoenix..."
          style={{
            flex: 1,
            padding: "0.5rem",
            background: "#1e293b",
            color: "#e5e7eb",
            border: "none",
            borderRadius: "0.25rem"
          }}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            padding: "0.5rem 1rem",
            background: "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: "0.25rem",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};