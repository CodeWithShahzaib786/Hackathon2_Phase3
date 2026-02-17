"""Unit tests for Task model."""

import pytest
from datetime import datetime
from src.models.task import Task
from src.models.exceptions import ValidationError


class TestTaskCreation:
    """Test task creation and initialization."""

    def test_create_task_with_title_only(self) -> None:
        """Test creating a task with only a title."""
        task = Task(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_title_and_description(self) -> None:
        """Test creating a task with title and description."""
        task = Task(title="Buy groceries", description="Milk, eggs, bread")
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False

    def test_task_id_is_zero_initially(self) -> None:
        """Test that task ID is 0 before being added to repository."""
        task = Task(title="Test task")
        assert task.id == 0


class TestTaskValidation:
    """Test task validation rules."""

    def test_empty_title_raises_validation_error(self) -> None:
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title is required"):
            Task(title="")

    def test_whitespace_only_title_raises_validation_error(self) -> None:
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title is required"):
            Task(title="   ")

    def test_title_too_long_raises_validation_error(self) -> None:
        """Test that title over 200 characters raises ValidationError."""
        long_title = "A" * 201
        with pytest.raises(ValidationError, match="Title is required and must be 1-200 characters"):
            Task(title=long_title)

    def test_title_exactly_200_chars_is_valid(self) -> None:
        """Test that title with exactly 200 characters is valid."""
        title = "A" * 200
        task = Task(title=title)
        assert len(task.title) == 200

    def test_description_too_long_raises_validation_error(self) -> None:
        """Test that description over 1000 characters raises ValidationError."""
        long_desc = "X" * 1001
        with pytest.raises(ValidationError, match="Description must not exceed 1000 characters"):
            Task(title="Valid title", description=long_desc)

    def test_description_exactly_1000_chars_is_valid(self) -> None:
        """Test that description with exactly 1000 characters is valid."""
        desc = "X" * 1000
        task = Task(title="Valid title", description=desc)
        assert len(task.description) == 1000

    def test_title_whitespace_is_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped from title."""
        task = Task(title="  Buy groceries  ")
        assert task.title == "Buy groceries"

    def test_description_whitespace_is_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped from description."""
        task = Task(title="Test", description="  Some description  ")
        assert task.description == "Some description"


class TestTaskToggleCompletion:
    """Test task completion toggling."""

    def test_toggle_completion_from_incomplete_to_complete(self) -> None:
        """Test toggling task from incomplete to complete."""
        task = Task(title="Test task")
        assert task.completed is False
        task.toggle_completion()
        assert task.completed is True

    def test_toggle_completion_from_complete_to_incomplete(self) -> None:
        """Test toggling task from complete to incomplete."""
        task = Task(title="Test task")
        task.toggle_completion()  # Make it complete
        assert task.completed is True
        task.toggle_completion()  # Toggle back
        assert task.completed is False


class TestTaskUpdateTitle:
    """Test task title updates."""

    def test_update_title_with_valid_title(self) -> None:
        """Test updating task title with valid input."""
        task = Task(title="Original title")
        task.update_title("New title")
        assert task.title == "New title"

    def test_update_title_with_empty_title_raises_error(self) -> None:
        """Test that updating with empty title raises ValidationError."""
        task = Task(title="Original title")
        with pytest.raises(ValidationError, match="Title is required"):
            task.update_title("")
        # Original title should be preserved
        assert task.title == "Original title"

    def test_update_title_with_too_long_title_raises_error(self) -> None:
        """Test that updating with too long title raises ValidationError."""
        task = Task(title="Original title")
        long_title = "A" * 201
        with pytest.raises(ValidationError, match="Title is required and must be 1-200 characters"):
            task.update_title(long_title)
        # Original title should be preserved
        assert task.title == "Original title"


class TestTaskUpdateDescription:
    """Test task description updates."""

    def test_update_description_with_valid_description(self) -> None:
        """Test updating task description with valid input."""
        task = Task(title="Test task", description="Original description")
        task.update_description("New description")
        assert task.description == "New description"

    def test_update_description_with_empty_description(self) -> None:
        """Test updating task description with empty string."""
        task = Task(title="Test task", description="Original description")
        task.update_description("")
        assert task.description == ""

    def test_update_description_with_too_long_description_raises_error(self) -> None:
        """Test that updating with too long description raises ValidationError."""
        task = Task(title="Test task", description="Original description")
        long_desc = "X" * 1001
        with pytest.raises(ValidationError, match="Description must not exceed 1000 characters"):
            task.update_description(long_desc)
        # Original description should be preserved
        assert task.description == "Original description"
