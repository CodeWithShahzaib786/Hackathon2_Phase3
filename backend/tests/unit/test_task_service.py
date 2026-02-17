"""Unit tests for TaskService."""

import pytest
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="task_service")
def task_service_fixture(session: Session):
    """Create a TaskService instance."""
    return TaskService(session)


@pytest.mark.asyncio
async def test_create_task_success(task_service: TaskService, session: Session):
    """Test creating a task successfully."""
    user_id = uuid4()
    title = "Test Task"
    description = "Test Description"

    task = await task_service.create_task(
        user_id=user_id,
        title=title,
        description=description,
    )

    assert task.id is not None
    assert task.title == title
    assert task.description == description
    assert task.user_id == user_id
    assert task.completed is False


@pytest.mark.asyncio
async def test_create_task_without_description(task_service: TaskService, session: Session):
    """Test creating a task without description."""
    user_id = uuid4()
    title = "Test Task"

    task = await task_service.create_task(
        user_id=user_id,
        title=title,
    )

    assert task.id is not None
    assert task.title == title
    assert task.description is None
    assert task.user_id == user_id
    assert task.completed is False


@pytest.mark.asyncio
async def test_create_task_empty_title_raises_error(task_service: TaskService):
    """Test that creating a task with empty title raises error."""
    user_id = uuid4()

    with pytest.raises(ValueError, match="Title cannot be empty"):
        await task_service.create_task(
            user_id=user_id,
            title="",
        )


@pytest.mark.asyncio
async def test_create_task_whitespace_title_raises_error(task_service: TaskService):
    """Test that creating a task with whitespace-only title raises error."""
    user_id = uuid4()

    with pytest.raises(ValueError, match="Title cannot be empty"):
        await task_service.create_task(
            user_id=user_id,
            title="   ",
        )


@pytest.mark.asyncio
async def test_create_task_title_too_long_raises_error(task_service: TaskService):
    """Test that creating a task with title exceeding max length raises error."""
    user_id = uuid4()
    long_title = "x" * 256  # Exceeds max_length=255

    with pytest.raises(ValueError, match="Title cannot exceed 255 characters"):
        await task_service.create_task(
            user_id=user_id,
            title=long_title,
        )


@pytest.mark.asyncio
async def test_get_all_tasks_empty_list(task_service: TaskService):
    """Test getting all tasks when none exist."""
    user_id = uuid4()

    tasks = await task_service.get_all_tasks(user_id=user_id)

    assert tasks == []


@pytest.mark.asyncio
async def test_get_all_tasks_returns_user_tasks(task_service: TaskService, session: Session):
    """Test getting all tasks for a specific user."""
    user_id = uuid4()

    # Create tasks for this user
    task1 = Task(title="Task 1", user_id=user_id)
    task2 = Task(title="Task 2", user_id=user_id)
    task3 = Task(title="Task 3", user_id=user_id)

    session.add_all([task1, task2, task3])
    session.commit()

    tasks = await task_service.get_all_tasks(user_id=user_id)

    assert len(tasks) == 3
    assert all(task.user_id == user_id for task in tasks)


@pytest.mark.asyncio
async def test_get_all_tasks_user_isolation(task_service: TaskService, session: Session):
    """Test that get_all_tasks only returns tasks for the specified user."""
    user1_id = uuid4()
    user2_id = uuid4()

    # Create tasks for user1
    task1 = Task(title="User 1 Task 1", user_id=user1_id)
    task2 = Task(title="User 1 Task 2", user_id=user1_id)

    # Create tasks for user2
    task3 = Task(title="User 2 Task 1", user_id=user2_id)
    task4 = Task(title="User 2 Task 2", user_id=user2_id)

    session.add_all([task1, task2, task3, task4])
    session.commit()

    # Get tasks for user1
    user1_tasks = await task_service.get_all_tasks(user_id=user1_id)

    assert len(user1_tasks) == 2
    assert all(task.user_id == user1_id for task in user1_tasks)
    assert all(task.title.startswith("User 1") for task in user1_tasks)


@pytest.mark.asyncio
async def test_get_all_tasks_ordered_by_created_at(task_service: TaskService, session: Session):
    """Test that tasks are returned in descending order by created_at."""
    user_id = uuid4()

    # Create tasks (they will have slightly different timestamps)
    task1 = Task(title="First Task", user_id=user_id)
    session.add(task1)
    session.commit()

    task2 = Task(title="Second Task", user_id=user_id)
    session.add(task2)
    session.commit()

    task3 = Task(title="Third Task", user_id=user_id)
    session.add(task3)
    session.commit()

    tasks = await task_service.get_all_tasks(user_id=user_id)

    # Most recent task should be first
    assert tasks[0].title == "Third Task"
    assert tasks[1].title == "Second Task"
    assert tasks[2].title == "First Task"


@pytest.mark.asyncio
async def test_get_all_tasks_includes_completed_and_incomplete(task_service: TaskService, session: Session):
    """Test that get_all_tasks returns both completed and incomplete tasks."""
    user_id = uuid4()

    # Create completed and incomplete tasks
    task1 = Task(title="Incomplete Task", user_id=user_id, completed=False)
    task2 = Task(title="Completed Task", user_id=user_id, completed=True)

    session.add_all([task1, task2])
    session.commit()

    tasks = await task_service.get_all_tasks(user_id=user_id)

    assert len(tasks) == 2
    assert any(task.completed is False for task in tasks)
    assert any(task.completed is True for task in tasks)
