"""MCP tool definitions for AI agent to interact with task management system."""

from typing import List, Dict, Any


# System prompt is defined in chat_service.py
# This file will contain MCP tool definitions


def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get MCP tool definitions in OpenAI function calling format.

    Returns:
        List of tool definitions for OpenAI API
    """
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
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Get all tasks for the user, optionally filtered by completion status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status (optional). If true, show only completed tasks. If false, show only incomplete tasks. If omitted, show all tasks."
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_task",
                "description": "Get details of a specific task by ID",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's title and/or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "format": "uuid",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title (optional, 1-200 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description (optional, max 1000 characters)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task permanently. This action cannot be undone.",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "mark_complete",
                "description": "Mark a task as complete or incomplete",
                "parameters": {
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
            }
        }
    ]

    return tools
