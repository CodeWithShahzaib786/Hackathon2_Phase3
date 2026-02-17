import React from 'react';
import { ToolCall } from '@/lib/chat';

interface ChatMessageProps {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  toolCalls?: ToolCall[];
}

export function ChatMessage({ role, content, timestamp, toolCalls }: ChatMessageProps) {
  const isUser = role === 'user';
  const isSystem = role === 'system';

  if (isSystem) {
    return null; // Don't display system messages to users
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
        }`}
      >
        <div className="text-sm">{content}</div>

        {toolCalls && toolCalls.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600">
            <div className="text-xs opacity-75">
              {toolCalls.map((tc, idx) => (
                <div key={idx} className="mb-1">
                  {tc.error ? (
                    <span className="text-red-500">❌ {tc.tool_name} failed</span>
                  ) : (
                    <span className="text-green-500">✓ {tc.tool_name}</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="text-xs opacity-50 mt-1">
          {new Date(timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
