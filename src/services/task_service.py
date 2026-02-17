"""Task service for business logic."""

from typing import Optional

from src.models.task import Task
from src.services.task_repository import TaskRepository


class TaskService:
    """Service layer for task operations.

    Provides business logic for managing tasks, delegating storage
    to the TaskRepository.

    Attributes:
        _repository: The task repository for data storage.
    """

    def __init__(self) -> None:
        """Initialize the task service with an empty repository."""
        self._repository = TaskRepository()

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task.

        Args:
            title: The task title (required, 1-200 characters).
            description: The task description (optional, max 1000 characters).

        Returns:
            The created task with assigned ID.

        Raises:
            ValidationError: If title or description is invalid.
        """
        task = Task(title=title, description=description)
        return self._repository.add(task)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            A list of all tasks, ordered by ID.
        """
        return self._repository.get_all()

    def toggle_completion(self, task_id: int) -> Task:
        """Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        task = self._repository.get(task_id)
        task.toggle_completion()
        return task

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: The new title (if provided).
            description: The new description (if provided).

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            ValidationError: If title or description is invalid.
        """
        return self._repository.update(task_id, title=title, description=description)

    def delete_task(self, task_id: int) -> Task:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted task (before removal).

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        task = self._repository.get(task_id)
        self._repository.delete(task_id)
        return task
