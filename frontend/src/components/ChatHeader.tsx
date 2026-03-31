"use client";

import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";

export default function ChatHeader() {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    checkHealth()
      .then((h) => setOnline(h.status === "healthy"))
      .catch(() => setOnline(false));
  }, []);

  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06] bg-surface-secondary/80 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-500/20">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="white"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>

        <div>
          <h1 className="font-display font-bold text-sm tracking-tight text-text-primary">
            Support Agent
          </h1>
          <p className="text-[11px] text-text-muted font-mono tracking-wide uppercase">
            AI-Powered Assistant
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div
          className={`w-2 h-2 rounded-full ${
            online === null
              ? "bg-yellow-500 animate-pulse"
              : online
              ? "bg-emerald-400 shadow-sm shadow-emerald-400/50"
              : "bg-red-400"
          }`}
        />
        <span className="text-xs text-text-muted font-body">
          {online === null ? "Connecting" : online ? "Online" : "Offline"}
        </span>
      </div>
    </header>
  );
}