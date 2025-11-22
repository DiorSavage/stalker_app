from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from typing import final

from domain.entities.base import BaseEntity
from domain.entities.user import User
from domain.exceptions import EmptyContentAndImagesComment, EmptyContentAndImagesPost


@final
@dataclass(
	frozen=True,
	kw_only=True
)
class PostImage(BaseEntity):
	post_id: int
	image_url: str #! по идее тоже валидировать надо
	latitude: Optional[float] = None
	longitude: Optional[float] = None


@final
@dataclass(
	frozen=True,
	kw_only=True
)
class Post(BaseEntity):
	user_id: int
	title: str
	content: Optional[str] = None
	updated_at: datetime = None

	author: User
	images: Optional[list[PostImage]] = None

	def validate(self) -> bool:
		if len(self.images) == 0 and not self.content:
			raise EmptyContentAndImagesPost()
		
		return True

	def __post_init__(self):
		self.validate()

@final
@dataclass(
	frozen=True,
	kw_only=True
)
class CommentImage(BaseEntity):
	comment_id: int
	image_url: str


@final
@dataclass(
	frozen=True,
	kw_only=True
)
class PostComment(BaseEntity):
	user_id: int
	post_id: int
	content: Optional[str] = None
	updated_at: datetime = None
	images: Optional[list[CommentImage]] = None

	def validate(self) -> bool:
		if len(self.images) == 0 and not self.content:
			raise EmptyContentAndImagesComment()
		
		return True
	
	def __post_init__(self):
		self.validate()