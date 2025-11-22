from dataclasses import dataclass

from domain.exceptions import InvalidEmail, TooSmallUsername

@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
	order=True
)
class Username:
	value: str

	def validate_username(self) -> bool:
		if len(self.value) < 3:
			raise TooSmallUsername(self.value)
		
		return True

	def __post_init__(self) -> None:
		self.validate_username()