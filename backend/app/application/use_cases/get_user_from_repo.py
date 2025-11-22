from typing import final
from dataclasses import dataclass

from application.interfaces.mappers import DtoUserEntityMapper

from application.interfaces.repositories import UserRepository

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class GetUserFromRepo:
	
	user_repo = UserRepository
	mapper = DtoUserEntityMapper

	async def get_user_by_id(self, user_id: int):
		...