from fastapi import APIRouter, status, Depends

from presentation.api.v1.schemas.responses import PostResponse, DetailPostResponse, PostComment as PostCommentResponse
from presentation.api.v1.schemas.requests import PostCreateSchema, PostCommentCreateSchema
from application.use_cases.create_post_repo import CreatePost
from application.use_cases.get_post_repo import GetPost
from application.use_cases.create_comment_repo import CreatePostComment
from presentation.api.v1.mappers.post_mapper import PostResponseMapper, DetailPostResponseMapper
from presentation.api.v1.mappers.comment_mapper import CommentResponseMapper
from presentation.di import get_create_post_use_case, get_post_use_case, get_post_response_mapper, get_detail_post_response_mapper, get_create_comment_use_case, get_comment_response_mapper

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
	mapper: PostResponseMapper = Depends(get_post_response_mapper),
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
	response_model=DetailPostResponse,
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
	mapper: DetailPostResponseMapper = Depends(get_detail_post_response_mapper),
	use_case: GetPost = Depends(get_post_use_case)
):
	result = await use_case(post_id=post_id)
	if result:
		response = mapper.to_response(
			post_dto=result
		)

		return response
	
	return None

@router.post(
	"/comments/create",
	response_model=PostCommentResponse,
	summary="Get post by id",
	responses={
		201: {"description": "Comment was created"},
		400: {"description": "Bad request (e.g., invalid external API response)"},
		500: {"description": "Internal server error"},
		502: {"description": "Failed to notify via message broker"},
	},
	status_code=status.HTTP_201_CREATED
)
async def create_comment(
	new_comment: PostCommentCreateSchema,
	mapper: CommentResponseMapper = Depends(get_comment_response_mapper),
	use_case: CreatePostComment = Depends(get_create_comment_use_case)
):
	new_comment_dto = mapper.to_dto(
		schema=new_comment,
		user_id="7e03811c-3ee1-4bd8-9e90-5384641084f4" #? из jwt токена
	)
	result = await use_case(comment_data=new_comment_dto)
	if result:
		response = mapper.to_response(
			comment_dto=result
		)

		return response
	
	return None