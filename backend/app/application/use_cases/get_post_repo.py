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
			return self.mapper.to_dto(
				post_entity=post_entity,
				author_entity=author_entity
			)
		
		return None