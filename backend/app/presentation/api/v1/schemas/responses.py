from pydantic import BaseModel, field_serializer
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID
from enum import StrEnum
from typing import List, Optional

class SubscriptionEnum(StrEnum):
	free = "free"
	premium = "premium"

class UserBase(BaseModel):
	email: str
	username: str

class PostBase(BaseModel):
	title: str
	content: str
	author_id: str

class UserCreateRequest(UserBase):
	password: str

class UserResponse(UserBase):
	id: str
	firstname: str | None = None
	lastname: str | None = None
	birthday: datetime | None = None
	created_at: datetime
	timezone: str
	subscription_type: SubscriptionEnum = SubscriptionEnum.free
	subscription_expired_at: datetime | None = None
	is_banned: bool
	is_admin: bool
	avatar: str | None = None

	@field_serializer("created_at", "subscription_expired_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()

		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["created_at"] = datetime.fromisoformat(data["created_at"]).astimezone(tz).isoformat()
		if data["birthday"]:
			data["birthday"] = datetime.fromisoformat(data["birthday"]).astimezone(tz).isoformat()
		if data["subscription_expired_at"]:
			data["subscription_expired_at"] = datetime.fromisoformat(data["subscription_expired_at"]).astimezone(tz).isoformat()

		return data

class UserResponseWithFriends(UserResponse):
	friends: List[UserResponse]


class AddFriendRequest(BaseModel):
	user_id: int
	friend_id: int

class PostImageResponse(BaseModel):
	id: str
	post_id: str
	image_url: str
	created_at: datetime
	latitude: Optional[float] = None
	longitude: Optional[float] = None

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
	
class CommentImage(BaseModel):
	id: str
	comment_id: str
	image_url: str
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

class PostComment(BaseModel):
	id: str
	user_id: str
	post_id: str
	content: Optional[str] = None

	updated_at: datetime
	created_at: datetime

	images: Optional[List[CommentImage]] = []
	# author: UserResponse

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


class PostResponse(PostBase):
	id: str
	updated_at: datetime
	created_at: datetime

	author: UserResponse
	images: List[PostImageResponse] = []

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

class DetailPostResponse(PostResponse):
	comments: List[PostComment] = []