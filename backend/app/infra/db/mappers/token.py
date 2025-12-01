from dataclasses import dataclass
from typing import final
from datetime import datetime

from application.interfaces.mappers import DtoTokenEntityMapper
from domain.entities.token import Token
from infra.db.models.models import Token as TokenORM


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class TokenDtoEntityMapper(DtoTokenEntityMapper):

	def to_entity(self, user_id: str, expire_at: datetime, token: str):
		return Token(
			user_id=user_id,
			token=token,
			expire_at=expire_at,
		)

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class TokenDBMapper:

	def to_entity(self, orm_obj: TokenORM) -> Token:
		return Token(
			user_id=orm_obj.user_id,
			token=orm_obj.token,
			created_at=orm_obj.created_at,
			updated_at=orm_obj.updated_at,
			expire_at=orm_obj.expire_at,
		)

	def to_orm(self, entity: Token) -> TokenORM:
		return TokenORM(
			user_id=str(entity.user_id),
			token=entity.token,
			created_at=entity.created_at,
			updated_at=entity.updated_at,
			expire_at=entity.expire_at,
		)