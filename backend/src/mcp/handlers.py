"""MCP tool handlers that execute task operations."""

from uuid import UUID
from typing import Optional, Dict, Any, List

from backend.src.services.task_service import TaskService
from backend.src.core.database import get_session


async def handle_create_task(
    user_id: UUID,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """Handler for create_task tool.

    Args:
        user_id: User creating the task
        title: Task title
        description: Optional task description

    Returns:
        Task data as dictionary

    Raises:
        Exception: If task creation fails
    """
    async with get_session() as session:
        task_service = TaskService(session)
        task = await task_service.create_task(
            user_id=user_id,
            title=title,
            description=description
        )
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def handle_list_tasks(
    user_id: UUID,
    completed: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Handler for list_tasks tool.

    Args:
        user_id: User whose tasks to list
        completed: Optional filter by completion status

    Returns:
        List of task data as dictionaries
    """
    async with get_session() as session:
        task_service = TaskService(session)
        tasks = await task_service.get_all_tasks(user_id=user_id, completed=completed)
        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]


async def handle_get_task(
    user_id: UUID,
    task_id: str
) -> Dict[str, Any]:
    """Handler for get_task tool.

    Args:
        user_id: User requesting the task
        task_id: Task ID to retrieve

    Returns:
        Task data as dictionary

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    async with get_session() as session:
        task_service = TaskService(session)
        task = await task_service.get_task_by_id(
            task_id=UUID(task_id),
            user_id=user_id
        )

        if not task:
            raise ValueError(f"Task {task_id} not found")

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def handle_update_task(
    user_id: UUID,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """Handler for update_task tool.

    Args:
        user_id: User updating the task
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated task data as dictionary

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    async with get_session() as session:
        task_service = TaskService(session)
        task = await task_service.update_task(
            task_id=UUID(task_id),
            user_id=user_id,
            title=title,
            description=description
        )

        if not task:
            raise ValueError(f"Task {task_id} not found")

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def handle_delete_task(
    user_id: UUID,
    task_id: str
) -> Dict[str, Any]:
    """Handler for delete_task tool.

    Args:
        user_id: User deleting the task
        task_id: Task ID to delete

    Returns:
        Success message

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    async with get_session() as session:
        task_service = TaskService(session)
        success = await task_service.delete_task(
            task_id=UUID(task_id),
            user_id=user_id
        )

        if not success:
            raise ValueError(f"Task {task_id} not found")

        return {
            "success": True,
            "message": "Task deleted successfully"
        }


async def handle_mark_complete(
    user_id: UUID,
    task_id: str,
    completed: bool
) -> Dict[str, Any]:
    """Handler for mark_complete tool.

    Args:
        user_id: User updating the task
        task_id: Task ID to update
        completed: True to mark complete, False to mark incomplete

    Returns:
        Updated task data as dictionary

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    async with get_session() as session:
        task_service = TaskService(session)
        task = await task_service.mark_task_complete(
            task_id=UUID(task_id),
            user_id=user_id,
            completed=completed
        )

        if not task:
            raise ValueError(f"Task {task_id} not found")

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
