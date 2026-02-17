"""Task repository for in-memory storage."""

from typing import Optional

from src.models.task import Task
from src.models.exceptions import TaskNotFoundError


class TaskRepository:
    """Manages the collection of tasks in memory using a dictionary.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects.
        _next_id: Counter for generating unique task IDs.
    """

    def __init__(self) -> None:
        """Initialize an empty task repository."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """Add a new task to the repository and assign it a unique ID.

        Args:
            task: The task to add.

        Returns:
            The task with its assigned ID.
        """
        task.id = self._next_id
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task with the given ID.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def get_all(self) -> list[Task]:
        """Retrieve all tasks from the repository.

        Returns:
            A list of all tasks, ordered by ID.
        """
        return list(self._tasks.values())

    def update(
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
        """
        task = self.get(task_id)

        if title is not None:
            task.update_title(title)
        if description is not None:
            task.update_description(description)

        return task

    def delete(self, task_id: int) -> None:
        """Remove a task from the repository.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    def exists(self, task_id: int) -> bool:
        """Check if a task with the given ID exists.

        Args:
            task_id: The ID to check.

        Returns:
            True if the task exists, False otherwise.
        """
        return task_id in self._tasks
