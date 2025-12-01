from dataclasses import dataclass
from typing import final, Optional
from datetime import datetime

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class TokenDTO:
	id: Optional[str] = None
	user_id: str
	token: str
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
	expire_at: Optional[datetime] = None