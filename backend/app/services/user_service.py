from abc import abstractmethod, ABCMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from services.jwt_service import JwtService
from schemas.user_schema import UserCreateRequest, UserResponse
from db.models import User

class IUserService:

	@abstractmethod
	async def register_user(self, user_data: UserCreateRequest, session: AsyncSession) -> UserResponse:
		pass

	@abstractmethod
	async def get_user(self, email: str, username: str, session: AsyncSession):
		pass

class UserService(IUserService):
	def __init__(
			self,
			jwt_service: JwtService = JwtService(),
	):
		self.jwt_service: JwtService = jwt_service

	async def register_user(self, user_data: UserCreateRequest, session: AsyncSession) -> UserResponse:
		user_data.password = self.jwt_service.hash_password(user_data.password)
		new_user = User(**user_data.model_dump())
		session.add(new_user)
		await session.flush()

		user_response = UserResponse.model_validate(new_user, from_attributes=True).model_dump()

		return user_response
		
	async def get_user(self, email: str, username: str, session: AsyncSession):
		result = await session.execute(
			select(User).where(User.email == email, User.username == username)
		)
		return result.scalar_one_or_none()
