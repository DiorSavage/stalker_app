from pydantic import BaseModel, field_serializer
from typing import Optional

from datetime import datetime

class UserCreateSchema(BaseModel):
	email: str
	username: str
	password: str

	firstname: Optional[str] = None
	lastname: Optional[str] = None
	birthday: Optional[datetime] = None