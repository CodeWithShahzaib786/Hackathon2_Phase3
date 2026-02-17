"""Chat API endpoints for Phase III AI-powered chatbot."""

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
import html

from backend.src.models.chat import ChatRequest, ChatResponse
from backend.src.models.user import User
from backend.src.services.chat_service import ChatService
from backend.src.core.security import get_current_user
from backend.src.core.rate_limit import check_rate_limit


router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service() -> ChatService:
    """Dependency to get ChatService instance.

    Returns:
        ChatService instance
    """
    return ChatService()


@router.post("", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    """Send a chat message and receive AI response.

    Args:
        request: Chat request with message and optional session_id
        current_user: Authenticated user from JWT token
        chat_service: ChatService instance

    Returns:
        ChatResponse with AI's reply

    Raises:
        HTTPException: If request is invalid or processing fails
    """
    try:
        # Check rate limit (20 requests per minute per user)
        check_rate_limit(str(current_user.id), max_requests=20, window_seconds=60)

        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )

        if len(request.message) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message too long (max 1000 characters)"
            )

        # Sanitize HTML to prevent XSS
        request.message = html.escape(request.message)

        # Process message with user_id from JWT token (not from request)
        response = await chat_service.process_message(
            user_id=current_user.id,
            request=request
        )
        return response

    except HTTPException:
        # Re-raise HTTP exceptions (rate limit, validation errors)
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
) -> None:
    """Clear a chat session and its conversation history.

    Args:
        session_id: Session ID to clear
        current_user: Authenticated user from JWT token
        chat_service: ChatService instance

    Raises:
        HTTPException: If session not found or belongs to different user
    """
    try:
        success = chat_service.clear_session(session_id, current_user.id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear session: {str(e)}"
        )
