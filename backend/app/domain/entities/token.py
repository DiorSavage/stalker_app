from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional
from typing import final

from domain.entities.base import BaseEntity
from domain.entities.user import User

@final
@dataclass(
	frozen=True,
	kw_only=True
)
class Token(BaseEntity):
	user_id: int
	token: str
	updated_at: Optional[datetime] = None
	expire_at: datetime = None
	user: User