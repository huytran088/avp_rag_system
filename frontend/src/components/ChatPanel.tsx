import { useEffect, useRef } from "react";
import { useChat } from "../hooks/useChat";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

export default function ChatPanel() {
  const { messages, loading, error, send } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <h1 className="text-xl font-bold mb-4 text-center">AVP RAG Chat</h1>

      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
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

      <ChatInput disabled={loading} onSend={send} />
    </div>
  );
}
