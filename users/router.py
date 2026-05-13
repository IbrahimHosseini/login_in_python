# users/router.py

from fastapi import APIRouter, HTTPException, Depends, status
from auth.dependencies import get_current_user
from .schemas import RequestUser, UpdateUser, ResponseUser
from auth.service import hash_password
from auth.router import fake_users


user_router = APIRouter(prefix = "/users", tags = ["users"])

next_id = 2

#=========== CREATE USER ==============================
@user_router.post("/", response_model = ResponseUser, status_code = status.HTTP_201_CREATED)
async def create_user(user: RequestUser):

	global next_id

	new_user = {
		"id": next_id,
		"email": user.email,
		"password": hash_password(user.password)
	}


	fake_users[next_id] = new_user

	next_id += 1

	created_user = ResponseUser(
		id = new_user["id"],
		email = new_user["email"]
	)

	return created_user

#=========== GET USER BY ID ===========================
@user_router.get("/{id}", response_model = ResponseUser)
async def get_user(id: int):

	user = fake_users.get(id)

	return ResponseUser(
		id = user["id"],
		email = user["email"]
	)

#=========== UPDATE USER ===========================
@user_router.put("/{id}", response_model = RequestUser)
async def update_user(id: int, user: UpdateUser, current_user_id = Depends(get_current_user)):

	if id != int(current_user_id):
		raise HTTPException(
			status_code = 403,
			detail = "Not Authorized"
		)

	user_data = user.model_dump(exclude_unset = True)

	if "password" in user_data:
		user_data["password"] = hash_password(user_data["password"])

	fake_users[id].update(user_data)

	updated_user = fake_users.get(id)

	return ResponseUser(
		id = updated_user["id"],
		email = updated_user["email"]
	)

#=========== DELETE USER ===========================
@user_router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user_id = Depends(get_current_user)):

	if id != int(current_user_id):
		raise HTTPException(
			status_code = 403,
			detail = "Not Authorized"
		)

	del fake_users[id]





























