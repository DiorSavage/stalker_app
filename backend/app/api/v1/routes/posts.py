from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional

from schemas.post_schema import PostResponse, PostCreateRequest
from services.post_service import PostService
from db.session import db

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_post_service():
	return PostService()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(
	title: str = Form(...),
	content: str = Form(...),
	user_id: int = Form(...),
	images: Optional[List[UploadFile]] = File(None),
	session: AsyncSession = Depends(db.session_depedency),
	post_service: PostService = Depends(get_post_service)
):
	new_post_data = PostCreateRequest(title=title, content=content, user_id=user_id)
	if images:
		for image in images:
			if not image.content_type or not image.content_type.startswith("image/"):
				raise HTTPException(
					status_code=400,
					detail={
						"message": "Must be images"
					}
				)
		
	new_post = await post_service.create_post(post_data=new_post_data, images=images, session=session)
	return new_post