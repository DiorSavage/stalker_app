from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, Result
from sqlalchemy.orm import joinedload

from application.interfaces.repositories import PostRepository
from infra.db.models.models import Post as PostORM, PostImage as PostImageORM
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
		await self.session.commit()

		if post.images:
			new_images = [
				PostImageORM(
					id=image.id,
					latitude=image.latitude,
					longitude=image.longitude,
					post_id=new_post_model.id,
					image_url=image.image_url
				)
				for image in post.images
			]
			self.session.add_all(new_images)

		await self.session.commit()
		post_model = await self.session.scalar(select(PostORM).where(PostORM.id == new_post_model.id).options(joinedload(PostORM.images)))

		return self.mapper.to_entity(
			model=post_model
		)
	
	async def get_post_by_id(self, post_id: str) -> Post:
		post_model = await self.session.scalar(select(PostORM).where(PostORM.id == post_id).options(joinedload(PostORM.images)))
		if post_model:
			return self.mapper.to_entity(
				model=post_model
			)
		
		return None