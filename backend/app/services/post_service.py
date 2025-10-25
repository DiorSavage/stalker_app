from abc import abstractmethod, ABCMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, or_, Result
from typing import Optional, List
from fastapi import UploadFile

from services.upload_service import UploadService
from schemas.post_schema import PostCreateRequest, PostResponse
from db.models import Post, PostImage

class IPostService:
	@abstractmethod
	async def create_post(self, post_data: PostCreateRequest, session: AsyncSession):
		pass 


class PostService(IPostService):
	def __init__(
		self,
		upload_service: UploadService = UploadService()
	):
		self.upload_service = upload_service
	
	async def create_post(self, post_data: PostCreateRequest, session: AsyncSession, images: List[UploadFile] | None = None):
		new_post = Post(**post_data.model_dump())
		session.add(new_post)
		await session.flush()
		if images:
			image_urls = await self.upload_service.upload_post_files(files=images)

			for url in image_urls:
				new_photo = PostImage(
					post_id=new_post.id,
					image_url=url
				)
				session.add(new_photo)

		await session.commit()
		await session.refresh(new_post)

		query = select(Post).options(
			selectinload(Post.images),
			selectinload(Post.comments)
		).where(Post.id == new_post.id)
		result: Result = await session.execute(query)
		new_post = result.scalar_one()

		post_response = PostResponse.model_validate(new_post, from_attributes=True).model_dump()

		return post_response