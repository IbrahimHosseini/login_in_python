# service.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings


def create_access_token(user_id: int) -> str:
	expire = datatime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	pyload = {"sub": str(user_id), "exp": expire, "type": "access"}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm = settings.ALGORITHM)


def create_refresh_token(user_id: int) -> str:
	expire = datatime.utcnow() + timedelta(days = settings.REFRESH_TOKEN_EXPIRE_DAYS)
	payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm = settings.ALGORITHM)


def verify_token(token: str) -> dict:
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithm = [settings.ALGORITHM])
		return payload
	except JWTError:
		raise ValueError("Invalid Token") 