"""Pytest configuration and fixtures for todo-console-app tests."""

import pytest
from src.models.task import Task
from src.services.task_repository import TaskRepository
from src.services.task_service import TaskService


@pytest.fixture
def empty_repository() -> TaskRepository:
    """Provide an empty task repository for testing."""
    return TaskRepository()


@pytest.fixture
def repository_with_tasks() -> TaskRepository:
    """Provide a repository with sample tasks for testing."""
    repo = TaskRepository()
    task1 = Task(title="Buy groceries", description="Milk, eggs, bread")
    task2 = Task(title="Call mom", description="")
    task3 = Task(title="Finish homework", description="Math and science")

    repo.add(task1)
    repo.add(task2)
    repo.add(task3)

    return repo


@pytest.fixture
def task_service() -> TaskService:
    """Provide a task service with empty repository for testing."""
    return TaskService()


@pytest.fixture
def task_service_with_tasks() -> TaskService:
    """Provide a task service with sample tasks for testing."""
    service = TaskService()
    service.create_task("Buy groceries", "Milk, eggs, bread")
    service.create_task("Call mom", "")
    service.create_task("Finish homework", "Math and science")
    return service
