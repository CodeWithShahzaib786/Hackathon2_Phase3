# MCP Tools Specification

**Feature**: 003-ai-chatbot
**Date**: 2026-02-17
**Purpose**: Define MCP tools for AI agent to interact with task management system

## Overview

This document defines the MCP (Model Context Protocol) tools that the AI agent can use to manage tasks. Each tool wraps an existing Phase II API endpoint and provides a structured interface for the AI to interact with the task management system.

---

## Tool Definitions

### 1. create_task

**Description**: Create a new task for the user with a title and optional description.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "The task title (required, 1-200 characters)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional task description (max 1000 characters)",
      "maxLength": 1000
    }
  },
  "required": ["title"]
}
```

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": false,
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Example Usage**:
- User: "Add a task to buy groceries"
- AI calls: `create_task(title="Buy groceries")`
- AI responds: "I've created a task: Buy groceries"

**Wraps**: `POST /api/{user_id}/tasks`

---

### 2. list_tasks

**Description**: Get all tasks for the user, optionally filtered by completion status.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "completed": {
      "type": "boolean",
      "description": "Filter by completion status (optional). If true, show only completed tasks. If false, show only incomplete tasks. If omitted, show all tasks."
    }
  },
  "required": []
}
```

**Returns**:
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string | null",
    "completed": "boolean",
    "user_id": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

**Example Usage**:
- User: "Show me all my tasks"
- AI calls: `list_tasks()`
- AI responds: "You have 3 tasks: 1. Buy groceries (incomplete), 2. Call mom (complete), 3. Finish report (incomplete)"

- User: "What are my incomplete tasks?"
- AI calls: `list_tasks(completed=false)`
- AI responds: "You have 2 incomplete tasks: 1. Buy groceries, 2. Finish report"

**Wraps**: `GET /api/{user_id}/tasks?completed={true|false}`

---

### 3. get_task

**Description**: Get details of a specific task by ID.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to retrieve"
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Example Usage**:
- User: "Tell me about task 123"
- AI calls: `get_task(task_id="123")`
- AI responds: "Task 123 is 'Buy groceries' - it's currently incomplete and was created on Feb 17."

**Wraps**: `GET /api/{user_id}/tasks/{task_id}`

---

### 4. update_task

**Description**: Update a task's title and/or description.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (optional, 1-200 characters)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "New task description (optional, max 1000 characters)",
      "maxLength": 1000
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Example Usage**:
- User: "Change my first task to say meeting at 3pm"
- AI calls: `list_tasks()` to get first task ID
- AI calls: `update_task(task_id="123", title="Meeting at 3pm")`
- AI responds: "I've updated your task to 'Meeting at 3pm'"

**Wraps**: `PUT /api/{user_id}/tasks/{task_id}`

---

### 5. delete_task

**Description**: Delete a task permanently. This action cannot be undone.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Example Usage**:
- User: "Delete my first task"
- AI calls: `list_tasks()` to get first task ID
- AI asks: "Are you sure you want to delete 'Buy groceries'?"
- User: "Yes"
- AI calls: `delete_task(task_id="123")`
- AI responds: "I've deleted the task 'Buy groceries'"

**Wraps**: `DELETE /api/{user_id}/tasks/{task_id}`

**Note**: AI should always confirm before deleting tasks to prevent accidental data loss.

---

### 6. mark_complete

**Description**: Mark a task as complete or incomplete.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to update"
    },
    "completed": {
      "type": "boolean",
      "description": "True to mark as complete, false to mark as incomplete"
    }
  },
  "required": ["task_id", "completed"]
}
```

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Example Usage**:
- User: "Mark my first task as done"
- AI calls: `list_tasks()` to get first task ID
- AI calls: `mark_complete(task_id="123", completed=true)`
- AI responds: "I've marked 'Buy groceries' as complete"

- User: "Actually, mark it as incomplete"
- AI calls: `mark_complete(task_id="123", completed=false)`
- AI responds: "I've marked 'Buy groceries' as incomplete"

**Wraps**: `PATCH /api/{user_id}/tasks/{task_id}/complete?completed={true|false}`

---

## Tool Handler Implementation

Each tool has a corresponding handler function that executes the actual API call:

```python
async def handle_create_task(
    user_id: UUID,
    title: str,
    description: str = None
) -> dict:
    """Handler for create_task tool."""
    task_service = TaskService(session)
    task = await task_service.create_task(user_id, title, description)
    return task.dict()

