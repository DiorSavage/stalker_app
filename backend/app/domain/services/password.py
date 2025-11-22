from dataclasses import dataclass
from typing import final
import bcrypt

@final
@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class PasswordService:

	def generate_password(self, password: str) -> str:
		bytes_password = password.encode("utf-8")
		salt = bcrypt.gensalt()
		hash_password = bcrypt.hashpw(password=bytes_password, salt=salt)

		return hash_password.decode("utf-8")