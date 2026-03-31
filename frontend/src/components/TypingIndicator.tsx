"use client";

export default function TypingIndicator() {
  return (
    <div className="flex justify-start message-enter">
      <div className="max-w-[80%]">
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-bold font-mono bg-surface-elevated text-text-secondary">
            AI
          </div>
          <span className="text-[11px] text-text-muted font-mono">
            Agent is typing
          </span>
        </div>
        <div className="px-5 py-4 rounded-2xl rounded-bl-md bg-surface-tertiary border border-white/[0.04] flex items-center gap-1.5">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}