async def handle_list_tasks(
    user_id: UUID,
    completed: bool = None
) -> list[dict]:
    """Handler for list_tasks tool."""
    task_service = TaskService(session)
    tasks = await task_service.get_all_tasks(user_id, completed)
    return [task.dict() for task in tasks]

async def handle_get_task(
    user_id: UUID,
    task_id: UUID
) -> dict:
    """Handler for get_task tool."""
    task_service = TaskService(session)
    task = await task_service.get_task_by_id(task_id, user_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    return task.dict()

async def handle_update_task(
    user_id: UUID,
    task_id: UUID,
    title: str = None,
    description: str = None
) -> dict:
    """Handler for update_task tool."""
    task_service = TaskService(session)
    task = await task_service.update_task(task_id, user_id, title, description)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    return task.dict()

async def handle_delete_task(
    user_id: UUID,
    task_id: UUID
) -> dict:
    """Handler for delete_task tool."""
    task_service = TaskService(session)
    success = await task_service.delete_task(task_id, user_id)
    if not success:
        raise ValueError(f"Task {task_id} not found")
    return {"success": True, "message": "Task deleted successfully"}

async def handle_mark_complete(
    user_id: UUID,
    task_id: UUID,
    completed: bool
) -> dict:
    """Handler for mark_complete tool."""
    task_service = TaskService(session)
    task = await task_service.mark_task_complete(task_id, user_id, completed)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    return task.dict()
```

---

## OpenAI Function Calling Format

Tools are registered with OpenAI in this format:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task for the user with a title and optional description",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title (required, 1-200 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 characters)"
                    }
                },
                "required": ["title"]
            }
        }
    },
    # ... other tools
]
```

---

## System Prompt

The AI agent is initialized with this system prompt:

```
You are a helpful task management assistant. You help users manage their todo list through natural conversation.

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
```

---

## Error Handling

Tool handlers should raise appropriate errors:

```python
class ToolError(Exception):
    """Base exception for tool errors."""
    pass

class TaskNotFoundError(ToolError):
    """Raised when task ID doesn't exist or doesn't belong to user."""
    pass

class ValidationError(ToolError):
    """Raised when tool parameters are invalid."""
    pass
```

AI should handle errors gracefully:

```python
try:
    result = await handle_delete_task(user_id, task_id)
except TaskNotFoundError:
    return "I couldn't find that task. It may have already been deleted."
except ValidationError as e:
    return f"I couldn't complete that action: {str(e)}"
except Exception as e:
    return "I encountered an error. Please try again."
```

---

## Security

### User Isolation

All tool handlers receive `user_id` from JWT token (not from AI or user input):

```python
# In chat endpoint
current_user = get_current_user(token)  # Extract from JWT

# Pass to tool handler
result = await handle_create_task(
    user_id=current_user.id,  # From JWT, not from request
    title=tool_args["title"],
    description=tool_args.get("description")
)
```

### Input Validation

Tool parameters are validated before execution:

```python
def validate_tool_args(tool_name: str, args: dict):
    """Validate tool arguments against schema."""
    schema = get_tool_schema(tool_name)
    jsonschema.validate(args, schema)
```

### Rate Limiting

Tool calls are subject to rate limiting:

```python
@rate_limit(max_calls=20, window=60)  # 20 calls per minute
async def execute_tool(tool_name: str, args: dict, user_id: UUID):
    handler = get_tool_handler(tool_name)
    return await handler(user_id=user_id, **args)
```

---

## Testing

### Unit Tests

Test each tool handler independently:

```python
async def test_create_task_handler():
    user_id = UUID("...")
    result = await handle_create_task(user_id, "Test task")
    assert result["title"] == "Test task"
    assert result["completed"] is False

async def test_list_tasks_handler():
    user_id = UUID("...")
    tasks = await handle_list_tasks(user_id, completed=False)
    assert all(not task["completed"] for task in tasks)
```

### Integration Tests

Test tool execution through AI agent:

```python
async def test_ai_creates_task():
    response = await chat_endpoint(
        message="Add a task to buy milk",
        user_id=test_user_id
    )
    assert "buy milk" in response.message.lower()
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].tool_name == "create_task"
```

---

## Summary

**Total Tools**: 6 (create, list, get, update, delete, mark_complete)

**Wraps**: Existing Phase II task API endpoints

**Security**: User isolation via JWT, input validation, rate limiting

**Error Handling**: Graceful errors with user-friendly messages

**Testing**: Unit tests for handlers, integration tests for AI flows

**Next Steps**: Implement tool handlers and integrate with OpenAI SDK
