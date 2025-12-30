import React, { useState } from "react";
import { PhoenixLayout } from "./components/PhoenixLayout";
import { ChakraMode, PhoenixResponse } from "./types";

const API_URL = (import.meta as any).env.VITE_PHOENIX_API_URL as string;

export const App: React.FC = () => {
  const [chakra, setChakra] = useState<ChakraMode>("THIRD_EYE");
  const [messages, setMessages] = useState<PhoenixResponse[]>([]);
  const [loading, setLoading] = useState(false);

  async function sendPrompt(prompt: string) {
    if (!prompt.trim() || !API_URL) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/phoenix/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, chakra })
      });
      const data = (await res.json()) as PhoenixResponse;
      setMessages((prev) => [data, ...prev]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <PhoenixLayout
      chakra={chakra}
      onChakraChange={setChakra}
      messages={messages}
      loading={loading}
      onSend={sendPrompt}
    />
  );
};