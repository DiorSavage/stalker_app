from abc import abstractmethod, ABCMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, or_, Result
from typing import Optional

from services.jwt_service import JwtService
from services.token_service import TokenService
from schemas.user_schema import UserCreateRequest, UserResponse
from db.models import User

class IUserService:

	@abstractmethod
	async def register_user(self, user_data: UserCreateRequest, session: AsyncSession) -> UserResponse:
		pass

	@abstractmethod
	async def get_user(self, email: Optional[str], username: Optional[str], user_id: Optional[int], session: AsyncSession) -> UserResponse:
		pass

	@abstractmethod
	async def check_user_exist(self, email: str, username: str, session: AsyncSession) -> UserResponse:
		pass
	
	@abstractmethod
	async def get_user_model(self, session: AsyncSession, username: str | None = None, email: str | None = None, user_id: int | None = None):
		pass

	@abstractmethod
	async def get_friends(self, session: AsyncSession, user: User):
		pass

	@abstractmethod
	async def get_users(self, session: AsyncSession):
		pass

	@abstractmethod
	async def add_friend(self, session: AsyncSession, user: User, new_friend: User):
		pass

class UserService(IUserService):
	def __init__(
		self,
		jwt_service: JwtService = JwtService(),
		token_service: TokenService = TokenService()
	):
		self.jwt_service: JwtService = jwt_service
		self.token_service: TokenService = token_service

	async def register_user(self, user_data: UserCreateRequest, session: AsyncSession) -> UserResponse:
		user_data.password = self.jwt_service.hash_password(user_data.password)
		new_user = User(**user_data.model_dump())
		session.add(new_user)
		await session.flush()

		user_response = UserResponse.model_validate(new_user, from_attributes=True)
		token_data = await self.token_service.create_token(user_data=user_response, user_id=user_response.id, session=session)

		return {
			"user": user_response.model_dump(),
			"token": token_data.get("token"),
			"expire": token_data.get("expire")
		}

	async def check_user_exist(self, email: str, username: str, session: AsyncSession) -> UserResponse:
		result = await session.execute(
			select(User).filter(or_(User.email == email, User.username == username))
		)
		return result.scalar_one_or_none()
	
	async def get_user(self, email: Optional[str], username: Optional[str], user_id: Optional[int], session: AsyncSession) -> UserResponse:
		if not any([email, username, user_id]):
			raise ValueError("At least one of user_id, email, or username must be provided")

		if user_id is not None:
			result = await session.execute(select(User).where(User.id == user_id))
			user = result.scalar_one_or_none()
			if user:
				return UserResponse.model_validate(user, from_attributes=True)

		if email is not None:
			result = await session.execute(select(User).where(User.email == email))
			user = result.scalar_one_or_none()
			if user:
				return UserResponse.model_validate(user, from_attributes=True)

		if username is not None:
			result = await session.execute(select(User).where(User.username == username))
			user = result.scalar_one_or_none()
			if user:
				return UserResponse.model_validate(user, from_attributes=True)

		return None

	async def get_user_model(self, session: AsyncSession, username: str | None = None, email: str | None = None, user_id: int | None = None):
		if not any([email, username, user_id]):
			raise ValueError("At least one of user_id, email, or username must be provided")
		query = select(User)

		if email:
			query = query.where(User.email == email)

		elif username:
			query = query.where(User.username == username)

		elif user_id:
			query = query.where(User.id == user_id)

		result = await session.execute(query)

		user = result.scalar_one_or_none()

		return user
	
	async def get_friends(self, session: AsyncSession, user: User):
		friends = await user.get_friends(session=session)
		return friends

	async def get_users(self, session):
		users = await session.scalars(select(User))
		users_response = [UserResponse.model_validate(user, from_attributes=True).model_dump() for user in users.all()]
		return users_response
	
	async def add_friend(self, session: AsyncSession, user: User, new_friend: User):
		success = await user.add_friend(other=new_friend, session=session)
		return success