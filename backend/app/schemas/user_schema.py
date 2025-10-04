from pydantic import BaseModel, field_serializer
from datetime import datetime
from zoneinfo import ZoneInfo
from enum import StrEnum

class SubscriptionEnum(StrEnum):
	free = "free"
	premium = "premium"

class UserBase(BaseModel):
	email: str
	username: str

class UserCreateRequest(UserBase):
	password: str

class UserResponse(UserBase):
	id: int
	firstname: str | None = None
	lastname: str | None = None
	birthday: datetime | None = None
	registered_at: datetime
	timezone: str
	subscription_type: SubscriptionEnum = SubscriptionEnum.free
	subscription_expired_at: datetime | None = None

	@field_serializer("registered_at", "subscription_expired_at", "registered_at")
	def parse_datetime(self, value):
		if not isinstance(value, str) and value is not None:
			return value.isoformat()
		
		return value

	def model_dump(self, timezone: str = "Europe/Moscow", **kwargs):
		data = super().model_dump(**kwargs)
		tz = ZoneInfo(timezone)
		data["registered_at"] = datetime.fromisoformat(data["registered_at"]).astimezone(tz).isoformat()
		if data["birthday"]:
			data["birthday"] = datetime.fromisoformat(data["birthday"]).astimezone(tz).isoformat()
		if data["subscription_expired_at"]:
			data["subscription_expired_at"] = datetime.fromisoformat(data["subscription_expired_at"]).astimezone(tz).isoformat()

		return data
	
	# @field_validator("subscription_type")
	# def validate_subscription_type(self, value):
	# 	if isinstance(value, str):
	# 		return SubscriptionEnum(value=value)
	# 	return value