from datetime import timedelta
from src.core.security import generate_random_code
import redis.asyncio as redis
from src.redis_client.redis import pool

class RedisService:
    def __init__(self) -> None:
        self.session = redis.Redis(connection_pool=pool)

    async def create_reset_code(self, email: str, ttl: int) -> str:
        code = generate_random_code()
        key = f"reset_code:{email}"
        await self.session.setex(key, timedelta(seconds=ttl), code)
        return code

    async def get_reset_code(self, email: str) -> str:
        key = f"reset_code:{email}"
        return await self.session.get(key)

    async def delete_reset_code(self, email: str):
        key = f"reset_code:{email}"
        await self.session.delete(key)

    async def create_email_confirmation_code(self, email: str, ttl: int) -> str:
        code = generate_random_code()
        key = f"confirm_code:{email}"
        await self.session.setex(key, timedelta(seconds=ttl), code)
        return code

    async def get_email_confirmation_code(self, email: str) -> str:
        key = f"confirm_code:{email}"
        return await self.session.get(key)

    async def delete_email_confirmation_code(self, email: str):
        key = f"confirm_code:{email}"
        await self.session.delete(key)

redis_service = RedisService()