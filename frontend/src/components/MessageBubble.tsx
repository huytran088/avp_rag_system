import type { Message } from "../types";

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser ? "bg-blue-600 text-white" : "bg-slate-700 text-slate-100"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <pre className="whitespace-pre-wrap font-mono text-sm">{message.content}</pre>
        )}
      </div>
    </div>
  );
}
