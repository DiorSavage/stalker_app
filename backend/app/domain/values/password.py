from dataclasses import dataclass

@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
	order=True
)
class Password:
	value: str
  
	@property
	def hashed_password(self):
		return self.value.encode("utf-8")