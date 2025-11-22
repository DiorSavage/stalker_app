from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4, UUID

@dataclass(
	frozen=True,
	kw_only=True,
)
class BaseEntity(ABC):
	id: UUID = field(
		default_factory=uuid4,
	)
	created_at: datetime = field(
		default_factory=lambda: datetime.now(UTC)
	)

	def __hash__(self):
		return hash(self.id)
	
	def __eq__(self, __other: "BaseEntity") -> bool:
		return self.id == __other.id