from fastapi import APIRouter, status, Depends

from presentation.api.v1.schemas.responses import PostResponse
from presentation.api.v1.schemas.requests import PostCreateSchema
from application.use_cases.create_post_repo import CreatePost
from application.use_cases.get_post_repo import GetPost
from presentation.api.v1.mappers.post_mapper import PostResponseMapper
from infra.di import get_create_post_use_case, get_post_use_case

router = APIRouter(
	prefix="/v1/posts",
	tags=["Posts"]
)


@router.post(
	"/create",
		response_model=PostResponse,
		summary="Register user in db",
		responses={
			201: {"description": "Successful created post"},
			400: {"description": "Bad request (e.g., invalid external API response)"},
			500: {"description": "Internal server error"},
			502: {"description": "Failed to notify via message broker"},
		},
		status_code=status.HTTP_201_CREATED
)
async def create_post(
	new_post: PostCreateSchema,
	mapper: PostResponseMapper = Depends(PostResponseMapper),
	use_case: CreatePost = Depends(get_create_post_use_case)
):
	post_dto = mapper.to_dto(schema=new_post)
	result = await use_case(post_dto=post_dto)
	if result:
		response = mapper.to_response(
			post_dto=result
		)

		return response
	return None

@router.get(
	"/{post_id}",
	response_model=PostResponse,
	summary="Get post by id",
	responses={
		200: {"description": "Post was getted"},
		400: {"description": "Bad request (e.g., invalid external API response)"},
		500: {"description": "Internal server error"},
		502: {"description": "Failed to notify via message broker"},
	},
	status_code=status.HTTP_200_OK
)
async def get_post(
	post_id: str,
	mapper: PostResponseMapper = Depends(PostResponseMapper),
	use_case: GetPost = Depends(get_post_use_case)
):
	result = await use_case(post_id=post_id)
	if result:
		response = mapper.to_response(
			post_dto=result
		)

		return response
	
	return None