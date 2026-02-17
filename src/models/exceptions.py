"""Custom exception classes for the todo console application."""


class TodoError(Exception):
    """Base exception for todo application."""

    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with the given ID does not exist."""

    def __init__(self, task_id: int) -> None:
        """Initialize TaskNotFoundError with task ID.

        Args:
            task_id: The ID of the task that was not found.
        """
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(TodoError):
    """Raised when input validation fails."""

    pass
