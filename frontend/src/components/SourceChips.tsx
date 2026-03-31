"use client";

import { useState } from "react";
import { SourceDocument } from "@/lib/types";

interface Props {
  sources: SourceDocument[];
}

export default function SourceChips({ sources }: Props) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mt-2 ml-1">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1.5 text-[11px] text-text-muted hover:text-text-secondary transition-colors font-mono"
      >
        <svg
          width="12"
          height="12"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
        </svg>
        {sources.length} source{sources.length > 1 ? "s" : ""}
        <svg
          width="10"
          height="10"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          className={`transition-transform ${expanded ? "rotate-180" : ""}`}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {expanded && (
        <div className="mt-2 space-y-2 animate-fade-in">
          {sources.map((src, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-surface-secondary border border-white/[0.04] text-xs"
            >
              {src.source && (
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-mono text-brand-400 text-[10px]">
                    {src.source}
                  </span>
                  {src.score !== null && (
                    <span className="font-mono text-text-muted text-[10px]">
                      {(src.score * 100).toFixed(0)}% match
                    </span>
                  )}
                </div>
              )}
              <p className="text-text-secondary leading-relaxed line-clamp-3">
                {src.content}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}