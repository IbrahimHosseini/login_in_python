# router.py

from fastapi import APIRouter, HTTPException, Depends, status
from auth.dependencies import get_current_user
from .schemas import RequestUser, UpdateUser
from auth.service import hash_password
from auth.router import fake_users


router = APIRouter(prefix = "/users", tags = ["users"])

next_id = 2

#=========== IS USER EXIST ============================
def user_exist(id: int) -> bool:

	if id not in fake_users:
		raise HTTPException(
				status_code = 401,
				detail = "User not found"
		)
		
	return fake_users[id]

#=========== CREATE USER ==============================
@router.post("/users", response_model = RequestUser, status_code = status.HTTP_201_CREATED)
async def create_user(user: RequestUser):

	global next_id

	new_user = {
		"id": next_id,
		"email": user.email,
		"password": hash_password(user.password)
	}


	fake_users[next_id] = new_user

	next_id += 1

#=========== GET USER BY ID ===========================
@router.get("/users/{id}", response_model = RequestUser)
async def get_user(id: int, user = Depends(user_exist)):
	return user

#=========== UPDATE USER ===========================
@router.put("/update", response_model = RequestUser)
async def update_user(id: int, user: UpdateUser, exist_user = Depends(user_exist)):
	user_data = updates.dict(exclude_unset = True)
	exist_user.update(user_data)

	return exist_user


#=========== DELETE USER ===========================