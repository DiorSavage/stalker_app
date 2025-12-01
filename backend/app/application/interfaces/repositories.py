from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.entities.post import Post, PostComment
from domain.entities.token import Token

class UserRepository(ABC):
	@abstractmethod
	async def register_user(self, user: User) -> User:
		...

	@abstractmethod
	async def get_user_by_id(self, user_id: int) -> User | None:
		...

	@abstractmethod
	async def get_user_by_username_or_email(self, username: str, email: str) -> User | None:
		...

	@abstractmethod
	async def get_users_by_id(self, user_ids: list[str]) -> list[User]:
		...
	
class PostRepository(ABC):

	@abstractmethod
	async def create_post(self, post: Post) -> Post:
		...

	@abstractmethod
	async def get_post_by_id(self, post_id: str) -> Post:
		...

class CommentRepository(ABC):

	@abstractmethod
	async def create_comment(self, commentData: PostComment) -> PostComment:
		...

class TokenRepository(ABC):

	@abstractmethod
	async def get_by_user_id(self, user_id: str) -> Optional[Token]:
		...

	@abstractmethod
	async def save(self, token: Token) -> None:
		...

	@abstractmethod
	async def delete_by_token(self, token: str) -> None:
		...