"use client";

import { useState, useRef, KeyboardEvent } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${Math.min(el.scrollHeight, 150)}px`;
    }
  };

  return (
    <div className="px-4 py-4 border-t border-white/[0.06] bg-surface-secondary/80 backdrop-blur-md">
      <div className="max-w-3xl mx-auto">
        <div className="input-glow flex items-end gap-3 bg-surface-tertiary rounded-2xl border border-white/[0.06] px-4 py-3 transition-all">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            onInput={handleInput}
            placeholder="Ask a question..."
            disabled={disabled}
            rows={1}
            className="flex-1 bg-transparent text-sm text-text-primary placeholder:text-text-muted font-body outline-none resize-none max-h-[150px] leading-relaxed disabled:opacity-40"
          />

          <button
            onClick={handleSend}
            disabled={!value.trim() || disabled}
            className="flex-shrink-0 w-9 h-9 rounded-xl bg-brand-600 hover:bg-brand-500 disabled:bg-surface-elevated disabled:opacity-40 flex items-center justify-center transition-all duration-200 hover:shadow-lg hover:shadow-brand-500/20 disabled:shadow-none"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>

        <p className="text-center text-[10px] text-text-muted mt-2.5 font-mono">
          Powered by LangGraph + RAG · Responses may not always be accurate
        </p>
      </div>
    </div>
  );
}