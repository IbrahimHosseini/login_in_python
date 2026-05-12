# schemas.py

from pydantic import BaseModel, Field

class RequestUser(BaseModel):
	id: int
	email: str
	password: str


class UpdateUser(BaseModel):
	email: str
	password: str