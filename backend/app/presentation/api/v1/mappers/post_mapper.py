from dataclasses import dataclass
from typing import final

from application.dtos.post import PostDTO, PostImageDTO
from application.dtos.user import UserDTO
from presentation.api.v1.schemas.responses import PostResponse, PostImageResponse
from presentation.api.v1.schemas.requests import PostCreateSchema
from presentation.api.v1.schemas.responses import UserResponse


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostResponseMapper:

	def to_response(self, post_dto: PostDTO) -> PostResponse:
		images = None
		if post_dto.images:
			images = [
				PostImageResponse(created_at=image.created_at, post_id=image.post_id, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude) for image in post_dto.images
			]
		user_schema = UserResponse(
			avatar=post_dto.author.avatar,
			birthday=post_dto.author.birthday,
			email=post_dto.author.email,
			firstname=post_dto.author.firstname,
			id=post_dto.author.id,
			is_admin=post_dto.author.is_admin,
			is_banned=post_dto.author.is_banned,
			lastname=post_dto.author.lastname,
			created_at=post_dto.author.created_at,
			subscription_expired_at=post_dto.author.subscription_expired_at,
			subscription_type=post_dto.author.subscription_type,
			timezone=post_dto.author.timezone,
			username=post_dto.author.username
		)
		return PostResponse(
			content=post_dto.content,
			created_at=post_dto.created_at,
			id=post_dto.id,
			title=post_dto.title,
			updated_at=post_dto.updated_at,
			author_id=post_dto.author_id,
			images=images,
			author=user_schema
		)

	def to_dto(self, schema: PostCreateSchema) -> PostDTO:
		images = None
		if schema.images:
			images = [PostImageDTO(image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in schema.images]

		return PostDTO(
			author_id=schema.author_id,
			title=schema.title,
			content=schema.content,
			images=images
		)