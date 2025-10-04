from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, func, Enum
from enum import StrEnum

from datetime import datetime, timezone
from typing import List


class SubscriptionEnum(StrEnum):
	free = "free"
	premium = "premium"
	full_premium = "full_premium"

class Base(DeclarativeBase):
	__abstract__ = True

	@declared_attr.directive
	def __tablename__(cls):
		return f"{cls.__name__.lower()}s"

	@declared_attr
	def id(cls):
		return Column(Integer, primary_key=True, index=True, unique=True)

class User(Base):
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
	username: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
	firstname: Mapped[str] = mapped_column(String, nullable=True)
	lastname: Mapped[str] = mapped_column(String, nullable=True)
	birthday: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
	registered_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.timezone("utc", func.now()), default=datetime.now(timezone.utc))
	timezone: Mapped[str] = mapped_column(String, default="Europe/Moscow", server_default="Europe/Moscow", nullable=False)
	subscription_type: Mapped[SubscriptionEnum] = mapped_column(Enum(SubscriptionEnum, name="subscription_type_enum"), default=SubscriptionEnum.free, server_default=SubscriptionEnum.free.value)
	subscription_expired_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
	password: Mapped[bytes]