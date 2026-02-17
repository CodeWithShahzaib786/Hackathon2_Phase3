"""Unit tests for TaskRepository."""

import pytest
from src.models.task import Task
from src.services.task_repository import TaskRepository
from src.models.exceptions import TaskNotFoundError


class TestTaskRepositoryAdd:
    """Test adding tasks to repository."""

    def test_add_task_assigns_id(self) -> None:
        """Test that adding a task assigns a unique ID."""
        repo = TaskRepository()
        task = Task(title="Test task")
        added_task = repo.add(task)
        assert added_task.id == 1

    def test_add_multiple_tasks_assigns_sequential_ids(self) -> None:
        """Test that multiple tasks get sequential IDs."""
        repo = TaskRepository()
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")

        added1 = repo.add(task1)
        added2 = repo.add(task2)
        added3 = repo.add(task3)

        assert added1.id == 1
        assert added2.id == 2
        assert added3.id == 3


class TestTaskRepositoryGet:
    """Test retrieving tasks from repository."""

    def test_get_existing_task(self) -> None:
        """Test retrieving an existing task by ID."""
        repo = TaskRepository()
        task = Task(title="Test task")
        added_task = repo.add(task)
        retrieved_task = repo.get(added_task.id)
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == "Test task"

    def test_get_nonexistent_task_raises_error(self) -> None:
        """Test that getting a nonexistent task raises TaskNotFoundError."""
        repo = TaskRepository()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            repo.get(999)


class TestTaskRepositoryGetAll:
    """Test retrieving all tasks from repository."""

    def test_get_all_empty_repository(self) -> None:
        """Test getting all tasks from empty repository."""
        repo = TaskRepository()
        tasks = repo.get_all()
        assert tasks == []

    def test_get_all_with_tasks(self) -> None:
        """Test getting all tasks from repository with tasks."""
        repo = TaskRepository()
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")

        repo.add(task1)
        repo.add(task2)
        repo.add(task3)

        tasks = repo.get_all()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"


class TestTaskRepositoryUpdate:
    """Test updating tasks in repository."""

    def test_update_existing_task(self) -> None:
        """Test updating an existing task."""
        repo = TaskRepository()
        task = Task(title="Original title")
        added_task = repo.add(task)

        updated_task = repo.update(added_task.id, title="New title")
        assert updated_task.title == "New title"

    def test_update_nonexistent_task_raises_error(self) -> None:
        """Test that updating a nonexistent task raises TaskNotFoundError."""
        repo = TaskRepository()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            repo.update(999, title="New title")

    def test_update_task_title_only(self) -> None:
        """Test updating only the title."""
        repo = TaskRepository()
        task = Task(title="Original", description="Original desc")
        added_task = repo.add(task)

        updated_task = repo.update(added_task.id, title="New title")
        assert updated_task.title == "New title"
        assert updated_task.description == "Original desc"

    def test_update_task_description_only(self) -> None:
        """Test updating only the description."""
        repo = TaskRepository()
        task = Task(title="Original", description="Original desc")
        added_task = repo.add(task)

        updated_task = repo.update(added_task.id, description="New desc")
        assert updated_task.title == "Original"
        assert updated_task.description == "New desc"


class TestTaskRepositoryDelete:
    """Test deleting tasks from repository."""

    def test_delete_existing_task(self) -> None:
        """Test deleting an existing task."""
        repo = TaskRepository()
        task = Task(title="Test task")
        added_task = repo.add(task)

        repo.delete(added_task.id)

        with pytest.raises(TaskNotFoundError):
            repo.get(added_task.id)

    def test_delete_nonexistent_task_raises_error(self) -> None:
        """Test that deleting a nonexistent task raises TaskNotFoundError."""
        repo = TaskRepository()
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            repo.delete(999)

    def test_delete_task_from_multiple(self) -> None:
        """Test deleting one task from multiple tasks."""
        repo = TaskRepository()
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")

        added1 = repo.add(task1)
        repo.add(task2)
        repo.add(task3)

        repo.delete(added1.id)

        tasks = repo.get_all()
        assert len(tasks) == 2
        assert all(t.id != added1.id for t in tasks)


class TestTaskRepositoryExists:
    """Test checking task existence in repository."""

    def test_exists_for_existing_task(self) -> None:
        """Test that exists returns True for existing task."""
        repo = TaskRepository()
        task = Task(title="Test task")
        added_task = repo.add(task)
        assert repo.exists(added_task.id) is True

    def test_exists_for_nonexistent_task(self) -> None:
        """Test that exists returns False for nonexistent task."""
        repo = TaskRepository()
        assert repo.exists(999) is False
