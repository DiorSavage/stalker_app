from pydantic.v1 import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class AuthSettings(BaseModel):
	private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
	public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
	algorithm: str = "RS256"
	token_expire: int = 15 * 60 * 60 * 24

class RedisSettings(BaseModel):
	REDIS_HOST: str = "redis"
	REDIS_PORT: int = 6379
	REDIS_PROTOCOL: int = 3
	REDIS_DECODE_RESPONSES: bool = True
	REDIS_DB: int = 0
	CACHE_EXPIRATION_MIN: int = 5

class Settings(BaseModel):
	DB_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/stalkappdb"
	# DB_URL: str = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/stalkappdb"
	DB_ECHO: bool = True
	UPLOAD_DIR: str = "/stalk_app/uploads/"

	auth_settings: AuthSettings = AuthSettings()
	redis_settings: RedisSettings = RedisSettings()

settings = Settings()