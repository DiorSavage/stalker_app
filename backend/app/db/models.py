from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped, relationship, object_session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, func, Enum, ForeignKey, Boolean, Table, CheckConstraint, Index, select, or_, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.exc import IntegrityError
from enum import StrEnum

from datetime import datetime, timezone
from typing import List


class SubscriptionEnum(StrEnum):
	free = "free"
	premium = "premium"
	full_premium = "full_premium"

class BanStatusEnum(StrEnum):
	banned = "banned"
	unbanned = "unbanned"

class Base(DeclarativeBase):
	__abstract__ = True

	@declared_attr.directive
	def __tablename__(cls):
		return f"{cls.__name__.lower()}s"

	@declared_attr
	def id(cls):
		return Column(Integer, primary_key=True, index=True, unique=True)

class FriendsList(Base):
	__tablename__ = "friends_list"
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
	friend_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
	added_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.timezone("utc", func.now()), default=datetime.now(timezone.utc), nullable=False)

	__table_args__ = (
		UniqueConstraint("user_id", "friend_id", name="uq_user_friend_constraint"), 
	)


#! РЕАЛИЗАЦИЯ FRIENDS_LIST
#? без min/max id, что занимает куда больше места
#! НЕ юзаем relationship для friends, он не подходит для симметричной связи с одной записью
	# Вместо этого — методы или гибридные свойства
# friends: Mapped[List["User"]] = relationship(
# 	"User",
# 	secondary=FriendsList,
# 	primaryjoin=FriendsList.user_id == id,
# 	secondaryjoin=FriendsList.friend_id == id,
# 	back_populates="friends_of"
# )
# friends_of: Mapped[List["User"]] = relationship(
# 	"User",
# 	secondary=FriendsList,
# 	primaryjoin=FriendsList.friend_id == id,
# 	secondaryjoin=FriendsList.user_id == id,
# 	back_populates="friends"
# )

#! Использовать одну запись с правилом min/max ID, но это сложнее в ORM»
#? primary_join для одной записи двух id (1, 2)
#* primaryjoin=or_(
#* 	User.id == friendship_table.c.user_id,
#* 	User.id == friendship_table.c.friend_id
#* )
#? Но тогда secondaryjoin становится неоднозначным — непонятно откуда брать "друга"
#? поэтому юзаем гибридные свойства
# @hybrid_property
# def friends(self):
# 	session = object_session(self)
# 	friends =  session.scalars(
# 		select(User).join(FriendsList, or_(
# 			(FriendsList.user_id == self.id) & (FriendsList.friend_id == User.id),
# 			(FriendsList.friend_id == self.id) & (FriendsList.user_id == User.id)
# 		))
# 	)
# 	return friends.all()

# token = relationship("Token", back_populates="user")

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
	is_banned: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0", nullable=True)
	is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0", nullable=True)
	avatar: Mapped[str] = mapped_column(String, nullable=True)
	password: Mapped[bytes]

	token: Mapped["Token"] = relationship("Token", back_populates="user")

	async def add_friend(self, other: "User", session: AsyncSession) -> bool:
		if self.id == other.id:
			raise ValueError("Cannot be friend of yourself")
		
		a, b = sorted([self.id, other.id])

		exists = await session.scalar(
			select(FriendsList).where(
				FriendsList.user_id == a,
				FriendsList.friend_id == b
			)
		)
		if exists:
			return False
		
		try:
			new_friends_list = FriendsList(
				user_id=a,
				friend_id=b
			)
			session.add(new_friends_list)
			await session.commit()
			return True
		except IntegrityError:
			await session.rollback()
			return False
	
	async def remove_friend(self, other: "User", session: AsyncSession) -> bool:
		a, b = sorted([self.id, other.id])
		friends_list = await session.scalar(select(FriendsList).where(FriendsList.user_id == a, FriendsList.friend_id == b))
		if not friends_list:
			return False
		
		await session.delete(friends_list)
		await session.commit()

		return True

	async def get_friends(self, session: AsyncSession) -> List["User"]:
		query = (
			select(User)
			.select_from(FriendsList)
			.join(User, or_(
				(FriendsList.user_id == self.id) & (FriendsList.friend_id == User.id),
				(FriendsList.friend_id == self.id) & (FriendsList.user_id == User.id)
			))
		)
		query = (
			select(User)
			.join(FriendsList, or_(
				(FriendsList.user_id == self.id) & (FriendsList.friend_id == User.id),
				(FriendsList.friend_id == self.id) & (FriendsList.user_id == User.id)
			))
		)
		result = await session.scalars(query)
		return result.all()

class Token(Base):
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
	token: Mapped[str] = mapped_column(String, index=True)
	created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), server_default=func.timezone("utc", func.now()), nullable=False)
	updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True, server_default=func.timezone("utc", func.now()), default=datetime.now(timezone.utc), server_onupdate=func.timezone("utc", func.now()))
	expire_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

	user = relationship("User", back_populates="token")

class BanList(Base):
	__tablename__ = "ban_list"

	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
	admin_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True, server_default=func.timezone("utc", func.now()), default=datetime.now(timezone.utc), server_onupdate=func.timezone("utc", func.now()))
	reason: Mapped[str] = mapped_column(String, nullable=True)
	ban_status: Mapped[BanStatusEnum] = mapped_column(Enum(BanStatusEnum, name="ban_status_enum"), default=BanStatusEnum.unbanned, server_default=BanStatusEnum.unbanned.value)
	
	admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])
	user: Mapped["User"] = relationship("User", foreign_keys=[user_id])