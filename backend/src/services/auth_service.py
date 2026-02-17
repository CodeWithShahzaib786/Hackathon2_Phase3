"""Authentication service for user signup, signin, and verification."""

from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User
from src.models import UserCreate, UserLogin, TokenResponse
from src.core.security import verify_password, get_password_hash, create_access_token
from fastapi import HTTPException, status


class AuthService:
    """Service layer for authentication operations.

    Handles user signup, signin, and token generation.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the authentication service.

        Args:
            session: The database session for queries.
        """
        self.session = session

    async def signup(self, user_data: UserCreate) -> TokenResponse:
        """Create a new user account.

        Args:
            user_data: The user signup data (email and password).

        Returns:
            TokenResponse with user info and JWT token.

        Raises:
            HTTPException: 409 if email already exists.
        """
        # Check if email already exists
        existing_user = await self._get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        new_user = User(
            email=user_data.email.lower(),
            hashed_password=hashed_password,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        # Generate JWT token
        token = create_access_token({"sub": str(new_user.id), "email": new_user.email})

        return TokenResponse(
            id=new_user.id,
            email=new_user.email,
            token=token,
        )

    async def signin(self, credentials: UserLogin) -> TokenResponse:
        """Authenticate a user and generate JWT token.

        Args:
            credentials: The user login credentials (email and password).

        Returns:
            TokenResponse with user info and JWT token.

        Raises:
            HTTPException: 401 if credentials are invalid.
        """
        # Get user by email
        user = await self._get_user_by_email(credentials.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Generate JWT token
        token = create_access_token({"sub": str(user.id), "email": user.email})

        return TokenResponse(
            id=user.id,
            email=user.email,
            token=token,
        )

    async def verify_user(self, user_id: UUID) -> Optional[User]:
        """Verify that a user exists.

        Args:
            user_id: The user's UUID.

        Returns:
            The User object if found, None otherwise.
        """
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address.

        Args:
            email: The user's email address.

        Returns:
            The User object if found, None otherwise.
        """
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()
