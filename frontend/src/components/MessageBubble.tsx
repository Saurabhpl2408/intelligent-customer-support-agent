"use client";

import { ChatMessage, SourceDocument } from "@/lib/types";
import SourceChips from "./SourceChips";

interface Props {
  message: ChatMessage;
  sources?: SourceDocument[];
  intent?: string | null;
  isLatest?: boolean;
}

export default function MessageBubble({
  message,
  sources,
  intent,
  isLatest,
}: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={`message-enter flex w-full ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] md:max-w-[70%] ${
          isUser ? "order-1" : "order-1"
        }`}
      >
        <div
          className={`flex items-center gap-2 mb-1.5 ${
            isUser ? "flex-row-reverse" : "flex-row"
          }`}
        >
          <div
            className={`w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-bold font-mono ${
              isUser
                ? "bg-brand-600/30 text-brand-300"
                : "bg-surface-elevated text-text-secondary"
            }`}
          >
            {isUser ? "U" : "AI"}
          </div>
          <span className="text-[11px] text-text-muted font-mono">
            {isUser ? "You" : "Agent"}
          </span>
          {intent && !isUser && (
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 font-mono border border-brand-500/20">
              {intent}
            </span>
          )}
        </div>

        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed font-body ${
            isUser
              ? "bg-brand-600 text-white rounded-br-md"
              : "bg-surface-tertiary text-text-primary border border-white/[0.04] rounded-bl-md"
          }`}
        >
          {message.content}
        </div>

        {!isUser && sources && sources.length > 0 && (
          <SourceChips sources={sources} />
        )}
      </div>
    </div>
  );
}