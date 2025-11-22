from dataclasses import dataclass
from typing import final

from application.dtos.user import UserDTO
from presentation.api.v1.schemas.responses import UserResponse
from presentation.api.v1.schemas.requests import UserCreateSchema

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class UserResponseMapper:

	def to_response(self, dto: UserDTO) -> UserResponse:
		return UserResponse(
			avatar=dto.avatar,
			birthday=dto.birthday,
			email=dto.email,
			firstname=dto.firstname,
			id=dto.id,
			is_admin=dto.is_admin,
			is_banned=dto.is_banned,
			lastname=dto.lastname,
			created_at=dto.created_at,
			subscription_expired_at=dto.subscription_expired_at,
			subscription_type=dto.subscription_type,
			timezone=dto.timezone,
			username=dto.username
		)
	
	def to_dto(self, schema: UserCreateSchema):
		return UserDTO(
			email=schema.email,
			firstname=schema.firstname,
			lastname=schema.lastname,
			password=schema.password,
			username=schema.username,
			birthday=schema.birthday
		)