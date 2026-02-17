"""Chat service for managing conversations and OpenAI integration."""

from datetime import datetime, timedelta
from typing import Optional, Dict
from uuid import UUID
import json
import logging
import asyncio
import openai
from openai import OpenAI

from backend.src.core.config import get_settings
from backend.src.models.chat import Conversation, ChatMessage, ChatRequest, ChatResponse, ToolCall


# Configure logging
logger = logging.getLogger(__name__)

# Global in-memory session store
sessions: Dict[UUID, Conversation] = {}


class ChatService:
    """Service for managing chat conversations and AI interactions."""

    def __init__(self):
        """Initialize ChatService with OpenAI client."""
        settings = get_settings()

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for chat functionality")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

        logger.info(f"ChatService initialized with model: {self.model}")

    def get_or_create_conversation(
        self,
        user_id: UUID,
        session_id: Optional[UUID] = None
    ) -> Conversation:
        """Get existing conversation or create a new one.

        Args:
            user_id: User who owns the conversation
            session_id: Existing session ID (None for new session)

        Returns:
            Conversation object

        Raises:
            ValueError: If session_id provided but not found or belongs to different user
        """
        if session_id:
            # Try to get existing conversation
            conversation = sessions.get(session_id)

            if not conversation:
                raise ValueError(f"Session {session_id} not found")

            if conversation.user_id != user_id:
                raise ValueError("Session belongs to different user")

            if not conversation.is_active:
                raise ValueError("Session has expired")

            # Update last activity
            conversation.last_activity = datetime.utcnow()
            return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)

        # Add system message
        system_message = ChatMessage(
            role="system",
            content=self._get_system_prompt()
        )
        conversation.messages.append(system_message)

        # Store in session store
        sessions[conversation.session_id] = conversation

        return conversation

    def add_message(self, conversation: Conversation, message: ChatMessage) -> None:
        """Add a message to the conversation with sliding window management.

        Args:
            conversation: Conversation to add message to
            message: Message to add
        """
        conversation.messages.append(message)

        # Keep only last 15 messages (plus system message)
        if len(conversation.messages) > 16:  # 1 system + 15 messages
            # Keep system message (index 0) and last 15 messages
            conversation.messages = [conversation.messages[0]] + conversation.messages[-15:]

        conversation.last_activity = datetime.utcnow()

    def clear_session(self, session_id: UUID, user_id: UUID) -> bool:
        """Clear a conversation session.

        Args:
            session_id: Session to clear
            user_id: User requesting the clear (for authorization)

        Returns:
            True if session was cleared, False if not found

        Raises:
            ValueError: If session belongs to different user
        """
        conversation = sessions.get(session_id)

        if not conversation:
            return False

        if conversation.user_id != user_id:
            raise ValueError("Session belongs to different user")

        conversation.is_active = False
        del sessions[session_id]

        return True

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI assistant.

        Returns:
            System prompt text
        """
        return """You are a helpful task management assistant. You help users manage their todo list through natural conversation.

Available Tools:
- create_task: Create a new task
- list_tasks: View all tasks or filter by completion status
- get_task: Get details of a specific task
- update_task: Modify a task's title or description
- delete_task: Remove a task (always confirm first)
- mark_complete: Mark a task as complete or incomplete

Guidelines:
1. Be conversational and friendly
2. Always confirm before deleting tasks
3. When users say "first task" or "second task", call list_tasks first to get the correct task ID
4. If a command is ambiguous, ask clarifying questions
5. Provide clear confirmation after each action
6. If an error occurs, explain it in simple terms

Examples:
- User: "Add a task to buy groceries"
  → Call create_task(title="Buy groceries")
  → Respond: "I've created a task: Buy groceries"

- User: "Show my incomplete tasks"
  → Call list_tasks(completed=false)
  → Respond: "You have 2 incomplete tasks: [list them]"

- User: "Mark the first one as done"
  → Call list_tasks() to get first task
  → Call mark_complete(task_id=..., completed=true)
  → Respond: "I've marked '[task title]' as complete"
