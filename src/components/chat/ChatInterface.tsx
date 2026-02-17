import React, { useState, useEffect } from 'react';
import { ChatWindow } from './ChatWindow';
import { ChatInput } from './ChatInput';
import { Message, sendChatMessage, clearChatSession } from '@/lib/chat';

interface ChatInterfaceProps {
  token?: string;
}

export function ChatInterface({ token }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);
    setError(null);

    try {
      // Send message to backend
      const response = await sendChatMessage(messageText, sessionId, token);

      // Update session ID if this is a new conversation
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      // Add assistant response to UI
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
        tool_calls: response.tool_calls || undefined,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');

      // Add error message to chat
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${err instanceof Error ? err.message : 'Unknown error'}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleClearSession = async () => {
    if (!sessionId) return;

    try {
      await clearChatSession(sessionId, token);
      setMessages([]);
      setSessionId(null);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to clear session');
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900 rounded-lg shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 p-4">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            AI Task Assistant
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Manage your tasks with natural language
          </p>
        </div>
        {sessionId && (
          <button
            onClick={handleClearSession}
            className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            Clear conversation
          </button>
        )}
      </div>

      {/* Error banner */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 p-3">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      {/* Messages */}
      <ChatWindow messages={messages} isTyping={isTyping} />

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
    </div>
  );
}
