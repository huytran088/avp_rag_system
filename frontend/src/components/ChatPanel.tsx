import { useState, useRef, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit(e?: { preventDefault(): void }) {
    e?.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      if (res.status === 429) {
        setError("Rate limit exceeded. Please wait a moment and try again.");
        return;
      }

      if (!res.ok) {
        const detail = await res.json().catch(() => null);
        setError(detail?.detail ?? `Error: ${res.status}`);
        return;
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.generated_code ?? "No code generated." },
      ]);
    } catch {
      setError("Failed to connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <h1 className="text-xl font-bold mb-4 text-center">AVP RAG Chat</h1>

      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-700 text-slate-100"
              }`}
            >
              {msg.role === "assistant" ? (
                <pre className="whitespace-pre-wrap font-mono text-sm">
                  {msg.content}
                </pre>
              ) : (
                <p className="whitespace-pre-wrap">{msg.content}</p>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-700 rounded-lg px-4 py-2 text-slate-400">
              <span className="animate-pulse">Generating...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-center">
            <div className="bg-red-900/50 text-red-300 rounded-lg px-4 py-2 text-sm">
              {error}
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me to generate AVP code..."
          rows={2}
          className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 resize-none focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white px-4 rounded-lg font-medium transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
}
