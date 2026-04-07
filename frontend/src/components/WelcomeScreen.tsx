"use client";

interface Props {
  onSuggestionClick: (text: string) => void;
}

const suggestions = [
  { icon: "📦", text: "How do I track my order?" },
  { icon: "💳", text: "What payment methods do you accept?" },
  { icon: "↩️", text: "I want to return an item" },
  { icon: "🔑", text: "Help me reset my password" },
];

export default function WelcomeScreen({ onSuggestionClick }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-6 animate-fade-in">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center mb-6 shadow-2xl shadow-brand-500/20">
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
      </div>

      <h2 className="font-display font-bold text-2xl text-text-primary mb-2 tracking-tight">
        How can I help you?
      </h2>
      <p className="text-text-secondary text-sm font-body max-w-md text-center leading-relaxed mb-8">
        I&apos;m your AI support assistant. Ask me about orders, shipping,
        returns, account issues, and more.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
        {suggestions.map((s, idx) => (
          <button
            key={idx}
            onClick={() => onSuggestionClick(s.text)}
            className="group flex items-center gap-3 px-4 py-3.5 rounded-xl bg-surface-tertiary border border-white/[0.04] hover:border-brand-500/30 hover:bg-surface-elevated transition-all duration-200 text-left"
          >
            <span className="text-lg">{s.icon}</span>
            <span className="text-sm text-text-secondary group-hover:text-text-primary transition-colors font-body">
              {s.text}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}