"""Base Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseSchema):
    """Base user schema."""

    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, max_length=128, description="User's password")


class UserLogin(UserBase):
    """Schema for user login."""

    password: str = Field(..., description="User's password")


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="Account creation timestamp")


class TokenResponse(BaseSchema):
    """Schema for authentication token response."""

    id: UUID = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    token: str = Field(..., description="JWT access token")


# Task schemas
class TaskBase(BaseSchema):
    """Base task schema."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseSchema):
    """Schema for updating a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="New task title")
    description: Optional[str] = Field(None, max_length=1000, description="New task description")
    completed: Optional[bool] = Field(None, description="Task completion status")


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: UUID = Field(..., description="Task's unique identifier")
    user_id: UUID = Field(..., description="Owner's user ID")
    completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")


class TaskListResponse(BaseSchema):
    """Schema for task list response."""

    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    status_filter: str = Field(..., description="Applied status filter")


# Error schemas
class ErrorResponse(BaseSchema):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")


class MessageResponse(BaseSchema):
    """Schema for simple message responses."""

    message: str = Field(..., description="Response message")
