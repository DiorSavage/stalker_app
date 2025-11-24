from typing import final
from dataclasses import dataclass

from infra.db.models.models import Post as PostORM
from infra.db.models.models import User as UserORM
from domain.entities.post import Post as PostEntity, PostImage
from domain.entities.user import User as UserEntity
from application.dtos.user import UserDTO
from application.dtos.post import PostDTO, PostImageDTO
from application.interfaces.mappers import DtoPostEntityMapper


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostDBMapper:
	
	def to_entity(self, model: PostORM):
		images = None
		if model.images:
			images = [PostImage(created_at=image.created_at, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in model.images]

		return PostEntity(
			content=model.content,
			created_at=model.created_at,
			id=model.id,
			title=model.title,
			updated_at=model.updated_at,
			author_id=model.user_id,
			images=images
		)
	
@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PostDTOEntityMapper(DtoPostEntityMapper):
	
	def to_dto(self, post_entity: PostEntity, author_entity: UserEntity) -> PostDTO:
		images = None
		if post_entity.images:
			images = [PostImageDTO(id=image_schema.id, created_at=image_schema.created_at, post_id=image_schema.post_id, image_url=image_schema.image_url,longitude=image_schema.longitude, latitude=image_schema.latitude) for image_schema in post_entity.images]

		print(post_entity, author_entity)
		
		author_dto = UserDTO(
			id=author_entity.id,
			email=author_entity.email.value,
			username=author_entity.username.value,
			password=author_entity.password,
			firstname=author_entity.firstname,
			lastname=author_entity.lastname,
			birthday=author_entity.birthday,
			timezone=author_entity.timezone,
			subscription_type=author_entity.subscription_type.value,
			subscription_expired_at=author_entity.subscription_expired_at,
			is_banned=author_entity.is_banned,
			is_admin=author_entity.is_admin,
			avatar=author_entity.avatar,
			created_at=author_entity.created_at
		)

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
		images = None
		if dto.images:
			images = [PostImage(created_at=image.created_at, id=image.id, image_url=image.image_url, latitude=image.latitude, longitude=image.longitude, post_id=image.post_id) for image in dto.images]

		return PostEntity(
			author_id=dto.author_id,
			content=dto.content,
			created_at=dto.created_at,
			id=dto.id,
			title=dto.title,
			images=images,
			updated_at=dto.updated_at
		)