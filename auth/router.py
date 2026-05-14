# auth/router.py

from fastapi import APIRouter, HTTPException, Depends
from .schemas import Token, RefreshRequest, LoginRequest
from .service import verify_token, create_access_token, create_refresh_token, verify_password, hash_password
from .dependencies import get_current_user
from . import repository
from db.session import get_db
from users.repository import get_user_by_email, get_user_by_id

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post("/login", response_model = Token)
async def login(data: LoginRequest, session = Depends(get_db)):

	user = await get_user_by_email(session = session, email = data.email)

	if user is None:
		raise HTTPException(status_code = 401, detail = "Invalid credentials")

	
	if not verify_password(data.password, hashed = user.hashed_password):
		raise HTTPException(status_code = 401, detail = "Invalid credentials")

	access_token = create_access_token(user.id)
	refresh_token, new_expires_at = create_refresh_token(user.id)

	await repository.create_refresh_token(session = session, token = refresh_token, user_id = user.id, expires_at = new_expires_at)

	return Token(
		access_token = access_token,
		refresh_token = refresh_token,
		token_type = "bearer"
	)


@router.post("/refresh", response_model = Token)
async def refresh(data: RefreshRequest, session = Depends(get_db)):

	refresh_token_data = await repository.get_refresh_token(session = session, token = data.refresh_token)

	if refresh_token_data is None:
		raise HTTPException(status_code = 401, detail = "Invalid refresh token")

	payload = verify_token(refresh_token_data.token)

	if payload.get("type") != "refresh":
		raise HTTPException(status_code = 401, detail = "Wrong token type")

	user_id = refresh_token_data.user_id
	revoked_token = await repository.revoke_refresh_token(session = session, token = data.refresh_token)

	new_access = create_access_token(user_id)
	new_refresh = create_refresh_token(user_id)
	
	created_refresh_token = await repository.create_refresh_token(
		session = session,
		token = new_refresh,
		user_id = user_id,
		expires_at = refresh_token_data.expires_at
		)

	return Token(
		access_token = new_access,
		refresh_token = new_refresh,
		token_type = "bearer"
	)


@router.post("/logout")
async def logout(current_user_id = Depends(get_current_user), session = Depends(get_db)):
	deleted_refresh_token = await repository.revoke_refresh_token(session = session, user_id = current_user_id)

	if deleted_refresh_token is None:
		raise HTTPException(status_code = 404, detail = "User not found")

	return {"message": "Logged out"}


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user), session = Depends(get_db)):
	user = await get_user_by_id(session = session, id = int(user_id))

	if user is None:
		raise HTTPException(
			status_code=404,
			detail="User not found"
		)
		
	return {
		"user_id": user_id,
		"email": user.email,
		"is_active": user.is_active,
	}
