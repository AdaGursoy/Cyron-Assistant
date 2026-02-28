"""Backend configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()

# Minimum cosine similarity for knowledge retrieval (low_confidence if below this).
# Tune lower to capture short semantic matches (e.g. 0.57 for "support hours" style queries).
MIN_SIMILARITY_THRESHOLD: float = 0.57


class BackendConfig:
    """Backend configuration loaded from environment variables."""

    def __init__(self) -> None:
        """Initialize configuration from environment variables."""
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_ticket_assistant",
        )
        self.redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


# Global config instance
config = BackendConfig()

