from dataclasses import dataclass
from typing import final

@final
@dataclass(
	eq=False,
	frozen=True
)
class UserAlreadyExists(Exception):
	email: str

	@property
	def message(self):
		return f"User with email {self.email} already exists"