import type { Metadata } from "next";
import "./../styles/global.css";

export const metadata: Metadata = {
  title: "Support Agent — AI Customer Support",
  description:
    "Intelligent customer support agent powered by LangGraph and RAG",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}