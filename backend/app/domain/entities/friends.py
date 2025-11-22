from dataclasses import dataclass
from datetime import datetime
from typing import final

from domain.entities.base import BaseEntity
@final
@dataclass(
	frozen=True,
	kw_only=True
)
class FriendsList(BaseEntity):
	user_id: int
	friend_id: int

@final
@dataclass(
	frozen=True,
	kw_only=True
)
class FriendsRequests(BaseEntity):
	user_id: int
	from_user_id: int