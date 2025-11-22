from dataclasses import dataclass
from typing import final

from application.dtos.user import UserDTO
from application.interfaces.mappers import DtoUserEntityMapper
from application.interfaces.repositories import UserRepository

from application.exceptions import UserAlreadyExists
from domain.services.password import PasswordService

@final
@dataclass(
	frozen=True,
	slots=True,
	kw_only=True
)
class SaveUser:

	mapper: DtoUserEntityMapper
	user_repo: UserRepository
	password_service: PasswordService

	async def __call__(self, user_dto: UserDTO) -> UserDTO | None:
		user_entity = self.mapper.to_entity(user_dto)
		existing_user = await self.user_repo.get_user_by_username_or_email(username=user_entity.username, email=user_entity.email)
		if existing_user:
			raise UserAlreadyExists(email=user_entity.email)
		
		result = await self.user_repo.register_user(user=user_entity)
		print(result)
		if result:
			result_dto = self.mapper.to_dto(result)

			return result_dto
		return None