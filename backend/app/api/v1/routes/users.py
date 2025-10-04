from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import UserCreateRequest, UserResponse
from services.user_service import UserService
from db.session import db

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service():
	return UserService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(
	user_data: UserCreateRequest,
	session: AsyncSession = Depends(db.session_depedency),
	service: UserService = Depends(get_user_service)
):
	# try:
	existing_user = await service.get_user(email=user_data.email, username=user_data.username, session=session)
	if existing_user:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="User with this username or email already exists"
		)
	
	new_user = await service.register_user(user_data=user_data, session=session)
	await session.commit()
	return new_user
	# except Exception as exc:
	# 	await session.rollback()
	# 	raise HTTPException(
	# 		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
	# 		detail=f"Error with creating user: {exc}"
	# 	)