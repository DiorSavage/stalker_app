from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from schemas.user_schema import UserCreateRequest, UserResponse, AddFriendRequest
from services.user_service import UserService
from services.redis_service import RedisService, get_redis_client
from db.session import db


router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service():
	return UserService()

async def get_redis_service():
	redis = await get_redis_client()
	return RedisService(redis=redis)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(
	user_data: UserCreateRequest,
	session: AsyncSession = Depends(db.session_depedency),
	service: UserService = Depends(get_user_service)
):
	# try:
	existing_user = await service.check_user_exist(email=user_data.email, username=user_data.username, session=session)
	if existing_user:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="User with this username or email already exists"
		)
	new_user_data = await service.register_user(user_data=user_data, session=session)
	print(new_user_data)
	response = JSONResponse(
		status_code=201,
		content=new_user_data.get("user")
	)
	response.set_cookie("gmtoken", new_user_data.get("token"), samesite="none", secure=True, httponly=True, expires=int(new_user_data.get("expire")/1000))
	await session.commit()
	return response

@router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_endpoint(
	email: Optional[str] = None,
	username: Optional[str] = None,
	user_id: Optional[int] = None,
	user_service: UserService = Depends(get_user_service),
	redis_service: RedisService = Depends(get_redis_service),
	session: AsyncSession = Depends(db.session_depedency)
):
	user = await user_service.get_user(email=email, username=username, user_id=user_id, session=session)
	await redis_service.set(f"user:{user.id}", value="nigger", expire=20)
	if not user:
		raise HTTPException(
			status_code=404,
			detail={
				"message": f"User not found"
			}
		)
	response = user.model_dump()
	return response

@router.get("/all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users_endpoint(
	user_service: UserService = Depends(get_user_service),
	session: AsyncSession = Depends(db.session_depedency)
):
	users = await user_service.get_users(session=session)
	if not users:
		raise HTTPException(
			status_code=404,
			detail={
				"message": "Users not found"
			}
		)
	return users

@router.post("/friends/add", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_friend_endpoint(
	new_friendship_data: AddFriendRequest,
	user_service: UserService = Depends(get_user_service),
	session: AsyncSession = Depends(db.session_depedency)
):
	if new_friendship_data.user_id == new_friendship_data.friend_id:
		raise HTTPException(
			status_code=400,
			detail={
				"message": "Cannot be friend of yourself"
			}
		)
	
	user = await user_service.get_user_model(user_id=new_friendship_data.user_id, session=session)
	if not user:
		raise HTTPException(
			status_code=404,
			detail={
				"message": f"User with id: {new_friendship_data.user_id} not found"
			}
		)
	new_friend = await user_service.get_user_model(user_id=new_friendship_data.friend_id, session=session)
	if not new_friend:
		raise HTTPException(
			status_code=404,
			detail={
				"message": f"New friend with id: {new_friendship_data.friend_id} not found"
			}
		)
	
	success = await user_service.add_friend(session=session, user=user, new_friend=new_friend)
	if not success:
		raise HTTPException(
			status_code=400,
			detail={
				"message": "Already friends"
			}
		)
	
	response_friend = UserResponse.model_validate(new_friend, from_attributes=True).model_dump()

	return response_friend

@router.get("/friends", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_friends_endpoint(
	request: Request,
	user_service: UserService = Depends(get_user_service),
	session: AsyncSession = Depends(db.session_depedency),
	user_id: Optional[int] = None
):
	if user_id:
		user = await user_service.get_user_model(user_id=user_id, session=session)
	else:
		user_id = 27 #? из куков
		user = await user_service.get_user_model(user_id=user_id, session=session)

	friends = await user_service.get_friends(session=session, user=user)
	friends_response = [UserResponse.model_validate(friend, from_attributes=True) for friend in friends]
	return friends_response