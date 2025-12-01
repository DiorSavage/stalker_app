from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, Result
from sqlalchemy.orm import joinedload, selectinload

from application.interfaces.repositories import PostRepository
from infra.db.models.models import Post as PostORM, PostComment as PostCommentORM
from domain.entities.post import Post
from infra.db.mappers.post import PostDBMapper

@final
@dataclass
class MySQLPostRepository(PostRepository):

	mapper: PostDBMapper
	session: AsyncSession

	async def create_post(self, post: Post) -> Post:
		new_post_model = PostORM(
			user_id=post.author_id,
			content=post.content,
			title=post.title
		)
		self.session.add(new_post_model)
		await self.session.flush()

		if post.images:
			new_images = [
				self.mapper.image_to_orm(post_image=image, post_id=new_post_model.id)
				for image in post.images
			]
			self.session.add_all(new_images)

		await self.session.commit()
		post_model = await self.session.scalar(select(PostORM).where(PostORM.id == new_post_model.id).options(joinedload(PostORM.images)))

		return self.mapper.to_entity(
			model=post_model
		)
	
	async def get_post_by_id(self, post_id: str) -> Post:
		post_model = await self.session.scalar(select(PostORM).where(PostORM.id == post_id).options(selectinload(PostORM.images), selectinload(PostORM.comments).selectinload(PostCommentORM.images), selectinload(PostORM.comments).joinedload(PostCommentORM.author)))
		if post_model:
			return self.mapper.to_entity(
				model=post_model
			)
		
		return None