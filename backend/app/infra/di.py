from sqlalchemy.orm import Session
from fastapi import Depends
from infra.db.models.session import db
from infra.db.repositories.user import MySQLUserRepository
from infra.db.mappers.user import UserDBMapper, UserDTOEntityMapper
from domain.services.password import PasswordService
from application.use_cases.save_user_repo import SaveUser

def get_register_user_use_case(session: Session = Depends(db.session_depedency)):
	db_mapper = UserDBMapper()
	entity_mapper = UserDTOEntityMapper()
	repo = MySQLUserRepository(session=session, mapper=db_mapper)
	password_service = PasswordService()
	return SaveUser(mapper=entity_mapper, password_service=password_service, user_repo=repo)