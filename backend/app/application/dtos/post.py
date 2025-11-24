from dataclasses import dataclass
from typing import final, Optional, List
from datetime import datetime

from application.dtos.user import UserDTO


@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostImageDTO:
	id: Optional[str] = None
	post_id: Optional[str] = None
	image_url: str
	created_at: Optional[datetime] = None
	longitude: Optional[str] = None
	latitude: Optional[str] = None


@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostDTO:
	id: Optional[str] = None
	title: str
	content: str
	author_id: str
	updated_at: Optional[datetime] = None
	created_at: Optional[datetime] = None
	images: Optional[List[PostImageDTO]] = None
	author: Optional[UserDTO] = None