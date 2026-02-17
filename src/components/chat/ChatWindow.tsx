import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { Message } from '@/lib/chat';

interface ChatWindowProps {
  messages: Message[];
  isTyping?: boolean;
}

export function ChatWindow({ messages, isTyping = false }: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
          <div className="text-center">
            <p className="text-lg font-medium mb-2">Welcome to your AI Task Assistant!</p>
            <p className="text-sm">
              Try saying: "Add a task to buy groceries" or "Show me all my tasks"
            </p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((msg, idx) => (
            <ChatMessage
              key={idx}
              role={msg.role}
              content={msg.content}
              timestamp={msg.timestamp}
              toolCalls={msg.tool_calls}
            />
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
