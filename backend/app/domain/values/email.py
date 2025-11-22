from dataclasses import dataclass
from typing import Optional
import re

from domain.exceptions import InvalidEmail

@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
	order=True
)
class Email:
	value: str
	__email_template: Optional[str] = r'[a-z0-9]{3,}@(gmail|mail|yandex).(ru|com)'

	def validate_email(self) -> bool:
		email_match = re.match(self.__email_template, self.value)
		if email_match is None:
			raise InvalidEmail(self.value)
		
		return True

	def __post_init__(self) -> None:
		self.validate_email()