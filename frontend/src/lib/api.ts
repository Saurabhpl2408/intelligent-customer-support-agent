import { ChatRequest, ChatResponse, HealthResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "Unknown error");
    throw new ApiError(body, res.status);
  }

  return res.json();
}

export async function sendMessage(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function checkHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}