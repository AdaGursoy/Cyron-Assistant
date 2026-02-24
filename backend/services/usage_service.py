"""Usage logging service."""

from datetime import datetime

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.usage_log import UsageLog
from backend.services.limit_service import _redis_key_monthly_tokens


async def log_usage(
    session: AsyncSession,
    redis: Redis,
    guild_id: int,
    tokens_used: int,
    request_type: str = "relay",
) -> None:
    """Persist usage log and synchronize monthly token counter."""
    log = UsageLog(
        guild_id=guild_id,
        tokens_used=tokens_used,
        request_type=request_type,
        timestamp=datetime.utcnow(),
    )
    session.add(log)
    await session.flush()

    # Phase 2 uses placeholder reply, so tokens_used may be 0.
    # We still keep Redis and DB in sync for Phase 3 readiness.
    key = _redis_key_monthly_tokens(guild_id)
    if tokens_used > 0:
        await redis.incrby(key, tokens_used)
