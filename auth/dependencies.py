# dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .service import verify_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

async def get_current_user(token: str = Depends(oauth_scheme)):
	payload = verify_token(token)

	token_type = payload["type"]

	if token_type != "access":
		raise HTTPException(status_code = 401, detail = "Invalid token type")	

	return payload["sub"]