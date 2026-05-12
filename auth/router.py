# router.py

from fastapi import APIRouter, HTTPException, Depends
from .schemas import Token, RefreshRequest
from .service import verify_token, create_access_token, create_refresh_token, verify_password, hash_password

router = APIRouter(prefix = "/auth", tags = ["auth"])

fake_user = {"user@test.com": {"id": 1, "password": hash_password("testpass123")}}
refresh_tokens = set() # change with BD

@router.post("/login", response_model = Token)
async def login(email: str, password: str):
	user = fake_user.get(email)

	if not user:
		raise HTTPException(status_code = 401, detail = "Invalid credentials")

	
	if not verify_password(password, hashed = user["password"]):
		raise HTTPException(status_code = 401, detail = "Invalid credentials")

	access_token = create_access_token(user["id"])
	refresh_token = create_refresh_token(user["id"])
	refresh_tokens.add(refresh_token)

	return Token(
		access_token = access_token,
		refresh_token = refresh_token,
		token_type = "bearer"
	)


@router.post("/refresh", response_model = Token)
async def refresh(data: RefreshRequest):

	refresh_token = data["refresh_token"]

	if refresh_token not in  refresh_tokens:
		raise HTTPException(status_code = 401, detail = "Invalid refresh token")

	payload = verify_token(refresh_token)
	if payload.get("type") != "refresh":
		raise HTTPException(status_code = 401, detail = "Wrong token type")


	user_id = int(payload["sub"])
	refresh_tokens.discard(refresh_token)

	new_access = create_access_token(user_id)
	new_refresh = create_refresh_token(user_id)
	refresh_tokens.add(new_refresh)

	return Token(
		access_token = new_access,
		refresh_token = new_refresh,
		token_type = "bearer"
	)


@router.post("/logout")
async def logout(refresh_token: str):
	refresh_tokens.discard(refresh_token)
	return {"message": "Logged out"}










