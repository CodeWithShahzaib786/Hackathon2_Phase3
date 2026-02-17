"""Integration tests for authentication API endpoints."""

import pytest
from httpx import AsyncClient
from fastapi import status
from src.main import app


@pytest.mark.asyncio
class TestSignupEndpoint:
    """Test suite for POST /api/auth/signup endpoint."""

    async def test_signup_with_valid_credentials(self):
        """Test successful user signup with valid email and password."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "newuser@example.com",
                    "password": "SecurePass123",
                },
            )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == "newuser@example.com"
        assert "token" in data
        assert "created_at" in data

    async def test_signup_with_duplicate_email(self):
        """Test signup fails with duplicate email."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First signup
            await client.post(
                "/api/auth/signup",
                json={
                    "email": "duplicate@example.com",
                    "password": "SecurePass123",
                },
            )

            # Second signup with same email
            response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "duplicate@example.com",
                    "password": "DifferentPass456",
                },
            )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already registered" in response.json()["detail"].lower()

    async def test_signup_with_invalid_email(self):
        """Test signup fails with invalid email format."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "invalid-email",
                    "password": "SecurePass123",
                },
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_with_weak_password(self):
        """Test signup fails with password less than 8 characters."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "test@example.com",
                    "password": "short",
                },
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_with_missing_fields(self):
        """Test signup fails with missing required fields."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signup",
                json={"email": "test@example.com"},
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestSigninEndpoint:
    """Test suite for POST /api/auth/signin endpoint."""

    async def test_signin_with_correct_credentials(self):
        """Test successful signin with correct credentials."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First create a user
            await client.post(
                "/api/auth/signup",
                json={
                    "email": "signin@example.com",
                    "password": "SecurePass123",
                },
            )

            # Then sign in
            response = await client.post(
                "/api/auth/signin",
                json={
                    "email": "signin@example.com",
                    "password": "SecurePass123",
                },
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == "signin@example.com"
        assert "token" in data

    async def test_signin_with_incorrect_password(self):
        """Test signin fails with incorrect password."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First create a user
            await client.post(
                "/api/auth/signup",
                json={
                    "email": "wrongpass@example.com",
                    "password": "CorrectPass123",
                },
            )

            # Try to sign in with wrong password
            response = await client.post(
                "/api/auth/signin",
                json={
                    "email": "wrongpass@example.com",
                    "password": "WrongPass456",
                },
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()

    async def test_signin_with_nonexistent_email(self):
        """Test signin fails with non-existent email."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signin",
                json={
                    "email": "nonexistent@example.com",
                    "password": "SomePass123",
                },
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()

    async def test_signin_with_missing_fields(self):
        """Test signin fails with missing required fields."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signin",
                json={"email": "test@example.com"},
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestSignoutEndpoint:
    """Test suite for POST /api/auth/signout endpoint."""

    async def test_signout_with_valid_token(self):
        """Test successful signout with valid token."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First create a user and get token
            signup_response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "signout@example.com",
                    "password": "SecurePass123",
                },
            )
            token = signup_response.json()["token"]

            # Then sign out
            response = await client.post(
                "/api/auth/signout",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    async def test_signout_with_invalid_token(self):
        """Test signout fails with invalid token."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/auth/signout",
                headers={"Authorization": "Bearer invalid.token.here"},
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_signout_without_token(self):
        """Test signout fails without token."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/auth/signout")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
class TestJWTAuthenticationMiddleware:
    """Test suite for JWT authentication middleware."""

    async def test_protected_endpoint_with_valid_token(self):
        """Test accessing protected endpoint with valid token succeeds."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First create a user and get token
            signup_response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "protected@example.com",
                    "password": "SecurePass123",
                },
            )
            token = signup_response.json()["token"]
            user_id = signup_response.json()["id"]

            # Try to access a protected endpoint (tasks list)
            response = await client.get(
                f"/api/{user_id}/tasks",
                headers={"Authorization": f"Bearer {token}"},
            )

        # Should not return 401 Unauthorized
        assert response.status_code != status.HTTP_401_UNAUTHORIZED

    async def test_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token fails."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/550e8400-e29b-41d4-a716-446655440000/tasks",
                headers={"Authorization": "Bearer invalid.token.here"},
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token fails."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/550e8400-e29b-41d4-a716-446655440000/tasks"
            )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_isolation_with_mismatched_token(self):
        """Test that user cannot access another user's resources."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create first user
            user1_response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "user1@example.com",
                    "password": "SecurePass123",
                },
            )
            user1_token = user1_response.json()["token"]

            # Create second user
            user2_response = await client.post(
                "/api/auth/signup",
                json={
                    "email": "user2@example.com",
                    "password": "SecurePass123",
                },
            )
            user2_id = user2_response.json()["id"]

            # Try to access user2's tasks with user1's token
            response = await client.get(
                f"/api/{user2_id}/tasks",
                headers={"Authorization": f"Bearer {user1_token}"},
            )

        assert response.status_code == status.HTTP_403_FORBIDDEN
