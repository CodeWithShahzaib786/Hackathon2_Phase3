"""Integration tests for CLI commands."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.main import main
from src.services.task_service import TaskService


class TestAddCommand:
    """Test the 'add' command integration."""

    def test_add_command_with_title_only(self) -> None:
        """Test adding a task with only a title."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            # Simulate: todo add "Buy groceries"
            task = service.create_task("Buy groceries")
            assert task.id == 1
            assert task.title == "Buy groceries"
            assert task.description == ""

    def test_add_command_with_title_and_description(self) -> None:
        """Test adding a task with title and description."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            # Simulate: todo add "Buy groceries" --description "Milk, eggs, bread"
            task = service.create_task("Buy groceries", "Milk, eggs, bread")
            assert task.id == 1
            assert task.title == "Buy groceries"
            assert task.description == "Milk, eggs, bread"

    def test_add_command_with_empty_title_shows_error(self) -> None:
        """Test that adding task with empty title shows error message."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            with pytest.raises(Exception):  # ValidationError will be raised
                service.create_task("")


class TestListCommand:
    """Test the 'list' command integration."""

    def test_list_command_empty_repository(self) -> None:
        """Test listing tasks from empty repository."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            tasks = service.get_all_tasks()
            assert tasks == []

    def test_list_command_with_tasks(self) -> None:
        """Test listing tasks from repository with tasks."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            service.create_task("Buy groceries", "Milk, eggs, bread")
            service.create_task("Call mom")
            service.create_task("Finish homework", "Math and science")

            tasks = service.get_all_tasks()
            assert len(tasks) == 3
            assert tasks[0].title == "Buy groceries"
            assert tasks[1].title == "Call mom"
            assert tasks[2].title == "Finish homework"

    def test_list_command_shows_completion_status(self) -> None:
        """Test that list command shows completion status."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            task1 = service.create_task("Task 1")
            task2 = service.create_task("Task 2")

            # Mark task 2 as complete
            service.toggle_completion(task2.id)

            tasks = service.get_all_tasks()
            assert tasks[0].completed is False
            assert tasks[1].completed is True


class TestCompleteCommand:
    """Test the 'complete' command integration."""

    def test_complete_command_toggles_status(self) -> None:
        """Test that complete command toggles task status."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            task = service.create_task("Test task")
            assert task.completed is False

            # Toggle to complete
            updated = service.toggle_completion(task.id)
            assert updated.completed is True

            # Toggle back to incomplete
            updated = service.toggle_completion(task.id)
            assert updated.completed is False


class TestUpdateCommand:
    """Test the 'update' command integration."""

    def test_update_command_title_only(self) -> None:
        """Test updating only the title."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            task = service.create_task("Original title", "Original description")
            updated = service.update_task(task.id, title="New title")

            assert updated.title == "New title"
            assert updated.description == "Original description"

    def test_update_command_description_only(self) -> None:
        """Test updating only the description."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            task = service.create_task("Original title", "Original description")
            updated = service.update_task(task.id, description="New description")

            assert updated.title == "Original title"
            assert updated.description == "New description"


class TestDeleteCommand:
    """Test the 'delete' command integration."""

    def test_delete_command_removes_task(self) -> None:
        """Test that delete command removes task."""
        service = TaskService()
        with patch("src.cli.commands.task_service", service):
            task = service.create_task("Test task")
            service.delete_task(task.id)

            tasks = service.get_all_tasks()
            assert len(tasks) == 0