"""

    async def process_message(
        self,
        user_id: UUID,
        request: ChatRequest
    ) -> ChatResponse:
        """Process a user message and generate AI response with tool calling.

        Args:
            user_id: User sending the message
            request: Chat request with message and optional session_id

        Returns:
            ChatResponse with AI's reply and any tool calls made
        """
        from backend.src.mcp.tools import get_mcp_tools
        from backend.src.mcp import handlers

        # Get or create conversation
        conversation = self.get_or_create_conversation(user_id, request.session_id)

        # Check if there's a pending confirmation
        if conversation.pending_action:
            # Check if user is confirming or canceling
            user_response = request.message.lower().strip()
            if user_response in ["yes", "y", "confirm", "ok", "sure"]:
                # Execute the pending action
                try:
                    result = await self._execute_tool(
                        tool_name=conversation.pending_action["tool_name"],
                        user_id=user_id,
                        arguments=conversation.pending_action["arguments"]
                    )

                    # Clear pending action
                    conversation.pending_action = None

                    # Add user confirmation message
                    user_message = ChatMessage(role="user", content=request.message)
                    self.add_message(conversation, user_message)

                    # Add success response
                    assistant_message = ChatMessage(
                        role="assistant",
                        content=f"Done! I've deleted the task."
                    )
                    self.add_message(conversation, assistant_message)

                    return ChatResponse(
                        message=assistant_message.content,
                        session_id=conversation.session_id,
                        tool_calls=None
                    )
                except Exception as e:
                    conversation.pending_action = None
                    error_message = f"Failed to delete task: {str(e)}"

                    user_message = ChatMessage(role="user", content=request.message)
                    self.add_message(conversation, user_message)

                    assistant_message = ChatMessage(role="assistant", content=error_message)
                    self.add_message(conversation, assistant_message)

                    return ChatResponse(
                        message=error_message,
                        session_id=conversation.session_id,
                        tool_calls=None
                    )
            elif user_response in ["no", "n", "cancel", "nevermind", "never mind"]:
                # Cancel the pending action
                conversation.pending_action = None

                user_message = ChatMessage(role="user", content=request.message)
                self.add_message(conversation, user_message)

                assistant_message = ChatMessage(
                    role="assistant",
                    content="Okay, I've canceled that action. The task was not deleted."
                )
                self.add_message(conversation, assistant_message)

                return ChatResponse(
                    message=assistant_message.content,
                    session_id=conversation.session_id,
                    tool_calls=None
                )

        # Add user message
        user_message = ChatMessage(role="user", content=request.message)
        self.add_message(conversation, user_message)

        # Prepare messages for OpenAI API
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]

        # Get MCP tool definitions
        tools = get_mcp_tools()

        try:
            # Call OpenAI API with tool calling support (with retry logic)
            max_retries = 3
            retry_delay = 1  # seconds

            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=tools,
                        tool_choice="auto"
                    )
                    break  # Success, exit retry loop

                except openai.RateLimitError as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit error, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        logger.error(f"Rate limit error after {max_retries} attempts")
                        raise

                except openai.APIConnectionError as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Connection error, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.error(f"Connection error after {max_retries} attempts")
                        raise

                except openai.APITimeoutError as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Timeout error, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.error(f"Timeout error after {max_retries} attempts")
                        raise

            assistant_message_content = response.choices[0].message.content or ""
            tool_calls_made = []

            # Check if AI wants to call tools
            if response.choices[0].message.tool_calls:
                # Execute tool calls
                for tool_call in response.choices[0].message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)  # Parse JSON arguments safely

                    # Check if this is a delete operation - require confirmation
                    if tool_name == "delete_task":
                        # Store pending action and ask for confirmation
                        conversation.pending_action = {
                            "tool_name": tool_name,
                            "arguments": tool_args
                        }

                        # Get task details for confirmation message
                        try:
                            task_info = await handlers.handle_get_task(
                                user_id=user_id,
                                task_id=tool_args.get("task_id")
                            )
                            confirmation_message = f"Are you sure you want to delete the task '{task_info['title']}'? This cannot be undone. (yes/no)"
                        except:
                            confirmation_message = "Are you sure you want to delete this task? This cannot be undone. (yes/no)"

                        assistant_message = ChatMessage(
                            role="assistant",
                            content=confirmation_message
                        )
                        self.add_message(conversation, assistant_message)

                        return ChatResponse(
                            message=confirmation_message,
                            session_id=conversation.session_id,
                            tool_calls=None
                        )

                    try:
                        # Execute non-delete tools immediately
                        result = await self._execute_tool(
                            tool_name=tool_name,
                            user_id=user_id,
                            arguments=tool_args
                        )

                        # Log successful tool call
                        logger.info(f"Tool call successful: {tool_name} for user {user_id}")

                        tool_calls_made.append(ToolCall(
                            tool_name=tool_name,
                            arguments=tool_args,
                            result=result,
                            error=None
                        ))

                    except Exception as e:
                        # Log failed tool call
                        logger.error(f"Tool call failed: {tool_name} for user {user_id} - {str(e)}")

                        tool_calls_made.append(ToolCall(
                            tool_name=tool_name,
                            arguments=tool_args,
                            result=None,
                            error=str(e)
                        ))

                # If tools were called, send results back to OpenAI for final response
                if tool_calls_made:
                    # Add assistant message with tool calls
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message_content,
                        "tool_calls": [
                            {
                                "id": f"call_{i}",
                                "type": "function",
                                "function": {
                                    "name": tc.tool_name,
                                    "arguments": str(tc.arguments)
                                }
                            }
                            for i, tc in enumerate(tool_calls_made)
                        ]
                    })

                    # Add tool results
                    for i, tc in enumerate(tool_calls_made):
                        messages.append({
                            "role": "tool",
                            "tool_call_id": f"call_{i}",
                            "content": str(tc.result if tc.result else tc.error)
                        })

                    # Get final response from OpenAI
                    final_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages
                    )

                    assistant_message_content = final_response.choices[0].message.content or ""

            # Add assistant message to conversation
            assistant_message = ChatMessage(
                role="assistant",
                content=assistant_message_content,
                tool_calls=tool_calls_made if tool_calls_made else None
            )
            self.add_message(conversation, assistant_message)

            return ChatResponse(
                message=assistant_message_content,
                session_id=conversation.session_id,
                tool_calls=tool_calls_made if tool_calls_made else None
            )

        except Exception as e:
            # Handle OpenAI API errors gracefully
            error_message = f"I encountered an error processing your request: {str(e)}"
            assistant_message = ChatMessage(
                role="assistant",
                content=error_message
            )
            self.add_message(conversation, assistant_message)

            return ChatResponse(
                message=error_message,
                session_id=conversation.session_id,
                tool_calls=None
            )

    async def _execute_tool(
        self,
        tool_name: str,
        user_id: UUID,
        arguments: dict
    ) -> dict:
        """Execute a tool handler with the given arguments.

        Args:
            tool_name: Name of the tool to execute
            user_id: User executing the tool
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool name is unknown
        """
        from backend.src.mcp import handlers

        # Route to appropriate handler
        if tool_name == "create_task":
            return await handlers.handle_create_task(
                user_id=user_id,
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        elif tool_name == "list_tasks":
            return await handlers.handle_list_tasks(
                user_id=user_id,
                completed=arguments.get("completed")
            )
        elif tool_name == "get_task":
            return await handlers.handle_get_task(
                user_id=user_id,
                task_id=arguments.get("task_id")
            )
        elif tool_name == "update_task":
            return await handlers.handle_update_task(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        elif tool_name == "delete_task":
            return await handlers.handle_delete_task(
                user_id=user_id,
                task_id=arguments.get("task_id")
            )
        elif tool_name == "mark_complete":
            return await handlers.handle_mark_complete(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                completed=arguments.get("completed")
            )
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


def cleanup_inactive_sessions() -> int:
    """Remove inactive sessions (30+ minutes of inactivity).

    Returns:
        Number of sessions cleaned up
    """
    now = datetime.utcnow()
    inactive_threshold = timedelta(minutes=30)

    sessions_to_remove = []

    for session_id, conversation in sessions.items():
        if now - conversation.last_activity > inactive_threshold:
            conversation.is_active = False
            sessions_to_remove.append(session_id)

    for session_id in sessions_to_remove:
        del sessions[session_id]

    return len(sessions_to_remove)
