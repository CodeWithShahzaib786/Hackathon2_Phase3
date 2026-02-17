"""Application configuration and settings management."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database Configuration
    database_url: str = ""

    # JWT Configuration
    better_auth_secret: str = ""
    access_token_expire_days: int = 7

    # API Configuration
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_reload: bool = True

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Environment
    python_env: str = "development"

    # OpenAI Configuration (Phase III)
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.python_env.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.python_env.lower() == "production"

    def validate_required_settings(self) -> None:
        """Validate that required settings are configured.

        Raises:
            ValueError: If required settings are missing or invalid.
        """
        errors = []

        if not self.database_url:
            errors.append("DATABASE_URL is required")

        if not self.better_auth_secret:
            errors.append("BETTER_AUTH_SECRET is required")

        if len(self.better_auth_secret) < 32:
            errors.append("BETTER_AUTH_SECRET must be at least 32 characters")

        if errors:
            raise ValueError(
                "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings.

    Returns:
        The global settings instance.
    """
    return settings
