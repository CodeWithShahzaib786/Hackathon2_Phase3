"""Unit tests for password hashing and JWT token utilities."""

import pytest
from datetime import datetime, timedelta
from src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    get_user_id_from_token,
)


class TestPasswordHashing:
    """Test suite for password hashing utilities."""

    def test_hash_password(self):
        """Test that password is hashed correctly."""
        password = "SecurePass123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60  # bcrypt hash length

    def test_verify_correct_password(self):
        """Test that correct password verification succeeds."""
        password = "SecurePass123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test that incorrect password verification fails."""
        password = "SecurePass123"
        wrong_password = "WrongPass456"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "SecurePass123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test suite for JWT token utilities."""

    def test_create_access_token(self):
        """Test that JWT token is created correctly."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token({"sub": user_id})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_valid_token(self):
        """Test that valid token is verified correctly."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token({"sub": user_id})

        payload = verify_token(token)

        assert payload is not None
        assert payload["sub"] == user_id
        assert "exp" in payload
        assert "iat" in payload

    def test_verify_invalid_token(self):
        """Test that invalid token verification fails."""
        invalid_token = "invalid.token.here"

        payload = verify_token(invalid_token)

        assert payload is None

    def test_verify_expired_token(self):
        """Test that expired token verification fails."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        # Create token that expires immediately
        token = create_access_token(
            {"sub": user_id},
            expires_delta=timedelta(seconds=-1)
        )

        payload = verify_token(token)

        assert payload is None

    def test_get_user_id_from_valid_token(self):
        """Test extracting user ID from valid token."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token({"sub": user_id})

        extracted_id = get_user_id_from_token(token)

        assert extracted_id == user_id

    def test_get_user_id_from_invalid_token(self):
        """Test extracting user ID from invalid token returns None."""
        invalid_token = "invalid.token.here"

        extracted_id = get_user_id_from_token(invalid_token)

        assert extracted_id is None

    def test_token_contains_expiration(self):
        """Test that token contains expiration claim."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token({"sub": user_id})

        payload = verify_token(token)

        assert "exp" in payload
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)

        # Token should expire in approximately 7 days
        now = datetime.utcnow()
        delta = exp_datetime - now
        assert 6 < delta.days <= 7

    def test_token_contains_issued_at(self):
        """Test that token contains issued at claim."""
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        token = create_access_token({"sub": user_id})

        payload = verify_token(token)

        assert "iat" in payload
        iat_timestamp = payload["iat"]
        iat_datetime = datetime.fromtimestamp(iat_timestamp)

        # Issued at should be approximately now
        now = datetime.utcnow()
        delta = abs((now - iat_datetime).total_seconds())
        assert delta < 5  # Within 5 seconds
