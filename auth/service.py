# service.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
import bcrypt
from typing import Tuple


def create_access_token(user_id: int) -> str:
	expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	payload = {"sub": str(user_id), "exp": expire, "type": "access"}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm = settings.ALGORITHM)


def create_refresh_token(user_id: int) -> Tuple[str, datetime]:
	expire = datetime.utcnow() + timedelta(days = settings.REFRESH_TOKEN_EXPIRE_DAYS)
	payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm = settings.ALGORITHM), expire


def verify_token(token: str) -> dict:
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
		return payload
	except JWTError:
		raise ValueError("Invalid Token") 


def hash_password(password: str) -> str:
	return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
	return bcrypt.checkpw(plain.encode(), hashed.encode())