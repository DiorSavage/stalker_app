from dataclasses import dataclass
from typing import final
from datetime import datetime, timedelta

from application.dtos.user import UserDTO
from application.interfaces.mappers import DtoUserEntityMapper, DtoTokenEntityMapper
from application.interfaces.repositories import UserRepository, TokenRepository

from application.exceptions import UserAlreadyExists
from domain.services.password import PasswordService
from application.services.jwt_service import JWTService

@final
@dataclass(
	frozen=True,
	slots=True,
	kw_only=True
)
class SaveUser:

	user_mapper: DtoUserEntityMapper
	token_mapper: DtoTokenEntityMapper
	user_repo: UserRepository
	token_repo: TokenRepository
	password_service: PasswordService
	jwt_service: JWTService

	async def __call__(self, user_dto: UserDTO) -> tuple[UserDTO, str, int] | None:
		user_entity = self.user_mapper.to_entity(user_dto)
		existing_user = await self.user_repo.get_user_by_username_or_email(username=user_entity.username, email=user_entity.email)
		if existing_user:
			raise UserAlreadyExists(email=user_entity.email)
		
		result = await self.user_repo.register_user(user=user_entity)

		if result:
			result_dto = self.user_mapper.to_dto(result)
			jwt_payload = self.user_mapper.to_jwt_dict(
				dto=result_dto
			)
			token = self.jwt_service.encode_jwt(
				payload=jwt_payload
			)
			expire_at = datetime.now() + timedelta(seconds=self.jwt_service.expire_token)
			token_entity = self.token_mapper.to_entity(
				expire_at=expire_at,
				token=token,
				user_id=result_dto.id
			)
			await self.token_repo.save(
				token=token_entity
			)

			return result_dto, token, expire_at.timestamp()
		return None
	