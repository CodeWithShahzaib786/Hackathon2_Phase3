# Research: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-17
**Purpose**: Document technology decisions and research findings for Phase III implementation

## Overview

This document captures research findings and technology decisions for integrating conversational AI into the Phase II todo application. The goal is to enable natural language task management while maintaining security, performance, and integration with existing systems.

---

## 1. OpenAI Agents SDK Integration

### Research Question
How to integrate OpenAI Agents SDK in Python backend for natural language processing?

### Findings

**OpenAI Agents SDK (Python)**:
- Official Python SDK: `openai` package (v1.0+)
- Agents SDK provides structured way to create AI agents with tools
- Supports function calling (tools) for structured outputs
- Handles conversation context automatically
- Streaming responses supported via async generators

**Key Features**:
- **Function Calling**: Define tools as Python functions with type hints
- **Conversation History**: SDK manages message history automatically
- **Streaming**: Real-time response generation via `stream=True`
- **Error Handling**: Built-in retry logic and error types
- **Token Management**: Automatic token counting and context window management

**Best Practices**:
1. Use `gpt-4-turbo` or `gpt-3.5-turbo` for cost/performance balance
2. Define tools with clear descriptions and parameter schemas
3. Implement exponential backoff for rate limit errors
4. Stream responses for better UX (show typing indicator)
5. Set reasonable `max_tokens` to control costs
6. Use `temperature=0.7` for balanced creativity/consistency

**Code Pattern**:
```python
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=conversation_history,
    tools=mcp_tools,
    stream=True
)
```

### Decision

**Selected**: OpenAI Python SDK with GPT-4-turbo model
- **Rationale**: Official SDK, well-documented, supports all required features
- **Cost**: ~$0.01 per 1K tokens (input), ~$0.03 per 1K tokens (output)
- **Performance**: 2-3 second response time for typical queries
- **Alternatives Considered**:
  - GPT-3.5-turbo: Cheaper but less accurate for complex commands
  - Claude API: Good alternative but requires different SDK
  - Local models: Too slow and resource-intensive

---

## 2. MCP SDK Implementation

### Research Question
How to implement MCP (Model Context Protocol) tools that wrap existing REST APIs?

### Findings

**MCP SDK Overview**:
- MCP is a protocol for AI agents to interact with external tools
- Official MCP SDK provides Python implementation
- Tools are defined as JSON schemas with parameter validation
- Handlers execute the actual tool logic (API calls)

**Tool Definition Pattern**:
```python
{
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description"}
            },
            "required": ["title"]
        }
    }
}
```

**Handler Pattern**:
```python
async def handle_create_task(user_id: str, title: str, description: str = None):
    # Call existing Phase II task API
    task_service = TaskService(session)
    return await task_service.create_task(user_id, title, description)
```

**Best Practices**:
1. Keep tool descriptions clear and concise (AI reads these)
2. Use JSON Schema for parameter validation
3. Return structured data (JSON) from handlers
4. Include error handling in handlers
5. Pass user context (user_id, auth) to handlers
6. Log all tool calls for debugging

### Decision

**Selected**: Custom MCP tool implementation using OpenAI function calling
- **Rationale**: OpenAI SDK has built-in function calling support, no need for separate MCP SDK
- **Implementation**: Define tools as OpenAI functions, handlers call existing Phase II APIs
- **Alternatives Considered**:
  - Official MCP SDK: Adds complexity, OpenAI function calling is sufficient
  - LangChain: Overkill for our use case, adds heavy dependency

**Tool List**:
1. `create_task(title, description?)` → POST /api/{user_id}/tasks
2. `list_tasks(completed?)` → GET /api/{user_id}/tasks
3. `get_task(task_id)` → GET /api/{user_id}/tasks/{id}
4. `update_task(task_id, title?, description?)` → PUT /api/{user_id}/tasks/{id}
5. `delete_task(task_id)` → DELETE /api/{user_id}/tasks/{id}
6. `mark_complete(task_id, completed)` → PATCH /api/{user_id}/tasks/{id}/complete

---

## 3. Conversation Context Management

### Research Question
How to manage conversation context (message history) efficiently?

### Findings

**Context Storage Options**:
1. **In-Memory (Python dict)**: Simple, fast, lost on restart
2. **Redis**: Persistent, scalable, requires infrastructure
3. **Database**: Persistent, queryable, slower
4. **Session cookies**: Limited size, client-side storage

**Context Pruning Strategies**:
- **Sliding Window**: Keep last N messages (e.g., 10-20)
- **Token-Based**: Keep messages until token limit reached
- **Summarization**: Summarize old messages, keep recent ones
- **Importance-Based**: Keep important messages, drop filler

