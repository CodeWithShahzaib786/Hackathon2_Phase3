"""Task service for business logic."""

from uuid import UUID
from typing import Optional, List
from sqlmodel import Session, select
from datetime import datetime

from src.models.task import Task


class TaskService:
    """Service for managing tasks."""

    def __init__(self, session: Session):
        """Initialize TaskService with database session."""
        self.session = session

    async def create_task(
        self,
        user_id: UUID,
        title: str,
        description: Optional[str] = None,
    ) -> Task:
        """
        Create a new task for a user.

        Args:
            user_id: UUID of the user creating the task
            title: Task title
            description: Optional task description

        Returns:
            Created Task object

        Raises:
            ValueError: If title is empty or exceeds max length
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters")

        # Create task
        task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
            user_id=user_id,
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    async def get_all_tasks(
        self,
        user_id: UUID,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """
        Get all tasks for a user.

        Args:
            user_id: UUID of the user
            completed: Optional filter by completion status

        Returns:
            List of Task objects ordered by created_at descending
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Filter by completion status if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Order by created_at descending (most recent first)
        statement = statement.order_by(Task.created_at.desc())

        results = self.session.exec(statement)
        return list(results.all())

    async def get_task_by_id(
        self,
        task_id: UUID,
        user_id: UUID,
    ) -> Optional[Task]:
        """
        Get a specific task by ID for a user.

        Args:
            task_id: UUID of the task
            user_id: UUID of the user (for authorization)

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )

        result = self.session.exec(statement)
        return result.first()

    async def update_task(
        self,
        task_id: UUID,
        user_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Task]:
        """
        Update a task.

        Args:
            task_id: UUID of the task
            user_id: UUID of the user (for authorization)
            title: Optional new title
            description: Optional new description
            completed: Optional new completion status

        Returns:
            Updated Task object if found and belongs to user, None otherwise

        Raises:
            ValueError: If title is empty or exceeds max length
        """
        task = await self.get_task_by_id(task_id, user_id)

        if not task:
            return None

        # Update fields if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title) > 255:
                raise ValueError("Title cannot exceed 255 characters")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description else None

        if completed is not None:
            task.completed = completed

        # Update timestamp
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    async def delete_task(
        self,
        task_id: UUID,
        user_id: UUID,
    ) -> bool:
        """
        Delete a task.

        Args:
            task_id: UUID of the task
            user_id: UUID of the user (for authorization)

        Returns:
            True if task was deleted, False if not found or doesn't belong to user
        """
        task = await self.get_task_by_id(task_id, user_id)

        if not task:
            return False

        self.session.delete(task)
        self.session.commit()

        return True

    async def mark_task_complete(
        self,
        task_id: UUID,
        user_id: UUID,
        completed: bool = True,
    ) -> Optional[Task]:
        """
        Mark a task as complete or incomplete.

        Args:
            task_id: UUID of the task
            user_id: UUID of the user (for authorization)
            completed: Completion status (default: True)

        Returns:
            Updated Task object if found and belongs to user, None otherwise
        """
        return await self.update_task(task_id, user_id, completed=completed)
