from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import final
from datetime import datetime

from domain.entities.user import User
from domain.entities.post import Post, PostComment, CommentImage
from domain.entities.token import Token

from application.dtos.user import UserDTO
from application.dtos.post import PostDTO, PostCommentDTO, CommentImageDTO
from application.dtos.token import TokenDTO

# @dataclass(
# 	frozen=True,
# 	kw_only=True,
# 	slots=True
# )
# class DBPostMapper(ABC):
# 	def to_entity(self, model: PostORM):
# 		...
	
# 	def image_to_orm(self, post_image: PostImage, post_id: str) -> PostImageORM:
# 		...

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
	
	@abstractmethod
	def to_jwt_dict(self, dto: UserDTO) -> dict:
		...


@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoPostEntityMapper(ABC):
	user_mapper: DtoUserEntityMapper

	@abstractmethod
	def to_dto(self, post_entity: Post, author_entity: User, comments_authors: dict[str, User]) -> PostDTO:
		...

	@abstractmethod
	def to_entity(self, dto: PostDTO) -> Post:
		...


@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoCommentEntityMapper(ABC):

	@abstractmethod
	def to_dto(self, comment_entity: PostComment, author_entity: User) -> PostCommentDTO:
		...

	@abstractmethod
	def to_entity(self, dto: PostCommentDTO) -> PostComment:
		...

@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoTokenEntityMapper(ABC):

	# @abstractmethod
	# def to_dto(self, entity: Token) -> TokenDTO:
	# 	...

	@abstractmethod
	def to_entity(self, user_id: str, expire_at: datetime, token: str) -> Token:
		...