**Best Practices**:
1. Limit context to last 10-20 messages (balance memory/relevance)
2. Include system message with instructions at start
3. Reset context after 30 minutes of inactivity
4. Provide "clear context" command for users
5. Don't persist sensitive information in context
6. Use session IDs to isolate user conversations

**Token Management**:
- GPT-4-turbo: 128K token context window
- Average message: 50-100 tokens
- 20 messages ≈ 1,000-2,000 tokens (safe limit)
- Reserve tokens for tool definitions and responses

### Decision

**Selected**: In-memory session-based context with sliding window
- **Rationale**: Simple, sufficient for Phase III, no infrastructure overhead
- **Implementation**: Python dict keyed by session_id, keep last 15 messages
- **Timeout**: Clear context after 30 minutes of inactivity
- **Alternatives Considered**:
  - Redis: Overkill for Phase III, adds deployment complexity
  - Database: Too slow for real-time chat, unnecessary persistence

**Context Structure**:
```python
{
    "session_id": "uuid",
    "user_id": "uuid",
    "messages": [
        {"role": "system", "content": "You are a task management assistant..."},
        {"role": "user", "content": "Add a task to buy groceries"},
        {"role": "assistant", "content": "I've created a task: buy groceries"}
    ],
    "last_activity": "2026-02-17T10:30:00Z"
}
```

---

## 4. Chat UI Integration

### Research Question
What React patterns work best for real-time chat interfaces?

### Findings

**Chat UI Patterns**:
1. **Message List**: Scrollable container with auto-scroll to bottom
2. **Input Area**: Text input with send button, Enter key support
3. **Typing Indicator**: Show when AI is generating response
4. **Message Bubbles**: Different styles for user vs assistant
5. **Timestamps**: Show message time, relative or absolute

**Streaming Response Rendering**:
- Use Server-Sent Events (SSE) or WebSockets for streaming
- Render partial responses as they arrive (word-by-word)
- Show typing indicator while waiting for first token
- Handle connection errors gracefully

**React Implementation**:
```typescript
const [messages, setMessages] = useState<Message[]>([]);
const [isTyping, setIsTyping] = useState(false);

const sendMessage = async (text: string) => {
    setMessages([...messages, { role: 'user', content: text }]);
    setIsTyping(true);

    const response = await api.chat.send(text);
    setMessages([...messages, { role: 'assistant', content: response }]);
    setIsTyping(false);
};
```

**Accessibility Best Practices**:
1. Use semantic HTML (`<main>`, `<article>`, `<form>`)
2. ARIA labels for screen readers
3. Keyboard navigation (Tab, Enter, Escape)
4. Focus management (auto-focus input after send)
5. Live regions for new messages (screen reader announcements)

### Decision

**Selected**: Custom React components with SSE streaming
- **Rationale**: Full control over UI/UX, no heavy dependencies
- **Components**: ChatInterface, ChatMessage, ChatInput, ChatWindow
- **Streaming**: Server-Sent Events (SSE) for real-time responses
- **Alternatives Considered**:
  - react-chat-widget: Limited customization, doesn't match our design
  - stream-chat-react: Overkill, designed for multi-user chat
  - WebSockets: More complex than SSE, not needed for one-way streaming

**Component Structure**:
- `ChatInterface`: Main container, manages state
- `ChatWindow`: Scrollable message list
- `ChatMessage`: Individual message bubble
- `ChatInput`: Text input with send button

---

## 5. Security Considerations

### Research Question
How to secure the chat interface and prevent common AI security issues?

### Findings

**Security Threats**:
1. **Prompt Injection**: User tricks AI into ignoring instructions
2. **Data Leakage**: AI reveals other users' data
3. **API Key Exposure**: OpenAI key leaked to frontend
4. **Rate Limit Abuse**: User spams API, incurs high costs
5. **XSS Attacks**: Malicious input rendered as HTML

**Mitigation Strategies**:

**1. API Key Security**:
- Store OpenAI key in backend environment variables
- Never send key to frontend
- Use backend proxy for all OpenAI API calls
- Rotate keys periodically

**2. User Isolation**:
- Always pass user_id from JWT token (not from request body)
- Validate user_id matches authenticated user
- Filter all tool calls by user_id
- Never trust client-provided user_id

**3. Input Validation**:
- Sanitize all user inputs before processing
- Limit message length (e.g., 1000 characters)
- Escape HTML in rendered messages
- Validate tool parameters before execution

