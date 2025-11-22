from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

class DatabaseHelper:
	def __init__(self):
		self.engine = create_async_engine(
			url=settings.DB_URL,
			echo=settings.DB_ECHO
		)
		self.session_factory = async_sessionmaker(
			bind=self.engine,
			autoflush=False,
			expire_on_commit=False
		)

	def get_session(self) -> AsyncSession:
		return self.session_factory()
	
	async def session_depedency(self):
		async with self.session_factory() as session:
			yield session
			await session.close()

db = DatabaseHelper()