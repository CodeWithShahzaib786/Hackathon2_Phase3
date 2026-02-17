"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session, get_current_user
from src.models import UserCreate, UserLogin, TokenResponse, MessageResponse
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Create a new user account.

    Args:
        user_data: User signup data (email and password).
        session: Database session.

    Returns:
        TokenResponse with user info and JWT token.

    Raises:
        HTTPException: 409 if email already exists.
        HTTPException: 422 if validation fails.
    """
    auth_service = AuthService(session)
    return await auth_service.signup(user_data)


@router.post("/signin", response_model=TokenResponse)
async def signin(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Authenticate a user and generate JWT token.

    Args:
        credentials: User login credentials (email and password).
        session: Database session.

    Returns:
        TokenResponse with user info and JWT token.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    auth_service = AuthService(session)
    return await auth_service.signin(credentials)


@router.post("/signout", response_model=MessageResponse)
async def signout(
    current_user_id: str = Depends(get_current_user),
) -> MessageResponse:
    """Sign out the current user.

    Note: JWT tokens are stateless, so signout is primarily client-side.
    This endpoint validates the token and returns a success message.

    Args:
        current_user_id: The authenticated user's ID from JWT token.

    Returns:
        MessageResponse confirming successful signout.

    Raises:
        HTTPException: 401 if token is invalid.
    """
    return MessageResponse(message="Successfully signed out")
