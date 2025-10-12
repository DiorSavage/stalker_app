from abc import ABCMeta, ABC, abstractmethod
from typing import Optional, List
from redis.asyncio import Redis
from redis import asyncio as aioredis

from core.config import settings

async def get_redis_client():
	return await aioredis.Redis(
		host=settings.redis_settings.REDIS_HOST,
		port=settings.redis_settings.REDIS_PORT,
		protocol=settings.redis_settings.REDIS_PROTOCOL,
		decode_responses=settings.redis_settings.REDIS_DECODE_RESPONSES,
		db=settings.redis_settings.REDIS_DB,
	)

class IRedisService(ABC):
	@abstractmethod
	async def get(self, key: str) -> Optional[str]:
		pass
	
	@abstractmethod
	async def set(self, key: str, value: str, expire: int = 0) -> None:
		pass

	@abstractmethod
	async def delete(self, keys: List[str]):
		pass


class RedisService(IRedisService):
	def __init__(self, redis: Redis):
		self.redis_client: Redis = redis

	async def get(self, key):
		if self.redis_client:
			return await self.redis_client.get(key)

	async def set(self, key, value, expire: int = 0):
		if self.redis_client:
			args = [key, value, expire] if expire else [key, value]
			return await self.redis_client.set(*args)

	async def delete(self, keys: List[str]):
		if self.redis_client:
			return await self.redis_client.delete(*keys)