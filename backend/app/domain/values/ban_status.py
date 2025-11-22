from dataclasses import dataclass

from domain.exceptions import InvalidBanStatus

@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
	order=True
)
class BanStatus:
	value: str

	__ban_statuses = [
		"banned",
		"unbanned",
	]

	def validate_ban_status(self) -> bool:
		if self.value not in self.__ban_statuses:
			raise InvalidBanStatus(self.value)
		
		return True

	def __post_init__(self) -> None:
		self.validate_ban_status()