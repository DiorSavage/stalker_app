from typing import final
from dataclasses import dataclass

from application.dtos.post import PostCommentDTO, CommentImageDTO
from presentation.api.v1.schemas.responses import PostComment, CommentImage
from presentation.api.v1.schemas.requests import PostCommentCreateSchema, CommentImageCreateSchema
from presentation.api.v1.mappers.user_mapper import UserResponseMapper

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class CommentResponseMapper:
	user_db_mapper: UserResponseMapper

	def to_response(self, comment_dto: PostCommentDTO) -> PostComment:
		images = []
		if comment_dto.images:
			images = [
				CommentImage(comment_id=comment_dto.id, id=image.id, created_at=image.created_at, image_url=image.image_url) for image in comment_dto.images
			]
		user_schema = self.user_db_mapper.to_response(dto=comment_dto.author)

		return PostComment(
			content=comment_dto.content,
			created_at=comment_dto.created_at,
			id=comment_dto.id,
			post_id=comment_dto.post_id,
			updated_at=comment_dto.updated_at,
			user_id=comment_dto.author.id,
			images=images,
			author=user_schema
		)

	def to_dto(self, schema: PostCommentCreateSchema, user_id: str) -> PostCommentDTO:
		images = []
		if schema.images:
			images = images = [
				CommentImageDTO(image_url=image.image_url) for image in schema.images
			]

		return PostCommentDTO(
			user_id=user_id,
			post_id=schema.post_id,
			images=images,
			content=schema.content,
		)
