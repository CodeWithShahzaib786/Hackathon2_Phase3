"""Unit tests for Task model validation."""

import pytest
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.models.task import Task


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


def test_task_model_creation(session: Session):
    """Test creating a valid Task model."""
    user_id = uuid4()
    task = Task(
        title="Test Task",
        description="Test Description",
        user_id=user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.id is not None
    assert isinstance(task.id, UUID)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.user_id == user_id
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_model_title_required(session: Session):
    """Test that title is required."""
    user_id = uuid4()

    with pytest.raises(Exception):  # SQLModel will raise validation error
        task = Task(
            title=None,  # type: ignore
            user_id=user_id,
        )
        session.add(task)
        session.commit()


def test_task_model_title_max_length(session: Session):
    """Test that title has maximum length constraint."""
    user_id = uuid4()
    long_title = "x" * 256  # Exceeds max_length=255

    task = Task(
        title=long_title,
        user_id=user_id,
    )

    session.add(task)

    with pytest.raises(Exception):  # Database will enforce constraint
        session.commit()


def test_task_model_description_optional(session: Session):
    """Test that description is optional."""
    user_id = uuid4()
    task = Task(
        title="Test Task",
        user_id=user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.description is None


def test_task_model_completed_defaults_to_false(session: Session):
    """Test that completed defaults to False."""
    user_id = uuid4()
    task = Task(
        title="Test Task",
        user_id=user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.completed is False


def test_task_model_timestamps_auto_generated(session: Session):
    """Test that created_at and updated_at are auto-generated."""
    user_id = uuid4()
    task = Task(
        title="Test Task",
        user_id=user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.created_at is not None
    assert task.updated_at is not None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_model_user_id_required(session: Session):
    """Test that user_id is required."""
    with pytest.raises(Exception):  # SQLModel will raise validation error
        task = Task(
            title="Test Task",
            user_id=None,  # type: ignore
        )
        session.add(task)
        session.commit()


def test_task_model_user_id_is_uuid(session: Session):
    """Test that user_id is a valid UUID."""
    user_id = uuid4()
    task = Task(
        title="Test Task",
        user_id=user_id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert isinstance(task.user_id, UUID)


def test_task_model_id_is_unique(session: Session):
    """Test that task IDs are unique."""
    user_id = uuid4()

    task1 = Task(title="Task 1", user_id=user_id)
    task2 = Task(title="Task 2", user_id=user_id)

    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)

    assert task1.id != task2.id


def test_task_model_multiple_tasks_per_user(session: Session):
    """Test that a user can have multiple tasks."""
    user_id = uuid4()

    task1 = Task(title="Task 1", user_id=user_id)
    task2 = Task(title="Task 2", user_id=user_id)
    task3 = Task(title="Task 3", user_id=user_id)

    session.add_all([task1, task2, task3])
    session.commit()

    # Query all tasks for this user
    tasks = session.query(Task).filter(Task.user_id == user_id).all()

    assert len(tasks) == 3
