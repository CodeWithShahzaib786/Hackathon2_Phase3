"""Task model for SQLModel ORM."""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task model representing a todo item."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    completed: bool = Field(default=False, nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "user_id": "660e8400-e29b-41d4-a716-446655440001",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00",
            }
        }
