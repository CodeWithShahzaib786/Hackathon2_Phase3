# API Contract: Authentication Endpoints

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17
**Base URL**: `http://localhost:8000` (development) | `https://api.yourdomain.com` (production)

## Overview

This document defines the authentication API endpoints for user signup, signin, and signout. Authentication uses JWT tokens issued by Better Auth (frontend) and validated by FastAPI (backend).

---

## Authentication Flow

```
┌─────────────┐                ┌─────────────┐                ┌─────────────┐
│   Frontend  │                │  Better     │                │   FastAPI   │
│  (Next.js)  │                │   Auth      │                │   Backend   │
└─────────────┘                └─────────────┘                └─────────────┘
       │                              │                              │
       │ 1. POST /api/auth/signup     │                              │
       ├─────────────────────────────>│                              │
       │                              │ 2. Hash password             │
       │                              │ 3. Store in DB               │
       │                              │ 4. Generate JWT              │
       │<─────────────────────────────┤                              │
       │ 5. JWT token in cookie       │                              │
       │                              │                              │
       │ 6. GET /api/{user_id}/tasks  │                              │
       │    (with JWT in header)      │                              │
       ├──────────────────────────────────────────────────────────>│
       │                              │                              │ 7. Verify JWT
       │                              │                              │ 8. Extract user_id
       │                              │                              │ 9. Query DB
       │<──────────────────────────────────────────────────────────┤
       │ 10. Tasks data               │                              │
```

---

## Endpoint: POST /api/auth/signup

**Purpose**: Create a new user account

### Request

**Method**: `POST`
**URL**: `/api/auth/signup`
**Content-Type**: `application/json`
**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | Yes | Valid email format, max 255 chars | User's email address |
| `password` | string | Yes | Min 8 chars, must contain uppercase, lowercase, digit | User's password (will be hashed) |

### Response

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2026-02-17T10:30:00Z",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique user identifier |
| `email` | string | User's email address |
| `created_at` | string (ISO 8601) | Account creation timestamp |
| `token` | string | JWT token for authentication |

**Error Responses**:

**400 Bad Request** - Invalid input:
```json
{
  "detail": "Invalid email format"
}
```

**409 Conflict** - Email already exists:
```json
{
  "detail": "Email already registered"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must be at least 8 characters",
      "type": "value_error"
    }
  ]
}
```

### Validation Rules

**Email**:
- Must be valid email format
- Must be unique (not already registered)
- Converted to lowercase
- Max length: 255 characters

**Password**:
- Min length: 8 characters
- Must contain at least one uppercase letter
- Must contain at least one lowercase letter
- Must contain at least one digit
- Max length: 128 characters (before hashing)

### Security Notes

- Password is hashed with bcrypt (cost factor 12) before storage
- JWT token is signed with shared secret (BETTER_AUTH_SECRET)
- Token expires after 7 days
- Token includes user_id in payload

---

## Endpoint: POST /api/auth/signin

**Purpose**: Authenticate existing user and issue JWT token

### Request

**Method**: `POST`
**URL**: `/api/auth/signin`
**Content-Type**: `application/json`
**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Request Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User's email address |
| `password` | string | Yes | User's password |

### Response

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | User identifier |
| `email` | string | User's email address |
| `token` | string | JWT token for authentication |

**Error Responses**:

**401 Unauthorized** - Invalid credentials:
```json
{
  "detail": "Invalid email or password"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Security Notes

- Password is verified against bcrypt hash
- Failed login attempts are logged (for security monitoring)
- Generic error message prevents user enumeration
- JWT token is signed with shared secret

---

## Endpoint: POST /api/auth/signout

**Purpose**: Invalidate user session (client-side token removal)

### Request

**Method**: `POST`
**URL**: `/api/auth/signout`
**Content-Type**: `application/json`
**Authentication**: Required (JWT token in Authorization header)

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**: None (empty)

### Response

**Success Response** (200 OK):
```json
{
  "message": "Successfully signed out"
}
```

**Error Responses**:

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Invalid authentication credentials"
}
```

### Security Notes

- JWT tokens are stateless (cannot be revoked server-side)
- Signout is primarily client-side (remove token from storage)
- Token will expire after 7 days regardless of signout
- For true revocation, would need token blacklist (out of scope for Phase II)

---

## JWT Token Structure

### Token Payload

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "exp": 1708776600,
  "iat": 1708171800
}
```

**Payload Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `sub` | string (UUID) | Subject (user ID) |
| `email` | string | User's email address |
| `exp` | integer | Expiration timestamp (Unix epoch) |
| `iat` | integer | Issued at timestamp (Unix epoch) |

### Token Validation (Backend)

**FastAPI Dependency**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Extract and validate JWT token, return user_id."""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

---

## Shared Secret Configuration

**Environment Variable**: `BETTER_AUTH_SECRET`

**Requirements**:
- Must be identical in frontend (Better Auth) and backend (FastAPI)
- Minimum 256 bits (32 characters)
- Use cryptographically secure random string
- Store in environment variables (never commit to Git)

**Example** (.env.example):
```
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long-random-string
```

**Generation** (Python):
```python
import secrets
secret = secrets.token_urlsafe(32)
print(secret)  # Use this value for BETTER_AUTH_SECRET
```

---

## CORS Configuration

**Backend CORS Settings**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**:
- Update `allow_origins` to include production frontend URL
- Consider more restrictive `allow_methods` and `allow_headers`

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message here"
}
```

Or for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

---

## Testing Scenarios

### Signup Tests

1. ✅ Valid signup with email and password
2. ✅ Signup with existing email (409 Conflict)
3. ✅ Signup with invalid email format (400 Bad Request)
4. ✅ Signup with weak password (422 Unprocessable Entity)
5. ✅ Signup with missing fields (422 Unprocessable Entity)

### Signin Tests

1. ✅ Valid signin with correct credentials
2. ✅ Signin with incorrect password (401 Unauthorized)
3. ✅ Signin with non-existent email (401 Unauthorized)
4. ✅ Signin with missing fields (422 Unprocessable Entity)

### Signout Tests

1. ✅ Valid signout with valid token
2. ✅ Signout with invalid token (401 Unauthorized)
3. ✅ Signout with missing token (401 Unauthorized)

### JWT Validation Tests

1. ✅ Valid token is accepted
2. ✅ Expired token is rejected (401 Unauthorized)
3. ✅ Tampered token is rejected (401 Unauthorized)
4. ✅ Token with wrong signature is rejected (401 Unauthorized)

---

## Summary

The authentication API provides three endpoints for user account management:
- **POST /api/auth/signup**: Create new account
- **POST /api/auth/signin**: Authenticate and get JWT token
- **POST /api/auth/signout**: Sign out (client-side token removal)

All protected endpoints (task management) require JWT token in Authorization header. The backend validates tokens on every request and extracts user_id for user isolation.
