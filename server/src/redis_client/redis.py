import redis.asyncio as redis
from src.core.config import settings
from fastapi import Depends
from src.core.config import settings
from datetime import timedelta
from src.core.security import generate_random_code

def create_redis():
  return redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
  )

pool = create_redis()
