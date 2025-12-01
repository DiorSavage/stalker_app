from typing import final
from dataclasses import dataclass

from infra.db.models.models import Post as PostORM, User as UserORM, PostImage as PostImageORM
from domain.entities.post import Post as PostEntity, PostImage as PostImageEntity, PostComment as PostCommentEntity, CommentImage as CommentImageEntity
from domain.entities.user import User as UserEntity
from application.dtos.user import UserDTO
from application.dtos.post import PostDTO, PostImageDTO, PostCommentDTO, CommentImageDTO, PostDetailDTO
from application.interfaces.mappers import DtoPostEntityMapper, DtoUserEntityMapper


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostDBMapper:
	
	def to_entity(self, model: PostORM):
		images = []
		if model.images:
			images = [PostImageEntity(created_at=image.created_at, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in model.images]
			
		return PostEntity(
			content=model.content,
			created_at=model.created_at,
			id=model.id,
			title=model.title,
			updated_at=model.updated_at,
			author_id=model.user_id,
			images=images
		)
	
	def image_to_orm(self, post_image: PostImageEntity, post_id: str) -> PostImageORM:
		return PostImageORM(
			id=post_image.id,
			latitude=post_image.latitude,
			longitude=post_image.longitude,
			post_id=post_id,
			image_url=post_image.image_url
		)
	
@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DetailPostDBMapper:
	
	def to_entity(self, model: PostORM):
		images = []
		comments = []
		if model.images:
			images = [PostImageEntity(created_at=image.created_at, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in model.images]
		
		if model.comments:
			for comment in model.comments:
				comment_images = []
				if comment.images:
					comment_images = [CommentImageEntity(id=image.id, created_at=image.created_at, comment_id=comment.id, image_url=image.image_url) for image in comment.images]
				comments.append(PostCommentEntity(id=comment.id, created_at=comment.created_at, user_id=comment.user_id, post_id=model.id, content=comment.content, updated_at=comment.updated_at, images=comment_images))

		return PostEntity(
			content=model.content,
			created_at=model.created_at,
			id=model.id,
			title=model.title,
			updated_at=model.updated_at,
			author_id=model.user_id,
			images=images,
			comments=comments
		)
	
	def image_to_orm(self, post_image: PostImageEntity, post_id: str) -> PostImageORM:
		return PostImageORM(
			id=post_image.id,
			latitude=post_image.latitude,
			longitude=post_image.longitude,
			post_id=post_id,
			image_url=post_image.image_url
		)
	
@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostDTOEntityMapper(DtoPostEntityMapper):
	user_mapper: DtoUserEntityMapper
	
	def to_dto(self, post_entity: PostEntity, author_entity: UserEntity) -> PostDTO:
		images = []
		if post_entity.images:
			images = [PostImageDTO(id=image_schema.id, created_at=image_schema.created_at, post_id=image_schema.post_id, image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in post_entity.images]
		
		author_dto = self.user_mapper.to_dto(entity=author_entity)

		return PostDTO(
			author_id=post_entity.author_id,
			content=post_entity.content,
			created_at=post_entity.created_at,
			id=post_entity.id,
			title=post_entity.title,
			updated_at=post_entity.updated_at,
			images=images,
			author=author_dto
		)

	def to_entity(self, dto: PostDTO) -> PostEntity:
		images = []
		if dto.images:
			images = [PostImageEntity(image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in dto.images]

		return PostEntity(
			author_id=dto.author_id,
			content=dto.content,
			created_at=dto.created_at,
			id=dto.id,
			title=dto.title,
			images=images,
			updated_at=dto.updated_at
		)
	
class DetailPostDTOEntityMapper(DtoPostEntityMapper):
	user_mapper: DtoUserEntityMapper
	
	def to_dto(self, post_entity: PostEntity, author_entity: UserEntity, comments_authors: dict[str, UserEntity]) -> PostDetailDTO:
	# def to_dto(self, post_entity: PostEntity, author_entity: UserEntity, comments_author_entity: list[UserEntity]) -> PostDetailDTO:
		images = []
		comments = []
		if post_entity.images:
			images = [PostImageDTO(id=image_schema.id, created_at=image_schema.created_at, post_id=image_schema.post_id, image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in post_entity.images]
		if post_entity.comments:
			comments: list[PostCommentDTO] = []
			for comment in post_entity.comments:
				comment_images = []
				if comment.images:
					comment_images = [CommentImageDTO(id=image.id, comment_id=comment.id, image_url=image.image_url, created_at=image.created_at) for image in comment.images]
				comment_author = self.user_mapper.to_dto(entity=comments_authors[comment.user_id])
				comment = PostCommentDTO(
					content=comment.content,
					id=comment.id,
					images=comment_images,
					post_id=post_entity.id,
					updated_at=comment.updated_at,
					user_id=comment.user_id,
					author=comment_author,
					created_at=comment.created_at,
				)
				comments.append(comment)
		
		author_dto = self.user_mapper.to_dto(entity=author_entity)

		return PostDetailDTO(
			author_id=post_entity.author_id,
			content=post_entity.content,
			created_at=post_entity.created_at,
			id=post_entity.id,
			title=post_entity.title,
			updated_at=post_entity.updated_at,
			images=images,
			comments=comments,
			author=author_dto
		)

	def to_entity(self, dto: PostDetailDTO) -> PostEntity:
		images = []
		if dto.images:
			images = [PostImageEntity(created_at=image.created_at, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in dto.images]
		if dto.comments:
			comments: list[PostCommentDTO] = []
			for comment in dto.comments:
				comment_images = []
				if comment.images:
					comment_images = [CommentImageDTO(id=image.id, comment_id=comment.id, image_url=image.image_url) for image in comment.images]
				comment = PostEntity(
					content=comment.content,
					id=comment.id,
					images=comment_images,
					post_id=dto.id,
					updated_at=comment.updated_at,
					user_id=comment.user_id
				)
				comments.append(comment)

		return PostEntity(
			author_id=dto.author_id,
			content=dto.content,
			created_at=dto.created_at,
			id=dto.id,
			title=dto.title,
			images=images,
			updated_at=dto.updated_at
		)