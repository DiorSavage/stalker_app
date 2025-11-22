from dataclasses import dataclass
from datetime import datetime
from typing import final
from typing import Optional

from domain.entities.base import BaseEntity
from domain.values.email import Email
from domain.values.username import Username
from domain.values.subscription import SubscriptionType
from domain.values.password import Password
from domain.exceptions import EntityValueTypeError
from domain.services.password import PasswordService

@final
@dataclass(
	frozen=True,
	kw_only=True
)
class User(BaseEntity):
	email: Email
	username: Username
	password: Password
	firstname: Optional[str] = None
	lastname: Optional[str] = None
	birthday: Optional[datetime] = None
	timezone: str = "Europe/Moscow"
	subscription_type: SubscriptionType = "free"
	subscription_expired_at: Optional[datetime] = None
	is_banned: bool = False
	is_admin: bool = False
	avatar: Optional[str] = "default-user.png"

	def validate(self):
		if not isinstance(self.email, Email):
			raise EntityValueTypeError("email", type(self.email), Email)
		if not isinstance(self.username, Username):
			raise EntityValueTypeError("username", type(self.username), Username)
		if not isinstance(self.subscription_type, SubscriptionType):
			raise EntityValueTypeError("subscription_type", type(self.subscription_type), SubscriptionType)
	
	@classmethod
	def create(cls, email: str, username: str, password: str, password_service: PasswordService):
		email_obj = Email(value=email)
		username = Username(value=username)
		hashed_password = password_service.generate_password(password=password)
		return cls(email=email_obj, username=username, password=hashed_password)

	def __post_init__(self):
		self.validate()