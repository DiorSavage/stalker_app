from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.models.session import db
from infra.db.repositories.user import MySQLUserRepository
from infra.db.repositories.post import MySQLPostRepository
from infra.db.mappers.post import PostDBMapper, PostDTOEntityMapper
from infra.db.mappers.user import UserDBMapper, UserDTOEntityMapper
from domain.services.password import PasswordService
from application.use_cases.save_user_repo import SaveUser
from application.use_cases.create_post_repo import CreatePost
from application.use_cases.get_post_repo import GetPost

def get_register_user_use_case(session: AsyncSession = Depends(db.session_depedency)):
	db_mapper = UserDBMapper()
	entity_mapper = UserDTOEntityMapper()
	repo = MySQLUserRepository(session=session, mapper=db_mapper)
	password_service = PasswordService()
	return SaveUser(mapper=entity_mapper, password_service=password_service, user_repo=repo)

def get_create_post_use_case(session: AsyncSession = Depends(db.session_depedency)):
	post_db_mapper = PostDBMapper()
	user_db_mapper= UserDBMapper()
	entity_mapper = PostDTOEntityMapper()
	post_repo = MySQLPostRepository(mapper=post_db_mapper, session=session)
	user_repo = MySQLUserRepository(mapper=user_db_mapper, session=session)
	return CreatePost(mapper=entity_mapper, post_repo=post_repo, user_repo=user_repo)

def get_post_use_case(session: AsyncSession = Depends(db.session_depedency)):
	post_db_mapper = PostDBMapper()
	user_db_mapper= UserDBMapper()
	entity_mapper = PostDTOEntityMapper()
	post_repo = MySQLPostRepository(mapper=post_db_mapper, session=session)
	user_repo = MySQLUserRepository(mapper=user_db_mapper, session=session)
	return GetPost(mapper=entity_mapper, post_repo=post_repo, user_repo=user_repo)