# repository.py

from datetime import datetime
from db.models import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_refresh_token(session: AsyncSession, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
	
	new_refresh_token = RefreshToken(
			token = token,
			user_id = user_id,
			expires_at = expires_at
		)

	session.add(new_refresh_token)
	await session.commit()
	await session.refresh(new_refresh_token)

	return new_refresh_token


async def get_refresh_token(session: AsyncSession, token: str) -> RefreshToken | None:
	result = await session.execute(
			select(RefreshToken).where(RefreshToken.token == token)
		)

	token = result.scalar_one_or_none()

	if token is None:
		return None

	return token


async def revoke_refresh_token(session: AsyncSession, token: str):
	
	result = await session.execute(
			select(RefreshToken).where(RefreshToken.token == token)
		)

	refresh_token = result.scalar_one_or_none()

	if refresh_token is None:
		return None

	await session.delete(refresh_token)
	await session.flush()