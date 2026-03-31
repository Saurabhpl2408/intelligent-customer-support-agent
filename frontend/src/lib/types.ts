export interface ChatMessage {
    role: "user" | "assistant" | "system";
    content: string;
    timestamp: string;
  }
  
  export interface SourceDocument {
    content: string;
    source: string | null;
    score: number | null;
  }
  
  export interface ChatRequest {
    session_id: string;
    message: string;
    history: ChatMessage[];
  }
  
  export interface ChatResponse {
    session_id: string;
    reply: string;
    intent: string | null;
    sources: SourceDocument[];
    status: "active" | "escalated" | "resolved";
    timestamp: string;
  }
  
  export interface HealthResponse {
    status: string;
    version: string;
    vectorstore_loaded: boolean;
  }