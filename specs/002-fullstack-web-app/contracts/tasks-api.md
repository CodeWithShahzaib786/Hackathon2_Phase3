# API Contract: Task Management Endpoints

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17
**Base URL**: `http://localhost:8000` (development) | `https://api.yourdomain.com` (production)

## Overview

This document defines the task management API endpoints for creating, reading, updating, and deleting tasks. All endpoints require JWT authentication and enforce user isolation (users can only access their own tasks).

---

## Authentication

**All endpoints require JWT token in Authorization header**:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**User Isolation**: All endpoints automatically filter by authenticated user's ID extracted from JWT token. The `{user_id}` in URLs must match the authenticated user's ID, otherwise 403 Forbidden is returned.

---

## Endpoint: GET /api/{user_id}/tasks

**Purpose**: Retrieve all tasks for the authenticated user

### Request

**Method**: `GET`
**URL**: `/api/{user_id}/tasks`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | `all` | Filter by completion status: `all`, `pending`, `completed` |

**Example Requests**:
```
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks?status=pending
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks?status=completed
```

### Response

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-02-17T10:30:00Z",
      "updated_at": "2026-02-17T10:30:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Call mom",
      "description": null,
      "completed": true,
      "created_at": "2026-02-17T09:15:00Z",
      "updated_at": "2026-02-17T11:20:00Z"
    }
  ],
  "total": 2,
  "status_filter": "all"
}
```

**Empty List Response** (200 OK):
```json
{
  "tasks": [],
  "total": 0,
  "status_filter": "all"
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `tasks` | array | List of task objects |
| `total` | integer | Total number of tasks returned |
| `status_filter` | string | Applied status filter |

**Task Object Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Task identifier |
| `user_id` | string (UUID) | Owner user ID |
| `title` | string | Task title (1-200 chars) |
| `description` | string or null | Task description (max 1000 chars) |
| `completed` | boolean | Completion status |
| `created_at` | string (ISO 8601) | Creation timestamp |
| `updated_at` | string (ISO 8601) | Last update timestamp |

**Error Responses**:

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

---

## Endpoint: POST /api/{user_id}/tasks

**Purpose**: Create a new task for the authenticated user

### Request

**Method**: `POST`
**URL**: `/api/{user_id}/tasks`
**Content-Type**: `application/json`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 chars, not empty after trim | Task title |
| `description` | string | No | Max 1000 chars | Task description (optional) |

### Response

**Success Response** (201 Created):
```json
{
  "id": 3,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-17T12:00:00Z",
  "updated_at": "2026-02-17T12:00:00Z"
}
```

**Error Responses**:

**400 Bad Request** - Invalid input:
```json
{
  "detail": "Title is required and cannot be empty"
}
```

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

### Validation Rules

**Title**:
- Required (cannot be null or empty)
- Min length: 1 character (after trimming whitespace)
- Max length: 200 characters
- Leading/trailing whitespace is trimmed

**Description**:
- Optional (can be null or empty string)
- Max length: 1000 characters
- Leading/trailing whitespace is trimmed

---

## Endpoint: GET /api/{user_id}/tasks/{id}

**Purpose**: Retrieve a specific task by ID

### Request

**Method**: `GET`
**URL**: `/api/{user_id}/tasks/{id}`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |
| `id` | integer | Yes | Task identifier |

**Example Request**:
```
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
```

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-17T10:30:00Z",
  "updated_at": "2026-02-17T10:30:00Z"
}
```

**Error Responses**:

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

**404 Not Found** - Task not found or doesn't belong to user:
```json
{
  "detail": "Task not found"
}
```

---

## Endpoint: PUT /api/{user_id}/tasks/{id}

**Purpose**: Update a task's title and/or description

### Request

**Method**: `PUT`
**URL**: `/api/{user_id}/tasks/{id}`
**Content-Type**: `application/json`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |
| `id` | integer | Yes | Task identifier |

**Request Body**:
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | No | 1-200 chars if provided | New task title |
| `description` | string | No | Max 1000 chars if provided | New task description |

**Note**: At least one field (title or description) must be provided.

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas",
  "completed": false,
  "created_at": "2026-02-17T10:30:00Z",
  "updated_at": "2026-02-17T12:30:00Z"
}
```

**Error Responses**:

**400 Bad Request** - No fields provided:
```json
{
  "detail": "At least one field (title or description) must be provided"
}
```

