from pydantic import BaseModel, field_serializer
from typing import Optional, List

from datetime import datetime

class UserCreateSchema(BaseModel):
	email: str
	username: str
	password: str

	firstname: Optional[str] = None
	lastname: Optional[str] = None
	birthday: Optional[datetime] = None

class PostImageCreateSchema(BaseModel):
	image_url: str
	longitude: Optional[str] = None
	latitude: Optional[str] = None

class PostCreateSchema(BaseModel):
	title: str
	content: str
	author_id: str

	images: Optional[List[PostImageCreateSchema]] = None