"""Task model for the todo console application."""

from dataclasses import dataclass, field
from datetime import datetime

from src.models.exceptions import ValidationError


@dataclass
class Task:
    """Represents a todo task with validation.

    Attributes:
        title: Short description of the task (required, 1-200 characters).
        description: Detailed information about the task (optional, max 1000 characters).
        completed: Whether the task is done (default: False).
        id: Unique identifier assigned by repository (default: 0).
        created_at: Timestamp when task was created.
    """

    title: str
    description: str = ""
    completed: bool = False
    id: int = field(init=False, default=0)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        self._validate_title()
        self._validate_description()

    def _validate_title(self) -> None:
        """Validate title field.

        Raises:
            ValidationError: If title is empty or exceeds 200 characters.
        """
        self.title = self.title.strip()
        if not self.title or len(self.title) > 200:
            raise ValidationError("Title is required and must be 1-200 characters")

    def _validate_description(self) -> None:
        """Validate description field.

        Raises:
            ValidationError: If description exceeds 1000 characters.
        """
        self.description = self.description.strip()
        if len(self.description) > 1000:
            raise ValidationError("Description must not exceed 1000 characters")

    def toggle_completion(self) -> None:
        """Toggle the completion status of the task."""
        self.completed = not self.completed

    def update_title(self, new_title: str) -> None:
        """Update task title with validation.

        Args:
            new_title: The new title for the task.

        Raises:
            ValidationError: If new title is invalid.
        """
        old_title = self.title
        self.title = new_title
        try:
            self._validate_title()
        except ValidationError:
            self.title = old_title
            raise

    def update_description(self, new_description: str) -> None:
        """Update task description with validation.

        Args:
            new_description: The new description for the task.

        Raises:
            ValidationError: If new description is invalid.
        """
        old_description = self.description
        self.description = new_description
        try:
            self._validate_description()
        except ValidationError:
            self.description = old_description
            raise
