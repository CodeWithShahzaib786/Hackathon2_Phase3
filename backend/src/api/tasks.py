"""Tasks API endpoints."""

from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.api.deps import get_current_user
from src.models.user import User
from src.models.task import Task
from src.models import TaskCreate, TaskResponse, TaskUpdate
from src.services.task_service import TaskService


router = APIRouter()


def verify_user_access(user_id: UUID, current_user: User) -> None:
    """
    Verify that the current user has access to the specified user_id.

    Args:
        user_id: The user_id from the URL path
        current_user: The authenticated user from JWT token

    Raises:
        HTTPException: 403 if user_id doesn't match current user
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from URL path
        task_data: Task creation data (title, description)
        session: Database session
        current_user: Authenticated user from JWT token

    Returns:
        Created task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 400 if validation fails
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Create task service
    task_service = TaskService(session)

    try:
        task = await task_service.create_task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
        )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
)
async def get_all_tasks(
    user_id: UUID,
    completed: Optional[bool] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> List[Task]:
    """
    Get all tasks for the authenticated user.

    Args:
        user_id: User ID from URL path
        completed: Optional filter by completion status
        session: Database session
        current_user: Authenticated user from JWT token

    Returns:
        List of tasks ordered by created_at descending

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Get tasks
    task_service = TaskService(session)
    tasks = await task_service.get_all_tasks(
        user_id=user_id,
        completed=completed,
    )

    return tasks


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Get a specific task by ID.

    Args:
        user_id: User ID from URL path
        task_id: Task ID from URL path
        session: Database session
        current_user: Authenticated user from JWT token

    Returns:
        Task object

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Get task
    task_service = TaskService(session)
    task = await task_service.get_task_by_id(task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Update a task.

    Args:
        user_id: User ID from URL path
        task_id: Task ID from URL path
        task_data: Task update data
        session: Database session
        current_user: Authenticated user from JWT token

    Returns:
        Updated task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 400 if validation fails
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Update task
    task_service = TaskService(session)

    try:
        task = await task_service.update_task(
            task_id=task_id,
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a task.

    Args:
        user_id: User ID from URL path
        task_id: Task ID from URL path
        session: Database session
        current_user: Authenticated user from JWT token

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Delete task
    task_service = TaskService(session)
    deleted = await task_service.delete_task(task_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
async def mark_task_complete(
    user_id: UUID,
    task_id: UUID,
    completed: bool = True,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Mark a task as complete or incomplete.

    Args:
        user_id: User ID from URL path
        task_id: Task ID from URL path
        completed: Completion status (default: True)
        session: Database session
        current_user: Authenticated user from JWT token

    Returns:
        Updated task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Mark task complete
    task_service = TaskService(session)
    task = await task_service.mark_task_complete(task_id, user_id, completed)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task
