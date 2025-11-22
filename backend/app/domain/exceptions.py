from dataclasses import dataclass

@dataclass(eq=False)
class InvalidEmail(Exception):
	email: str

	@property
	def message(self):
		return f"Wrong email, please input valid email: {self.email}"
	
@dataclass(eq=False)
class TooSmallUsername(Exception):
	username: str

	@property
	def message(self):
		return f"Username is too small, please use at least 3 letters: {self.username}"
	
@dataclass(eq=False)
class InvalidSubscriptionType(Exception):
	sub: str

	@property
	def message(self):
		return f"Invalid subscription type: {self.sub}"

@dataclass(eq=False)
class EmptyContentAndImagesComment(Exception):
	@property
	def message(self):
		return f"A comment must have at least one property: images and content are empty"
	
@dataclass(eq=False)
class EmptyContentAndImagesPost(Exception):
	@property
	def message(self):
		return f"A post must have at least one property: images and content are empty"
	
@dataclass(eq=False)
class InvalidBanStatus(Exception):
	ban_status: str

	@property
	def message(self):
		return f"Invalid ban status: {self.ban_status}"
	
@dataclass(eq=False)
class SameAdminAndUserInBanList(Exception):
	user_id: int
	admin_id: int

	@property
	def message(self):
		return f"An admin cannot be a banned user at the same time: user_id - {self.user_id}, admin_id - {self.admin_id}"
	
@dataclass(eq=False)
class EntityValueTypeError(Exception):
	value_name: str
	value_type: type
	necessary_type: object

	@property
	def message(self):
		return f"Inappropriate type for the field {self.value_name}, type - {self.value_type}, necessary type - {self.necessary_type}"