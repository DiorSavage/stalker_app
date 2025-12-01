from dataclasses import dataclass
from typing import final

from application.interfaces.mappers import DtoPostEntityMapper
from application.interfaces.repositories import PostRepository, UserRepository


@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class GetPost:
	mapper: DtoPostEntityMapper
	post_repo: PostRepository
	user_repo: UserRepository

	async def __call__(self, post_id: str):
		post_entity = await self.post_repo.get_post_by_id(post_id=post_id)
		if post_entity:
			author_entity = await self.user_repo.get_user_by_id(user_id=post_entity.author_id)
			comments_authors = {}
			if post_entity.comments:
				author_id_comments_map = [comment.user_id for comment in post_entity.comments]
				comments_authors_list = await self.user_repo.get_users_by_id(user_ids=author_id_comments_map)
				comments_authors = { author_id: author for author_id, author in zip(author_id_comments_map, comments_authors_list) }

			return self.mapper.to_dto(
				post_entity=post_entity,
				author_entity=author_entity,
				comments_authors=comments_authors
			)
		
		return None