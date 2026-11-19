import { useState } from "react";
import { ApiError, generateCode } from "../api/client";
import type { Message } from "../types";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /** Send a query; ignored when empty or a request is already in flight. */
  async function send(text: string): Promise<void> {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setLoading(true);

    try {
      const data = await generateCode(trimmed);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.generated_code ?? "No code generated." },
      ]);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  return { messages, loading, error, send };
}
