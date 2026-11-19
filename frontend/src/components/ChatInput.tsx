import { useState } from "react";

interface ChatInputProps {
  disabled: boolean;
  onSend: (text: string) => Promise<void>;
}

export default function ChatInput({ disabled, onSend }: ChatInputProps) {
  const [input, setInput] = useState("");

  function submit() {
    const text = input;
    if (!text.trim() || disabled) return;
    setInput("");
    void onSend(text);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    submit();
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
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
        disabled={disabled || !input.trim()}
        className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white px-4 rounded-lg font-medium transition-colors"
      >
        Send
      </button>
    </form>
  );
}
