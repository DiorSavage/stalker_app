from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from typing import final

from domain.entities.base import BaseEntity
from domain.values.ban_status import BanStatus
from domain.entities.user import User
from domain.exceptions import SameAdminAndUserInBanList, EntityValueTypeError

@final
@dataclass(
	frozen=True,
	kw_only=True
)
class BanList(BaseEntity):
	user_id: int
	admin_id: int
	updated_at: Optional[datetime] = None
	reason: Optional[str] = None
	ban_status: BanStatus

	admin: User
	user: User

	def validate(self) -> bool:
		if self.admin_id == self.user_id:
			raise SameAdminAndUserInBanList(user_id=self.user_id, admin_id=self.admin_id)
		if not isinstance(self.ban_status, BanStatus):
			raise EntityValueTypeError("ban_status", type(self.ban_status), BanStatus)
		
		return True
	
	def __post_init__(self):
		self.validate()