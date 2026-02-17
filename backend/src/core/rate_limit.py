"""Rate limiting middleware for chat API endpoints."""

from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict


# In-memory rate limit store: {user_id: [(timestamp, count)]}
rate_limit_store: Dict[str, list] = defaultdict(list)


def check_rate_limit(user_id: str, max_requests: int = 20, window_seconds: int = 60) -> None:
    """Check if user has exceeded rate limit.

    Args:
        user_id: User identifier
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Raises:
        HTTPException: If rate limit exceeded
    """
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=window_seconds)

    # Get user's request history
    requests = rate_limit_store[user_id]

    # Remove old requests outside the window
    requests = [req_time for req_time in requests if req_time > window_start]
    rate_limit_store[user_id] = requests

    # Check if limit exceeded
    if len(requests) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
        )

    # Add current request
    requests.append(now)
