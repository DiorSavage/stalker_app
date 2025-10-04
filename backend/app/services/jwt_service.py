import jwt
from core.config import settings
from datetime import datetime, timezone, UTC
import bcrypt

class JwtService:
	def __init__(self):
		self.private_key = settings.auth_settings.private_key_path.read_text()
		self.public_key = settings.auth_settings.public_key_path.read_text()
		self.algorithm = settings.auth_settings.algorithm
		self.token_expire = settings.auth_settings.token_expire

	def decode_jwt(self, token: str, public_key: str = settings.auth_settings.public_key_path.read_text(), algorithm: str = settings.auth_settings.algorithm):
		decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
		
		return decoded

	def encode_jwt(self, payload: dict, private_key: str = settings.auth_settings.private_key_path.read_text(), algorithm: str = settings.auth_settings.algorithm):
		to_encode = payload.copy()
		expire = datetime.now().timestamp() + settings.auth_settings.token_expire
		iat = datetime.now().timestamp()

		to_encode.update(
			exp=expire,
			iat=iat
		)

		encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)

		return {
			"encoded": encoded,
			"iat": iat,
			"exp": expire
		}

	def hash_password(self, password: str) -> bytes:
		salt = bcrypt.gensalt()
		pwd_bytes: bytes = password.encode()
		hashed_password = bcrypt.hashpw(pwd_bytes, salt)

		return hashed_password

	def validate_password(self, password: str, hashed_password: bytes) -> bool:
		return bcrypt.checkpw(password=password, hashed_password=hashed_password)