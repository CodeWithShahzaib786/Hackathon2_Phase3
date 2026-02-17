"""Unit tests for TaskService."""

import pytest
from src.services.task_service import TaskService
from src.models.exceptions import TaskNotFoundError, ValidationError


class TestTaskServiceCreateTask:
    """Test creating tasks via TaskService."""

    def test_create_task_with_title_only(self) -> None:
        """Test creating a task with only a title."""
        service = TaskService()
        task = service.create_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_with_title_and_description(self) -> None:
        """Test creating a task with title and description."""
        service = TaskService()
        task = service.create_task("Buy groceries", "Milk, eggs, bread")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_create_multiple_tasks_assigns_sequential_ids(self) -> None:
        """Test that multiple tasks get sequential IDs."""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_with_empty_title_raises_error(self) -> None:
        """Test that creating task with empty title raises ValidationError."""
        service = TaskService()
        with pytest.raises(ValidationError, match="Title is required"):
            service.create_task("")

    def test_create_task_with_too_long_title_raises_error(self) -> None:
        """Test that creating task with too long title raises ValidationError."""
        service = TaskService()
        long_title = "A" * 201
        with pytest.raises(ValidationError, match="Title is required and must be 1-200 characters"):
            service.create_task(long_title)


class TestTaskServiceGetAllTasks:
    """Test retrieving all tasks via TaskService."""

    def test_get_all_tasks_empty_repository(self) -> None:
        """Test getting all tasks from empty repository."""
        service = TaskService()
        tasks = service.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_with_tasks(self) -> None:
        """Test getting all tasks from repository with tasks."""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")

        tasks = service.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_get_all_tasks_returns_copy(self) -> None:
        """Test that get_all_tasks returns a list that can be modified."""
        service = TaskService()
        service.create_task("Task 1")

        tasks1 = service.get_all_tasks()
        tasks2 = service.get_all_tasks()

        # Should be separate lists
        assert tasks1 is not tasks2
        assert len(tasks1) == len(tasks2)


class TestTaskServiceToggleCompletion:
    """Test toggling task completion via TaskService."""

    def test_toggle_completion_existing_task(self) -> None:
        """Test toggling completion status of existing task."""
        service = TaskService()
        task = service.create_task("Test task")

        assert task.completed is False

        updated_task = service.toggle_completion(task.id)
        assert updated_task.completed is True

        updated_task = service.toggle_completion(task.id)
        assert updated_task.completed is False

    def test_toggle_completion_nonexistent_task_raises_error(self) -> None:
        """Test that toggling nonexistent task raises TaskNotFoundError."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service.toggle_completion(999)


class TestTaskServiceUpdateTask:
    """Test updating tasks via TaskService."""

    def test_update_task_title_only(self) -> None:
        """Test updating only the task title."""
        service = TaskService()
        task = service.create_task("Original title", "Original description")

        updated_task = service.update_task(task.id, title="New title")
        assert updated_task.title == "New title"
        assert updated_task.description == "Original description"

    def test_update_task_description_only(self) -> None:
        """Test updating only the task description."""
        service = TaskService()
        task = service.create_task("Original title", "Original description")

        updated_task = service.update_task(task.id, description="New description")
        assert updated_task.title == "Original title"
        assert updated_task.description == "New description"

    def test_update_task_both_fields(self) -> None:
        """Test updating both title and description."""
        service = TaskService()
        task = service.create_task("Original title", "Original description")

        updated_task = service.update_task(task.id, title="New title", description="New description")
        assert updated_task.title == "New title"
        assert updated_task.description == "New description"

    def test_update_nonexistent_task_raises_error(self) -> None:
        """Test that updating nonexistent task raises TaskNotFoundError."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service.update_task(999, title="New title")


class TestTaskServiceDeleteTask:
    """Test deleting tasks via TaskService."""

    def test_delete_existing_task(self) -> None:
        """Test deleting an existing task."""
        service = TaskService()
        task = service.create_task("Test task")

        deleted_task = service.delete_task(task.id)
        assert deleted_task.id == task.id
        assert deleted_task.title == "Test task"

        # Verify task is deleted
        with pytest.raises(TaskNotFoundError):
            service.toggle_completion(task.id)

    def test_delete_nonexistent_task_raises_error(self) -> None:
        """Test that deleting nonexistent task raises TaskNotFoundError."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service.delete_task(999)
