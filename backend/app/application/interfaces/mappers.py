from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.user import User
from application.dtos.user import UserDTO

@dataclass(
	frozen=True,
	kw_only=True,
	slots=True
)
class DtoUserEntityMapper(ABC):

	@abstractmethod	
	def to_dto(self, entity: User) -> UserDTO:
		...

	@abstractmethod
	def to_entity(self, dto: UserDTO) -> User:
		...