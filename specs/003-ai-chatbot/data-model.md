# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-17
**Purpose**: Define data structures for chat functionality

## Overview

This document defines the data model for Phase III chat functionality. All entities are **transient** (session-based, not persisted to database) to keep implementation simple and avoid database schema changes.

---

## Entities

### 1. ChatMessage

Represents a single message in a conversation (user or assistant).

**Attributes**:
- `role`: string - Message sender ("user", "assistant", or "system")
- `content`: string - Message text content
- `timestamp`: datetime - When message was created
- `tool_calls`: list[ToolCall] | null - Tool calls made by assistant (if any)

**Validation Rules**:
- `role` must be one of: "user", "assistant", "system"
- `content` must not be empty
- `content` max length: 1000 characters (user messages)
- `timestamp` auto-generated on creation

**Example**:
```python
{
    "role": "user",
    "content": "Add a task to buy groceries",
    "timestamp": "2026-02-17T10:30:00Z",
    "tool_calls": null
}
```

---

### 2. Conversation

Represents a chat session with message history and context.

**Attributes**:
- `session_id`: UUID - Unique session identifier
- `user_id`: UUID - User who owns this conversation
- `messages`: list[ChatMessage] - Conversation history (max 15 messages)
- `created_at`: datetime - When conversation started
- `last_activity`: datetime - Last message timestamp
- `is_active`: boolean - Whether session is still active

**Validation Rules**:
- `session_id` must be unique UUID
- `user_id` must match authenticated user
- `messages` limited to last 15 messages (sliding window)
- Session expires after 30 minutes of inactivity
- `is_active` set to false when expired

**Relationships**:
- One Conversation belongs to one User (from Phase II)
- One Conversation has many ChatMessages

**Example**:
```python
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440001",
    "messages": [
        {"role": "system", "content": "You are a task management assistant..."},
        {"role": "user", "content": "Show me my tasks"},
        {"role": "assistant", "content": "You have 3 tasks: ..."}
    ],
    "created_at": "2026-02-17T10:00:00Z",
    "last_activity": "2026-02-17T10:30:00Z",
    "is_active": true
}
```

---

### 3. ToolCall

Represents a function call made by the AI assistant.

**Attributes**:
- `tool_name`: string - Name of the tool being called
- `arguments`: dict - Tool parameters
- `result`: dict | null - Tool execution result
- `error`: string | null - Error message if tool failed

**Validation Rules**:
- `tool_name` must be one of the defined MCP tools
- `arguments` must match tool's parameter schema
- Either `result` or `error` is set, not both

**Example**:
```python
{
    "tool_name": "create_task",
    "arguments": {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread"
    },
    "result": {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "title": "Buy groceries",
        "completed": false
    },
    "error": null
}
```

---

### 4. MCPTool

Represents a tool definition that the AI can use.

**Attributes**:
- `name`: string - Tool identifier (e.g., "create_task")
- `description`: string - What the tool does (AI reads this)
- `parameters`: dict - JSON Schema for parameters
- `handler`: callable - Python function that executes the tool

**Validation Rules**:
- `name` must be unique across all tools
- `description` should be clear and concise (AI uses this to decide when to call)
- `parameters` must be valid JSON Schema
- `handler` must be async function

**Example**:
```python
{
    "name": "create_task",
    "description": "Create a new task for the user with a title and optional description",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The task title"
            },
            "description": {
                "type": "string",
                "description": "Optional task description"
            }
        },
        "required": ["title"]
    },
    "handler": handle_create_task
}
```

---

### 5. ChatRequest

Represents an incoming chat message from the user.

**Attributes**:
- `message`: string - User's message text
- `session_id`: UUID | null - Existing session ID (null for new session)

**Validation Rules**:
- `message` must not be empty
- `message` max length: 1000 characters
- `session_id` must exist if provided

**Example**:
```python
{
    "message": "Add a task to buy groceries",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 6. ChatResponse

Represents the assistant's response to the user.

**Attributes**:
- `message`: string - Assistant's response text
- `session_id`: UUID - Session identifier
- `tool_calls`: list[ToolCall] - Tools that were called (if any)
- `timestamp`: datetime - Response timestamp

**Example**:
```python
{
    "message": "I've created a task: Buy groceries",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "tool_calls": [
        {
            "tool_name": "create_task",
            "arguments": {"title": "Buy groceries"},
            "result": {"id": "...", "title": "Buy groceries"}
        }
    ],
    "timestamp": "2026-02-17T10:30:15Z"
}
```

---

## Storage Strategy

### In-Memory Session Store

**Implementation**: Python dictionary keyed by session_id

```python
# Global session store (in-memory)
sessions: dict[UUID, Conversation] = {}

# Cleanup inactive sessions periodically
def cleanup_inactive_sessions():
    now = datetime.utcnow()
    for session_id, conversation in list(sessions.items()):
        if (now - conversation.last_activity).seconds > 1800:  # 30 minutes
            conversation.is_active = False
            del sessions[session_id]
