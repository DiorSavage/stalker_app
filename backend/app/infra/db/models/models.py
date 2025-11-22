from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped, relationship, object_session
from sqlalchemy import Column, Integer, String, DateTime, DATETIME, func, Enum, ForeignKey, Boolean, Table, CheckConstraint, Index, select, or_, UniqueConstraint, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.exc import IntegrityError
from enum import StrEnum
import uuid

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
		return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

	@declared_attr
	def created_at(cls):
		return mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)

class FriendsList(Base):
	__tablename__ = "friends_list"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)


	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
	friend_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

	__table_args__ = (
		UniqueConstraint("user_id", "friend_id", name="uq_user_friend_constraint"), 
	)

class User(Base):
	email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
	username: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
	firstname: Mapped[str] = mapped_column(String(50), nullable=True)
	lastname: Mapped[str] = mapped_column(String(50), nullable=True)
	birthday: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)

	timezone: Mapped[str] = mapped_column(String(20), default="Europe/Moscow", server_default="Europe/Moscow", nullable=False)
	subscription_type: Mapped[SubscriptionEnum] = mapped_column(Enum(SubscriptionEnum, name="subscription_type_enum"), default=SubscriptionEnum.free, server_default=SubscriptionEnum.free.value)
	subscription_expired_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)
	is_banned: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0", nullable=True)
	is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0", nullable=True)
	avatar: Mapped[str] = mapped_column(String(255), nullable=True)
	password: Mapped[bytes]

	token: Mapped["Token"] = relationship("Token", back_populates="user")
	posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
	comments: Mapped[List["PostComment"]] = relationship("PostComment", back_populates="author")
	incoming_friend_requests: Mapped[List["FriendsRequests"]] = relationship("FriendsRequests", foreign_keys="[FriendsRequests.user_id]", back_populates="user")
	outgoing_friend_requests: Mapped[List["FriendsRequests"]] = relationship("FriendsRequests", foreign_keys="[FriendsRequests.from_user_id]", back_populates="from_user")


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
			print("Already friends")
			return False
		
		try:
			new_friends_list = FriendsList(
				user_id=a,
				friend_id=b
			)
			session.add(new_friends_list)
			await session.commit()
			return True
		except IntegrityError as exc:
			print(exc)
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
			.join(FriendsList, or_(
				(FriendsList.user_id == self.id) & (FriendsList.friend_id == User.id),
				(FriendsList.friend_id == self.id) & (FriendsList.user_id == User.id)
			))
		)
		result = await session.scalars(query)
		return result.all()

class FriendsRequests(Base):
	__tablename__ = "friends_requests"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)


	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
	from_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
	created_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)

	user = relationship("User", foreign_keys=user_id, back_populates="incoming_friend_requests")
	from_user = relationship("User", foreign_keys=from_user_id, back_populates="outgoing_friend_requests")

	__table_args__ = (
		UniqueConstraint("from_user_id", "user_id", name="uq_from_to_requests"), 
		CheckConstraint("from_user_id != user_id", name="ck_no_self_request")
	)

class Token(Base):
	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
	token: Mapped[str] = mapped_column(String(400), index=True)
	created_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False, server_onupdate=func.now())
	expire_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)

	user = relationship("User", back_populates="token")


class BanList(Base):
	__tablename__ = "ban_list"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)

	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
	admin_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False, server_onupdate=func.now())
	reason: Mapped[str] = mapped_column(String(100), nullable=True)
	ban_status: Mapped[BanStatusEnum] = mapped_column(Enum(BanStatusEnum, name="ban_status_enum"), default=BanStatusEnum.unbanned, server_default=BanStatusEnum.unbanned.value)

	admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])
	user: Mapped["User"] = relationship("User", foreign_keys=[user_id])


class Post(Base):
	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
	content: Mapped[str] = mapped_column(String(500), nullable=True)
	title: Mapped[str] = mapped_column(String(50), nullable=False)
	
	updated_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False, server_onupdate=func.now())

	author: Mapped["User"] = relationship("User", back_populates="posts")
	images: Mapped[List["PostImage"]] = relationship("PostImage", back_populates="post")
	comments: Mapped[List["PostComment"]] = relationship("PostComment", back_populates="post")


class PostImage(Base):
	__tablename__ = "post_images"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)

	post_id: Mapped[str] = mapped_column(String(36), ForeignKey("posts.id"), nullable=False, index=True)
	image_url: Mapped[str] = mapped_column(String(500), nullable=False)
	latitude: Mapped[float] = mapped_column(Float, nullable=True)
	longitude: Mapped[float] = mapped_column(Float, nullable=True)
	

	post: Mapped["Post"] = relationship("Post", back_populates="images")


class PostComment(Base):
	__tablename__ = "post_comments"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)

	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
	post_id: Mapped[str] = mapped_column(String(36), ForeignKey("posts.id"), index=True, nullable=False)
	content: Mapped[str] = mapped_column(String(500), nullable=True)
	
	updated_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), server_default=func.now(), default=datetime.now, nullable=False, server_onupdate=func.now())

	images: Mapped[List["CommentImage"]] = relationship(
		"CommentImage",
		back_populates="post_comment"
	)
	post: Mapped["Post"] = relationship(
		"Post",
		back_populates="comments"
	)
	author: Mapped["User"] = relationship(
		"User",
		back_populates="comments"
	)


class CommentImage(Base):
	__tablename__ = "comment_images"

	id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, unique=True, default=uuid.uuid4)

	comment_id: Mapped[str] = mapped_column(String(36), ForeignKey("post_comments.id"), nullable=False, index=True)
	image_url: Mapped[str] = mapped_column(String(500), nullable=False)
	

	post_comment: Mapped["PostComment"] = relationship(
		"PostComment",
		back_populates="images"
	)