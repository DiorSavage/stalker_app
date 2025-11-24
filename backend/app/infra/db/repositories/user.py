from dataclasses import dataclass
from typing import final
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from application.interfaces.repositories import UserRepository
from domain.entities.user import User
from infra.db.models.models import User as UserORM
from infra.db.mappers.user import UserDBMapper


@final
@dataclass
class MySQLUserRepository(UserRepository):

	session: AsyncSession
	mapper: UserDBMapper

	async def register_user(self, user: User) -> User:
		orm_user = UserORM(
			id=user.id,
			username=user.username.value,
			email=user.email.value,
			password=user.password.hashed_password,
			firstname=user.firstname,
			lastname=user.lastname,
			birthday=user.birthday
		)
		self.session.add(orm_user)
		await self.session.commit()

		return self.mapper.to_entity(
			model=orm_user
		)

	async def get_user_by_username_or_email(self, username: str, email: str) -> User | None:
		orm_user = await self.session.scalar(select(UserORM).filter(or_(UserORM.email == email, UserORM.username == username)))
		if orm_user:
			return self.mapper.to_entity(
				model=orm_user
			)

		return None

	async def get_user_by_id(self, user_id: str):
		orm_user = await self.session.scalar(select(UserORM).where(UserORM.id == user_id))
		if orm_user:
			return self.mapper.to_entity(
				model=orm_user
			)

		return None