```

**Advantages**:
- Fast access (O(1) lookup)
- No database overhead
- Simple implementation
- Automatic cleanup on server restart

**Limitations**:
- Lost on server restart
- Not shared across multiple server instances
- Limited by server memory

**Scaling Strategy** (future):
- For production: Use Redis for session storage
- For multi-instance: Use distributed cache
- For persistence: Store in database (optional)

---

## Data Flow

### 1. User Sends Message

```
User → Frontend → POST /api/chat
                  ↓
              ChatRequest {message, session_id?}
                  ↓
              Backend validates JWT
                  ↓
              Get or create Conversation
                  ↓
              Add user message to conversation
```

### 2. AI Processes Message

```
Conversation → OpenAI API
               ↓
           AI analyzes message
               ↓
           AI decides to call tool(s)
               ↓
           Execute tool handlers
               ↓
           Get tool results
               ↓
           AI generates response
```

### 3. Response Sent to User

```
AI Response → Add to conversation
              ↓
          Update last_activity
              ↓
          Return ChatResponse
              ↓
          Frontend displays message
```

---

## Context Management

### Sliding Window Strategy

Keep only the last 15 messages in conversation history:

```python
def add_message(conversation: Conversation, message: ChatMessage):
    conversation.messages.append(message)

    # Keep only last 15 messages (plus system message)
    if len(conversation.messages) > 16:  # 1 system + 15 messages
        # Keep system message (index 0) and last 15 messages
        conversation.messages = [conversation.messages[0]] + conversation.messages[-15:]

    conversation.last_activity = datetime.utcnow()
```

### Token Estimation

Approximate token counts for context management:

- System message: ~200 tokens
- User message: ~50 tokens
- Assistant message: ~100 tokens
- Tool definitions: ~300 tokens
- 15 messages: ~2,250 tokens
- **Total context**: ~2,750 tokens (well within 128K limit)

---

## Integration with Phase II

### No Database Changes

Phase III does **not** modify the Phase II database schema:

- **Users table**: Unchanged (existing from Phase II)
- **Tasks table**: Unchanged (existing from Phase II)
- **No new tables**: Chat data is transient (in-memory only)

### Reusing Existing Models

Chat functionality reuses Phase II models:

- **User**: For authentication (JWT token → user_id)
- **Task**: For task operations (via MCP tools)
- **TaskService**: For business logic (wrapped by tool handlers)

### API Integration

MCP tool handlers call existing Phase II API endpoints:

```python
async def handle_create_task(user_id: UUID, title: str, description: str = None):
    # Reuse existing Phase II TaskService
    task_service = TaskService(session)
    task = await task_service.create_task(user_id, title, description)
    return task.dict()
```

---

## Security Considerations

### User Isolation

Every conversation is tied to a user_id from JWT token:

```python
# Extract user_id from JWT token (not from request body)
current_user = get_current_user(token)

# Create or get conversation for this user
conversation = get_or_create_conversation(session_id, current_user.id)

# Validate user owns this conversation
if conversation.user_id != current_user.id:
    raise HTTPException(403, "Forbidden")
```

### Input Validation

All user inputs are validated before processing:

```python
def validate_chat_request(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise ValueError("Message cannot be empty")

    if len(request.message) > 1000:
        raise ValueError("Message too long (max 1000 characters)")

    # Sanitize HTML to prevent XSS
    request.message = escape_html(request.message)
```

---

## Performance Considerations

### Memory Usage

Estimated memory per conversation:

- 15 messages × 150 bytes/message = 2.25 KB
- Metadata (session_id, timestamps, etc.) = 0.5 KB
- **Total per conversation**: ~3 KB

For 100 concurrent users:
- 100 conversations × 3 KB = 300 KB
- Negligible memory footprint

### Cleanup Strategy

Remove inactive sessions to prevent memory leaks:

```python
# Run cleanup every 5 minutes
@scheduler.scheduled_job('interval', minutes=5)
def cleanup_sessions():
    now = datetime.utcnow()
    inactive_threshold = timedelta(minutes=30)

    for session_id in list(sessions.keys()):
        conversation = sessions[session_id]
        if now - conversation.last_activity > inactive_threshold:
            del sessions[session_id]
```

---

## Testing Strategy

### Unit Tests

Test individual components:

- ChatMessage validation
- Conversation context management
- Tool call execution
- Session cleanup logic

### Integration Tests

Test end-to-end flows:

- User sends message → AI responds
- Tool calls execute correctly
- Context is maintained across messages
- Sessions expire after timeout

### Test Data

Sample conversations for testing:

```python
test_conversation = {
    "session_id": "test-session-1",
    "user_id": "test-user-1",
    "messages": [
        {"role": "system", "content": "You are a task assistant..."},
        {"role": "user", "content": "Add a task to buy milk"},
        {"role": "assistant", "content": "I've created a task: Buy milk"}
    ]
}
```

---

## Summary

**New Entities**: 6 (ChatMessage, Conversation, ToolCall, MCPTool, ChatRequest, ChatResponse)

**Storage**: In-memory (no database changes)

**Integration**: Reuses Phase II User and Task models

**Security**: User isolation via JWT, input validation

**Performance**: ~3 KB per conversation, automatic cleanup

**Next Steps**: Create API contracts and quickstart guide
