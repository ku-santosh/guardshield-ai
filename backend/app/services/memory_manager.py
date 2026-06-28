import redis.asyncio as aioredis
from typing import Dict, Any, Optional
from mem0 import Memory
from backend.app.core.config import settings
from backend.app.core.logging import system_logger

class CognitiveMemoryManager:
    """
    Manages dual-layer memory infrastructure:
    1. Short-term caching/session data via Redis.
    2. Long-term contextual memory via Mem0.
    """
    def __init__(self):
        self.redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        # Initialize Mem0 with a vector-store configuration fallback
        self.mem0_config = {
            "vector_store": {
                "provider": "chroma",
                "config": {"collection_name": "compliance_memory", "path": "/tmp/chroma"}
            }
        }
        self.long_term_memory = Memory.from_config(self.mem0_config)

    async def get_session_context(self, session_id: str) -> Optional[str]:
        """Fetches short-term transactional caching snapshots from Redis."""
        try:
            return await self.redis_client.get(f"session:{session_id}")
        except Exception as e:
            system_logger.error(f"Redis lookup error: {str(e)}")
            return None

    async def save_session_context(self, session_id: str, context_blob: str, ttl_seconds: int = 3600) -> None:
        """Stores short-term transactional state snapshots in Redis."""
        try:
            await self.redis_client.setex(f"session:{session_id}", ttl_seconds, context_blob)
        except Exception as e:
            system_logger.error(f"Redis write error: {str(e)}")

    def add_long_term_violation_pattern(self, entity_id: str, pattern_summary: str) -> None:
        """Persists high-level behavioral risk patterns in Mem0."""
        try:
            self.long_term_memory.add(
                f"Entity exhibiting risk patterns: {pattern_summary}",
                user_id=entity_id,
                metadata={"category": "compliance_breach", "year": "2026"}
            )
        except Exception as e:
            system_logger.error(f"Mem0 persistence error: {str(e)}")

    def query_long_term_history(self, entity_id: str, query: str) -> str:
        """Queries historical behavioral trends from Mem0."""
        try:
            memories = self.long_term_memory.search(query, user_id=entity_id)
            return " ".join([m["text"] for m in memories]) if memories else ""
        except Exception as e:
            system_logger.error(f"Mem0 search error: {str(e)}")
            return ""