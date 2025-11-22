from dataclasses import dataclass
from typing import final, Optional
from datetime import datetime
from uuid import UUID

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class UserDTO:
	id: Optional[UUID] = None
	email: str
	username: str
	firstname: Optional[str] = None
	lastname: Optional[str] = None
	birthday: Optional[datetime] = None
	timezone: str  = "Europe/Moscow"
	subscription_type: str = "free"
	subscription_expired_at: Optional[datetime] = None
	is_banned: bool = False
	is_admin: bool = False
	avatar: Optional[str] = None
	created_at: Optional[datetime] = None
	password: str