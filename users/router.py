# users/router.py

from fastapi import APIRouter, HTTPException, Depends, status
from auth.dependencies import get_current_user
from .schemas import UserRequest, UserUpdateRequest, UserResponse
from db.session import get_db
from . import repository


user_router = APIRouter(prefix = "/users", tags = ["users"])

#=========== CREATE USER ==============================
@user_router.post("/", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def create_user(user: UserRequest, session = Depends(get_db)):

	created_user = await repository.create_user(session = session, user = user)

	return UserResponse(
			id = created_user.id,
			email = created_user.email
		)

#=========== GET USER BY ID ===========================
@user_router.get("/{id}", response_model = UserResponse)
async def get_user(id: int, session = Depends(get_db)):

	user = await repository.get_user_by_id(session = session, id = id)

	if user is None:
		raise HTTPException(
			status_code = 404,
			detail = "User not found"
		)

	return UserResponse(
		id = user.id,
		email = user.email
	)

#=========== UPDATE USER ===========================
@user_router.put("/{id}", response_model = UserResponse)
async def update_user(id: int, user: UserUpdateRequest, current_user_id = Depends(get_current_user), session = Depends(get_db)):

	if id != int(current_user_id):
		raise HTTPException(
			status_code = 403,
			detail = "Not Authorized"
		)

	updated_user = await repository.update_user(session = session, id = id, new_data = user)

	if updated_user is None:
		raise HTTPException(
			status_code = 404,
			detail = "User not found"
		)

	return UserResponse(
		id = updated_user.id,
		email = updated_user.email
	)

#=========== DELETE USER ===========================
@user_router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user_id = Depends(get_current_user), session = Depends(get_db)):

	if id != int(current_user_id):
		raise HTTPException(
			status_code = 403,
			detail = "Not Authorized"
		)

	deleted = await repository.delete_user(session = session, id = id)
	
	if not deleted:
		raise HTTPException(
			status_code = 404,
			detail = "User not found"
		)





