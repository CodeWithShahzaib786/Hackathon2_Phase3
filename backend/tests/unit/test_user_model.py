"""Unit tests for User model validation."""

import pytest
from uuid import uuid4
from datetime import datetime
from src.models.user import User


class TestUserModel:
    """Test suite for User model."""

    def test_create_user_with_valid_data(self):
        """Test creating a user with valid data."""
        user = User(
            id=uuid4(),
            email="test@example.com",
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.utcnow(),
        )
        assert user.email == "test@example.com"
        assert user.hashed_password == "$2b$12$hashedpassword"
        assert user.id is not None
        assert user.created_at is not None

    def test_user_email_must_be_lowercase(self):
        """Test that user email is stored in lowercase."""
        user = User(
            id=uuid4(),
            email="Test@Example.COM",
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.utcnow(),
        )
        assert user.email == "test@example.com"

    def test_user_email_validation(self):
        """Test that invalid email formats are rejected."""
        with pytest.raises(ValueError):
            User(
                id=uuid4(),
                email="invalid-email",
                hashed_password="$2b$12$hashedpassword",
                created_at=datetime.utcnow(),
            )

    def test_user_email_max_length(self):
        """Test that email exceeding 255 characters is rejected."""
        long_email = "a" * 250 + "@example.com"  # 263 characters
        with pytest.raises(ValueError):
            User(
                id=uuid4(),
                email=long_email,
                hashed_password="$2b$12$hashedpassword",
                created_at=datetime.utcnow(),
            )

    def test_user_hashed_password_required(self):
        """Test that hashed_password is required."""
        with pytest.raises(ValueError):
            User(
                id=uuid4(),
                email="test@example.com",
                hashed_password="",
                created_at=datetime.utcnow(),
            )

    def test_user_id_is_uuid(self):
        """Test that user ID is a valid UUID."""
        user_id = uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            hashed_password="$2b$12$hashedpassword",
            created_at=datetime.utcnow(),
        )
        assert user.id == user_id
        assert isinstance(user.id, type(uuid4()))
