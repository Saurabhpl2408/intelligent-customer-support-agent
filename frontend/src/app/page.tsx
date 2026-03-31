"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { sendMessage } from "@/lib/api";
import { ChatMessage, SourceDocument } from "@/lib/types";
import {
  ChatHeader,
  ChatInput,
  MessageBubble,
  TypingIndicator,
  WelcomeScreen,
  EscalationBanner,
} from "@/components";

interface DisplayMessage {
  message: ChatMessage;
  sources?: SourceDocument[];
  intent?: string | null;
}

export default function Home() {
  const [sessionId] = useState(() => uuidv4().replace(/-/g, "").slice(0, 16));
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isEscalated, setIsEscalated] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = useCallback(
    async (text: string) => {
      if (isEscalated) return;

      const userMsg: ChatMessage = {
        role: "user",
        content: text,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, { message: userMsg }]);
      setIsLoading(true);

      // Build history from existing messages (only role + content for the API)
      const history: ChatMessage[] = messages.map((m) => ({
        role: m.message.role,
        content: m.message.content,
        timestamp: m.message.timestamp,
      }));

      try {
        const response = await sendMessage({
          session_id: sessionId,
          message: text,
          history,
        });

        const assistantMsg: DisplayMessage = {
          message: {
            role: "assistant",
            content: response.reply,
            timestamp: response.timestamp,
          },
          sources: response.sources,
          intent: response.intent,
        };

        setMessages((prev) => [...prev, assistantMsg]);

        if (response.status === "escalated") {
          setIsEscalated(true);
        }
      } catch (err) {
        const errorMsg: DisplayMessage = {
          message: {
            role: "assistant",
            content:
              "Sorry, something went wrong. Please try again or refresh the page.",
            timestamp: new Date().toISOString(),
          },
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [messages, sessionId, isEscalated]
  );

  return (
    <div className="h-screen flex flex-col bg-surface-primary">
      <ChatHeader />

      {/* Messages area */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto">
        {messages.length === 0 && !isLoading ? (
          <WelcomeScreen onSuggestionClick={handleSend} />
        ) : (
          <div className="max-w-3xl mx-auto px-4 py-6 space-y-5">
            {messages.map((m, idx) => (
              <MessageBubble
                key={idx}
                message={m.message}
                sources={m.sources}
                intent={m.intent}
                isLatest={idx === messages.length - 1}
              />
            ))}

            {isLoading && <TypingIndicator />}
          </div>
        )}
      </div>

      {/* Escalation banner */}
      {isEscalated && <EscalationBanner />}

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading || isEscalated} />
    </div>
  );
}