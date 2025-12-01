from fastapi import APIRouter, Path, Depends, Response, status
from fastapi.responses import JSONResponse

from presentation.api.v1.schemas.responses import UserResponse
from presentation.api.v1.schemas.requests import UserCreateSchema
from presentation.api.v1.mappers.user_mapper import UserResponseMapper
from application.use_cases.save_user_repo import SaveUser

from presentation.di import get_register_user_use_case

router = APIRouter(
	prefix="/v1/users",
	tags=["Users"]
)

@router.post(
		"/register",
		response_model=UserResponse,
		summary="Register user in db",
		responses={
			201: {"description": "Successful registered user"},
			400: {"description": "Bad request (e.g., invalid external API response)"},
			500: {"description": "Internal server error"},
			502: {"description": "Failed to notify via message broker"},
		},
		status_code=status.HTTP_201_CREATED
)
async def register_user(
	schema: UserCreateSchema,
	mapper: UserResponseMapper = Depends(UserResponseMapper),
	use_case: SaveUser = Depends(get_register_user_use_case),
):
	user_dto, token, expire_at = await use_case(user_dto=mapper.to_dto(schema=schema))
	if user_dto is None:
		return Response(
			content="user_dto is None",
			status_code=500
		)
	response_data = mapper.to_response(dto=user_dto)
	response = JSONResponse(
		content=response_data.model_dump(),
		status_code=status.HTTP_201_CREATED
	)
	response.set_cookie(
		key="stalktoken",
		value=token,
		samesite="none",
		secure=True,
		httponly=True,
		expires=int(expire_at/1000)
	)

	return response