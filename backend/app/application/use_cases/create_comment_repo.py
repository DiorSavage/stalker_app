from typing import final
from dataclasses import dataclass

from application.interfaces.mappers import DtoCommentEntityMapper
from application.interfaces.repositories import CommentRepository, UserRepository

from application.dtos.post import PostCommentDTO

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class CreatePostComment:
	mapper: DtoCommentEntityMapper
	comment_repo: CommentRepository
	user_repo: UserRepository

	async def __call__(self, comment_data: PostCommentDTO):
		comment_entity = self.mapper.to_entity(dto=comment_data)
		new_comment_entity = await self.comment_repo.create_comment(commentData=comment_entity)
		author_entity = await self.user_repo.get_user_by_id(user_id=new_comment_entity.user_id)
		if new_comment_entity:
			return self.mapper.to_dto(
				author_entity=author_entity,
				comment_entity=new_comment_entity
			)
		
		return None