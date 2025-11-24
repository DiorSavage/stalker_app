from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import final

from domain.entities.user import User
from domain.entities.post import Post

from application.dtos.user import UserDTO
from application.dtos.post import PostDTO


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoUserEntityMapper(ABC):

	@abstractmethod	
	def to_dto(self, entity: User) -> UserDTO:
		...

	@abstractmethod
	def to_entity(self, dto: UserDTO) -> User:
		...


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoPostEntityMapper(ABC):

	@abstractmethod
	def to_dto(self, post_entity: Post, author_entity: User) -> PostDTO:
		...

	@abstractmethod
	def to_entity(self, dto: PostDTO) -> Post:
		...