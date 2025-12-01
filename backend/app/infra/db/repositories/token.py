from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, Result
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional

from application.interfaces.repositories import TokenRepository
from infra.db.mappers.token import TokenDBMapper
from domain.entities.token import Token
from infra.db.models.models import Token as TokenORM

@final
@dataclass
class MySQLTokenRepository(TokenRepository):

	mapper: TokenDBMapper
	session: AsyncSession

	async def save(self, token: Token) -> None:
		orm_obj = self.mapper.to_orm(token)
		self.session.add(orm_obj)
		await self.session.commit()

	async def get_by_user_id(self, user_id: str) -> Optional[Token]:
		stmt = select(TokenORM).where(TokenORM.user_id == str(user_id))
		result = await self.session.execute(stmt)
		orm_obj = result.scalar_one_or_none()
		return self.mapper.to_entity(orm_obj) if orm_obj else None

	async def delete_by_token(self, token_str: str) -> None:
		stmt = select(TokenORM).where(TokenORM.token == token_str)
		result = await self.session.execute(stmt)
		orm_obj = result.scalar_one_or_none()
		if orm_obj:
			await self.session.delete(orm_obj)
			await self.session.commit()