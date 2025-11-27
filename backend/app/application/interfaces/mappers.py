from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import final

from domain.entities.user import User
from domain.entities.post import Post, PostComment, CommentImage

from application.dtos.user import UserDTO
from application.dtos.post import PostDTO, PostCommentDTO, CommentImageDTO

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


@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoPostEntityMapper(ABC):
	user_mapper: DtoUserEntityMapper

	@abstractmethod
	def to_dto(self, post_entity: Post, author_entity: User) -> PostDTO:
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