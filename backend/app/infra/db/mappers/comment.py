from typing import final
from dataclasses import dataclass

from application.interfaces.mappers import DtoCommentEntityMapper, DtoUserEntityMapper
from application.dtos.post import PostCommentDTO, CommentImageDTO

from domain.entities.post import PostComment as PostCommentEntity, CommentImage as CommentImageEntity
from domain.entities.user import User as UserEntity
from domain.entities.post import PostComment, CommentImage

from infra.db.models.models import CommentImage as CommentImageORM, PostComment as PostCommentORM

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class CommentDBMapper:

	def to_comment_orm(self, comment_entity: PostComment) -> PostCommentORM:
		return PostCommentORM(
			id=comment_entity.id,
			created_at=comment_entity.created_at,
			content=comment_entity.content,
			post_id=comment_entity.post_id,
			user_id=comment_entity.user_id
		)

	def to_comment_image_orm(self, image_entity: CommentImage, comment_id: str) -> CommentImageORM:
		return CommentImageORM(
			comment_id=comment_id,
			image_url=image_entity.image_url,
			created_at=image_entity.created_at,
			id=image_entity.id
		)

	def to_entity(self, model: PostCommentORM) -> PostCommentEntity:
		images = []
		if model.images:
			images = [CommentImageEntity(id=image.id, comment_id=model.id, image_url=image.image_url, created_at=image.created_at) for image in model.images]

		return PostCommentEntity(
			content=model.content,
			id=model.id,
			images=images,
			post_id=model.post_id,
			updated_at=model.updated_at,
			user_id=model.user_id,
			created_at=model.created_at
		)

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class CommentDtoEntityMapper(DtoCommentEntityMapper):
	user_mapper: DtoUserEntityMapper

	def to_dto(self, comment_entity: PostCommentEntity, author_entity: UserEntity) -> PostCommentDTO:
		images = []
		if comment_entity.images:
			images = [CommentImageDTO(id=image.id, comment_id=comment_entity.id, image_url=image.image_url, created_at=image.created_at) for image in comment_entity.images]
		
		author_dto = self.user_mapper.to_dto(entity=author_entity)

		return PostCommentDTO(
			content=comment_entity.content,
			id=comment_entity.id,
			images=images,
			post_id=comment_entity.post_id,
			updated_at=comment_entity.updated_at,
			user_id=comment_entity.user_id,
			author=author_dto,
			created_at=comment_entity.created_at
		)
	
	def to_entity(self, dto: PostCommentDTO) -> PostCommentEntity:
		images = []
		if dto.images:
			images = [CommentImageEntity(comment_id=dto.id, image_url=image.image_url) for image in dto.images]

		return PostCommentEntity(
			content=dto.content,
			id=dto.id,
			images=images,
			post_id=dto.post_id,
			updated_at=dto.updated_at,
			user_id=dto.user_id,
			created_at=dto.created_at
		)