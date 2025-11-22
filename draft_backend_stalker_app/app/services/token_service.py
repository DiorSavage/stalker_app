from abc import abstractmethod, ABCMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from services.jwt_service import JwtService
from schemas.user_schema import UserCreateRequest, UserResponse
from db.models import Token


class ITokenService:
	@abstractmethod
	def create_payload(user_data: UserResponse):
		pass

	@abstractmethod
	async def create_token(user_data: UserResponse, user_id: int, session: AsyncSession):
		pass
	
	@abstractmethod
	async def get_token(user_id: int, session: AsyncSession):
		pass


class TokenService(ITokenService):
	def __init__(
			self,
			jwt_service: JwtService = JwtService(),
	):
		self.jwt_service: JwtService = jwt_service

	def create_payload(self, user_data: UserResponse):
		payload = {
			"sub": str(user_data.id),
		}

		return payload

	async def create_token(self, user_data: UserResponse, user_id: int, session: AsyncSession):
		existing_token = await self.get_token(user_id=user_id, session=session)
		if not existing_token:
			payload = self.create_payload(user_data=user_data)
			new_token_data = self.jwt_service.encode_jwt(payload=payload)


			token = Token(
				user_id=user_id,
				token=new_token_data.get("encoded"),
				expire_at=new_token_data.get("exp")
			)
			session.add(token)
			await session.flush()

			return {
				"token": new_token_data.get("encoded"),
				"expire": new_token_data.get("exp").timestamp()
			}

	async def get_token(self, user_id: int, session: AsyncSession):
		result = await session.execute(
			select(Token).where(Token.user_id == user_id)
		)
		token = result.scalar_one_or_none()

		return token