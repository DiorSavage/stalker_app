from abc import ABC, abstractmethod
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from services.user_service import UserService
from typing import List
import uuid
import os

class IUploadService(ABC):
	@abstractmethod
	async def upload_user_photo(self, file: UploadFile, username: str):
		pass

	@abstractmethod
	async def save_user_photo(self, file: UploadFile, username: str, session: AsyncSession):
		pass

	@abstractmethod
	async def upload_post_files(self, file: List[UploadFile]):
		pass


class UploadService(IUploadService):
	def __init__(self, user_service: UserService = UserService()):
		self.user_service = user_service

	async def upload_user_photo(self, file, username):
		if not file.content_type.startswith("image/"):
			raise HTTPException(
				status_code=400,
				detail={
					"message": "Content type of file must be image"
				}
			)
		
		file_ext = os.path.splitext(file.filename)[1]
		new_filename = f"{username}-avatar{file_ext}"
		
		file_path = os.path.join(f"{settings.UPLOAD_DIR}users", new_filename)

		with open(file_path, "wb") as file:
			file.write(await file.read())

		return new_filename
	
	async def save_user_photo(self, file: UploadFile, username: str, session: AsyncSession):
		filename = await self.upload_user_photo(file=file, username=username)
		user = await self.user_service.get_user_model()

	async def upload_post_files(self, files: list[UploadFile]) -> list[str]:
		uploaded_urls = []
		upload_dir = os.path.join(settings.UPLOAD_DIR, "posts")
		os.makedirs(upload_dir, exist_ok=True)

		for file in files:
			ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
			filename = f"{uuid.uuid4().hex}.{ext}"
			file_path = os.path.join(upload_dir, filename)

			with open(file_path, "wb") as f:
				content = await file.read()
				f.write(content)

			url = f"/uploads/posts/{filename}"
			uploaded_urls.append(url)

		return uploaded_urls