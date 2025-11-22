from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user import User

class UserRepository(ABC):
	@abstractmethod
	async def register_user(self, user: User) -> User:
		...

	# @abstractmethod
	# async def get_user_by_id(self, user_id: int) -> User | None:
	# 	...

	@abstractmethod
	async def get_user_by_username_or_email(self, username: str, email: str) -> User | None:
		...