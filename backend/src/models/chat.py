"""Chat models and schemas for Phase III AI-powered chatbot."""

from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Represents a function call made by the AI assistant.

    Attributes:
        tool_name: Name of the tool being called
        arguments: Tool parameters as a dictionary
        result: Tool execution result (if successful)
        error: Error message if tool failed
    """
    tool_name: str
    arguments: dict[str, Any]
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class ChatMessage(BaseModel):
    """Represents a single message in a conversation.

    Attributes:
        role: Message sender ("user", "assistant", or "system")
        content: Message text content
        timestamp: When message was created
        tool_calls: Tool calls made by assistant (if any)
    """
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[List[ToolCall]] = None


class Conversation(BaseModel):
    """Represents a chat session with message history and context.

    Attributes:
        session_id: Unique session identifier
        user_id: User who owns this conversation
        messages: Conversation history (max 15 messages)
        created_at: When conversation started
        last_activity: Last message timestamp
        is_active: Whether session is still active
        pending_action: Action awaiting user confirmation (for delete operations)
    """
    session_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    pending_action: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Represents an incoming chat message from the user.

    Attributes:
        message: User's message text
        session_id: Existing session ID (null for new session)
    """
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    """Represents the assistant's response to the user.

    Attributes:
        message: Assistant's response text
        session_id: Session identifier
        tool_calls: Tools that were called (if any)
        timestamp: Response timestamp
    """
    message: str
    session_id: UUID
    tool_calls: Optional[List[ToolCall]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