**400 Bad Request** - Empty title:
```json
{
  "detail": "Title cannot be empty"
}
```

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

**404 Not Found** - Task not found:
```json
{
  "detail": "Task not found"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

---

## Endpoint: DELETE /api/{user_id}/tasks/{id}

**Purpose**: Delete a task

### Request

**Method**: `DELETE`
**URL**: `/api/{user_id}/tasks/{id}`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |
| `id` | integer | Yes | Task identifier |

**Example Request**:
```
DELETE /api/550e8400-e29b-41d4-a716-446655440000/tasks/1
```

### Response

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully",
  "id": 1
}
```

**Error Responses**:

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

**404 Not Found** - Task not found:
```json
{
  "detail": "Task not found"
}
```

---

## Endpoint: PATCH /api/{user_id}/tasks/{id}/complete

**Purpose**: Toggle task completion status

### Request

**Method**: `PATCH`
**URL**: `/api/{user_id}/tasks/{id}/complete`
**Authentication**: Required (JWT token)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User identifier (must match JWT token user_id) |
| `id` | integer | Yes | Task identifier |

**Request Body**: None (empty)

**Example Request**:
```
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete
```

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-02-17T10:30:00Z",
  "updated_at": "2026-02-17T13:00:00Z"
}
```

**Note**: The `completed` field is toggled (false → true or true → false).

**Error Responses**:

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - user_id mismatch:
```json
{
  "detail": "Access denied: user_id does not match authenticated user"
}
```

**404 Not Found** - Task not found:
```json
{
  "detail": "Task not found"
}
```

---

## User Isolation Enforcement

**Critical Security Requirement**: All endpoints MUST enforce user isolation.

### Implementation Strategy

**Step 1**: Extract user_id from JWT token (via dependency injection)
```python
current_user_id = get_current_user(token)  # From JWT
```

**Step 2**: Verify path user_id matches JWT user_id
```python
if path_user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

**Step 3**: Filter all database queries by user_id
```python
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user_id  # Critical filter
).first()
```

**Never trust user_id from URL alone** - always verify against JWT token.

---

## Testing Scenarios

### List Tasks Tests

1. ✅ Get all tasks for authenticated user
2. ✅ Get pending tasks only (status=pending)
3. ✅ Get completed tasks only (status=completed)
4. ✅ Get tasks returns empty list when no tasks exist
5. ✅ Get tasks with invalid token (401 Unauthorized)
6. ✅ Get tasks with mismatched user_id (403 Forbidden)

### Create Task Tests

1. ✅ Create task with title only
2. ✅ Create task with title and description
3. ✅ Create task with empty title (400 Bad Request)
4. ✅ Create task with title > 200 chars (422 Unprocessable Entity)
5. ✅ Create task with description > 1000 chars (422 Unprocessable Entity)
6. ✅ Create task with invalid token (401 Unauthorized)
7. ✅ Create task with mismatched user_id (403 Forbidden)

### Get Task Tests

1. ✅ Get existing task by ID
2. ✅ Get non-existent task (404 Not Found)
3. ✅ Get another user's task (404 Not Found - user isolation)
4. ✅ Get task with invalid token (401 Unauthorized)

### Update Task Tests

1. ✅ Update task title only
2. ✅ Update task description only
3. ✅ Update both title and description
4. ✅ Update with no fields provided (400 Bad Request)
5. ✅ Update with empty title (400 Bad Request)
6. ✅ Update non-existent task (404 Not Found)
7. ✅ Update another user's task (404 Not Found - user isolation)
8. ✅ Update with invalid token (401 Unauthorized)

### Delete Task Tests

1. ✅ Delete existing task
2. ✅ Delete non-existent task (404 Not Found)
3. ✅ Delete another user's task (404 Not Found - user isolation)
4. ✅ Delete with invalid token (401 Unauthorized)

### Toggle Completion Tests

1. ✅ Toggle incomplete task to complete
2. ✅ Toggle complete task to incomplete
3. ✅ Toggle non-existent task (404 Not Found)
4. ✅ Toggle another user's task (404 Not Found - user isolation)
5. ✅ Toggle with invalid token (401 Unauthorized)

---

## API Summary

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/{user_id}/tasks` | List all tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get task details | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |

**Total Endpoints**: 6 task management endpoints + 3 authentication endpoints = 9 total API endpoints

All endpoints return JSON responses and use standard HTTP status codes for success and error conditions.
