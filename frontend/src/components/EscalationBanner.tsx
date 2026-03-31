"use client";

export default function EscalationBanner() {
  return (
    <div className="mx-4 mb-4 p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 animate-fade-in">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center flex-shrink-0">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#f59e0b"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="8.5" cy="7" r="4" />
            <line x1="20" y1="8" x2="20" y2="14" />
            <line x1="23" y1="11" x2="17" y2="11" />
          </svg>
        </div>
        <div>
          <p className="text-sm font-display font-bold text-amber-300">
            Escalated to Human Agent
          </p>
          <p className="text-xs text-amber-300/60 font-body mt-0.5">
            A support representative will be with you shortly.
          </p>
        </div>
      </div>
    </div>
  );
}