"""API dependencies for authentication and database sessions."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_user_id_from_token

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Extract and validate JWT token, return user_id.

    Args:
        credentials: HTTP Bearer token credentials from request header.

    Returns:
        The authenticated user's ID (UUID as string).

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or missing.
    """
    token = credentials.credentials
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


# Type aliases for dependency injection
CurrentUser = Annotated[str, Depends(get_current_user)]
DBSession = Annotated[AsyncSession, Depends(get_session)]
