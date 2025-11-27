from dataclasses import dataclass
from typing import final

from application.dtos.post import PostDTO, PostImageDTO, PostDetailDTO
from application.dtos.user import UserDTO
from presentation.api.v1.schemas.responses import PostResponse, PostImageResponse, DetailPostResponse, CommentImage, PostComment
from presentation.api.v1.schemas.requests import PostCreateSchema
from presentation.api.v1.mappers.user_mapper import UserResponseMapper


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostResponseMapper:
	user_db_mapper: UserResponseMapper

	def to_response(self, post_dto: PostDTO) -> PostResponse:
		images = []
		if post_dto.images:
			images = [
				PostImageResponse(created_at=image.created_at, post_id=image.post_id, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude) for image in post_dto.images
			]
		user_schema = self.user_db_mapper.to_response(dto=post_dto.author)
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
		images = []
		if schema.images:
			images = [PostImageDTO(image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in schema.images]

		return PostDTO(
			author_id=schema.author_id,
			title=schema.title,
			content=schema.content,
			images=images
		)

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DetailPostResponseMapper:
	user_db_mapper: UserResponseMapper

	def to_response(self, post_dto: PostDetailDTO) -> DetailPostResponse:
		images = []
		comments = []
		if post_dto.images:
			images = [
				PostImageResponse(created_at=image.created_at, post_id=image.post_id, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude) for image in post_dto.images
			]
		if post_dto.comments:
			for comment in post_dto.comments:
				comment_images = []
				if comment.images:
					comment_images = [CommentImage(id=image.id, created_at=image.created_at, comment_id=comment.id, image_url=image.image_url) for image in comment.images]
				comments.append(PostComment(id=comment.id, created_at=comment.created_at, user_id=comment.user_id, post_id=post_dto.id, content=comment.content, updated_at=comment.updated_at, images=comment_images))
		
		user_schema = self.user_db_mapper.to_response(dto=post_dto.author)
		return DetailPostResponse(
			content=post_dto.content,
			created_at=post_dto.created_at,
			id=post_dto.id,
			title=post_dto.title,
			updated_at=post_dto.updated_at,
			author_id=post_dto.author_id,
			images=images,
			comments=comments,
			author=user_schema
		)

	# def to_dto(self, schema: PostCreateSchema) -> PostDTO:
	# 	images = []
	# 	comments = []
	# 	if schema.images:
	# 		images = [PostImageDTO(image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in schema.images]
	# 	if post_dto.comments:
	# 		for comment in post_dto.comments:
	# 			comment_images = []
	# 			if comment.images:
	# 				comment_images = [CommentImage(id=image.id, created_at=image.created_at, comment_id=comment.id, image_url=image.image_url) for image in comment.images]
	# 			comments.append(PostComment(id=comment.id, created_at=comment.created_at, user_id=comment.user_id, post_id=post_dto.id, content=comment.content, updated_at=comment.updated_at, images=comment_images))

	# 	return DetailPostResponse(
	# 		author_id=schema.author_id,
	# 		title=schema.title,
	# 		content=schema.content,
	# 		images=images,
	# 		comments=comments
	# 	)