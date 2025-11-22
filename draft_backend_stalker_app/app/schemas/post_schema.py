from pydantic import BaseModel, field_serializer
from datetime import datetime
from fastapi import UploadFile
from zoneinfo import ZoneInfo
from enum import StrEnum
from typing import List, Optional

class CommentImageBase(BaseModel):
	comment_id: int
	image_url: str

class CommentImage(CommentImageBase):
	id: int
	created_at: datetime

	@field_serializer("created_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()

		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["created_at"] = datetime.fromisoformat(data["created_at"]).astimezone(tz).isoformat()

		return data

class PostCommentBase(BaseModel):
	post_id: int
	user_id: int

class PostCommentCreateRequest(PostCommentBase):
	content: Optional[str] = None

class PostComment(PostCommentBase):
	id: int
	created_at: datetime
	updated_at: datetime
	content: Optional[str] = None

	images: List[CommentImage] | None = None

	@field_serializer("created_at", "updated_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()

		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["created_at"] = datetime.fromisoformat(data["created_at"]).astimezone(tz).isoformat()
		data["updated_at"] = datetime.fromisoformat(data["updated_at"]).astimezone().isoformat()
		return data

class PostImageBase(BaseModel):
	post_id: int
	image_url: str

class PostImage(PostImageBase):
	id: int
	latitude: float | None = None
	longitude: float | None = None
	created_at: datetime

	@field_serializer("created_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()

		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["created_at"] = datetime.fromisoformat(data["created_at"]).astimezone(tz).isoformat()

		return data

class PostBase(BaseModel):
	content: str | None = None
	title: str

class PostCreateRequest(PostBase):
	user_id: int

class PostResponse(PostBase):
	id: int
	created_at: datetime
	updated_at: datetime

	images: List[PostImage] | None = None
	comments: List[PostComment] | None = None

	@field_serializer("created_at", "updated_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()

		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["created_at"] = datetime.fromisoformat(data["created_at"]).astimezone(tz).isoformat()
		data["updated_at"] = datetime.fromisoformat(data["updated_at"]).astimezone(tz).isoformat()

		return data