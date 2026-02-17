// Chat API client functions

export interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  result?: Record<string, any> | null;
  error?: string | null;
}

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  tool_calls?: ToolCall[];
}

export interface ChatRequest {
  message: string;
  session_id?: string | null;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  tool_calls?: ToolCall[] | null;
  timestamp: string;
}

/**
 * Send a chat message to the backend API
 */
export async function sendChatMessage(
  message: string,
  sessionId?: string | null,
  token?: string
): Promise<ChatResponse> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const response = await fetch(`${apiUrl}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    } as ChatRequest),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to send message' }));
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}

/**
 * Clear a chat session
 */
export async function clearChatSession(
  sessionId: string,
  token?: string
): Promise<void> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const response = await fetch(`${apiUrl}/api/chat/session/${sessionId}`, {
    method: 'DELETE',
    headers: {
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to clear session' }));
    throw new Error(error.detail || 'Failed to clear session');
  }
}
