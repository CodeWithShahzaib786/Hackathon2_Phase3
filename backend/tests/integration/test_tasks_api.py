"""Integration tests for tasks API endpoints."""

import pytest
from uuid import uuid4
from httpx import AsyncClient
from sqlmodel import Session, create_engine, SQLModel, select
from sqlmodel.pool import StaticPool

from src.main import app
from src.core.database import get_session
from src.models.user import User
from src.models.task import Task
from src.core.security import hash_password, create_access_token


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


@pytest.fixture(name="client")
async def client_fixture(session: Session):
    """Create a test client with database session override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("SecurePass123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user_token")
def test_user_token_fixture(test_user: User):
    """Create a JWT token for the test user."""
    return create_access_token({"sub": str(test_user.id)})


@pytest.fixture(name="other_user")
def other_user_fixture(session: Session):
    """Create another test user for isolation tests."""
    user = User(
        email="other@example.com",
        hashed_password=hash_password("SecurePass123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="other_user_token")
def other_user_token_fixture(other_user: User):
    """Create a JWT token for the other user."""
    return create_access_token({"sub": str(other_user.id)})


@pytest.mark.asyncio
async def test_create_task_success(client: AsyncClient, test_user: User, test_user_token: str):
    """Test creating a task successfully."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["user_id"] == str(test_user.id)
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_task_without_description(client: AsyncClient, test_user: User, test_user_token: str):
    """Test creating a task without description."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",
        json={
            "title": "Test Task",
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_create_task_empty_title_fails(client: AsyncClient, test_user: User, test_user_token: str):
    """Test that creating a task with empty title fails."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",
        json={
            "title": "",
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 400
    assert "title" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_task_missing_title_fails(client: AsyncClient, test_user: User, test_user_token: str):
    """Test that creating a task without title fails."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",
        json={
            "description": "Test Description",
        },
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_create_task_unauthorized(client: AsyncClient, test_user: User):
    """Test that creating a task without authentication fails."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",
        json={
            "title": "Test Task",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task_wrong_user_forbidden(client: AsyncClient, test_user: User, other_user: User, other_user_token: str):
    """Test that creating a task for another user is forbidden."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",  # Trying to create task for test_user
        json={
            "title": "Test Task",
        },
        headers={"Authorization": f"Bearer {other_user_token}"},  # But authenticated as other_user
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_tasks_empty_list(client: AsyncClient, test_user: User, test_user_token: str):
    """Test getting all tasks when none exist."""
    response = await client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_all_tasks_returns_user_tasks(client: AsyncClient, test_user: User, test_user_token: str, session: Session):
    """Test getting all tasks for a specific user."""
    # Create tasks for this user
    task1 = Task(title="Task 1", user_id=test_user.id)
    task2 = Task(title="Task 2", user_id=test_user.id)
    task3 = Task(title="Task 3", user_id=test_user.id)

    session.add_all([task1, task2, task3])
    session.commit()

    response = await client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(task["user_id"] == str(test_user.id) for task in data)


@pytest.mark.asyncio
async def test_get_all_tasks_unauthorized(client: AsyncClient, test_user: User):
    """Test that getting tasks without authentication fails."""
    response = await client.get(f"/api/{test_user.id}/tasks")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_tasks_wrong_user_forbidden(client: AsyncClient, test_user: User, other_user: User, other_user_token: str):
    """Test that getting tasks for another user is forbidden."""
    response = await client.get(
        f"/api/{test_user.id}/tasks",  # Trying to get test_user's tasks
        headers={"Authorization": f"Bearer {other_user_token}"},  # But authenticated as other_user
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_user_isolation_cannot_see_other_users_tasks(
    client: AsyncClient,
    test_user: User,
    test_user_token: str,
    other_user: User,
    other_user_token: str,
    session: Session,
):
    """Test that users can only see their own tasks."""
    # Create tasks for test_user
    task1 = Task(title="Test User Task 1", user_id=test_user.id)
    task2 = Task(title="Test User Task 2", user_id=test_user.id)

    # Create tasks for other_user
    task3 = Task(title="Other User Task 1", user_id=other_user.id)
    task4 = Task(title="Other User Task 2", user_id=other_user.id)

    session.add_all([task1, task2, task3, task4])
    session.commit()

    # Get tasks for test_user
    response1 = await client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response1.status_code == 200
    test_user_tasks = response1.json()
    assert len(test_user_tasks) == 2
    assert all(task["user_id"] == str(test_user.id) for task in test_user_tasks)
    assert all("Test User" in task["title"] for task in test_user_tasks)

    # Get tasks for other_user
    response2 = await client.get(
        f"/api/{other_user.id}/tasks",
        headers={"Authorization": f"Bearer {other_user_token}"},
    )

    assert response2.status_code == 200
    other_user_tasks = response2.json()
    assert len(other_user_tasks) == 2
    assert all(task["user_id"] == str(other_user.id) for task in other_user_tasks)
    assert all("Other User" in task["title"] for task in other_user_tasks)


@pytest.mark.asyncio
async def test_user_isolation_cannot_create_task_for_other_user(
    client: AsyncClient,
    test_user: User,
    other_user: User,
    other_user_token: str,
):
    """Test that users cannot create tasks for other users."""
    response = await client.post(
        f"/api/{test_user.id}/tasks",  # Trying to create for test_user
        json={"title": "Malicious Task"},
        headers={"Authorization": f"Bearer {other_user_token}"},  # Authenticated as other_user
    )

    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower() or "forbidden" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_tasks_ordered_by_created_at_desc(
    client: AsyncClient,
    test_user: User,
    test_user_token: str,
    session: Session,
):
    """Test that tasks are returned in descending order by created_at."""
    # Create tasks with different timestamps
    task1 = Task(title="First Task", user_id=test_user.id)
    session.add(task1)
    session.commit()

    task2 = Task(title="Second Task", user_id=test_user.id)
    session.add(task2)
    session.commit()

    task3 = Task(title="Third Task", user_id=test_user.id)
    session.add(task3)
    session.commit()

    response = await client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 200
    tasks = response.json()

    # Most recent task should be first
    assert tasks[0]["title"] == "Third Task"
    assert tasks[1]["title"] == "Second Task"
    assert tasks[2]["title"] == "First Task"