**4. Rate Limiting**:
- Limit requests per user (e.g., 10 per minute)
- Implement exponential backoff for retries
- Set max tokens per request
- Monitor API usage and costs

**5. Prompt Injection Prevention**:
- Use system message to set clear boundaries
- Validate tool calls before execution
- Require confirmation for destructive actions
- Log suspicious patterns

**System Prompt Template**:
```
You are a task management assistant. You can only help users manage their own tasks.

Rules:
1. Only use the provided tools to interact with tasks
2. Never access or mention other users' data
3. Always confirm before deleting tasks
4. If asked to do something outside task management, politely decline

Available tools: create_task, list_tasks, update_task, delete_task, mark_complete
```

### Decision

**Selected**: Multi-layered security approach
- **API Key**: Backend-only, environment variable
- **Authentication**: JWT token required for all chat endpoints
- **User Isolation**: user_id from JWT, validated on every request
- **Rate Limiting**: 20 requests per minute per user
- **Input Validation**: Max 1000 chars, HTML escaped
- **Prompt Engineering**: Clear system message with boundaries

**Implementation Checklist**:
- [ ] Store OpenAI key in backend .env
- [ ] Add JWT authentication to chat endpoint
- [ ] Validate user_id from token (not request)
- [ ] Implement rate limiting middleware
- [ ] Sanitize and escape all user inputs
- [ ] Add system prompt with security rules
- [ ] Log all tool calls for audit
- [ ] Add confirmation for delete operations

---

## Technology Stack Summary

### Backend
- **AI SDK**: OpenAI Python SDK (v1.0+)
- **Model**: GPT-4-turbo (gpt-4-turbo-preview)
- **Tools**: Custom function calling (OpenAI format)
- **Context**: In-memory session storage (Python dict)
- **Authentication**: Existing JWT from Phase II
- **Rate Limiting**: FastAPI middleware (20 req/min)

### Frontend
- **Framework**: React 19+ with Next.js 16+ (existing)
- **Components**: Custom chat components
- **Streaming**: Server-Sent Events (SSE)
- **State**: React hooks (useState, useEffect)
- **Styling**: Tailwind CSS (existing)

### Integration
- **Task API**: Existing Phase II REST endpoints
- **Database**: Existing Neon PostgreSQL (no changes)
- **Authentication**: Existing JWT system (no changes)

---

## Cost Estimation

### OpenAI API Costs (GPT-4-turbo)
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens

**Typical Conversation**:
- User message: ~50 tokens
- System prompt + tools: ~500 tokens
- AI response: ~100 tokens
- Total per exchange: ~650 tokens
- Cost per exchange: ~$0.02

**Monthly Estimate** (100 users, 10 messages/day):
- 100 users × 10 messages × 30 days = 30,000 messages
- 30,000 × $0.02 = $600/month

**Optimization Strategies**:
- Use GPT-3.5-turbo for simple queries (5x cheaper)
- Cache common responses
- Implement smart context pruning
- Set max_tokens limits

---

## Performance Targets

### Response Time
- **Target**: 2-3 seconds for typical commands
- **Breakdown**:
  - OpenAI API call: 1-2 seconds
  - Tool execution: 0.5-1 second
  - Network overhead: 0.5 seconds

### Throughput
- **Target**: 100 concurrent chat sessions
- **Bottleneck**: OpenAI API rate limits (depends on tier)
- **Mitigation**: Request queuing, rate limiting

### Context Management
- **Memory per session**: ~10KB (15 messages)
- **100 sessions**: ~1MB total
- **Cleanup**: Remove inactive sessions after 30 minutes

---

## Risk Mitigation

### Technical Risks
1. **OpenAI API Downtime**: Implement fallback error messages
2. **Rate Limits**: Queue requests, show wait time to users
3. **High Costs**: Set budget alerts, implement usage caps
4. **Context Loss**: Warn users when context is cleared

### Security Risks
1. **Prompt Injection**: System prompt boundaries, input validation
2. **Data Leakage**: Strict user isolation, audit logs
3. **API Key Theft**: Backend-only storage, key rotation
4. **Abuse**: Rate limiting, usage monitoring

---

## Next Steps

1. ✅ Complete research documentation
2. ⏭️ Create data-model.md (Phase 1)
3. ⏭️ Create API contracts (Phase 1)
4. ⏭️ Create quickstart.md (Phase 1)
5. ⏭️ Generate tasks.md (Phase 2)
6. ⏭️ Begin implementation (Phase 3)

---

## References

- OpenAI API Documentation: https://platform.openai.com/docs
- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Chat UI Patterns: https://react.dev/learn
- Security Best Practices: OWASP Top 10
