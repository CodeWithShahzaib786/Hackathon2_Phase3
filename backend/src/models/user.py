"""User model for authentication."""

from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from pydantic import EmailStr, field_validator


class User(SQLModel, table=True):
    """User account for authentication.

    Attributes:
        id: Unique identifier for the user (UUID).
        email: User's email address (unique, lowercase).
        hashed_password: Bcrypt-hashed password.
        created_at: Timestamp when account was created.
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    @field_validator("email")
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        """Ensure email is stored in lowercase.

        Args:
            v: The email value to validate.

        Returns:
            The email in lowercase.
        """
        return v.lower()

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        """Validate email format.

        Args:
            v: The email value to validate.

        Returns:
            The validated email.

        Raises:
            ValueError: If email format is invalid.
        """
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v

    @field_validator("hashed_password")
    @classmethod
    def password_must_not_be_empty(cls, v: str) -> str:
        """Ensure hashed password is not empty.

        Args:
            v: The hashed password value to validate.

        Returns:
            The validated hashed password.

        Raises:
            ValueError: If hashed password is empty.
        """
        if not v or len(v.strip()) == 0:
            raise ValueError("Hashed password cannot be empty")
        return v
