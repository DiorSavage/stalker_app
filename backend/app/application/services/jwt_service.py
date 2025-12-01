from datetime import datetime
from typing import final
from dataclasses import dataclass
import jwt


@final
@dataclass(
	frozen=False,
	kw_only=True,
	slots=True
)
class JWTService:
	secret_key: str
	public_key: str
	expire_token: int = 15 * 60 * 60 * 24
	algorithm: str = "RS256"

	def __post_init__(self):
		with open(self.secret_key, "r") as file:
			self.secret_key = file.read()

		with open(self.public_key, "r") as file:
			self.public_key = file.read()

	def decode_jwt(self, token: str):
		decoded = jwt.decode(token, key=self.public_key, algorithms=[self.algorithm])

		return decoded
	
	def encode_jwt(self, payload: dict):
		to_encode = payload.copy()
		to_encode.update(
			exp = datetime.now().timestamp() + self.expire_token,
			iat = datetime.now().timestamp()
		)
		encoded = jwt.encode(payload=to_encode, key=self.secret_key, algorithm=self.algorithm)

		return encoded