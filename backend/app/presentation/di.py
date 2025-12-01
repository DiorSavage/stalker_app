from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import os

from infra.db.models.session import db
from infra.db.repositories.user import MySQLUserRepository
from infra.db.repositories.post import MySQLPostRepository
from infra.db.repositories.token import MySQLTokenRepository
from infra.db.repositories.comment import MySQLCommentRepository
from infra.db.mappers.post import PostDBMapper, PostDTOEntityMapper, DetailPostDTOEntityMapper, DetailPostDBMapper
from infra.db.mappers.user import UserDBMapper, UserDTOEntityMapper
from infra.db.mappers.comment import CommentDBMapper, CommentDtoEntityMapper
from infra.db.mappers.token import TokenDtoEntityMapper, TokenDBMapper
from domain.services.password import PasswordService
from application.services.jwt_service import JWTService
from application.use_cases.save_user_repo import SaveUser
from application.use_cases.create_post_repo import CreatePost
from application.use_cases.get_post_repo import GetPost
from application.use_cases.create_comment_repo import CreatePostComment
from presentation.api.v1.mappers.user_mapper import UserResponseMapper
from presentation.api.v1.mappers.post_mapper import PostResponseMapper, DetailPostResponseMapper
from presentation.api.v1.mappers.comment_mapper import CommentResponseMapper

def get_register_user_use_case(session: AsyncSession = Depends(db.session_depedency)):
	user_db_mapper = UserDBMapper()
	token_db_mapper = TokenDBMapper()
	user_entity_mapper = UserDTOEntityMapper()
	token_entity_mapper = TokenDtoEntityMapper()
	user_repo = MySQLUserRepository(session=session, mapper=user_db_mapper)
	token_repo = MySQLTokenRepository(session=session, mapper=token_db_mapper)
	jwt_service = JWTService(algorithm="RS256", public_key= os.path.join("./certs/jwt-public.pem"), secret_key= os.path.join("./certs/jwt-private.pem"))
	password_service = PasswordService()
	return SaveUser(
		user_mapper=user_entity_mapper,
		password_service=password_service,
		user_repo=user_repo,
		jwt_service=jwt_service,
		token_mapper=token_entity_mapper,
		token_repo=token_repo
	)

def get_create_post_use_case(session: AsyncSession = Depends(db.session_depedency)):
	post_db_mapper = PostDBMapper()
	user_db_mapper= UserDBMapper()
	user_entity_mapper = UserDTOEntityMapper()
	post_entity_mapper = PostDTOEntityMapper(user_mapper=user_entity_mapper)
	post_repo = MySQLPostRepository(mapper=post_db_mapper, session=session)
	user_repo = MySQLUserRepository(mapper=user_db_mapper, session=session)
	return CreatePost(mapper=post_entity_mapper, post_repo=post_repo, user_repo=user_repo)

def get_post_use_case(session: AsyncSession = Depends(db.session_depedency)):
	user_db_mapper= UserDBMapper()
	post_db_mapper = DetailPostDBMapper()
	user_entity_mapper = UserDTOEntityMapper()
	post_entity_mapper = DetailPostDTOEntityMapper(user_mapper=user_entity_mapper)
	post_repo = MySQLPostRepository(mapper=post_db_mapper, session=session)
	user_repo = MySQLUserRepository(mapper=user_db_mapper, session=session)
	return GetPost(mapper=post_entity_mapper, post_repo=post_repo, user_repo=user_repo)

def get_post_response_mapper():
	user_db_mapper = UserResponseMapper()
	return PostResponseMapper(user_db_mapper=user_db_mapper)

def get_detail_post_response_mapper():
	user_db_mapper = UserResponseMapper()
	return DetailPostResponseMapper(user_db_mapper=user_db_mapper)

def get_comment_response_mapper():
	user_db_mapper = UserResponseMapper()
	return CommentResponseMapper(
		user_db_mapper=user_db_mapper
	)

def get_create_comment_use_case(session: AsyncSession = Depends(db.session_depedency)):
	user_db_mapper = UserDBMapper()
	comment_db_mapper = CommentDBMapper()
	user_entity_mapper = UserDTOEntityMapper()
	comment_entity_mapper = CommentDtoEntityMapper(user_mapper=user_entity_mapper)
	comment_repo = MySQLCommentRepository(mapper=comment_db_mapper, session=session)
	user_repo = MySQLUserRepository(mapper=user_db_mapper, session=session)
	return CreatePostComment(
		mapper=comment_entity_mapper,
		comment_repo=comment_repo,
		user_repo=user_repo
	)