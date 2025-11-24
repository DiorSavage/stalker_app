from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session, AsyncSession, AsyncEngine
from typing import Any
from dotenv import load_dotenv

import asyncio
import os

load_dotenv()

@final
@dataclass(
	frozen=True,
	slots=True,
	kw_only=True,
)
class DatabaseHelper:
	engine: AsyncEngine = create_async_engine(
		url=os.environ.get("MYSQL_URL"),
		echo=True
	)
	session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
		bind=engine,
		autoflush=False,
		expire_on_commit=False
	)

	async def session_depedency(self):
		async with self.session_factory() as session:
			yield session
			await session.close()

db = DatabaseHelper()