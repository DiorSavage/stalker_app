from typing import final
from dataclasses import dataclass

from application.dtos.post import PostDTO
from application.interfaces.mappers import DtoPostEntityMapper
from application.interfaces.repositories import PostRepository, UserRepository

@final
@dataclass(
	frozen=True,
	slots=True,
	kw_only=True
)
class CreatePost:

	mapper: DtoPostEntityMapper
	post_repo: PostRepository
	user_repo: UserRepository

	async def __call__(self, post_dto: PostDTO) -> PostDTO | None:
		post_entity = self.mapper.to_entity(dto=post_dto)
		new_post_entity = await self.post_repo.create_post(post=post_entity)
		user_entity = await self.user_repo.get_user_by_id(user_id=new_post_entity.author_id)

		if new_post_entity:
			return self.mapper.to_dto(
				post_entity=new_post_entity,
				author_entity=user_entity
			)
		
		return None