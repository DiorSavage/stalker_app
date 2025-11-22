from dataclasses import dataclass
from typing import final

from domain.entities.user import User as UserEntity
from domain.values.email import Email
from domain.values.username import Username
from domain.values.password import Password
from domain.values.subscription import SubscriptionType
from application.dtos.user import UserDTO
from infra.db.models.models import User as UserORM
from application.interfaces.mappers import DtoUserEntityMapper


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class UserDBMapper:
	
	def to_entity(self, model: UserORM):
		email_vo = Email(value=model.email)
		username_vo = Username(value=model.username)
		password_vo = Password(value=model.password)
		subscription_type_vo = SubscriptionType(value=model.subscription_type)
		return UserEntity(
			avatar=model.avatar,
			birthday=model.birthday,
			created_at=model.created_at,
			email=email_vo,
			password=password_vo,
			firstname=model.firstname,
			id=model.id,
			is_admin=model.is_admin,
			is_banned=model.is_banned,
			lastname=model.lastname,
			subscription_expired_at=model.subscription_expired_at,
			subscription_type=subscription_type_vo,
			timezone=model.timezone,
			username=username_vo
		)
	

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class UserDTOEntityMapper(DtoUserEntityMapper):
	
	def to_dto(self, entity: UserEntity) -> UserDTO:
		return UserDTO(
			id=entity.id,
			email=entity.email.value,
			username=entity.username.value,
			password=entity.password,
			firstname=entity.firstname,
			lastname=entity.lastname,
			birthday=entity.birthday,
			timezone=entity.timezone,
			subscription_type=entity.subscription_type.value,
			subscription_expired_at=entity.subscription_expired_at,
			is_banned=entity.is_banned,
			is_admin=entity.is_admin,
			avatar=entity.avatar,
			created_at=entity.created_at
		)

	def to_entity(self, dto: UserDTO) -> UserEntity:
		email_vo = Email(value=dto.email)
		username_vo = Username(value=dto.username)
		password_vo = Password(value=dto.password)
		subscription_type_vo = SubscriptionType(value=dto.subscription_type)
		return UserEntity(
			email=email_vo,
			username=username_vo,
			password=password_vo,
			firstname=dto.firstname,
			lastname=dto.lastname,
			birthday=dto.birthday,
			timezone=dto.timezone,
			subscription_type=subscription_type_vo,
			subscription_expired_at=dto.subscription_expired_at,
			is_banned=dto.is_banned,
			is_admin=dto.is_admin,
			avatar=dto.avatar,
			created_at=dto.created_at,
		)