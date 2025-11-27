from typing import final
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infra.db.mappers.comment import CommentDBMapper
from domain.entities.post import PostComment as PostCommentEntity
from infra.db.models.models import PostComment

@final
@dataclass
class MySQLCommentRepository():
	mapper: CommentDBMapper
	session: AsyncSession

	async def create_comment(self, commentData: PostCommentEntity) -> PostCommentEntity:
		new_post_comment = self.mapper.to_comment_orm(comment_entity=commentData)
		self.session.add(new_post_comment)
		await self.session.flush()

		if commentData.images:
			new_images = [
				self.mapper.to_comment_image_orm(image_entity=image, comment_id=new_post_comment.id) for image in commentData.images
			]
			self.session.add_all(new_images)
		await self.session.commit()
		comment_model = await self.session.scalar(select(PostComment).where(PostComment.id == new_post_comment.id).options(joinedload(PostComment.images)))
		return self.mapper.to_entity(
			model=comment_model
		)