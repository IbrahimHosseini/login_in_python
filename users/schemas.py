# schemas.py

from pydantic import BaseModel, Field

class RequestUser(BaseModel):
	email: str
	password: str


class UpdateUser(BaseModel):
	email: str
	password: str


class ResponseUser(BaseModel):
	id: int
	email: str