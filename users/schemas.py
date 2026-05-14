# schemas.py

from pydantic import BaseModel, Field

class UserRequest(BaseModel):
	email: str
	password: str


class UserUpdateRequest(BaseModel):
	email: str
	password: str


class UserResponse(BaseModel):
	id: int
	email: str