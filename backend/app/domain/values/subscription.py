from dataclasses import dataclass

from domain.exceptions import InvalidSubscriptionType

@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
	order=True
)
class SubscriptionType:
	value: str

	__subscription_types = [
		"free",
		"premium",
		"full_premium"
	]

	def validate_subscription_type(self) -> bool:
		if self.value not in self.__subscription_types:
			raise InvalidSubscriptionType(self.value)
		
		return True

	def __post_init__(self) -> None:
		self.validate_subscription_type()